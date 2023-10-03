import pytest

from pglift import exceptions, roles
from pglift.ctx import Context
from pglift.models import interface
from pglift.models.system import Instance


def test_standby_role_drop(ctx: Context, standby_instance: Instance) -> None:
    role = interface.Role(name="alice")
    with pytest.raises(
        exceptions.InstanceReadOnlyError,
        match=f"^{standby_instance.version}/standby is a read-only standby instance$",
    ):
        roles.drop(ctx, standby_instance, role)
