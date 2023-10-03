from pathlib import Path
from typing import Protocol


class KeyMapper(Protocol):
    """A protocol for classes that map keys to and from paths."""

    def get_path(self, key: str, parent: Path) -> Path | None:
        """Get the child of parent for the given key, or return None if the key does not correspond to a path."""
        ...

    def key_of(self, path: Path) -> str | None:
        """Get the key for the given path, or return None if the path does not correspond to a key."""
        ...
