# flake8: noqa: B902
import enum
import warnings
from collections.abc import Iterator
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Final,
    Literal,
    Optional,
    TypeVar,
    Union,
)

import psycopg.conninfo
import pydantic
from pgtoolkit import conf as pgconf
from pydantic import (
    Field,
    PostgresDsn,
    SecretStr,
    ValidationError,
    fields,
    root_validator,
    validator,
)
from pydantic.error_wrappers import ErrorWrapper
from pydantic.fields import ModelField
from pydantic.utils import lenient_issubclass

from .. import settings as s
from .. import types, util
from .._compat import Self
from ..postgresql import Standby
from ..types import (
    AnsibleConfig,
    AutoStrEnum,
    CLIConfig,
    CompositeManifest,
    Manifest,
    Port,
    ServiceManifest,
    Status,
)

if TYPE_CHECKING:
    from ..pm import PluginManager

default_port: Final = 5432


def validate_ports(model: pydantic.BaseModel) -> None:
    """Walk fields of 'model', checking those with type Port if their value is
    available.
    """

    def _validate(
        model: pydantic.BaseModel, *, loc: tuple[str, ...] = ()
    ) -> Iterator[ErrorWrapper]:
        cls = model.__class__
        for name, field in cls.__fields__.items():
            if (value := getattr(model, name)) is None:
                continue
            ftype = field.outer_type_
            if lenient_issubclass(ftype, pydantic.BaseModel):
                yield from _validate(value, loc=loc + (name,))
            elif lenient_issubclass(ftype, Port):
                assert isinstance(value, Port)
                if not value.available():
                    yield ErrorWrapper(
                        ValueError(f"port {value} already in use"), loc + (name,)
                    )

    if errors := list(_validate(model)):
        raise ValidationError(errors, model.__class__)


def validate_state_is_absent(
    value: Union[bool, str], values: dict[str, Any], field: fields.ModelField
) -> Union[bool, str]:
    """Make sure state is absent.

    >>> r =  Role(name="bob",  drop_owned=True)
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Role
    drop_owned
      drop_owned can not be set if state is not absent (type=value_error)

    >>> r =  Role(name="bob",  reassign_owned="postgres")
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Role
    reassign_owned
      reassign_owned can not be set if state is not absent (type=value_error)

    >>> r =  Database(name="db1", force_drop=True)
    Traceback (most recent call last):
        ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Database
    force_drop
      force_drop can not be set if state is not absent (type=value_error)
    """
    absent = PresenceState.absent
    if value and values["state"] != absent:
        raise ValueError(f"{field.name} can not be set if state is not {absent}")
    return value


class InstanceState(AutoStrEnum):
    """Instance state."""

    stopped = enum.auto()
    """stopped"""

    started = enum.auto()
    """started"""

    absent = enum.auto()
    """absent"""

    restarted = enum.auto()
    """restarted"""

    @classmethod
    def from_pg_status(cls, status: Status) -> Self:
        """Instance state from PostgreSQL status.

        >>> InstanceState.from_pg_status(Status.running)
        <InstanceState.started: 'started'>
        >>> InstanceState.from_pg_status(Status.not_running)
        <InstanceState.stopped: 'stopped'>
        """
        return cls(
            {
                status.running: cls.started,
                status.not_running: cls.stopped,
            }[status]
        )


class PresenceState(AutoStrEnum):
    """Should the object be present or absent?"""

    present = enum.auto()
    absent = enum.auto()


class BaseInstance(Manifest):
    """PostgreSQL instance suitable for lookup"""

    name: str = Field(readOnly=True, description="Instance name.")
    version: Optional[s.PostgreSQLVersion] = Field(
        default=None, description="PostgreSQL version.", readOnly=True
    )

    @validator("name")
    def __validate_name_(cls, v: str) -> str:
        """Validate 'name' field.

        >>> Instance(name='without_dash')  # doctest: +ELLIPSIS
        Instance(name='without_dash', ...)
        >>> Instance(name='with-dash')
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        name
          instance name must not contain dashes (type=value_error)
        >>> Instance(name='with/slash')
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        name
          instance name must not contain slashes (type=value_error)
        """
        # Avoid dash as this will break systemd instance unit.
        if "-" in v:
            raise ValueError("instance name must not contain dashes")
        # Likewise, slash messes up with file paths.
        if "/" in v:
            raise ValueError("instance name must not contain slashes")
        return v


class BaseRole(CompositeManifest):
    name: str = Field(readOnly=True, description="Role name.")
    state: PresenceState = Field(
        const=True,
        default=PresenceState.absent,
        description="Whether the role be present or absent.",
    )
    password: Optional[SecretStr] = Field(
        const=True, default=None, description="Role password.", exclude=True
    )
    encrypted_password: Optional[SecretStr] = Field(
        const=True,
        default=None,
        description="Role password, already encrypted.",
        exclude=True,
    )

    @classmethod
    def component_models(cls, pm: "PluginManager") -> list[tuple[str, Any, Any]]:
        return pm.hook.role_model()  # type: ignore[no-any-return]

    @validator("password", "encrypted_password")
    def __validate_password_(
        cls, value: Optional[SecretStr], values: dict[str, Any], field: ModelField
    ) -> Optional[SecretStr]:
        """Make sure 'password' and 'encrypted_password' are not specified together.

        >>> Role(name="bob", password="secret", encrypted_password="tercec")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Role
        encrypted_password
          field is mutually exclusive with 'password' (type=value_error)

        >>> r = Role(name="bob", encrypted_password="tercec")
        >>> r.password, r.encrypted_password
        (None, SecretStr('**********'))
        """
        other = (
            "password" if field.name == "encrypted_password" else "encrypted_password"
        )
        if value and values.get(other):
            raise ValueError(f"field is mutually exclusive with '{other}'")
        return value


class _RoleExisting(BaseRole):
    """Base model for a role that exists (or should exist, after creation)."""

    _cli_config: ClassVar[dict[str, CLIConfig]] = {
        "in_roles": {"name": "in_role"},
        "state": {"hide": True},
        "has_password": {"hide": True},
    }
    _ansible_config: ClassVar[dict[str, AnsibleConfig]] = {
        "has_password": {"hide": True},
    }

    password: Optional[SecretStr] = Field(
        default=None, description="Role password.", exclude=True
    )
    encrypted_password: Optional[SecretStr] = Field(
        default=None, description="Role password, already encrypted.", exclude=True
    )
    has_password: bool = Field(
        default=False,
        description="True if the role has a password.",
        readOnly=True,
    )
    inherit: bool = Field(
        default=True,
        description="Let the role inherit the privileges of the roles it is a member of.",
    )
    login: bool = Field(default=False, description="Allow the role to log in.")
    superuser: bool = Field(
        default=False, description="Whether the role is a superuser."
    )
    createdb: bool = Field(
        default=False, description="Whether role can create new databases."
    )
    createrole: bool = Field(
        default=False, description="Whether role can create new roles."
    )
    replication: bool = Field(
        default=False, description="Whether the role is a replication role."
    )
    connection_limit: Optional[int] = Field(
        description="How many concurrent connections the role can make.",
        default=None,
    )
    validity: Optional[datetime] = Field(
        description="Date and time after which the role's password is no longer valid.",
        default=None,
    )
    in_roles: list[str] = Field(
        default=[],
        description="List of roles to which the new role will be added as a new member.",
    )
    state: PresenceState = Field(
        default=PresenceState.present,
        description="Whether the role be present or absent.",
        exclude=True,
    )

    @validator("has_password", always=True)
    def __set_has_password(cls, value: bool, values: dict[str, Any]) -> bool:
        """Set 'has_password' field according to 'password'.

        >>> r = Role(name="postgres")
        >>> r.has_password
        False
        >>> r = Role(name="postgres", password="P4zzw0rd")
        >>> r.has_password
        True
        >>> r = Role(name="postgres", has_password=True)
        >>> r.has_password
        True
        """
        return (
            value
            or values["password"] is not None
            or values["encrypted_password"] is not None
        )


class RoleDropped(BaseRole):
    """Model for a role that is being dropped."""

    drop_owned: bool = Field(
        default=False,
        description="Drop all PostgreSQL's objects owned by the role being dropped.",
        exclude=True,
    )
    reassign_owned: Optional[str] = Field(
        default=None,
        description="Reassign all PostgreSQL's objects owned by the role being dropped to the specified role name.",
        min_length=1,
        exclude=True,
    )

    @validator("reassign_owned")
    def __validate_reassign_owned(cls, value: str, values: dict[str, Any]) -> str:
        """Validate reassign_owned fields.

        >>> r = RoleDropped(name="bob", drop_owned=True, reassign_owned="postgres")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for RoleDropped
        reassign_owned
          drop_owned and reassign_owned are mutually exclusive (type=value_error)

        >>> r = RoleDropped(name="bob", reassign_owned="")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for RoleDropped
        reassign_owned
          ensure this value has at least 1 characters (type=value_error.any_str.min_length; limit_value=1)
        >>> RoleDropped(name="bob", reassign_owned=None, drop_owned=True)  # doctest: +ELLIPSIS
        RoleDropped(name='bob', state=<PresenceState.absent: 'absent'>, ..., drop_owned=True, reassign_owned=None)
        """
        if value and values["drop_owned"]:
            raise ValueError("drop_owned and reassign_owned are mutually exclusive")
        return value


class Role(_RoleExisting, RoleDropped):
    """PostgreSQL role"""

    _cli_config: ClassVar[dict[str, CLIConfig]] = _RoleExisting._cli_config | {
        "drop_owned": {"hide": True},
        "reassign_owned": {"hide": True},
    }

    _validate_drop_owned = validator("drop_owned", allow_reuse=True)(
        validate_state_is_absent
    )
    _validate_reassign_owned = validator("reassign_owned", allow_reuse=True)(
        validate_state_is_absent
    )


class BaseDatabase(Manifest):
    _cli_config: ClassVar[dict[str, CLIConfig]] = {
        "state": {"hide": True},
    }
    name: str = Field(readOnly=True, description="Database name.", examples=["demo"])

    state: PresenceState = Field(
        const=True,
        default=PresenceState.absent,
        description="Database state.",
        examples=["present"],
    )


class Schema(Manifest):
    name: str = Field(readonly=True, description="Schema name.")

    state: PresenceState = Field(
        default=PresenceState.present,
        description="Schema state.",
        examples=["present"],
        exclude=True,
    )


class Extension(Manifest):
    class Config:
        frozen = True

    name: str = Field(readOnly=True, description="Extension name.")
    schema_: Optional[str] = Field(
        alias="schema",
        default=None,
        description="Name of the schema in which to install the extension's object.",
    )
    version: Optional[str] = Field(
        default=None, description="Version of the extension to install."
    )

    state: PresenceState = Field(
        default=PresenceState.present,
        description="Extension state.",
        examples=["present"],
        exclude=True,
    )


class Publication(Manifest):
    name: str = Field(
        description="Name of the publication, unique in the database.",
    )
    state: PresenceState = Field(
        default=PresenceState.present,
        description="Presence state.",
        examples=["present"],
        exclude=True,
    )


class ConnectionString(Manifest):
    conninfo: str = Field(
        description="The libpq connection string, without password.",
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description="Optional password to inject into the connection string.",
        readOnly=True,
        exclude=True,
    )

    @classmethod
    def parse(cls, value: str) -> Self:
        conninfo = psycopg.conninfo.conninfo_to_dict(value)
        password = conninfo.pop("password", None)
        return cls(
            conninfo=psycopg.conninfo.make_conninfo(**conninfo), password=password
        )

    @property
    def full_conninfo(self) -> str:
        """The full connection string, including password field."""
        password = None
        if self.password:
            password = self.password.get_secret_value()
        return psycopg.conninfo.make_conninfo(self.conninfo, password=password)

    @validator("conninfo")
    def __validate_conninfo_(cls, value: str) -> str:
        s = psycopg.conninfo.conninfo_to_dict(value)
        if "password" in s:
            raise ValueError("must not contain a password")
        return psycopg.conninfo.make_conninfo(**{k: v for k, v in sorted(s.items())})


class Subscription(Manifest):
    name: str = Field(description="Name of the subscription.")
    connection: ConnectionString = Field(
        description="The libpq connection string defining how to connect to the publisher database.",
        readOnly=True,
    )
    publications: list[str] = Field(
        description="List of publications on the publisher to subscribe to.",
        min_items=1,
    )
    enabled: bool = Field(
        description="Enable or disable the subscription.",
        default=True,
    )
    state: PresenceState = Field(
        default=PresenceState.present,
        description="Presence state.",
        examples=["present"],
        exclude=True,
    )

    @classmethod
    def from_row(cls, **kwargs: Any) -> Self:
        return cls(
            connection=ConnectionString.parse(kwargs.pop("connection")), **kwargs
        )


class _DatabaseExisting(BaseDatabase):
    """Base model for a database that exists (or should exist, after creation)."""

    _cli_config: ClassVar[dict[str, CLIConfig]] = {
        "settings": {"hide": True},
        "state": {"hide": True},
        "extensions": {"name": "extension"},
        "publications": {"hide": True},
        "subscriptions": {"hide": True},
        "schemas": {"name": "schema"},
        "clone_from": {"hide": True},
    }
    _ansible_config: ClassVar[dict[str, AnsibleConfig]] = {
        "settings": {"spec": {"type": "dict", "required": False}},
    }

    state: PresenceState = Field(
        default=PresenceState.present,
        description="Database state.",
        examples=["present"],
        exclude=True,
    )
    owner: Optional[str] = Field(
        description="The role name of the user who will own the database.",
        examples=["postgres"],
        default=None,
    )
    settings: Optional[dict[str, Optional[pgconf.Value]]] = Field(
        default=None,
        description=(
            "Session defaults for run-time configuration variables for the database. "
            "Upon update, an empty (dict) value would reset all settings."
        ),
        examples=[{"work_mem": "5MB"}],
    )
    schemas: list[Schema] = Field(
        default=[],
        description="List of schemas to create in the database.",
        examples=[{"name": "sales"}, "accounting"],
    )
    extensions: list[Extension] = Field(
        default=[],
        description="List of extensions to create in the database.",
        examples=[{"name": "unaccent", "schema": "ext", "version": "1.0"}, "hstore"],
    )

    publications: list[Publication] = Field(
        default=[],
        description="List of publications to in the database.",
        examples=[{"name": "mypub"}],
    )

    subscriptions: list[Subscription] = Field(
        default=[],
        description="List of subscriptions to in the database.",
        examples=[
            {"name": "mysub", "publications": ["mypub"], "enabled": False},
        ],
    )

    class CloneOptions(Manifest):
        _cli_config: ClassVar[dict[str, CLIConfig]] = {
            "dsn": {"name": "from", "metavar": "conninfo"},
        }
        dsn: PostgresDsn = Field(
            description="Data source name of the database to restore into this one, specified as a libpq connection URI.",
        )
        schema_only: bool = Field(
            description="Only restore the schema (data definitions).",
            default=False,
        )

    clone: Optional[CloneOptions] = Field(
        description="Options for cloning a database into this one.",
        readOnly=True,
        writeOnly=True,
        examples=[
            "postgresql://app:password@dbserver:5455/appdb",
            {
                "dsn": "postgresql://app:password@dbserver:5455/appdb",
                "schema_only": True,
            },
        ],
        default=None,
        exclude=True,
    )

    clone_from: Optional[PostgresDsn] = Field(
        description="DEPRECATED, use 'clone' instead.",
        readOnly=True,
        writeOnly=True,
        default=None,
        exclude=True,
    )

    tablespace: Optional[str] = Field(
        description="The name of the tablespace that will be associated with the database.",
        default=None,
    )

    @validator("extensions", each_item=True, pre=True)
    def __validate_extensions_(
        cls, value: Union[str, dict[str, Any]]
    ) -> dict[str, Any]:
        """Turn extension values from strings (name) as full objects.

        >>> Database(name="x", extensions=["named", {"name": "obj", "schema": "sch", "version": "1.5"}])  # doctest: +ELLIPSIS
        Database(name='x', ..., extensions=[Extension(name='named', schema_=None, version=None, ...), Extension(name='obj', schema_='sch', version='1.5'...)], ...)
        """
        if isinstance(value, str):
            return {"name": value}
        return value

    @validator("schemas", each_item=True, pre=True)
    def __validate_schemas_(cls, value: Union[str, dict[str, Any]]) -> dict[str, Any]:
        """Turn schema values from strings (name) as full objects.

        >>> Database(name="x", schemas=["named", {"name": "obj"}])  # doctest: +ELLIPSIS
        Database(name='x', ..., schemas=[Schema(name='named', ...), Schema(name='obj', ...)], ...)
        """
        if isinstance(value, str):
            return {"name": value}
        return value

    @validator("clone_from")
    def __validate_clone_from_(
        cls, value: Optional[str], values: dict[str, Any]
    ) -> None:
        if value is not None:
            warnings.warn("'clone_from' is deprecated, use 'clone.dsn'", FutureWarning)
            if values.get("clone") is not None:
                raise ValueError(
                    "'clone_from' and 'clone' cannot be used together, use 'clone' only"
                )
            values["clone"] = cls.CloneOptions(dsn=value)
        return None

    @validator("tablespace")
    def __validate_tablespace_(cls, value: str) -> Optional[str]:
        """Convert 'DEFAULT' string for tablespace to None

        >>> Database(name="x", tablespace="default")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Database
        tablespace
          'default' is not a valid value ... (type=value_error)
        >>> Database(name="x", tablespace="DEFAULT")
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Database
        tablespace
          'DEFAULT' is not a valid value ... (type=value_error)
        """
        if value and value.lower() == "default":
            raise ValueError(
                f"'{value}' is not a valid value for 'tablespace'. "
                "Don't provide a value if you want the tablespace to be set to DEFAULT."
            )
        return value


class DatabaseDropped(BaseDatabase):
    """Model for a database that is being dropped."""

    _cli_config: ClassVar[dict[str, CLIConfig]] = {
        "force_drop": {"name": "force"},
    }

    force_drop: bool = Field(default=False, description="Force the drop.", exclude=True)


class Database(_DatabaseExisting, DatabaseDropped):
    """PostgreSQL database"""

    _cli_config: ClassVar[dict[str, CLIConfig]] = _DatabaseExisting._cli_config | {
        "force_drop": {"hide": True},
    }

    _validate_force_drop = validator("force_drop", allow_reuse=True)(
        validate_state_is_absent
    )


class Instance(CompositeManifest, BaseInstance):
    """PostgreSQL instance"""

    _cli_config: ClassVar[dict[str, CLIConfig]] = {
        "status": {"hide": True},
        "state": {
            "choices": [InstanceState.started.value, InstanceState.stopped.value]
        },
        "pending_restart": {"hide": True},
        "restart_on_changes": {"hide": True},
        "settings": {"hide": True},
        "roles": {"hide": True},
        "databases": {"hide": True},
    }
    _ansible_config: ClassVar[dict[str, AnsibleConfig]] = {
        "pending_restart": {"hide": True},
    }

    @classmethod
    def component_models(cls, pm: "PluginManager") -> list[tuple[str, Any, Any]]:
        return pm.hook.interface_model()  # type: ignore[no-any-return]

    port: Port = Field(
        default=Port(default_port),
        description=(
            "TCP port the postgresql instance will be listening to. "
            f"If unspecified, default to {default_port} unless a 'port' setting is found in 'settings'."
        ),
    )
    settings: dict[str, Any] = Field(
        default={},
        description=("Settings for the PostgreSQL instance."),
        examples=[
            {
                "listen_addresses": "*",
                "shared_buffers": "1GB",
                "ssl": True,
                "ssl_key_file": "/etc/certs/db.key",
                "ssl_cert_file": "/etc/certs/db.key",
                "shared_preload_libraries": "pg_stat_statements",
            }
        ],
    )
    surole_password: Optional[SecretStr] = Field(
        default=None,
        description="Super-user role password.",
        readOnly=True,
        exclude=True,
    )
    replrole_password: Optional[SecretStr] = Field(
        default=None,
        description="Replication role password.",
        readOnly=True,
        exclude=True,
    )
    data_checksums: Optional[bool] = Field(
        default=None,
        description=(
            "Enable or disable data checksums. "
            "If unspecified, fall back to site settings choice."
        ),
    )
    locale: Optional[str] = Field(
        default=None, description="Default locale.", readOnly=True
    )
    encoding: Optional[str] = Field(
        default=None,
        description="Character encoding of the PostgreSQL instance.",
        readOnly=True,
    )

    class Auth(types.BaseModel):
        local: Optional[s.AuthLocalMethod] = Field(
            default=None,
            description="Authentication method for local-socket connections",
            readOnly=True,
        )
        host: Optional[s.AuthHostMethod] = Field(
            default=None,
            description="Authentication method for local TCP/IP connections",
            readOnly=True,
        )
        hostssl: Optional[s.AuthHostSSLMethod] = Field(
            default=None,
            description="Authentication method for SSL-encrypted TCP/IP connections",
            readOnly=True,
        )

    auth: Optional[Auth] = Field(default=None, exclude=True, writeOnly=True)

    standby: Optional[Standby] = Field(default=None, description="Standby information.")

    state: InstanceState = Field(
        default=InstanceState.started,
        description="Runtime state.",
    )
    databases: list[Database] = Field(
        default=[],
        description="Databases defined in this instance (non-exhaustive list).",
        exclude=True,
        writeOnly=True,
    )
    roles: list[Role] = Field(
        default=[],
        description="Roles defined in this instance (non-exhaustive list).",
        exclude=True,
        writeOnly=True,
    )

    pending_restart: bool = Field(
        default=False,
        description="Whether the instance needs a restart to account for settings changes.",
        readOnly=True,
    )
    restart_on_changes: bool = Field(
        default=False,
        description="Whether or not to automatically restart the instance to account for settings changes.",
        exclude=True,
        writeOnly=True,
    )

    @root_validator(pre=True)
    def __validate_port_(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate that 'port' field and settings['port'] are consistent.

        If unspecified, 'port' is either set from settings value or from
        the default port value.

        >>> i = Instance(name="i")
        >>> i.port, "port" in i.settings
        (5432, False)
        >>> i = Instance(name="i", settings={"port": 5423})
        >>> i.port, i.settings["port"]
        (5423, 5423)
        >>> i = Instance(name="i", port=5454)
        >>> i.port, "port" in i.settings
        (5454, False)

        Otherwise, and if settings['port'] exists, make sure values are
        consistent and possibly cast the latter as an integer.

        >>> i = Instance(name="i", settings={"port": 5455})
        >>> i.port, i.settings["port"]
        (5455, 5455)
        >>> i = Instance(name="i", port=123, settings={"port": "123"})
        >>> i.port, i.settings["port"]
        (123, 123)
        >>> Instance(name="i", port=321, settings={"port": 123})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        __root__
          'port' field and settings['port'] mismatch (type=value_error)
        >>> Instance(name="i", settings={"port": "abc"})
        Traceback (most recent call last):
            ...
        pydantic.error_wrappers.ValidationError: 1 validation error for Instance
        __root__
          invalid literal for int() with base 10: 'abc' (type=value_error)
        """
        config_port = None
        try:
            port = values["port"]
        except KeyError:
            try:
                config_port = int(values["settings"]["port"])
            except KeyError:
                pass
            else:
                values["port"] = Port(config_port)
        else:
            try:
                config_port = int(values["settings"]["port"])
            except KeyError:
                pass
            else:
                if config_port != port:
                    raise ValueError("'port' field and settings['port'] mismatch")
        if config_port is not None:
            values["settings"]["port"] = config_port
        return values

    @root_validator
    def __validate_standby_and_patroni_(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values.get("standby") and values.get("patroni"):
            raise ValueError("'patroni' and 'standby' fields are mutually exclusive")
        return values

    _S = TypeVar("_S", bound=ServiceManifest)

    def service_manifest(self, stype: type[_S]) -> _S:
        """Return satellite service manifest attached to this instance.

        :raises ValueError: if not found.
        """
        fname = stype.__service__
        try:
            s = getattr(self, fname)
        except AttributeError as e:
            raise ValueError(fname) from e
        if s is None:
            raise ValueError(fname)
        assert isinstance(
            s, stype
        ), f"expecting field {fname} to have type {stype} (got {type(s)})"
        return s

    def surole(self, settings: s.Settings) -> Role:
        s = settings.postgresql.surole
        extra = {}
        if settings.postgresql.auth.passfile is not None:
            extra["pgpass"] = s.pgpass
        return Role(name=s.name, password=self.surole_password, **extra)

    def replrole(self, settings: s.Settings) -> Optional[Role]:
        if (name := settings.postgresql.replrole) is None:
            return None
        return Role(
            name=name,
            password=self.replrole_password,
            login=True,
            replication=True,
            in_roles=["pg_read_all_stats"],
        )

    def auth_options(self, settings: s.AuthSettings) -> Auth:
        local, host, hostssl = settings.local, settings.host, settings.hostssl
        if auth := self.auth:
            local = auth.local or local
            host = auth.host or host
            hostssl = auth.hostssl or hostssl
        return Instance.Auth(local=local, host=host, hostssl=hostssl)

    def pg_hba(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        replrole_name = replrole.name if replrole else None
        auth = self.auth_options(settings.postgresql.auth)
        return util.template("postgresql", "pg_hba.conf").format(
            auth=auth,
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole_name,
        )

    def pg_ident(self, settings: s.Settings) -> str:
        surole = self.surole(settings)
        replrole = self.replrole(settings)
        replrole_name = replrole.name if replrole else None
        return util.template("postgresql", "pg_ident.conf").format(
            surole=surole.name,
            backuprole=settings.postgresql.backuprole.name,
            replrole=replrole_name,
            sysuser=settings.sysuser[0],
        )

    def initdb_options(self, base: s.InitdbSettings) -> s.InitdbSettings:
        data_checksums: Union[None, Literal[True]] = {
            True: True,
            False: None,
            None: base.data_checksums or None,
        }[self.data_checksums]
        return s.InitdbSettings(
            locale=self.locale or base.locale,
            encoding=self.encoding or base.encoding,
            data_checksums=data_checksums,
        )


class ApplyChangeState(AutoStrEnum):
    """A apply change state for object handled by pglift"""

    created = enum.auto()  #:
    changed = enum.auto()  #:
    dropped = enum.auto()  #:


class ApplyResult(Manifest):
    """
    ApplyResult allows to describe the result of a call to apply function
    (Eg: pglift.database.apply) to an object (Eg: database, instance,...).

    The `change_state` attribute of this class can be set to one of to those values:
      - :attr:`~ApplyChangeState.created` if the object has been created,
      - :attr:`~ApplyChangeState.changed` if the object has been changed,
      - :attr:`~ApplyChangeState.dropped` if the object has been dropped,
      - :obj:`None` if nothing happened to the object we manipulate (neither created,
        changed or dropped)
    """

    change_state: Optional[ApplyChangeState] = Field(
        description="Define the change applied (created, changed or dropped) to a manipulated object",
    )  #:


class InstanceApplyResult(ApplyResult):
    pending_restart: bool = Field(
        default=False,
        description="Whether the instance needs a restart to account for settings changes.",
    )
