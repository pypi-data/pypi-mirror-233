from pathlib import Path
from typing import Optional

import pytest
from pydantic import SecretStr

from pglift import passfile as passfile_mod
from pglift.models import interface
from pglift.models.system import Instance
from pglift.settings import Settings


class Role(interface.Role):
    def __init__(
        self, name: str, password: Optional[str] = None, pgpass: bool = False
    ) -> None:
        super().__init__(
            name=name,
            password=SecretStr(password) if password is not None else None,
            pgpass=pgpass,
        )


@pytest.fixture
def passfile(settings: Settings) -> Path:
    fpath = settings.postgresql.auth.passfile
    assert fpath is not None
    fpath.write_text("*:999:*:edgar:fbi\n")
    return fpath


@pytest.mark.parametrize(
    "role, changed, pgpass",
    [
        (Role("alice"), False, "*:999:*:edgar:fbi\n"),
        (Role("bob", "secret"), False, "*:999:*:edgar:fbi\n"),
        (Role("charles", pgpass=True), False, "*:999:*:edgar:fbi\n"),
        (Role("danny", "sss", True), True, "*:999:*:danny:sss\n*:999:*:edgar:fbi\n"),
        (Role("edgar", "cia", True), True, "*:999:*:edgar:cia\n"),
        (Role("edgar", None, False), True, ""),
    ],
)
def test_role_change(
    instance: Instance, passfile: Path, role: Role, changed: bool, pgpass: str
) -> None:
    assert passfile_mod.role_change(instance=instance, role=role) == changed
    assert passfile.read_text() == pgpass


def test_role_inspect(instance: Instance) -> None:
    fpath = instance._settings.postgresql.auth.passfile
    assert fpath is not None
    fpath.write_text("*:999:*:edgar:fbi\n")
    assert passfile_mod.role_inspect(instance, "edgar") == {"pgpass": True}
    assert passfile_mod.role_inspect(instance, "alice") == {"pgpass": False}
