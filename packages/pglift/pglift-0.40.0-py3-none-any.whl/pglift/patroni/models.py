# flake8: noqa: B902
import functools
import json
import socket
import warnings
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, Union

import pgtoolkit.conf
import psycopg.conninfo
import pydantic
import yaml
from attrs import frozen
from pydantic import DirectoryPath, Extra, Field, FilePath, SecretStr, validator

from .. import exceptions, plugin_manager, types
from .._compat import Self
from . import impl

if TYPE_CHECKING:
    from ..models import interface, system
    from ..settings import PatroniSettings, Settings


def bootstrap(
    instance: "system.BaseInstance", manifest: "interface.Instance"
) -> dict[str, Any]:
    """Return values for the "bootstrap" section of Patroni configuration."""
    settings = instance._settings
    patroni_settings = settings.patroni
    assert patroni_settings
    initdb_options = manifest.initdb_options(settings.postgresql.initdb)
    initdb: list[Union[str, dict[str, Union[str, Path]]]] = [
        {key: value}
        for key, value in initdb_options.dict(
            exclude={"data_checksums"}, exclude_none=True
        ).items()
    ]
    initdb.append({"waldir": instance.waldir})
    if initdb_options.data_checksums:
        initdb.append("data-checksums")
    pg_hba = manifest.pg_hba(settings).splitlines()
    pg_ident = manifest.pg_ident(settings).splitlines()
    return dict(
        dcs={"loop_wait": patroni_settings.loop_wait},
        initdb=initdb,
        pg_hba=pg_hba,
        pg_ident=pg_ident,
    )


def export_model(model: pydantic.BaseModel) -> dict[str, Any]:
    """Export a model as a dict unshadowing secret fields.

    >>> class S(pydantic.BaseModel):
    ...     user: str
    ...     pw: Optional[SecretStr] = None
    >>> export_model(S(user="bob", pw="s3kret"))
    {'user': 'bob', 'pw': 's3kret'}
    """
    return {
        n: v.get_secret_value() if isinstance(v, SecretStr) else v
        for n, v in model
        if v is not None
    }


def libpq_ssl_settings(model: pydantic.BaseModel) -> dict[str, Any]:
    """Return a dict suitable for libpq connection SSL options.

    >>> class S(pydantic.BaseModel):
    ...     cert: str
    ...     password: Optional[SecretStr] = None
    ...     rootcert: Optional[str]

    >>> libpq_ssl_settings(S(cert="a", b=None))
    {'sslcert': 'a'}
    >>> libpq_ssl_settings(S(cert="z", rootcert="y", password="pwd"))
    {'sslcert': 'z', 'sslpassword': 'pwd', 'sslrootcert': 'y'}
    """
    options = {f"ssl{n}": v for n, v in export_model(model).items()}
    # Verify that the result is valid for libpq.
    assert not options or psycopg.conninfo.make_conninfo(**options)
    return options


def postgresql(
    instance: "system.BaseInstance",
    manifest: "interface.Instance",
    configuration: pgtoolkit.conf.Configuration,
    postgresql_options: Optional["ServiceManifest.PostgreSQL"],
    **args: Any,
) -> dict[str, Any]:
    """Return values for the "postgresql" section of Patroni configuration.

    Any values from `**args` are used over default values that would be
    inferred but values from `manifest` still take precedence.
    """
    settings = instance._settings
    if "authentication" not in args:
        patroni_settings = settings.patroni
        assert patroni_settings is not None
        sslopts = {}
        if (
            patroni_settings.postgresql.connection
            and patroni_settings.postgresql.connection.ssl
        ):
            sslopts = libpq_ssl_settings(patroni_settings.postgresql.connection.ssl)

        def r(
            role: "interface.Role",
            opts: Optional["ServiceManifest.PostgreSQL.ClientAuth"],
        ) -> dict[str, str]:
            d = {"username": role.name} | sslopts
            if role.password:
                d["password"] = role.password.get_secret_value()
            if opts and opts.ssl:
                d |= libpq_ssl_settings(opts.ssl)
            return d

        surole = manifest.surole(settings)
        replrole = manifest.replrole(settings)
        assert replrole  # Per settings validation
        args["authentication"] = {
            "superuser": r(surole, None),
            "replication": r(
                replrole,
                postgresql_options.replication if postgresql_options else None,
            ),
            "rewind": r(
                surole,
                postgresql_options.rewind if postgresql_options else None,
            ),
        }

    if postgresql_options and postgresql_options.connect_host is not None:
        args["connect_address"] = types.Address.validate(
            f"{postgresql_options.connect_host}:{manifest.port}"
        )
    else:
        args["connect_address"] = types.Address.get(manifest.port)

    def s(entry: pgtoolkit.conf.Entry) -> Union[str, bool, int, float]:
        # Serialize pgtoolkit entry without quoting; specially needed to
        # timedelta.
        if isinstance(entry.value, timedelta):
            return entry.serialize().strip("'")
        return entry.value

    parameters = args.setdefault("parameters", {})
    parameters.update({k: s(e) for k, e in sorted(configuration.entries.items())})

    listen_addresses = parameters.get("listen_addresses", "*")
    args["listen"] = types.Address.validate(f"{listen_addresses}:{manifest.port}")

    args.setdefault("use_unix_socket", True)
    args.setdefault("use_unix_socket_repl", True)
    args.setdefault("data_dir", instance.datadir)
    args.setdefault("bin_dir", instance.bindir)
    if "pg_hba" not in args:
        args["pg_hba"] = manifest.pg_hba(settings).splitlines()
    if "pg_ident" not in args:
        args["pg_ident"] = manifest.pg_ident(settings).splitlines()

    if "create_replica_methods" not in args:
        args["create_replica_methods"] = []
        pm = plugin_manager(settings)
        for method, config in pm.hook.patroni_create_replica_method(
            manifest=manifest, instance=instance
        ):
            args["create_replica_methods"].append(method)
            args[method] = config
        args["create_replica_methods"].append("basebackup")
        args.setdefault("basebackup", [{"waldir": instance.waldir}])
    return args


def etcd(
    model: Optional["ServiceManifest.Etcd"], settings: "PatroniSettings", **args: Any
) -> dict[str, Any]:
    if args:
        return args
    return settings.etcd.dict(exclude={"v2"}, exclude_none=True) | (
        export_model(model) if model is not None else {}
    )


class RESTAPI(types.BaseModel):
    connect_address: types.Address = Field(
        default_factory=functools.partial(types.Address.get, port=8008),
        description="IP address (or hostname) and port, to access the Patroni's REST API.",
    )
    listen: types.Address = Field(
        default_factory=types.Address.unspecified,
        description="IP address (or hostname) and port that Patroni will listen to for the REST API. Defaults to connect_address if not provided.",
    )

    @validator("listen", always=True, pre=True)
    def __validate_listen_(cls, value: str, values: dict[str, Any]) -> str:
        """Set 'listen' from 'connect_address' if unspecified.

        >>> RESTAPI()  # doctest: +ELLIPSIS
        RESTAPI(connect_address='...:8008', listen='...:8008')
        >>> RESTAPI(connect_address="localhost:8008")
        RESTAPI(connect_address='localhost:8008', listen='localhost:8008')
        >>> RESTAPI(connect_address="localhost:8008", listen="server:123")
        RESTAPI(connect_address='localhost:8008', listen='server:123')
        """
        if not value:
            value = values["connect_address"]
            assert isinstance(value, str)
        return value


class _BaseModel(types.BaseModel, extra=Extra.allow):
    pass


class Patroni(_BaseModel):
    """A partial representation of a patroni instance, as defined in a YAML
    configuration.

    Only fields that are handled explicitly on our side are modelled here.
    Other fields are loaded as "extra" (allowed by _BaseModel class).
    """

    class PostgreSQL(_BaseModel):
        connect_address: types.Address
        listen: types.Address
        parameters: dict[str, Any]

    class RESTAPI_(_BaseModel, RESTAPI):
        cafile: Optional[Path] = None
        certfile: Optional[Path] = None
        keyfile: Optional[Path] = None
        verify_client: Optional[Literal["optional", "required"]] = None

    scope: str = Field(description="Cluster name.")
    name: str = Field(description="Host name.")
    restapi: RESTAPI_ = Field(default_factory=RESTAPI_)
    postgresql: PostgreSQL

    @classmethod
    def build(
        cls,
        settings: "PatroniSettings",
        service: "ServiceManifest",
        instance: "system.BaseInstance",
        manifest: "interface.Instance",
        configuration: pgtoolkit.conf.Configuration,
        **args: Any,
    ) -> Self:
        """Build a Patroni instance from passed arguments."""
        if "bootstrap" not in args:
            args["bootstrap"] = bootstrap(instance, manifest)
        args["postgresql"] = postgresql(
            instance,
            manifest,
            configuration,
            service.postgresql,
            **args.pop("postgresql", {}),
        )
        dcs = "etcd" if settings.etcd.v2 else "etcd3"
        args[dcs] = etcd(service.etcd, settings, **args.pop(dcs, {}))
        return cls(**args)

    @classmethod
    def get(cls, qualname: str, settings: "PatroniSettings") -> Self:
        """Get a Patroni instance from its qualified name, by loading
        respective YAML configuration file.
        """
        if not (fpath := impl._configpath(qualname, settings)).exists():
            raise exceptions.FileNotFoundError(
                f"Patroni configuration for {qualname} node not found"
            )
        with fpath.open() as f:
            data = yaml.safe_load(f)
        return cls.parse_obj(data)

    def yaml(self, **kwargs: Any) -> str:
        data = json.loads(self.json(exclude_none=True, **kwargs))
        return yaml.dump(data, sort_keys=True)


@frozen
class Service:
    """A Patroni service bound to a PostgreSQL instance."""

    __service_name__: ClassVar = "patroni"
    cluster: str
    node: str
    name: str
    settings: "PatroniSettings"

    def __str__(self) -> str:
        return f"{self.__service_name__}@{self.name}"

    def args(self) -> list[str]:
        configpath = impl._configpath(self.name, self.settings)
        return [str(self.settings.execpath), str(configpath)]

    def pidfile(self) -> Path:
        return Path(str(self.settings.pid_file).format(name=self.name))

    def env(self) -> None:
        return None


class ClusterMember(types.BaseModel, extra=Extra.allow, frozen=True):
    """An item of the list of members returned by Patroni API /cluster endpoint."""

    host: str
    name: str
    port: int
    role: str
    state: str


class ServiceManifest(types.ServiceManifest, service_name="patroni"):
    _cli_config: ClassVar[dict[str, types.CLIConfig]] = {
        "cluster_members": {"hide": True},
        "postgresql_connect_host": {"hide": True},
    }
    _ansible_config: ClassVar[dict[str, types.AnsibleConfig]] = {
        "cluster_members": {"hide": True},
    }

    class PostgreSQL(types.BaseModel):
        class ClientAuth(types.BaseModel):
            class ClientSSLOptions(types.BaseModel):
                cert: FilePath = Field(description="Client certificate.")
                key: FilePath = Field(description="Private key.")
                password: Optional[SecretStr] = Field(
                    default=None, description="Password for the private key."
                )

            ssl: Optional[ClientSSLOptions] = Field(
                default=None,
                description="Client certificate options.",
            )

        connect_host: Optional[str] = Field(
            default=None,
            description="Host or IP address through which PostgreSQL is externally accessible.",
        )
        replication: Optional[ClientAuth] = Field(
            default=None,
            description="Authentication options for client (libpq) connections to remote PostgreSQL by the replication user.",
        )
        rewind: Optional[ClientAuth] = Field(
            default=None,
            description="Authentication options for client (libpq) connections to remote PostgreSQL by the rewind user.",
        )

    class Etcd(types.BaseModel):
        username: str = Field(
            description="Username for basic authentication to etcd.",
        )
        password: SecretStr = Field(
            description="Password for basic authentication to etcd."
        )

    # XXX Or simply use instance.qualname?
    cluster: str = Field(
        description="Name (scope) of the Patroni cluster.",
        readOnly=True,
    )
    node: str = Field(
        default_factory=socket.getfqdn,
        description="Name of the node (usually the host name).",
        readOnly=True,
    )
    restapi: RESTAPI = Field(
        default_factory=RESTAPI, description="REST API configuration"
    )

    postgresql: Optional[PostgreSQL] = Field(
        default=None,
        description="Configuration for PostgreSQL setup and remote connection.",
    )
    etcd: Optional[Etcd] = Field(
        default=None, description="Instance-specific options for etcd DCS backend."
    )
    cluster_members: list[ClusterMember] = Field(
        default=[],
        description="Members of the Patroni this instance is member of.",
        readOnly=True,
    )

    postgresql_connect_host: Optional[str] = Field(
        default=None, description="DEPRECATED; use postgresql.connect_host."
    )

    @validator("postgresql_connect_host")
    def __validate_postgresql_connect_host_(
        cls, value: Optional[str], values: dict[str, Any]
    ) -> Optional[str]:
        if value:
            if postgresql := values.get("postgresql"):
                if postgresql.connect_host is not None:
                    raise ValueError(
                        "postgresql_connect_host and postgresql.connect_host are mutually exclusive"
                    )
                postgresql = postgresql.copy(update={"connect_host": value})
            else:
                postgresql = cls.PostgreSQL(connect_host=value)
            warnings.warn(
                "postgresql_connect_host field is deprecated, use postgresql.connect_host",
                FutureWarning,
            )
            values["postgresql"] = postgresql
        return value

    __validate_none_values_ = validator("node", "restapi", pre=True, allow_reuse=True)(
        types.default_if_none
    )
