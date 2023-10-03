import logging

import psycopg.rows
from psycopg import sql

from . import db
from .models import interface

logger = logging.getLogger(__name__)


def ls(cnx: db.Connection) -> list[interface.Extension]:
    """Return list of extensions created in connected database using CREATE EXTENSION"""

    with cnx.cursor(row_factory=psycopg.rows.class_row(interface.Extension)) as cur:
        cur.execute(db.query("list_extensions"))
        return cur.fetchall()


def create(cnx: db.Connection, extension: interface.Extension) -> None:
    msg, args = "creating extension '%(name)s'", {"name": extension.name}
    query = sql.SQL("CREATE EXTENSION IF NOT EXISTS {}").format(
        sql.Identifier(extension.name)
    )
    if extension.schema_:
        query += sql.SQL(" SCHEMA {}").format(sql.Identifier(extension.schema_))
        msg += " in schema '%(schema)s'"
        args["schema"] = extension.schema_
    if extension.version:
        query += sql.SQL(" VERSION {}").format(sql.Identifier(extension.version))
        msg += " with version %(version)s"
        args["version"] = extension.version
    query += sql.SQL(" CASCADE")
    logger.info(msg, args)
    cnx.execute(query)


def alter_schema(cnx: db.Connection, name: str, schema: str) -> None:
    opts = sql.SQL("SET SCHEMA {}").format(sql.Identifier(schema))
    logger.info("setting '%s' extension schema to '%s'", name, schema)
    cnx.execute(
        db.query("alter_extension", extension=psycopg.sql.Identifier(name), opts=opts)
    )


def alter_version(cnx: db.Connection, name: str, version: str) -> None:
    opts = sql.SQL("UPDATE TO {}").format(sql.Identifier(version))
    logger.info("updating '%s' extension version to '%s'", name, version)
    cnx.execute(
        db.query("alter_extension", extension=psycopg.sql.Identifier(name), opts=opts)
    )


def drop(cnx: db.Connection, name: str) -> None:
    logger.info("dropping extension '%s'", name)
    cnx.execute(db.query("drop_extension", extension=psycopg.sql.Identifier(name)))


def current_schema(cnx: db.Connection) -> str:
    with cnx.cursor(row_factory=psycopg.rows.args_row(str)) as cur:
        r = cur.execute("SELECT current_schema()").fetchone()
        assert r is not None
        return r


def apply(cnx: db.Connection, extension: interface.Extension) -> bool:
    """Apply the state defined by 'extension' in connected database and return
    True if something changed.
    """
    for existing in ls(cnx):
        if extension.name == existing.name:
            if extension.state is interface.PresenceState.absent:
                drop(cnx, extension.name)
                return True

            changed = False
            new_schema = extension.schema_ or current_schema(cnx)
            if new_schema != existing.schema_:
                alter_schema(cnx, extension.name, new_schema)
                changed = True

            r = cnx.execute(
                db.query("extension_default_version"),
                {"extension_name": extension.name},
            ).fetchone()
            assert r
            default_version = str(r["default_version"])
            new_version = extension.version or default_version
            if new_version != existing.version:
                alter_version(cnx, extension.name, new_version)
                changed = True
            return changed

    if extension.state is not interface.PresenceState.absent:
        create(cnx, extension)
        return True

    return False
