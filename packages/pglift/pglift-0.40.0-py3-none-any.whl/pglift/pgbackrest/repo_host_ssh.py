import configparser
import logging
from typing import Optional

import pgtoolkit.conf as pgconf

from .. import hookimpl, util
from ..ctx import Context
from ..models import interface, system
from ..settings import PgBackRestSettings, Settings
from . import base
from . import register_if as base_register_if
from .base import get_settings, parser

HostRepository = PgBackRestSettings.SSHHostRepository
logger = logging.getLogger(__name__)


def register_if(settings: Settings) -> bool:
    if not base_register_if(settings):
        return False
    s = get_settings(settings)
    return isinstance(s.repository, HostRepository)


@hookimpl
def site_configure_install(settings: Settings) -> None:
    s = get_settings(settings)
    base.site_configure_install(settings, base_config(s))


@hookimpl
def site_configure_uninstall(settings: Settings) -> None:
    base.site_configure_uninstall(settings)


@hookimpl
def instance_configured(
    ctx: "Context",
    manifest: interface.Instance,
    config: pgconf.Configuration,
    upgrading_from: Optional[system.Instance],
) -> None:
    with base.instance_configured(ctx, manifest, config, upgrading_from):
        pass


@hookimpl
def instance_dropped(ctx: "Context", instance: system.Instance) -> None:
    with base.instance_dropped(ctx, instance):
        pass


def repository_settings(settings: PgBackRestSettings) -> HostRepository:
    assert isinstance(settings.repository, HostRepository)
    return settings.repository


def base_config(settings: PgBackRestSettings) -> configparser.ConfigParser:
    """Build the base configuration for pgbackrest clients on the database
    host.
    """
    cp = parser()
    cp.read_string(
        util.template("pgbackrest", "pgbackrest.conf").format(**dict(settings))
    )
    s = repository_settings(settings)
    rhost = {
        "repo1-host-type": "ssh",
        "repo1-host": s.host,
    }
    if s.host_port:
        rhost["repo1-host-port"] = str(s.host_port)
    if s.host_config:
        rhost["repo1-host-config"] = str(s.host_config)
    if s.host_user:
        rhost["repo1-host-user"] = s.host_user
    if s.cmd_ssh:
        rhost["cmd-ssh"] = str(s.cmd_ssh)
    cp["global"].update(rhost)
    return cp
