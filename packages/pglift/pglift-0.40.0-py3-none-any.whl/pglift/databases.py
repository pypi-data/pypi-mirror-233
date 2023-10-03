import datetime
import logging
import shlex
import subprocess
from collections.abc import Sequence
from typing import Any, Optional

import psycopg.rows
import pydantic
from pgtoolkit import conf as pgconf
from psycopg import sql

from . import (
    cmd,
    db,
    exceptions,
    extensions,
    hookimpl,
    publications,
    schemas,
    subscriptions,
    types,
)
from .ctx import Context
from .models import interface, system
from .postgresql.ctl import libpq_environ
from .task import task

logger = logging.getLogger(__name__)


def apply(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    database: interface.Database,
) -> interface.ApplyResult:
    """Apply state described by specified interface model as a PostgreSQL database.

    The instance should be running and not a standby.
    """
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)

    with db.connect(instance, ctx=ctx) as cnx:
        return _apply(cnx, database, instance, ctx)


def _apply(
    cnx: db.Connection,
    database: interface.Database,
    instance: "system.PostgreSQLInstance",
    ctx: Context,
) -> interface.ApplyResult:
    name = database.name
    if database.state == interface.PresenceState.absent:
        dropped = False
        if _exists(cnx, name):
            _drop(cnx, database)
            dropped = True
        return interface.ApplyResult(
            change_state=interface.ApplyChangeState.dropped if dropped else None
        )

    changed = created = False
    if not _exists(cnx, name):
        create(cnx, database, instance)
        created = True
    else:
        logger.info("altering '%s' database on instance %s", database.name, instance)
        changed = alter(cnx, database)

    if (
        database.schemas
        or database.extensions
        or database.publications
        or database.subscriptions
    ):
        with db.connect(instance, ctx=ctx, dbname=name) as db_cnx:
            for schema in database.schemas:
                if schemas.apply(db_cnx, schema, name):
                    changed = True
            for extension in database.extensions:
                if extensions.apply(db_cnx, extension):
                    changed = True
            for publication in database.publications:
                if publications.apply(db_cnx, publication, name):
                    changed = True
            for subscription in database.subscriptions:
                if subscriptions.apply(db_cnx, subscription, name):
                    changed = True

    if created:
        state = interface.ApplyChangeState.created
    elif changed:
        state = interface.ApplyChangeState.changed
    else:
        state = None
    return interface.ApplyResult(change_state=state)


def clone(
    name: str,
    options: interface.Database.CloneOptions,
    instance: system.PostgreSQLInstance,
) -> None:
    logger.info("cloning '%s' database in %s from %s", name, instance, options.dsn)

    def log_cmd(cmd_args: list[str]) -> None:
        args = [
            db.obfuscate_conninfo(a)
            if isinstance(a, (types.ConnectionString, pydantic.PostgresDsn))
            else a
            for a in cmd_args
        ]
        logger.debug(shlex.join(args))

    pg_dump = instance.bindir / "pg_dump"
    dump_cmd = [str(pg_dump), "--format", "custom", "-d", options.dsn]
    user = instance._settings.postgresql.surole.name
    restore_cmd = [
        str(instance.bindir / "pg_restore"),
        "--exit-on-error",
        "-d",
        db.dsn(instance, dbname=name, user=user),
    ]
    if options.schema_only:
        dump_cmd.append("--schema-only")
        restore_cmd.append("--schema-only")
    env = libpq_environ(instance, user)
    with subprocess.Popen(  # nosec
        dump_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    ) as dump:
        log_cmd(dump_cmd)
        restore = cmd.run(restore_cmd, stdin=dump.stdout, env=env)
        pg_dump_stderr = []
        assert dump.stderr
        for errline in dump.stderr:
            logger.debug("%s: %s", pg_dump, errline.rstrip())
            pg_dump_stderr.append(errline)

    if dump.returncode:
        raise exceptions.CommandError(
            dump.returncode, dump_cmd, stderr="".join(pg_dump_stderr)
        )
    if restore.returncode:
        raise exceptions.CommandError(
            restore.returncode, restore_cmd, restore.stdout, restore.stderr
        )


def get(
    ctx: Context, instance: "system.PostgreSQLInstance", name: str
) -> interface.Database:
    """Return the database object with specified name.

    :raises ~pglift.exceptions.DatabaseNotFound: if no database with specified
        'name' exists.
    """
    if not exists(ctx, instance, name):
        raise exceptions.DatabaseNotFound(name)
    with db.connect(instance, ctx=ctx, dbname=name) as cnx:
        return _get(cnx, dbname=name)


def _get(cnx: db.Connection, dbname: str) -> interface.Database:
    row = cnx.execute(db.query("database_inspect"), {"database": dbname}).fetchone()
    assert row is not None
    settings = row.pop("settings")
    if settings is None:
        row["settings"] = None
    else:
        row["settings"] = {}
        for s in settings:
            k, v = s.split("=", 1)
            row["settings"][k.strip()] = pgconf.parse_value(v.strip())
    row["schemas"] = schemas.ls(cnx)
    row["extensions"] = extensions.ls(cnx)
    row["publications"] = publications.ls(cnx)
    row["subscriptions"] = subscriptions.ls(cnx, dbname)
    return interface.Database.parse_obj(row)


def ls(
    ctx: Context, instance: "system.PostgreSQLInstance", dbnames: Sequence[str] = ()
) -> list[system.Database]:
    """List databases in instance.

    :param dbnames: restrict operation on databases with a name in this list.
    """
    with db.connect(instance, ctx=ctx) as cnx:
        return _list(cnx, dbnames)


def _list(cnx: db.Connection, dbnames: Sequence[str] = ()) -> list[system.Database]:
    where_clause = (
        sql.SQL("AND d.datname IN ({})").format(
            sql.SQL(", ").join(map(sql.Literal, dbnames))
        )
        if dbnames
        else sql.SQL("")
    )
    with cnx.cursor(row_factory=psycopg.rows.kwargs_row(system.Database.build)) as cur:
        cur.execute(db.query("database_list", where_clause=where_clause))
        return cur.fetchall()


def drop(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    database: interface.DatabaseDropped,
) -> None:
    """Drop a database from a primary instance.

    :raises ~pglift.exceptions.DatabaseNotFound: if no database with specified
        'name' exists.
    """
    if instance.standby:
        raise exceptions.InstanceReadOnlyError(instance)
    with db.connect(instance, ctx=ctx) as cnx:
        if not _exists(cnx, database.name):
            raise exceptions.DatabaseNotFound(database.name)
        _drop(cnx, database)


def _drop(cnx: db.Connection, database: interface.DatabaseDropped) -> None:
    logger.info("dropping '%s' database", database.name)
    options = ""
    if database.force_drop:
        if cnx.info.server_version < 130000:
            raise exceptions.UnsupportedError(
                "Force drop option can't be used with PostgreSQL < 13"
            )
        options = "WITH (FORCE)"

    cnx.execute(
        db.query(
            "database_drop",
            database=sql.Identifier(database.name),
            options=sql.SQL(options),
        )
    )


def exists(ctx: Context, instance: "system.PostgreSQLInstance", name: str) -> bool:
    """Return True if named database exists in 'instance'.

    The instance should be running.
    """
    with db.connect(instance, ctx=ctx) as cnx:
        return _exists(cnx, name)


def _exists(cnx: db.Connection, name: str) -> bool:
    cur = cnx.execute(db.query("database_exists"), {"database": name})
    return cur.rowcount == 1


@task("creating '{database.name}' database in {instance}")
def create(
    cnx: db.Connection,
    database: interface.Database,
    instance: system.PostgreSQLInstance,
) -> None:
    opts = []
    if database.owner is not None:
        opts.append(sql.SQL("OWNER {}").format(sql.Identifier(database.owner)))
    if database.tablespace is not None:
        opts.append(
            sql.SQL("TABLESPACE {}").format(sql.Identifier(database.tablespace))
        )

    cnx.execute(
        db.query(
            "database_create",
            database=sql.Identifier(database.name),
            options=sql.SQL(" ").join(opts),
        ),
    )
    if database.settings is not None:
        _configure(cnx, database.name, database.settings)

    if database.clone:
        clone(database.name, database.clone, instance)


@create.revert(None)
def revert_create(
    cnx: db.Connection,
    database: interface.Database,
    instance: system.PostgreSQLInstance,
) -> None:
    _drop(cnx, interface.DatabaseDropped(name=database.name))


def alter(cnx: db.Connection, database: interface.Database) -> bool:
    owner: sql.Composable
    actual = _get(cnx, database.name)
    if database.owner is None:
        owner = sql.SQL("CURRENT_USER")
    else:
        owner = sql.Identifier(database.owner)
    options = sql.SQL("OWNER TO {}").format(owner)
    cnx.execute(
        db.query(
            "database_alter",
            database=sql.Identifier(database.name),
            options=options,
        ),
    )

    if database.settings is not None:
        _configure(cnx, database.name, database.settings)

    if actual.tablespace != database.tablespace and database.tablespace is not None:
        options = sql.SQL("SET TABLESPACE {}").format(
            sql.Identifier(database.tablespace)
        )
        cnx.execute(
            db.query(
                "database_alter",
                database=sql.Identifier(database.name),
                options=options,
            ),
        )

    return _get(cnx, database.name) != actual


def _configure(
    cnx: db.Connection, dbname: str, db_settings: dict[str, Optional[pgconf.Value]]
) -> None:
    if not db_settings:
        # Empty input means reset all.
        cnx.execute(
            db.query(
                "database_alter",
                database=sql.Identifier(dbname),
                options=sql.SQL("RESET ALL"),
            )
        )
    else:
        with cnx.transaction():
            for k, v in db_settings.items():
                if v is None:
                    options = sql.SQL("RESET {}").format(sql.Identifier(k))
                else:
                    options = sql.SQL("SET {} TO {}").format(
                        sql.Identifier(k), sql.Literal(v)
                    )
                cnx.execute(
                    db.query(
                        "database_alter",
                        database=sql.Identifier(dbname),
                        options=options,
                    )
                )


def encoding(cnx: db.Connection) -> str:
    """Return the encoding of connected database."""
    row = cnx.execute(db.query("database_encoding")).fetchone()
    assert row is not None
    value = row["encoding"]
    return str(value)


def run(
    ctx: Context,
    instance: "system.PostgreSQLInstance",
    sql_command: str,
    *,
    dbnames: Sequence[str] = (),
    exclude_dbnames: Sequence[str] = (),
    notice_handler: types.NoticeHandler = db.default_notice_handler,
) -> dict[str, list[dict[str, Any]]]:
    """Execute a SQL command on databases of `instance`.

    :param dbnames: restrict operation on databases with a name in this list.
    :param exclude_dbnames: exclude databases with a name in this list from
        the operation.
    :param notice_handler: a function to handle notice.

    :returns: a dict mapping database names to query results, if any.

    :raises psycopg.ProgrammingError: in case of unprocessable query.
    """
    result = {}
    if dbnames:
        target = ", ".join(dbnames)
    else:
        target = "ALL databases"
        if exclude_dbnames:
            target += f" except {', '.join(exclude_dbnames)}"
    if not ctx.confirm(
        f"Confirm execution of {sql_command!r} on {target} of {instance}?", True
    ):
        raise exceptions.Cancelled(f"execution of {sql_command!r} cancelled")

    for database in ls(ctx, instance):
        if (
            dbnames and database.name not in dbnames
        ) or database.name in exclude_dbnames:
            continue
        with db.connect(instance, ctx=ctx, dbname=database.name) as cnx:
            cnx.add_notice_handler(notice_handler)
            logger.info(
                'running "%s" on %s database of %s',
                sql_command,
                database.name,
                instance,
            )
            cur = cnx.execute(sql_command)
            if cur.statusmessage:
                logger.info(cur.statusmessage)
            if cur.description is not None:
                result[database.name] = cur.fetchall()
    return result


def dump(ctx: Context, instance: "system.PostgreSQLInstance", dbname: str) -> None:
    """dump a database of `instance` (logical backup)."""
    logger.info("backing up database '%s' on instance %s", dbname, instance)
    if not exists(ctx, instance, dbname):
        raise exceptions.DatabaseNotFound(dbname)
    postgresql_settings = instance._settings.postgresql

    conninfo = db.dsn(instance, dbname=dbname, user=postgresql_settings.surole.name)

    date = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone()
        .isoformat(timespec="seconds")
    )
    dumps_directory = instance.dumps_directory
    cmds = [
        [
            c.format(
                bindir=instance.bindir,
                path=dumps_directory,
                conninfo=conninfo,
                dbname=dbname,
                date=date,
            )
            for c in cmd_args
        ]
        for cmd_args in postgresql_settings.dump_commands
    ]
    env = libpq_environ(instance, postgresql_settings.surole.name)
    for cmd_args in cmds:
        cmd.run(cmd_args, check=True, env=env)


@hookimpl
def instance_configured(
    ctx: "Context", manifest: "interface.Instance", creating: bool
) -> None:
    if creating:
        instance = system.BaseInstance.get(
            manifest.name, manifest.version, ctx.settings
        )
        instance.dumps_directory.mkdir(parents=True, exist_ok=True)


@hookimpl
def instance_dropped(ctx: "Context", instance: "system.Instance") -> None:
    dumps_directory = instance.dumps_directory
    if not dumps_directory.exists():
        return
    has_dumps = next(dumps_directory.iterdir(), None) is not None
    if not has_dumps or ctx.confirm(
        f"Confirm deletion of database dump(s) for instance {instance}?",
        True,
    ):
        ctx.rmtree(dumps_directory)
