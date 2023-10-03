import socket
from pathlib import Path
from typing import Any, Optional

import port_for
import psycopg.conninfo
import pydantic
import pytest

from pglift import plugin_manager, types
from pglift.models import interface
from pglift.prometheus import models as prometheus_models
from pglift.settings import Settings


def test_validate_ports() -> None:
    class S(pydantic.BaseModel):
        name: str
        port: types.Port

    class M(pydantic.BaseModel):
        p: types.Port
        s: S

    p1 = port_for.select_random()
    p2 = port_for.select_random()
    m = M.parse_obj({"p": p1, "s": {"name": "x", "port": p2}})
    interface.validate_ports(m)

    with socket.socket() as s1, socket.socket() as s2:
        s1.bind(("", p1))
        s1.listen()
        s2.bind(("", p2))
        s2.listen()
        with pytest.raises(pydantic.ValidationError) as cm:
            interface.validate_ports(m)
    assert f"{p1} already in use" in str(cm)
    assert f"{p2} already in use" in str(cm)


def test_instance_auth_options(
    settings: Settings, instance_manifest: interface.Instance
) -> None:
    assert instance_manifest.auth_options(
        settings.postgresql.auth
    ) == interface.Instance.Auth(local="peer", host="password", hostssl="trust")


def test_instance_pg_hba(
    settings: Settings,
    instance_manifest: interface.Instance,
    datadir: Path,
    write_changes: bool,
) -> None:
    actual = instance_manifest.pg_hba(settings)
    fpath = datadir / "pg_hba.conf"
    if write_changes:
        fpath.write_text(actual)
    expected = fpath.read_text()
    assert actual == expected


def test_instance_pg_ident(
    settings: Settings,
    instance_manifest: interface.Instance,
    datadir: Path,
    write_changes: bool,
) -> None:
    actual = instance_manifest.pg_ident(settings)
    fpath = datadir / "pg_ident.conf"
    if write_changes:
        fpath.write_text(actual)
    expected = fpath.read_text()
    assert actual == expected


def test_instance_initdb_options(
    settings: Settings, instance_manifest: interface.Instance
) -> None:
    initdb_settings = settings.postgresql.initdb
    assert instance_manifest.initdb_options(initdb_settings) == initdb_settings
    assert instance_manifest.copy(
        update={"locale": "X", "data_checksums": True}
    ).initdb_options(initdb_settings) == initdb_settings.copy(
        update={"locale": "X", "data_checksums": True}
    )
    assert instance_manifest.copy(update={"data_checksums": None}).initdb_options(
        initdb_settings.copy(update={"data_checksums": True})
    ) == initdb_settings.copy(update={"data_checksums": True})


def test_instance_composite_service(settings: Settings, pg_version: str) -> None:
    pm = plugin_manager(settings)
    Instance = interface.Instance.composite(pm)
    with pytest.raises(ValueError, match="none is not an allowed value"):
        m = Instance.parse_obj(
            {
                "name": "test",
                "version": pg_version,
                "prometheus": None,
                "pgbackrest": {"stanza": "mystanza"},
            }
        )

    m = Instance.parse_obj(
        {
            "name": "test",
            "version": pg_version,
            "prometheus": {"port": 123},
            "pgbackrest": {"stanza": "mystanza"},
        }
    )
    s = m.service_manifest(prometheus_models.ServiceManifest)
    assert s.port == 123

    class MyServiceManifest(types.ServiceManifest, service_name="notfound"):
        pass

    with pytest.raises(ValueError, match="notfound"):
        m.service_manifest(MyServiceManifest)


def test_role_state() -> None:
    assert interface.Role(name="exist").state.name == "present"
    assert interface.Role(name="notexist", state="absent").state.name == "absent"
    assert interface.RoleDropped(name="dropped").state.name == "absent"
    with pytest.raises(pydantic.ValidationError, match="unexpected value"):
        interface.RoleDropped(name="p", state="present")


def test_database_clone() -> None:
    with pytest.raises(pydantic.ValidationError, match="invalid or missing URL scheme"):
        interface.Database.parse_obj({"name": "cloned_db", "clone": {"dsn": "blob"}})

    expected = {
        "dbname": "base",
        "host": "server",
        "password": "pwd",
        "user": "dba",
    }
    db = interface.Database.parse_obj(
        {"name": "cloned_db", "clone": {"dsn": "postgres://dba:pwd@server/base"}}
    )
    assert db.clone is not None
    assert psycopg.conninfo.conninfo_to_dict(str(db.clone.dsn)) == expected

    with pytest.warns(FutureWarning):
        db = interface.Database.parse_obj(
            {"name": "cloned_db", "clone_from": "postgres://dba:pwd@server/base"}
        )
    assert db.clone is not None
    assert db.clone_from is None
    assert psycopg.conninfo.conninfo_to_dict(str(db.clone.dsn)) == expected

    with pytest.warns(FutureWarning), pytest.raises(
        pydantic.ValidationError,
        match="'clone_from' and 'clone' cannot be used together",
    ):
        interface.Database.parse_obj(
            {
                "name": "u",
                "clone_from": "postgres://u:p@s/b",
                "clone": {"dsn": "postgres://q@p/b"},
            }
        )


def test_connectionstring() -> None:
    assert (
        interface.ConnectionString(conninfo="host=x dbname=y").conninfo
        == "dbname=y host=x"
    )

    with pytest.raises(pydantic.ValidationError, match="contain a password"):
        interface.ConnectionString(conninfo="host=x password=s")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("host=x password=y", {"conninfo": "host=x", "password": "y"}),
        ("host=y", {"conninfo": "host=y", "password": None}),
    ],
)
def test_connectionstring_parse(value: str, expected: dict[str, Any]) -> None:
    parsed = interface.ConnectionString.parse(value)
    assert {
        "conninfo": parsed.conninfo,
        "password": parsed.password.get_secret_value() if parsed.password else None,
    } == expected


@pytest.mark.parametrize(
    "conninfo, password, full_conninfo",
    [
        ("host=x", "secret", "host=x password=secret"),
        ("host=y", None, "host=y"),
    ],
)
def test_connectionstring_full_conninfo(
    conninfo: str, password: Optional[str], full_conninfo: str
) -> None:
    assert (
        interface.ConnectionString(conninfo=conninfo, password=password).full_conninfo
        == full_conninfo
    )
