import logging
from typing import TYPE_CHECKING, Any, Optional

from pgtoolkit.conf import Configuration
from pydantic import Field

from .. import hookimpl
from ..models import interface
from . import models
from .impl import POWA_EXTENSIONS, POWA_LIBRARIES
from .impl import available as available

if TYPE_CHECKING:
    from ..settings import Settings

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl
def instance_settings() -> Configuration:
    conf = Configuration()
    conf["shared_preload_libraries"] = ", ".join(POWA_LIBRARIES)
    return conf


@hookimpl
def interface_model() -> tuple[str, Any, Any]:
    return (
        models.ServiceManifest.__service__,
        models.ServiceManifest,
        Field(
            default=models.ServiceManifest(),
            description="Configuration for the PoWA service, if enabled in site settings.",
        ),
    )


@hookimpl
def get() -> models.ServiceManifest:
    return models.ServiceManifest()


@hookimpl
def rolename(settings: "Settings") -> str:
    assert settings.powa
    return settings.powa.role


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional[interface.Role]:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(models.ServiceManifest)
    return interface.Role(
        name=name, password=service_manifest.password, login=True, superuser=True
    )


@hookimpl
def database(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional[interface.Database]:
    assert settings.powa
    return interface.Database(
        name=settings.powa.dbname,
        extensions=[{"name": item} for item in POWA_EXTENSIONS],
    )
