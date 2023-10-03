import datetime
import fnmatch
import logging
from collections.abc import Iterator
from functools import partial
from typing import Optional

import attrs
import psycopg
import pytest
from tenacity import Retrying, retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import databases, db, exceptions, instances, postgresql
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import PostgreSQLVersion, Settings

from . import connect, execute
from .conftest import DatabaseFactory, Factory, RoleFactory, TablespaceFactory


@pytest.fixture(scope="module", autouse=True)
def _postgresql_running(instance: system.Instance) -> None:
    if not postgresql.is_running(instance):
        pytest.fail("instance is not running")


@pytest.fixture
def standby_instance_stopped(
    ctx: Context, standby_instance: system.Instance
) -> Iterator[None]:
    instances.stop(ctx, standby_instance)
    try:
        yield
    finally:
        instances.start(ctx, standby_instance)


def test_exists(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    assert not databases.exists(ctx, instance, "absent")
    database_factory("present")
    assert databases.exists(ctx, instance, "present")


def test_apply(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
    role_factory: RoleFactory,
) -> None:
    r = execute(
        instance,
        "SELECT default_version FROM pg_available_extensions WHERE name='hstore'",
    )
    assert r is not None
    default_version = r[0]["default_version"]

    dbname = "applyme"
    database = interface.Database(
        name=dbname,
        settings={"work_mem": "1MB"},
        extensions=[{"name": "hstore", "version": default_version}],
        schemas=[{"name": "myapp"}, {"name": "my_schema"}],
        tablespace="pg_default",
    )
    assert not databases.exists(ctx, instance, database.name)

    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.created
    )

    db = databases.get(ctx, instance, dbname)
    assert db.settings == {"work_mem": "1MB"}

    assert db.schemas == [
        interface.Schema(name="my_schema"),
        interface.Schema(name="myapp"),
        interface.Schema(name="public"),
    ]

    assert db.extensions == [
        interface.Extension(name="hstore", schema="public", version=default_version),
    ]

    assert databases.apply(ctx, instance, database).change_state is None  # no-op

    database = interface.Database(
        name=dbname,
        owner="postgres",
        settings={"work_mem": "1MB"},
        schemas=[
            interface.Schema(name="my_schema"),
            interface.Schema(name="myapp"),
            interface.Schema(name="public"),
        ],
        extensions=[
            {"name": "hstore", "schema": "my_schema", "version": default_version},
        ],
        tablespace="pg_default",
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )
    assert databases.get(ctx, instance, dbname) == database

    database = interface.Database(name=dbname, state="absent")
    assert databases.exists(ctx, instance, dbname)
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.dropped
    )
    assert not databases.exists(ctx, instance, dbname)


def test_apply_change_owner(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
    role_factory: RoleFactory,
) -> None:
    database_factory("apply")
    database = interface.Database(name="apply")
    assert databases.apply(ctx, instance, database).change_state is None  # no-op
    assert databases.get(ctx, instance, "apply").owner == "postgres"

    role_factory("dbapply")
    database = interface.Database(
        name="apply",
        owner="dbapply",
        schemas=[interface.Schema(name="public")],
        tablespace="pg_default",
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )
    try:
        assert databases.get(ctx, instance, "apply") == database
    finally:
        databases.drop(ctx, instance, interface.DatabaseDropped(name="apply"))


def test_apply_change_tablespace(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
    tablespace_factory: TablespaceFactory,
    standby_instance_stopped: system.Instance,
) -> None:
    database_factory("apply")
    database = interface.Database(name="apply")
    assert databases.apply(ctx, instance, database).change_state is None  # no-op

    tablespace_factory("dbs2")
    database = interface.Database(
        name="apply",
        owner="postgres",
        tablespace="dbs2",
        schemas=[interface.Schema(name="public")],
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )
    try:
        assert databases.get(ctx, instance, "apply") == database
    finally:
        databases.drop(ctx, instance, interface.DatabaseDropped(name="apply"))


def test_apply_update_schemas(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
) -> None:
    database_factory("db3")
    execute(instance, "CREATE SCHEMA my_schema", fetch=False, dbname="db3")

    assert databases.get(ctx, instance, "db3").schemas == [
        interface.Schema(name="my_schema"),
        interface.Schema(name="public"),
    ]

    database = interface.Database(
        name="db3",
        schemas=[
            interface.Schema(name="my_schema", state="absent"),
            interface.Schema(name="public"),
        ],
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )

    assert databases.get(ctx, instance, "db3").schemas == [
        interface.Schema(name="public")
    ]


def test_apply_update_extensions(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
) -> None:
    database_factory("db4")
    execute(
        instance,
        "CREATE SCHEMA my_schema",
        "CREATE SCHEMA second_schema",
        "CREATE EXTENSION unaccent WITH SCHEMA my_schema",
        "CREATE EXTENSION hstore WITH VERSION '1.4'",
        fetch=False,
        dbname="db4",
    )
    r = execute(
        instance,
        "SELECT name, default_version FROM pg_available_extensions",
    )
    assert r is not None
    extversions = {e["name"]: e["default_version"] for e in r}
    unaccent_version = extversions["unaccent"]
    pgss_version = extversions["pg_stat_statements"]
    hstore_version = extversions["hstore"]
    intarray_version = extversions["intarray"]

    assert databases.get(ctx, instance, "db4").extensions == [
        interface.Extension(name="hstore", schema="public", version="1.4"),
        interface.Extension(
            name="unaccent", schema="my_schema", version=unaccent_version
        ),
    ]

    database = interface.Database(
        name="db4",
        extensions=[
            {"name": "pg_stat_statements", "schema": "my_schema"},
            {"name": "unaccent"},
            {"name": "hstore"},
            {"name": "intarray", "version": intarray_version},
        ],
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )
    assert databases.get(ctx, instance, "db4").extensions == [
        interface.Extension(name="hstore", schema="public", version=hstore_version),
        interface.Extension(name="intarray", schema="public", version=intarray_version),
        interface.Extension(
            name="pg_stat_statements", schema="my_schema", version=pgss_version
        ),
        interface.Extension(name="unaccent", schema="public", version=unaccent_version),
    ]

    database = interface.Database(
        name="db4",
        extensions=[
            {"name": "hstore", "state": "absent"},
            {"name": "pg_stat_statements", "state": "absent"},
            {"name": "unaccent", "state": "absent"},
        ],
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )
    assert [
        e.dict(by_alias=True) for e in databases.get(ctx, instance, "db4").extensions
    ] == [{"name": "intarray", "schema": "public", "version": intarray_version}]

    assert databases.apply(ctx, instance, database).change_state is None


def test_publications(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
) -> None:
    database_factory("publisher")
    execute(
        instance,
        "CREATE TABLE things (u int)",
        "CREATE TABLE users (s int)",
        "CREATE TABLE departments (n text)",
        "CREATE PUBLICATION test FOR TABLE users, departments",
        dbname="publisher",
        fetch=False,
    )
    db = databases.get(ctx, instance, "publisher")
    assert db.dict() == {
        "extensions": [],
        "name": "publisher",
        "owner": "postgres",
        "publications": [{"name": "test"}],
        "schemas": [{"name": "public"}],
        "settings": None,
        "subscriptions": [],
        "tablespace": "pg_default",
    }

    database = interface.Database(
        name="publisher",
        publications=[{"name": "mypub"}],
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )

    (row,) = execute(
        instance,
        "SELECT puballtables FROM pg_publication WHERE pubname = 'mypub'",
        dbname="publisher",
    )
    assert row["puballtables"] is True

    db = databases.get(ctx, instance, "publisher")
    assert db.dict() == {
        "extensions": [],
        "name": "publisher",
        "owner": "postgres",
        "publications": [
            {"name": "mypub"},
            {"name": "test"},
        ],
        "schemas": [{"name": "public"}],
        "settings": None,
        "subscriptions": [],
        "tablespace": "pg_default",
    }

    database = interface.Database(
        name="publisher",
        publications=[{"name": "test", "state": "absent"}],
    )
    assert (
        databases.apply(ctx, instance, database).change_state
        == interface.ApplyChangeState.changed
    )
    db = databases.get(ctx, instance, "publisher")
    assert db.dict()["publications"] == [
        {"name": "mypub"},
    ]

    assert databases.apply(ctx, instance, database).change_state is None


@pytest.fixture
def publisher_role() -> interface.Role:
    return interface.Role.parse_obj(
        {"name": "app", "login": True, "password": "secret", "replication": True}
    )


@pytest.fixture
def published_dbname() -> str:
    return "app"


@pytest.fixture
def publication_name() -> str:
    return "pub"


@pytest.fixture
def publisher_instance(
    settings: Settings,
    publisher_role: interface.Role,
    published_dbname: str,
    publication_name: str,
    surole_password: Optional[str],
    instance_factory: Factory[tuple[interface.Instance, system.Instance]],
) -> system.Instance:
    _, instance = instance_factory(
        settings.copy(
            update={
                "pgbackrest": None,
                "powa": None,
                "prometheus": None,
                "temboard": None,
            },
            deep=True,
        ),
        name="publisher",
        settings={
            "wal_level": "logical",
            "synchronous_commit": "remote_apply",
        },
        # Either use surole_password which would be in password_command or set
        # a dummy password only needed at instance creation in order to get
        # --auth-local=md5 working.
        surole_password=surole_password or "super",
        auth={
            "local": "md5",
            "host": "md5",
        },
        state="started",
        roles=[publisher_role],
        databases=[
            {
                "name": published_dbname,
                "owner": publisher_role.name,
                "publications": [
                    {"name": publication_name},
                ],
            },
        ],
    )
    assert instance.config()["wal_level"] == "logical"
    execute(
        instance,
        "CREATE TABLE t (s int)",
        dbname=published_dbname,
        role=publisher_role,
        fetch=False,
    )
    return instance


def test_subscriptions(
    ctx: Context,
    publisher_role: interface.Role,
    published_dbname: str,
    publication_name: str,
    publisher_instance: system.Instance,
    role_factory: RoleFactory,
    instance: system.Instance,
    logger: logging.Logger,
) -> None:
    assert publisher_role.password is not None
    publisher_password = publisher_role.password.get_secret_value()
    connection = interface.ConnectionString(
        conninfo=db.dsn(publisher_instance, user=publisher_role.name),
        password=publisher_password,
    )
    with psycopg.connect(connection.full_conninfo):
        # Make sure the connection string to be used for subscription is usable.
        pass
    subname = "subs"
    subscription = {
        "name": subname,
        "connection": connection,
        "publications": [publication_name],
        "enabled": True,
    }
    dbname = "subscriber"
    role_factory(publisher_role.name)
    target = {
        "name": dbname,
        "owner": publisher_role.name,
        "clone": {
            "dsn": f"postgresql://{publisher_role.name}:{publisher_password}@127.0.0.1:{publisher_instance.port}/{published_dbname}",
            "schema_only": True,
        },
        "subscriptions": [subscription],
    }

    @retry(reraise=True, wait=wait_fixed(1), stop=stop_after_attempt(5))
    def check_replication(expected: int) -> None:
        try:
            for line in postgresql.logs(instance, timeout=0):
                logger.debug(line)
        except TimeoutError:
            pass
        for _ in range(3):
            execute(instance, "SELECT pg_sleep(1)", dbname=dbname, fetch=False)
            (row,) = execute(instance, "SELECT MAX(s) AS m FROM t", dbname=dbname)
            if (m := row["m"]) == expected:
                break
        else:
            pytest.fail(f"not replicated: {m} != {expected}")

    try:
        assert (
            databases.apply(
                ctx, instance, interface.Database.parse_obj(target)
            ).change_state
            == interface.ApplyChangeState.created
        )
        actual = databases.get(ctx, instance, dbname)
        assert actual.dict() == {
            "name": dbname,
            "owner": publisher_role.name,
            "settings": None,
            "schemas": [{"name": "public"}],
            "extensions": [],
            "publications": [{"name": publication_name}],
            "subscriptions": [
                {
                    "name": "subs",
                    "connection": connection.dict(),
                    "publications": [publication_name],
                    "enabled": True,
                }
            ],
            "tablespace": "pg_default",
        }

        execute(
            publisher_instance,
            "INSERT INTO t VALUES (1), (2)",
            dbname=published_dbname,
            fetch=False,
        )
        check_replication(2)

        subscription["enabled"] = False
        assert (
            databases.apply(
                ctx, instance, interface.Database.parse_obj(target)
            ).change_state
            == interface.ApplyChangeState.changed
        )
        actual = databases.get(ctx, instance, dbname)
        assert actual.dict() == {
            "name": dbname,
            "owner": publisher_role.name,
            "settings": None,
            "schemas": [{"name": "public"}],
            "extensions": [],
            "publications": [{"name": publication_name}],
            "subscriptions": [
                {
                    "name": "subs",
                    "connection": connection.dict(),
                    "publications": [publication_name],
                    "enabled": False,
                }
            ],
            "tablespace": "pg_default",
        }

        execute(
            publisher_instance,
            "INSERT INTO t VALUES (10)",
            dbname=published_dbname,
            fetch=False,
        )
        check_replication(2)

    finally:
        if databases.exists(ctx, instance, dbname):
            subscription["state"] = "absent"
            assert (
                databases.apply(
                    ctx, instance, interface.Database.parse_obj(target)
                ).change_state
                == interface.ApplyChangeState.changed
            )
            actual = databases.get(ctx, instance, dbname)
            assert actual.dict()["subscriptions"] == []

            assert (
                databases.apply(
                    ctx, instance, interface.Database.parse_obj(target)
                ).change_state
                is None
            )

            databases.drop(ctx, instance, interface.DatabaseDropped(name=dbname))


@pytest.fixture
def clonable_database(
    ctx: Context,
    role_factory: RoleFactory,
    database_factory: DatabaseFactory,
    instance: system.Instance,
) -> str:
    role_factory("cloner", "LOGIN")
    database_factory("db1", owner="cloner")
    databases.run(
        ctx, instance, "CREATE TABLE persons AS (SELECT 'bob' AS name)", dbnames=["db1"]
    )
    databases.run(ctx, instance, "ALTER TABLE persons OWNER TO cloner", dbnames=["db1"])
    return f"postgresql://cloner@127.0.0.1:{instance.port}/db1"


def test_clone(ctx: Context, clonable_database: str, instance: system.Instance) -> None:
    database = interface.Database.parse_obj(
        {"name": "cloned_db", "clone": {"dsn": clonable_database}}
    )
    assert not databases.exists(ctx, instance, database.name)
    try:
        assert (
            databases.apply(ctx, instance, database).change_state
            == interface.ApplyChangeState.created
        )
        result = execute(instance, "SELECT * FROM persons", dbname="cloned_db")
        assert result == [{"name": "bob"}]
    finally:
        databases.drop(ctx, instance, interface.DatabaseDropped(name="cloned_db"))

    database = interface.Database.parse_obj(
        {
            "name": "cloned_schema",
            "clone": {"dsn": clonable_database, "schema_only": True},
        }
    )
    assert database.clone and database.clone.schema_only
    assert not databases.exists(ctx, instance, database.name)
    try:
        assert (
            databases.apply(ctx, instance, database).change_state
            == interface.ApplyChangeState.created
        )
        result = execute(instance, "SELECT * FROM persons", dbname="cloned_schema")
        assert result == []
    finally:
        databases.drop(ctx, instance, interface.DatabaseDropped(name="cloned_schema"))

    # DSN which target is a non existing database
    options = interface.Database.CloneOptions(
        dsn=f"postgresql://postgres@127.0.0.1:{instance.port}/nosuchdb"
    )
    with pytest.raises(exceptions.CommandError) as cm:
        databases.clone("cloned", options, instance)
    assert cm.value.cmd[0] == str(instance.bindir / "pg_dump")
    assert not databases.exists(ctx, instance, "cloned")

    # DSN which target is a non existing user
    options = interface.Database.CloneOptions(
        dsn=f"postgresql://nosuchuser@127.0.0.1:{instance.port}/postgres"
    )
    with pytest.raises(exceptions.CommandError) as cm:
        databases.clone("cloned", options, instance)
    assert cm.value.cmd[0] == str(instance.bindir / "pg_dump")
    assert not databases.exists(ctx, instance, "cloned")

    # Target database does not exist
    with pytest.raises(exceptions.CommandError) as cm:
        databases.clone("nosuchdb", database.clone, instance)
    assert cm.value.cmd[0] == str(instance.bindir / "pg_restore")
    assert not databases.exists(ctx, instance, "nosuchdb")


def test_get(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    with pytest.raises(exceptions.DatabaseNotFound, match="absent"):
        databases.get(ctx, instance, "absent")

    database_factory("describeme")
    execute(instance, "ALTER DATABASE describeme SET work_mem TO '3MB'", fetch=False)
    execute(
        instance,
        "CREATE SCHEMA my_schema",
        "CREATE EXTENSION unaccent WITH SCHEMA my_schema",
        fetch=False,
        dbname="describeme",
    )
    database = databases.get(ctx, instance, "describeme")
    assert database.name == "describeme"
    assert database.settings == {"work_mem": "3MB"}
    assert database.schemas == [
        interface.Schema(name="my_schema"),
        interface.Schema(name="public"),
    ]
    r = execute(
        instance,
        "SELECT default_version FROM pg_available_extensions WHERE name='unaccent'",
    )
    assert r is not None
    default_version = r[0]["default_version"]
    assert database.extensions == [
        interface.Extension(
            name="unaccent", schema="my_schema", version=default_version
        )
    ]


def test_encoding(instance: system.Instance) -> None:
    with connect(instance) as conn:
        assert databases.encoding(conn) == "UTF8"


def test_ls(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    database_factory("db1")
    database_factory("db2")
    dbs = databases.ls(ctx, instance)
    dbnames = [d.name for d in dbs]
    assert "db2" in dbnames
    dbs = databases.ls(ctx, instance, dbnames=("db1",))
    dbnames = [d.name for d in dbs]
    assert "db2" not in dbnames
    assert len(dbs) == 1
    db1 = attrs.asdict(next(d for d in dbs))
    db1.pop("size")
    db1["tablespace"].pop("size")
    assert db1 == {
        "acls": [],
        "collation": "C",
        "ctype": "C",
        "description": None,
        "encoding": "UTF8",
        "name": "db1",
        "owner": "postgres",
        "tablespace": {"location": "", "name": "pg_default"},
    }


def test_drop(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    with pytest.raises(exceptions.DatabaseNotFound, match="absent"):
        databases.drop(ctx, instance, interface.DatabaseDropped(name="absent"))

    database_factory("dropme")
    databases.drop(ctx, instance, interface.DatabaseDropped(name="dropme"))
    assert not databases.exists(ctx, instance, "dropme")


def test_drop_force(
    ctx: Context,
    pg_version: str,
    instance: system.Instance,
    database_factory: DatabaseFactory,
) -> None:
    database_factory("dropme")

    if pg_version >= PostgreSQLVersion.v13:
        with connect(instance, dbname="dropme"):
            with pytest.raises(psycopg.errors.ObjectInUse):
                databases.drop(ctx, instance, interface.DatabaseDropped(name="dropme"))
            databases.drop(
                ctx, instance, interface.DatabaseDropped(name="dropme", force_drop=True)
            )
        assert not databases.exists(ctx, instance, "dropme")
    else:
        with pytest.raises(
            exceptions.UnsupportedError,
            match=r"^Force drop option can't be used with PostgreSQL < 13$",
        ):
            databases.drop(
                ctx, instance, interface.DatabaseDropped(name="dropme", force_drop=True)
            )


def test_run(
    ctx: Context,
    instance: system.Instance,
    database_factory: DatabaseFactory,
    caplog: pytest.LogCaptureFixture,
) -> None:
    database_factory("test")
    caplog.clear()
    with caplog.at_level(logging.INFO, logger="pglift"):
        result_run = databases.run(
            ctx,
            instance,
            "CREATE TABLE persons AS (SELECT 'bob' AS name)",
            dbnames=["test"],
        )
    assert "CREATE TABLE persons AS (SELECT 'bob' AS name)" in caplog.records[0].message
    assert "SELECT 1" in caplog.records[1].message
    assert not result_run
    result = execute(instance, "SELECT * FROM persons", dbname="test")
    assert result == [{"name": "bob"}]
    result_run = databases.run(
        ctx,
        instance,
        "SELECT * from persons",
        dbnames=["test"],
    )
    assert result_run == {"test": [{"name": "bob"}]}


def test_run_analyze(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    database_factory("test")

    @retry(
        reraise=True,
        retry=retry_if_exception_type(AssertionError),
        stop=stop_after_attempt(5),
        wait=wait_fixed(1),
    )
    def last_analyze() -> datetime.datetime:
        result = execute(
            instance,
            "SELECT MIN(last_analyze) m FROM pg_stat_all_tables WHERE last_analyze IS NOT NULL",
            dbname="test",
        )[0]["m"]
        assert isinstance(result, datetime.datetime), result
        return result

    retrying = partial(
        Retrying,
        retry=retry_if_exception_type(AssertionError),
        stop=stop_after_attempt(5),
        wait=wait_fixed(0.2),
        reraise=True,
    )

    databases.run(ctx, instance, "ANALYZE")
    previous = last_analyze()
    databases.run(ctx, instance, "ANALYZE")
    for attempt in retrying():
        now = last_analyze()
        with attempt:
            assert now > previous
    databases.run(ctx, instance, "ANALYZE", exclude_dbnames=["test"])
    for attempt in retrying():
        with attempt:
            assert last_analyze() == now


def test_run_output_notices(
    ctx: Context, instance: system.Instance, capsys: pytest.CaptureFixture[str]
) -> None:
    databases.run(
        ctx, instance, "DO $$ BEGIN RAISE NOTICE 'foo'; END $$", dbnames=["postgres"]
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "foo\n"


def test_dump(
    ctx: Context, instance: system.Instance, database_factory: DatabaseFactory
) -> None:
    with pytest.raises(exceptions.DatabaseNotFound, match="absent"):
        databases.dump(ctx, instance, "absent")
    database_factory("dbtodump")
    databases.dump(ctx, instance, "dbtodump")
    directory = instance.dumps_directory
    assert directory.exists()
    (dumpfile,) = list(directory.iterdir())
    assert fnmatch.fnmatch(str(dumpfile), "*dbtodump_*.dump"), dumpfile
