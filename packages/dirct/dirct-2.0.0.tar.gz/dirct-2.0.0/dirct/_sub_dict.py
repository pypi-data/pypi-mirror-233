from os import PathLike
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from ._base_dirct import BaseDirct
from .key_mappers import BasenameKeyMapper, KeyMapper
from .loaders import DEFAULT_LOADERS


class SubDirct(BaseDirct):
    """A dict that reflects the contents of a directory, but without the __self__.* file."""

    def __init__(
        self,
        path: str | PathLike[str],
        create_dirct: Callable[[Path], BaseDirct],
        loaders: Iterable[Callable[[Path], Any]] = DEFAULT_LOADERS,
        key_mapper: KeyMapper = BasenameKeyMapper(),
    ) -> None:
        super().__init__(path, loaders)
        self._key_mapper = key_mapper
        self._create_dirct = create_dirct

    def __getitem__(self, key: str) -> Any:
        path = self._get_path(key)
        if path.is_dir():
            return self._create_dirct(path)
        return self._load(path)

    def __iter__(self) -> Iterator[str]:
        return (
            key
            for path in self._path.iterdir()
            if (
                not path.name.startswith("__self__.")
                and (key := self._key_mapper.key_of(path))
            )
        )

    def _get_path(self, key: str) -> Path:
        """Get the path for the given key, trying the key as a file name first, then as the prefix of a file name (follewed by a dot)."""
        if path := self._key_mapper.get_path(key, self._path):
            return path
        raise KeyError(f"{self._path} has no file that matches {key}")
