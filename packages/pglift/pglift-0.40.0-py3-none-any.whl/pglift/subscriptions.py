import logging

import psycopg.rows
from psycopg import sql

from . import db
from .models import interface

logger = logging.getLogger(__name__)


def ls(cnx: db.Connection, dbname: str) -> list[interface.Subscription]:
    with cnx.cursor(
        row_factory=psycopg.rows.kwargs_row(interface.Subscription.from_row)
    ) as cur:
        cur.execute(db.query("subscriptions"), {"datname": dbname})
        return cur.fetchall()


def apply(
    cnx: db.Connection, subscription: interface.Subscription, dbname: str
) -> bool:
    absent = subscription.state is interface.PresenceState.absent
    existing = {p.name: p for p in ls(cnx, dbname)}
    name = sql.Identifier(subscription.name)
    publications = ", ".join(p for p in subscription.publications)
    try:
        actual = existing[subscription.name]
    except KeyError:
        if not absent:
            logger.info(
                "creating subscription %s in database %s", subscription.name, dbname
            )
            conninfo = subscription.connection.full_conninfo
            cnx.execute(
                sql.SQL(
                    f"CREATE SUBSCRIPTION {{name}} CONNECTION {conninfo!r} PUBLICATION {publications} WITH (enabled = {{enabled}})"
                ).format(name=name, enabled=sql.Literal(subscription.enabled)),
            )
            return True
    else:
        if absent:
            logger.info(
                "dropping subscription %s from database %s", subscription.name, dbname
            )
            cnx.execute(sql.SQL("DROP SUBSCRIPTION IF EXISTS {name}").format(name=name))
            return True
        logger.info(
            "altering subscription %s of database %s", subscription.name, dbname
        )
        cnx.execute(
            sql.SQL(
                f"ALTER SUBSCRIPTION {{name}} SET PUBLICATION {publications}"
            ).format(name=name)
        )
        if actual.enabled != subscription.enabled:
            cnx.execute(
                sql.SQL(
                    f"ALTER SUBSCRIPTION {{name}} {'ENABLE' if subscription.enabled else 'DISABLE'}"
                ).format(name=name)
            )
        return True
    return False
