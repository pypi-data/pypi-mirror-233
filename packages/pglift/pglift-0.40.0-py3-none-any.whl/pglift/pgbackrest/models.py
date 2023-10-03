from datetime import datetime
from pathlib import Path
from typing import Literal, Optional

from attrs import field, frozen
from pydantic import Field, SecretStr

from .. import types


@frozen
class Service:
    """A pgbackrest service bound to a PostgreSQL instance."""

    stanza: str
    """Name of the stanza"""

    path: Path
    """Path to configuration file for this stanza"""

    index: int = 1
    """index of pg-path option in the stanza"""


class ServiceManifest(types.ServiceManifest, service_name="pgbackrest"):
    stanza: str = Field(
        description=(
            "Name of pgBackRest stanza. "
            "Something describing the actual function of the instance, such as 'app'."
        ),
        readOnly=True,
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description="Password of PostgreSQL role for pgBackRest.",
        exclude=True,
    )


@frozen
class Backup:
    label: str
    size: types.ByteSize = field(converter=types.ByteSize)
    repo_size: types.ByteSize = field(converter=types.ByteSize)
    date_start: datetime
    date_stop: datetime
    type: Literal["incr", "diff", "full"]
    databases: list[str]
