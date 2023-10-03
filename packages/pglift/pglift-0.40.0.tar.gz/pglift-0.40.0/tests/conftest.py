import itertools
import logging
import pathlib
import shutil
import tempfile
from collections.abc import Iterator
from typing import Any, Callable, Optional
from unittest.mock import MagicMock, patch

import port_for
import pytest
from trustme import CA

from . import CertFactory, Certificate
from .etcd import Etcd

default_pg_version: Optional[str]
try:
    from pglift.settings import _postgresql_bindir_version

    default_pg_version = _postgresql_bindir_version()[1]
except (ImportError, OSError):
    default_pg_version = None


def pytest_addoption(parser: Any) -> None:
    try:
        from pglift.settings import PostgreSQLVersion
    except ImportError:
        pass
    else:
        parser.addoption(
            "--pg-version",
            choices=list(PostgreSQLVersion),
            help="Run tests with specified PostgreSQL version (default: %(default)s)",
        )
    parser.addoption(
        "--no-plugins",
        action="store_true",
        default=False,
        help="Run tests without any pglift plugin loaded.",
    )


def pytest_report_header(config: Any) -> list[str]:
    try:
        pg_version = config.option.pg_version or default_pg_version
    except AttributeError:
        return []
    return [f"postgresql: {pg_version}"]


@pytest.fixture(scope="session")
def no_plugins(request: Any) -> bool:
    value = request.config.option.no_plugins
    assert isinstance(value, bool)
    return value


@pytest.fixture
def datadir() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    return logging.getLogger("pglift-tests")


@pytest.fixture(scope="session", autouse=True)
def _log_level(logger: logging.Logger) -> None:
    logging.getLogger("pglift").setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="session", autouse=True)
def site_config() -> Iterator[Callable[..., Optional[str]]]:
    """Avoid looking up for configuration files in site directories, fall back
    to distribution one.
    """
    try:
        from pglift import util
    except ImportError:
        yield  # type: ignore[misc]
        return

    with patch("pglift.util.site_config", new=util.dist_config) as fn:
        yield fn


@pytest.fixture(autouse=True)
def site_settings() -> Iterator[MagicMock]:
    """Prevent lookup of site settings in XDG user directory or /etc."""
    try:
        from pglift.settings import SiteSettings
    except ImportError:
        yield  # type: ignore[misc]
        return

    with patch.object(SiteSettings, "site_settings", return_value=None) as m:
        yield m


@pytest.fixture(scope="session")
def pg_bindir(request: Any) -> tuple[pathlib.Path, str]:
    from pglift.settings import _postgresql_bindir

    # --pg-version option should be available at this point
    version = request.config.option.pg_version or default_pg_version
    if version is None:
        pytest.skip("no PostgreSQL installation found")
    assert isinstance(version, str)
    bindir = _postgresql_bindir()
    assert bindir is not None  # otherwise, version would be None too.
    return pathlib.Path(bindir.format(version=version)), version


@pytest.fixture(scope="session")
def pg_version(pg_bindir: tuple[pathlib.Path, str]) -> str:
    return pg_bindir[1]


@pytest.fixture(scope="session")
def pgbackrest_execpath(no_plugins: bool) -> Optional[pathlib.Path]:
    if no_plugins:
        return None
    if (path := shutil.which("pgbackrest")) is not None:
        return pathlib.Path(path)
    return None


@pytest.fixture(scope="session")
def pgbackrest_available(pgbackrest_execpath: Optional[pathlib.Path]) -> bool:
    return pgbackrest_execpath is not None


@pytest.fixture(scope="session")
def prometheus_execpath(no_plugins: bool) -> Optional[pathlib.Path]:
    if no_plugins:
        return None
    for name in ("prometheus-postgres-exporter", "postgres_exporter"):
        path = shutil.which(name)
        if path is not None:
            return pathlib.Path(path)
    return None


@pytest.fixture(scope="session")
def temboard_execpath(no_plugins: bool) -> Optional[pathlib.Path]:
    if no_plugins:
        return None
    path = shutil.which("temboard-agent")
    if path is not None:
        return pathlib.Path(path)
    return None


@pytest.fixture(scope="session")
def patroni_execpath(no_plugins: bool) -> Optional[pathlib.Path]:
    if no_plugins:
        return None
    path = shutil.which("patroni")
    if path is not None:
        return pathlib.Path(path)
    return None


@pytest.fixture(scope="package")
def tmp_port_factory() -> Iterator[int]:
    """Return a generator producing available and distinct TCP ports."""

    def available_ports() -> Iterator[int]:
        used: set[int] = set()
        while True:
            port = port_for.select_random(exclude_ports=list(used))
            used.add(port)
            yield port

    return available_ports()


@pytest.fixture(scope="package")
def etcd_host(
    tmp_path_factory: pytest.TempPathFactory,
    tmp_port_factory: Iterator[int],
    ca: CA,
) -> Etcd:
    p = shutil.which("etcd")
    if p is None:
        pytest.skip("etcd executable not found")
    execdir = pathlib.Path(p).parent
    if not (execdir / "etcdctl").exists():
        pytest.skip("etcdctl executable not found")
    return Etcd(
        execdir=execdir,
        name="pglift-tests",
        basedir=tmp_path_factory.mktemp("etcd"),
        client_port=next(tmp_port_factory),
        peer_port=next(tmp_port_factory),
        ca=ca,
    )


@pytest.fixture(scope="package")
def ca(tmp_path_factory: pytest.TempPathFactory) -> CA:
    return CA(organization_name="dalibo", organization_unit_name="pglift")


@pytest.fixture(scope="package")
def _ssldir(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("ssl")


@pytest.fixture(scope="package")
def ca_cert(_ssldir: pathlib.Path, ca: CA) -> pathlib.Path:
    p = _ssldir / "root.crt"
    ca.cert_pem.write_to_path(p)
    return p


@pytest.fixture(scope="package")
def ca_private_key(_ssldir: pathlib.Path, ca: CA) -> pathlib.Path:
    p = _ssldir / "root.key"
    p.touch(mode=0o600)
    ca.private_key_pem.write_to_path(p)
    return p


@pytest.fixture(scope="package")
def cert_factory(ca: CA, _ssldir: pathlib.Path) -> CertFactory:
    itertools.count()

    def factory(*identities: str, common_name: Optional[str] = None) -> Certificate:
        cert = ca.issue_cert(*identities, common_name=common_name)
        with tempfile.NamedTemporaryFile(
            dir=_ssldir, delete=False, suffix=".pem"
        ) as certfile:
            certfile.write(cert.cert_chain_pems[0].bytes())
        with tempfile.NamedTemporaryFile(
            dir=_ssldir, delete=False, suffix=".pem"
        ) as keyfile:
            keyfile.write(cert.private_key_pem.bytes())
        return Certificate(
            path=pathlib.Path(certfile.name), private_key=pathlib.Path(keyfile.name)
        )

    return factory
