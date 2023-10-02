import logging
from pathlib import Path
from typing import Sequence

from dirct.exceptions import AmbiguityError

logger = logging.getLogger(__name__)


class BasenameKeyMapper:
    """A key mapper that ignores leading dots and trailing file extensions in both keys and file names.

    Args:
        hidden: Whether to include hidden files (i.e. files starting with a dot).
        strict: Whether to raise a AmbiguityError if multiple files match a key.
    """

    def __init__(self, hidden: bool = True, strict: bool = True) -> None:
        self._hidden = hidden
        self._strict = strict

    def get_path(self, key: str, parent: Path) -> Path | None:
        normalized = self._normalize(key)
        matches = self._find(parent, normalized)
        if len(matches) > 1:
            msg = f"{parent} has multiple matches for '{normalized}' ({', '.join(m.name for m in matches)}). Using {matches[0].name}."
            if self._strict:
                raise AmbiguityError(msg)
            logger.warning(msg)
        return next(iter(matches), None)

    def key_of(self, path: Path) -> str | None:
        return self._normalize(path.name)

    def _normalize(self, name: str) -> str:
        return name.lstrip(".").split(".")[0]

    def _find(self, parent: Path, normalized_key: str) -> Sequence[Path]:
        return (
            *parent.glob(normalized_key),
            *(parent.glob(f".{normalized_key}") if self._hidden else ()),
            *parent.glob(f"{normalized_key}.*"),
            *(parent.glob(f".{normalized_key}.*") if self._hidden else ()),
        )
