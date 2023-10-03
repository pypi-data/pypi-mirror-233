# flake8: noqa: B902
import enum
import grp
import json
import os
import pwd
import shutil
import string
import tempfile
import warnings
from collections.abc import Iterator
from pathlib import Path, PosixPath
from typing import Any, Callable, ClassVar, Literal, Optional, Union

import pydantic
import yaml
from pydantic import (
    AnyHttpUrl,
    DirectoryPath,
    Extra,
    Field,
    FilePath,
    root_validator,
    validator,
)
from pydantic.env_settings import SettingsSourceCallable
from pydantic.fields import ModelField

from . import __name__ as pkgname
from . import exceptions, types, util
from ._compat import Self


class BaseModel(pydantic.BaseModel):
    class Config:
        frozen = True
        extra = Extra.forbid
        smart_union = True


def default_prefix(uid: int) -> Path:
    """Return the default path prefix for 'uid'.

    >>> default_prefix(0)
    PosixPath('/')
    >>> default_prefix(42)  # doctest: +ELLIPSIS
    PosixPath('/.../.local/share/pglift')
    """
    if uid == 0:
        return Path("/")
    return util.xdg_data_home() / pkgname


def default_run_prefix(uid: int) -> Path:
    """Return the default run path prefix for 'uid'."""
    if uid == 0:
        base = Path("/run")
    else:
        try:
            base = util.xdg_runtime_dir(uid)
        except exceptions.FileNotFoundError:
            base = Path(tempfile.gettempdir())

    return base / pkgname


def default_systemd_unit_path(uid: int) -> Path:
    """Return the default systemd unit path for 'uid'.

    >>> default_systemd_unit_path(0)
    PosixPath('/etc/systemd/system')
    >>> default_systemd_unit_path(42)  # doctest: +ELLIPSIS
    PosixPath('/.../.local/share/systemd/user')
    """
    if uid == 0:
        return Path("/etc/systemd/system")
    return util.xdg_data_home() / "systemd" / "user"


def default_sysuser() -> tuple[str, str]:
    pwentry = pwd.getpwuid(os.getuid())
    grentry = grp.getgrgid(pwentry.pw_gid)
    return pwentry.pw_name, grentry.gr_name


def string_format_variables(fmt: str) -> set[str]:
    return {v for _, v, _, _ in string.Formatter().parse(fmt) if v is not None}


def prefix_values(values: dict[str, Any], prefixes: dict[str, Path]) -> dict[str, Any]:
    for key, child in values.items():
        if isinstance(child, PrefixedPath):
            values[key] = child.prefix(prefixes[child.key])
        elif isinstance(child, pydantic.BaseModel):
            child_values = {k: getattr(child, k) for k in child.__fields__}
            child_values = prefix_values(child_values, prefixes)
            # Use .construct() to avoid re-validating child.
            values[key] = child.construct(
                _fields_set=child.__fields_set__, **child_values
            )
    return values


class PrefixedPath(PosixPath):
    basedir = Path("")
    key = "prefix"

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[..., "PrefixedPath"]]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Path, field: ModelField) -> Self:
        if not isinstance(value, cls):
            value = cls(value)
        # Ensure all template variables used in default field value are also
        # used in user value and that no unhandled variables are used.
        expected = string_format_variables(str(field.default))
        if expected != string_format_variables(str(value)):
            raise ValueError(
                "value contains unknown or missing template variable(s); "
                f"expecting: {', '.join(sorted(expected)) or 'none'}"
            )
        return value

    def prefix(self, prefix: Union[str, Path]) -> Path:
        """Return the path prefixed if is not yet absolute.

        >>> PrefixedPath("documents").prefix("/home/alice")
        PosixPath('/home/alice/documents')
        >>> PrefixedPath("/root").prefix("/whatever")
        PosixPath('/root')
        """
        if self.is_absolute():
            return Path(self)
        assert Path(prefix).is_absolute(), (
            f"expecting an absolute prefix (got '{prefix}')",
        )
        return prefix / self.basedir / self


class ConfigPath(PrefixedPath):
    basedir = Path("etc")


class RunPath(PrefixedPath):
    basedir = Path("")
    key = "run_prefix"


class DataPath(PrefixedPath):
    basedir = Path("srv")


class LogPath(PrefixedPath):
    basedir = Path("log")


class PostgreSQLVersion(types.StrEnum):
    """PostgreSQL version

    >>> PostgreSQLVersion("12")
    <PostgreSQLVersion.v12: '12'>
    >>> PostgreSQLVersion(12)
    <PostgreSQLVersion.v12: '12'>
    """

    v16 = "16"
    v15 = "15"
    v14 = "14"
    v13 = "13"
    v12 = "12"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, int):
            return cls(str(value))
        return super()._missing_(value)


class PostgreSQLVersionSettings(BaseModel):
    """Version-specific settings for PostgreSQL."""

    version: PostgreSQLVersion
    bindir: DirectoryPath


def _postgresql_bindir_version() -> tuple[str, str]:
    usrdir = Path("/usr")
    for version in PostgreSQLVersion:
        # Debian packages
        if (usrdir / "lib" / "postgresql" / version).exists():
            return str(usrdir / "lib" / "postgresql" / "{version}" / "bin"), version

        # RPM packages from the PGDG
        if (usrdir / f"pgsql-{version}").exists():
            return str(usrdir / "pgsql-{version}" / "bin"), version
    else:
        raise OSError("no PostgreSQL installation found")


def _postgresql_bindir() -> Optional[str]:
    try:
        return _postgresql_bindir_version()[0]
    except OSError:
        return None


class AuthLocalMethod(types.AutoStrEnum):
    """Local authentication method"""

    trust = enum.auto()
    reject = enum.auto()
    md5 = enum.auto()
    password = enum.auto()
    scram_sha_256 = "scram-sha-256"
    gss = enum.auto()
    sspi = enum.auto()
    ident = enum.auto()
    peer = enum.auto()
    pam = enum.auto()
    ldap = enum.auto()
    radius = enum.auto()


class AuthHostMethod(types.AutoStrEnum):
    """Host authentication method"""

    trust = enum.auto()
    reject = enum.auto()
    md5 = enum.auto()
    password = enum.auto()
    scram_sha_256 = "scram-sha-256"
    gss = enum.auto()
    sspi = enum.auto()
    ident = enum.auto()
    pam = enum.auto()
    ldap = enum.auto()
    radius = enum.auto()


class AuthHostSSLMethod(types.AutoStrEnum):
    """Host SSL authentication method"""

    trust = enum.auto()
    reject = enum.auto()
    md5 = enum.auto()
    password = enum.auto()
    scram_sha_256 = "scram-sha-256"
    gss = enum.auto()
    sspi = enum.auto()
    ident = enum.auto()
    pam = enum.auto()
    ldap = enum.auto()
    radius = enum.auto()
    cert = enum.auto()


class AuthSettings(BaseModel):
    """PostgreSQL authentication settings."""

    local: AuthLocalMethod = Field(
        default=AuthLocalMethod.trust,
        description="Default authentication method for local-socket connections.",
    )

    host: AuthHostMethod = Field(
        default=AuthHostMethod.trust,
        description="Default authentication method for local TCP/IP connections.",
    )

    hostssl: Optional[AuthHostSSLMethod] = Field(
        default=AuthHostSSLMethod.trust,
        description="Default authentication method for SSL-encrypted TCP/IP connections.",
    )

    passfile: Optional[Path] = Field(
        default=Path.home() / ".pgpass", description="Path to .pgpass file."
    )

    password_command: tuple[str, ...] = Field(
        default=(), description="An optional command to retrieve PGPASSWORD from"
    )


class InitdbSettings(BaseModel):
    """Settings for initdb step of a PostgreSQL instance."""

    locale: Optional[str] = Field(
        default="C", description="Instance locale as used by initdb."
    )

    encoding: Optional[str] = Field(
        default="UTF8", description="Instance encoding as used by initdb."
    )

    data_checksums: Optional[bool] = Field(
        default=None, description="Use checksums on data pages."
    )


class PostgreSQLSettings(BaseModel):
    """Settings for PostgreSQL."""

    bindir: Optional[str] = Field(
        default_factory=_postgresql_bindir,
        description="Default PostgreSQL bindir, templated by version.",
    )

    @validator("bindir")
    def __bindir_is_templated_(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and "{version}" not in value:
            raise ValueError("missing '{version}' template placeholder")
        return value

    versions: tuple[PostgreSQLVersionSettings, ...] = Field(
        default=(), description="Available PostgreSQL versions."
    )

    @validator("versions", always=True)
    def __set_versions_(
        cls, value: tuple[PostgreSQLVersionSettings, ...], values: dict[str, Any]
    ) -> tuple[PostgreSQLVersionSettings, ...]:
        if (bindir := values.get("bindir")) is None and not value:
            raise ValueError(
                "either a value is required, or the 'bindir' setting is needed in order to enable 'versions' discovery"
            )
        pgversions = [v.version for v in value]
        versions = list(value)
        for version in PostgreSQLVersion:
            if version in pgversions:
                continue
            if bindir is not None:
                version_bindir = Path(bindir.format(version=version))
                if version_bindir.exists():
                    versions.append(
                        PostgreSQLVersionSettings(
                            version=version, bindir=version_bindir
                        )
                    )
        if not versions:
            raise ValueError(
                f"no value could be inferred from bindir template '{bindir}'"
            )
        versions.sort(key=lambda v: v.version)
        return tuple(versions)

    default_version: PostgreSQLVersion = Field(  # type: ignore[assignment]
        default=None,
        description=(
            "Default PostgreSQL version to use, if unspecified at instance creation or upgrade. "
            "If unset, defaults to the latest PostgreSQL version as declared in or inferred from 'versions' setting."
        ),
    )

    @validator("default_version", always=True)
    def __validate_default_version_(
        cls, value: Optional[PostgreSQLVersion], values: dict[str, Any]
    ) -> PostgreSQLVersion:
        if not (pgversions := {v.version for v in values.get("versions", ())}):
            raise ValueError("empty 'versions' field")
        if value is None:
            return max(pgversions)  # type: ignore[no-any-return]
        if value not in pgversions:
            raise ValueError(
                f"value must be amongst declared 'versions': {', '.join(pgversions)}"
            )
        return value

    initdb: InitdbSettings = Field(default_factory=InitdbSettings)

    auth: AuthSettings = Field(default_factory=AuthSettings)

    class Role(BaseModel):
        name: str
        pgpass: bool = Field(
            default=False, description="Whether to store the password in .pgpass file."
        )

    class SuRole(Role):
        """Super-user role."""

        name: str = "postgres"

    surole: SuRole = Field(default=SuRole(), description="Instance super-user role.")

    replrole: Optional[str] = Field(
        default=None, description="Instance replication role."
    )

    class BackupRole(Role):
        """Backup role."""

        name: str = "backup"

    backuprole: BackupRole = Field(
        default=BackupRole(), description="Instance role used to backup."
    )

    datadir: DataPath = Field(
        default=DataPath("pgsql/{version}/{name}/data"),
        description="Path segment from instance base directory to PGDATA directory.",
    )

    waldir: DataPath = Field(
        default=DataPath("pgsql/{version}/{name}/wal"),
        description="Path segment from instance base directory to WAL directory.",
    )

    logpath: LogPath = Field(
        default=LogPath("postgresql"),
        description="Path where log files are stored.",
    )

    socket_directory: RunPath = Field(
        default=RunPath("postgresql"),
        description="Path to directory where postgres unix socket will be written.",
    )

    dumps_directory: DataPath = Field(
        default=DataPath("dumps/{version}-{name}"),
        description="Path to directory where database dumps are stored.",
    )

    dump_commands: tuple[tuple[str, ...], ...] = Field(
        default=(
            (
                "{bindir}/pg_dump",
                "-Fc",
                "-f",
                "{path}/{dbname}_{date}.dump",
                "-d",
                "{conninfo}",
            ),
        ),
        description="Commands used to dump a database",
    )

    restore_commands: tuple[tuple[str, ...], ...] = Field(
        default=(
            (
                "{bindir}/pg_restore",
                "-d",
                "{conninfo}",
                "{createoption}",
                "{path}/{dbname}_{date}.dump",
            ),
        ),
        description="Commands used to restore a database",
    )

    @validator("surole", "backuprole")
    def __validate_role_pgpass_and_passfile_(
        cls, value: Role, values: dict[str, Any]
    ) -> Role:
        passfile = values["auth"].passfile
        if passfile is None and value.pgpass:
            raise ValueError("cannot set 'pgpass' without 'auth.passfile'")
        return value

    @validator("dump_commands", "restore_commands")
    def __validate_dump_restore_commands_(
        cls, value: tuple[tuple[str, ...], ...]
    ) -> tuple[tuple[str, ...], ...]:
        """Validate 'dump_commands' and 'restore_commands' when defined
        without {bindir} substitution variable.
        """
        for i, cmd in enumerate(value, 1):
            program = cmd[0]
            if "{bindir}" not in program:
                p = Path(program)
                if not p.is_absolute():
                    raise ValueError(
                        f"program '{p}' from command #{i} is not an absolute path"
                    )
                if not p.exists():
                    raise ValueError(f"program '{p}' from command #{i} does not exist")
        return value


class Etcd(BaseModel):
    """Settings for Etcd (for Patroni)."""

    v2: bool = Field(default=False, description="Configure Patroni to use etcd v2.")

    hosts: tuple[types.Address, ...] = Field(
        default=(types.Address("127.0.0.1:2379"),),
        description="List of etcd endpoint.",
    )

    protocol: Literal["http", "https"] = Field(
        default="http",
        description="http or https, if not specified http is used.",
    )

    cacert: Optional[FilePath] = Field(
        default=None,
        description="Certificate authority to validate the server certificate.",
    )

    cert: Optional[FilePath] = Field(
        default=None,
        description="Client certificate for authentication.",
    )

    key: Optional[FilePath] = Field(
        default=None,
        description="Private key corresponding to the client certificate.",
    )

    @validator("cacert", "cert")
    def __validate_cert_and_protocol_(
        cls, value: Optional[FilePath], values: dict[str, Any]
    ) -> Optional[FilePath]:
        """Make sure protocol https is used when setting certificates."""
        if value is not None and values["protocol"] == "http":
            raise ValueError("'https' protocol is required")
        return value


class WatchDog(BaseModel):
    """Settings for watchdog (for Patroni)."""

    mode: Literal["off", "automatic", "required"] = Field(
        default="off", description="watchdog mode."
    )

    device: Optional[Path] = Field(
        default=None,
        description="Path to watchdog.",
    )

    safety_margin: Optional[int] = Field(
        default=None,
        description=(
            "Number of seconds of safety margin between watchdog triggering"
            " and leader key expiration."
        ),
    )

    @validator("device")
    def __validate_device_(cls, value: Path) -> Path:
        if value and not value.exists():
            raise ValueError(f"path {value} does not exists")
        return value


class RESTAPI(BaseModel):
    """Settings for Patroni's REST API."""

    cafile: Optional[FilePath] = Field(
        default=None,
        description="Certificate authority (or bundle) to verify client certificates.",
    )

    certfile: Optional[FilePath] = Field(
        default=None,
        description="PEM-encoded server certificate to enable HTTPS.",
    )

    keyfile: Optional[FilePath] = Field(
        default=None,
        description="PEM-encoded private key corresponding to the server certificate.",
    )

    verify_client: Optional[Literal["optional", "required"]] = Field(
        default=None, description="Whether to check client certificates."
    )

    @validator("verify_client")
    def __validate_verify_client_and_certfile_(
        cls, value: Optional[Any], values: dict[str, Any]
    ) -> Optional[Any]:
        """Make sure that certfile is set when verify_client is."""
        if value is not None and values.get("certfile") is None:
            raise ValueError("requires 'certfile' to enable TLS")
        return value


class CTL(BaseModel):
    """Settings for Patroni's CTL."""

    certfile: FilePath = Field(
        description="PEM-encoded client certificate.",
    )

    keyfile: FilePath = Field(
        description="PEM-encoded private key corresponding to the client certificate.",
    )


class PatroniSettings(BaseModel):
    """Settings for Patroni."""

    class PostgreSQL(BaseModel):
        class ConnectionSettings(BaseModel):
            class ServerSSLOptions(BaseModel):
                """Settings for server certificate verification."""

                mode: Optional[
                    Literal[
                        "disable",
                        "allow",
                        "prefer",
                        "require",
                        "verify-ca",
                        "verify-full",
                    ]
                ] = Field(
                    default=None,
                    description="Verification mode.",
                )
                crl: Optional[FilePath] = Field(
                    default=None,
                    description="Certificate Revocation List (CRL).",
                )
                crldir: Optional[DirectoryPath] = Field(
                    default=None,
                    description="Directory with CRL files.",
                )
                rootcert: Optional[FilePath] = Field(
                    default=None,
                    description="Root certificate(s).",
                )

            ssl: Optional[ServerSSLOptions] = Field(
                default=None,
                description="Settings for server certificate verification when connecting to remote PostgreSQL instances.",
            )

        connection: Optional[ConnectionSettings] = Field(
            default=None,
            description="Client (libpq) connection options.",
        )
        passfile: ConfigPath = Field(
            default=ConfigPath("patroni/{name}.pgpass"),
            description="Path to .pgpass password file managed by Patroni.",
        )
        use_pg_rewind: bool = Field(
            default=False, description="Whether or not to use pg_rewind."
        )

    execpath: FilePath = Field(
        default=Path("/usr/bin/patroni"),
        description="Path to patroni executable.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("patroni/{name}.yaml"),
        description="Path to the config file.",
    )

    logpath: LogPath = Field(
        default=LogPath("patroni"),
        description="Path where directories are created (based on instance name) to store patroni log files.",
    )

    pid_file: RunPath = Field(
        default=RunPath("patroni/{name}.pid"),
        description="Path to which Patroni process PID will be written.",
    )

    loop_wait: int = Field(
        default=10, description="Number of seconds the loop will sleep."
    )

    etcd: Etcd = Field(default_factory=Etcd, description="Etcd settings.")

    watchdog: WatchDog = Field(
        default_factory=WatchDog, description="Watchdog settings."
    )

    ctl: Optional[CTL] = Field(default=None, description="CTL settings.")

    postgresql: PostgreSQL = Field(
        default_factory=PostgreSQL, description="PostgreSQL settings."
    )

    restapi: RESTAPI = Field(default_factory=RESTAPI, description="REST API settings.")

    passfile: Optional[Path] = Field(
        default=None,
        description="DEPRECATED; use postgresql.passfile.",
        exclude=True,
    )

    use_pg_rewind: Optional[bool] = Field(
        default=None,
        description="DEPRECATED; use postgresql.use_pg_rewind.",
        exclude=True,
    )

    @root_validator(pre=True)
    def __validate_moved_to_postgresql_(cls, values: dict[str, Any]) -> dict[str, Any]:
        for fname in ("passfile", "use_pg_rewind"):
            try:
                value = values.pop(fname)
            except KeyError:
                continue
            postgresql = values.setdefault("postgresql", {})
            if fname in postgresql:
                raise ValueError(
                    f"{fname} and postgresql.{fname} are mutually exclusive, prefer the latter"
                )
            warnings.warn(
                f"{fname} is deprecated; use postgresql.{fname} instead",
                FutureWarning,
            )
            postgresql[fname] = value
        return values

    @validator("restapi")
    def __validate_restapi_verify_client_(
        cls, value: RESTAPI, values: dict[str, Any], field: ModelField
    ) -> RESTAPI:
        """Make sure 'ctl' client certificates are provided when setting
        restapi.verify_client to required.
        """
        if value.verify_client == "required" and values.get("ctl") is None:
            raise ValueError(
                f"'ctl' must be provided when '{field.name}.verify_client' is set to 'required'"
            )
        return value


class Cert(BaseModel):
    """TLS certificate files."""

    ca_cert: FilePath = Field(description="Certificate Authority certificate.")
    cert: FilePath = Field(description="Certificate file.")
    key: FilePath = Field(description="Private key file.")


class PgBackRestSettings(BaseModel):
    """Settings for pgBackRest."""

    execpath: FilePath = Field(
        default=Path("/usr/bin/pgbackrest"),
        description="Path to the pbBackRest executable.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("pgbackrest"),
        description="Base path for pgBackRest configuration files.",
    )

    class HostRepository(BaseModel):
        """Remote repository host for pgBackRest."""

        host: str = Field(description="Host name of the remote repository.")
        host_port: Optional[int] = Field(
            default=None,
            description="Port to connect to the remote repository.",
        )
        host_config: Optional[Path] = Field(
            default=None,
            description="pgBackRest configuration file path on the remote repository.",
        )

    class TLSHostRepository(HostRepository):
        mode: Literal["host-tls"]
        cn: str = Field(description="Certificate Common Name of the remote repository.")
        certificate: Cert = Field(
            description="TLS certificate files for the pgBackRest server on site."
        )
        port: int = Field(default=8432, description="Port for the TLS server on site.")
        pid_file: RunPath = Field(
            default=RunPath("pgbackrest.pid"),
            description="Path to which pgbackrest server process PID will be written.",
        )

    class SSHHostRepository(HostRepository):
        mode: Literal["host-ssh"]
        host_user: Optional[str] = Field(
            default=None,
            description="Name of the user that will be used for operations on the repository host.",
        )
        cmd_ssh: Optional[Path] = Field(
            default=None,
            description="SSH client command. Use a specific SSH client command when an alternate is desired or the ssh command is not in $PATH.",
        )

    class PathRepository(BaseModel):
        """Remote repository (path) for pgBackRest."""

        class Retention(BaseModel):
            """Retention settings."""

            archive: int = 2
            diff: int = 3
            full: int = 2

        mode: Literal["path"]
        path: DataPath = Field(
            description="Base directory path where backups and WAL archives are stored.",
        )
        retention: Retention = Field(
            default=Retention(), description="Retention options."
        )

    repository: Union[TLSHostRepository, SSHHostRepository, PathRepository] = Field(
        description="Repository definition, either as a (local) path-repository or as a host-repository.",
        discriminator="mode",
    )

    logpath: LogPath = Field(
        default=LogPath("pgbackrest"),
        description="Path where log files are stored.",
    )

    spoolpath: DataPath = Field(
        default=DataPath("pgbackrest/spool"),
        description="Spool path.",
    )

    lockpath: RunPath = Field(
        default=RunPath("pgbackrest/lock"),
        description="Path where lock files are stored.",
    )


class PrometheusSettings(BaseModel):
    """Settings for Prometheus postgres_exporter"""

    execpath: FilePath = Field(description="Path to the postgres_exporter executable.")

    role: str = Field(
        default="prometheus",
        description="Name of the PostgreSQL role for Prometheus postgres_exporter.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("prometheus/postgres_exporter-{name}.conf"),
        description="Path to the config file.",
    )

    queriespath: ConfigPath = Field(
        default=ConfigPath("prometheus/postgres_exporter_queries-{name}.yaml"),
        description="Path to the queries file.",
    )

    @validator("queriespath")
    def __queriespath_is_deprecated_(cls, value: Any) -> Any:
        warnings.warn(
            "'queriespath' setting is deprecated and will be removed in the next release",
            FutureWarning,
        )
        return value

    pid_file: RunPath = Field(
        default=RunPath("prometheus/{name}.pid"),
        description="Path to which postgres_exporter process PID will be written.",
    )


class PowaSettings(BaseModel):
    """Settings for PoWA."""

    dbname: str = Field(default="powa", description="Name of the PoWA database")

    role: str = Field(default="powa", description="Instance role used for PoWA.")


class TemboardSettings(BaseModel):
    """Settings for temBoard agent"""

    class Plugin(types.AutoStrEnum):
        activity = enum.auto()
        administration = enum.auto()
        dashboard = enum.auto()
        maintenance = enum.auto()
        monitoring = enum.auto()
        pgconf = enum.auto()
        statements = enum.auto()

    class LogMethod(types.AutoStrEnum):
        stderr = enum.auto()
        syslog = enum.auto()
        file = enum.auto()

    ui_url: AnyHttpUrl = Field(description="URL of the temBoard UI.")

    signing_key: FilePath = Field(
        description="Path to the public key for UI connection."
    )

    certificate: Cert = Field(
        description="TLS certificate files for the temboard-agent."
    )

    execpath: FilePath = Field(
        default=Path("/usr/bin/temboard-agent"),
        description="Path to the temboard-agent executable.",
    )

    role: str = Field(
        default="temboardagent",
        description="Name of the PostgreSQL role for temBoard agent.",
    )

    configpath: ConfigPath = Field(
        default=ConfigPath("temboard-agent/temboard-agent-{name}.conf"),
        description="Path to the config file.",
    )

    pid_file: RunPath = Field(
        default=RunPath("temboard-agent/temboard-agent-{name}.pid"),
        description="Path to which temboard-agent process PID will be written.",
    )

    plugins: tuple[Plugin, ...] = Field(
        default=(
            Plugin.monitoring,
            Plugin.dashboard,
            Plugin.activity,
        ),
        description="Plugins to load.",
    )

    home: DataPath = Field(
        default=DataPath("temboard-agent/{name}"),
        description="Path to agent home directory containing files used to store temporary data",
    )

    logpath: LogPath = Field(
        default=LogPath("temboard"),
        description="Path where log files are stored.",
    )

    logmethod: LogMethod = Field(
        default=LogMethod.stderr, description="Method used to send the logs."
    )

    loglevel: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Log level."
    )


class SystemdSettings(BaseModel):
    """Systemd settings."""

    systemctl: ClassVar[Path]

    @root_validator
    def __systemctl_(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not hasattr(cls, "systemctl"):
            systemctl = shutil.which("systemctl")
            if systemctl is None:
                raise ValueError("systemctl command not found")
            cls.systemctl = Path(systemctl)  # type: ignore[misc]
        return values

    unit_path: Path = Field(
        default=default_systemd_unit_path(os.getuid()),
        description="Base path where systemd units will be installed.",
    )

    user: bool = Field(
        default=True,
        description="Use the system manager of the calling user, by passing --user to systemctl calls.",
    )

    sudo: bool = Field(
        default=False,
        description="Run systemctl command with sudo; only applicable when 'user' is unset.",
    )

    @validator("sudo")
    def __validate_sudo_and_user_(cls, value: bool, values: dict[str, Any]) -> bool:
        if value and values.get("user"):
            raise ValueError("cannot be used with 'user' mode")
        return value


class LogRotateSettings(BaseModel):
    """Settings for logrotate."""

    configdir: ConfigPath = Field(
        default=ConfigPath("logrotate.d"), description="Logrotate config directory"
    )


class RsyslogSettings(BaseModel):
    """Settings for rsyslog."""

    configdir: ConfigPath = Field(
        default=ConfigPath("rsyslog"), description="rsyslog config directory"
    )


class CLISettings(BaseModel):
    """Settings for pglift's command-line interface."""

    logpath: LogPath = Field(
        default=LogPath(),
        description="Directory where temporary log files from command executions will be stored",
        title="CLI log directory",
    )

    log_format: str = Field(
        default="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
        description="Format for log messages when written to a file",
    )

    date_format: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="Date format in log messages when written to a file",
    )

    lock_file: RunPath = Field(
        default=RunPath(".pglift.lock"),
        description="Path to lock file dedicated to pglift",
    )


def yaml_settings_source(settings: pydantic.BaseSettings) -> dict[str, Any]:
    """Load settings values 'settings.yaml' file if found in user or system
    config directory directory.
    """
    assert isinstance(settings, SiteSettings)
    path = settings.site_settings()
    if path is None:
        return {}
    settings = yaml.safe_load(path.read_text())
    if not isinstance(settings, dict):
        raise exceptions.SettingsError(
            f"failed to load site settings from {path}, expecting an object"
        )
    return settings


def json_config_settings_source(settings: pydantic.BaseSettings) -> dict[str, Any]:
    """Load settings values from 'SETTINGS' environment variable.

    If this variable has a value starting with @, it is interpreted as a path
    to a JSON file. Otherwise, a JSON serialization is expected.
    """
    env_settings = os.getenv("SETTINGS")
    if not env_settings:
        return {}
    if env_settings.startswith("@"):
        config = Path(env_settings[1:])
        encoding = settings.__config__.env_file_encoding
        # May raise FileNotFoundError, which is okay here.
        env_settings = config.read_text(encoding)
    try:
        return json.loads(env_settings)  # type: ignore[no-any-return]
    except json.decoder.JSONDecodeError as e:
        raise exceptions.SettingsError(str(e)) from e


def is_root() -> bool:
    return os.getuid() == 0


class Settings(pydantic.BaseSettings):
    """Settings for pglift."""

    class Config:
        frozen = True

    postgresql: PostgreSQLSettings = Field(default_factory=PostgreSQLSettings)
    patroni: Optional[PatroniSettings] = None
    pgbackrest: Optional[PgBackRestSettings] = None
    powa: Optional[PowaSettings] = None
    prometheus: Optional[PrometheusSettings] = None
    temboard: Optional[TemboardSettings] = None
    systemd: Optional[SystemdSettings] = None
    logrotate: Optional[LogRotateSettings] = None
    rsyslog: Optional[RsyslogSettings] = None
    cli: CLISettings = Field(default_factory=CLISettings)

    service_manager: Optional[Literal["systemd"]] = None
    scheduler: Optional[Literal["systemd"]] = None

    prefix: Path = Field(
        default=default_prefix(os.getuid()),
        description="Path prefix for configuration and data files.",
    )

    run_prefix: Path = Field(
        default=default_run_prefix(os.getuid()),
        description="Path prefix for runtime socket, lockfiles and PID files.",
    )

    sysuser: tuple[str, str] = Field(
        default_factory=default_sysuser,
        help=(
            "(username, groupname) of system user running PostgreSQL; "
            "mostly applicable when operating PostgreSQL with systemd in non-user mode"
        ),
    )

    @validator("prefix", "run_prefix")
    def __validate_prefix_(cls, value: Path) -> Path:
        """Make sure path settings are absolute."""
        if not value.is_absolute():
            raise ValueError("expecting an absolute path")
        return value

    @root_validator(skip_on_failure=True)
    def __prefix_paths(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Prefix child settings fields with the global 'prefix'."""
        return prefix_values(
            values,
            {"prefix": values["prefix"], "run_prefix": values["run_prefix"]},
        )

    @root_validator(pre=True)
    def __set_service_manager_scheduler(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Set 'service_manager' and 'scheduler' to 'systemd' by default if systemd is enabled."""
        if values.get("systemd") is not None:
            values.setdefault("service_manager", "systemd")
            values.setdefault("scheduler", "systemd")
        return values

    @validator("service_manager", "scheduler")
    def __validate_service_manager_scheduler_(
        cls, v: Optional[Literal["systemd"]], values: dict[str, Any]
    ) -> Optional[Literal["systemd"]]:
        """Make sure systemd is enabled globally when 'service_manager' or 'scheduler' are set."""
        if values.get("systemd") is None and v is not None:
            raise ValueError("cannot use systemd, if 'systemd' is not enabled globally")
        return v

    @root_validator(pre=True)
    def __validate_is_not_root(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Make sure current user is not root.

        This is not supported by postgres (cannot call neither initdb nor pg_ctl as root).
        """
        if is_root():
            raise exceptions.UnsupportedError("pglift cannot be used as root")
        return values

    @validator("patroni")
    def __validate_patroni_passfile_(
        cls, value: Optional[PatroniSettings], values: dict[str, Any], field: ModelField
    ) -> Optional[PatroniSettings]:
        try:
            postgresql_settings = values["postgresql"]
        except KeyError:  # Another validation probably failed.
            return value
        assert isinstance(postgresql_settings, PostgreSQLSettings)
        if (
            value
            and postgresql_settings.auth.passfile
            and value.postgresql.passfile == postgresql_settings.auth.passfile
        ):
            raise ValueError(
                f"'{field.name}.postgresql.passfile' must be different from 'postgresql.auth.passfile'"
            )
        return value

    @validator("patroni")
    def __validate_patroni_requires_replrole_(
        cls, value: Optional[PatroniSettings], values: dict[str, Any]
    ) -> Optional[PatroniSettings]:
        try:
            postgresql_settings = values["postgresql"]
        except KeyError:  # Another validation probably failed.
            return value
        assert isinstance(postgresql_settings, PostgreSQLSettings)
        if value and postgresql_settings.replrole is None:
            raise ValueError("'postgresql.replrole' must be provided to use 'patroni'")
        return value


class SiteSettings(Settings):
    """Settings loaded from site-sources.

    Load user or site settings from:
    - 'settings.yaml' if found in user or system configuration directory, and,
    - SETTINGS environment variable.
    """

    @staticmethod
    def site_settings() -> Optional[Path]:
        """Return content of 'settings.yaml' if found in site configuration
        directories.
        """
        for hdlr in (util.xdg_config, util.etc_config):
            if (fpath := hdlr("settings.yaml")) is not None:
                return fpath
        return None

    class Config:
        frozen = True

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                json_config_settings_source,
                yaml_settings_source,
            )
