import logging
from contextlib import suppress
from itertools import chain
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from more_itertools import unique_everseen

from ._base_dirct import BaseDirct
from ._self_dirct import SelfDirct
from ._sub_dict import SubDirct
from .key_mappers import ExactKeyMapper, KeyMapper
from .loaders import DEFAULT_LOADERS

logger = logging.getLogger(__name__)


class Dirct(BaseDirct):
    """A dict that reflects the contents of a directory.

    The keys are the names of the files/subdirectories in the directory (subject to the rules imposed by the given `key_mapper`). The values are the parsed contents of the files, or nested Dirct objects for subdirectories.

    This class does no caching, so it will reflect any changes to the directory's contents. If you want to load the contents of the directory once and then use them, use `to_dict()` method.

    Additionally, if the directory contains a file named __self__.* (where * is any file extension supported by the parsers), the contents of that file will be added to the Dirct as well. This allows you to keep some of the keys in a single file and the rest in separate files or subdirectories.

    The `loaders` parameter can be passed to specify which loaders to use to try to load files. A loader is a callable that takes a `Path` and returns the parsed contents. Loaders are tried in order. If a loader raises `UnsupportedFileError`, the next loader is tried, but if it raises any other kind of exception, it is propagated. If no loader can load a file, `UnsupportedFileError` is raised.

    Args:
        path: The path to the directory.
        loaders: The callables to use to try to load files. Defaults to `DEFAULT_LOADERS`, which supports JSON, YAML, TOML, plain text, and binary files.
        key_converter: A key converter to use to convert keys to paths and vice versa. Defaults to an `ExactKeyMapper` that uses the exact file names as keys.
    """

    def __init__(
        self,
        path: str | PathLike[str],
        loaders: Iterable[Callable[[Path], Any]] = DEFAULT_LOADERS,
        key_mapper: KeyMapper = ExactKeyMapper(),
    ) -> None:
        super().__init__(path, loaders)
        self._sub_dirct = SubDirct(
            path, lambda p: Dirct(p, loaders, key_mapper), loaders, key_mapper
        )
        self._self_dirct = SelfDirct(path, loaders)

    def to_dict(self) -> dict[str, Any]:
        """Convert this Dirct to a plain dict, recursively converting all subdirectories to dicts as well."""
        return {**self._self_dirct.to_dict(), **self._sub_dirct.to_dict()}

    def __getitem__(self, key: str) -> Any:
        with suppress(KeyError):
            return self._sub_dirct[key]
        with suppress(KeyError):
            return self._self_dirct.get(key)
        raise KeyError(
            f"'{key}' does not match any file in {self._path} or any key in {self._path}/__self__.*"
        )

    def __iter__(self) -> Iterator[str]:
        return unique_everseen(chain(self._sub_dirct, self._self_dirct))
