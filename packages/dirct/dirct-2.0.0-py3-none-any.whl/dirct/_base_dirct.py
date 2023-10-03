from contextlib import suppress
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from .exceptions import UnsupportedFileError
from .loaders import DEFAULT_LOADERS


class BaseDirct(Mapping[str, Any]):
    def __init__(
        self,
        path: str | PathLike[str],
        loaders: Iterable[Callable[[Path], Any]] = DEFAULT_LOADERS,
    ) -> None:
        if not (path := Path(path)).is_dir():
            raise NotADirectoryError(path)
        self._path = path
        self._loaders = tuple(loaders)

    def to_dict(self) -> dict[str, Any]:
        """Convert this Dirct to a plain dict, recursively converting all subdirectories to dicts as well."""
        return {
            key: value.to_dict() if isinstance(value, BaseDirct) else value
            for key, value in self.items()
        }

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._path!r})"

    def _load(self, path: Path) -> Any:
        """Get a parser for the file extension of the given path, trying the longest extension first."""
        for parser in self._loaders:
            with suppress(UnsupportedFileError):
                return parser(path)
        raise UnsupportedFileError(f"No parser supports {path}.")
