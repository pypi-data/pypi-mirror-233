from pathlib import Path


class ExactKeyMapper:
    """A key mapper that maps keys and file names if and only if they are exactly the same."""

    def get_path(self, key: str, parent: Path) -> Path | None:
        return path if (path := parent / key).exists() else None

    def key_of(self, path: Path) -> str | None:
        return path.name
