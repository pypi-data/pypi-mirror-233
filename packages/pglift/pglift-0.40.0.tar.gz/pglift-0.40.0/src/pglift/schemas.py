import logging

import psycopg.rows

from . import db
from .models import interface

logger = logging.getLogger(__name__)


def ls(cnx: db.Connection) -> list[interface.Schema]:
    """Return list of schemas of database."""
    with cnx.cursor(row_factory=psycopg.rows.class_row(interface.Schema)) as cur:
        cur.execute(db.query("list_schemas"))
        return cur.fetchall()


def apply(cnx: db.Connection, schema: interface.Schema, dbname: str) -> bool:
    """Apply the state defined by 'schema' in connected database and return
    True if something changed.
    """
    existing = {s.name for s in ls(cnx)}
    if schema.state is interface.PresenceState.absent and schema.name in existing:
        logger.info("dropping schema %s from database %s", schema.name, dbname)
        cnx.execute(db.query("drop_schema", schema=psycopg.sql.Identifier(schema.name)))
        return True
    elif (
        schema.state is not interface.PresenceState.absent
        and schema.name not in existing
    ):
        logger.info("creating schema %s in database %s", schema.name, dbname)
        cnx.execute(
            db.query("create_schema", schema=psycopg.sql.Identifier(schema.name))
        )
        return True
    return False
