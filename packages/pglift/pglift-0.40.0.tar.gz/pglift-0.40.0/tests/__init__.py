from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Protocol


@dataclass
class Certificate:
    path: Path
    private_key: Path

    def __post_init__(self) -> None:
        if not self.path.exists():
            raise ValueError(f"path={self.path} does not exist")
        if not self.private_key.exists():
            raise ValueError(f"private_key={self.private_key} does not exist")


class CertFactory(Protocol):
    def __call__(
        self, *identities: str, common_name: Optional[str] = None
    ) -> Certificate:
        ...
