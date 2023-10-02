import json
import logging
import tomllib
from contextlib import suppress
from itertools import chain
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, cast

import yaml
from more_itertools import unique_everseen

from .exceptions import InvalidSelfError, MultipleSelfError
from .key_mappers import BasenameKeyMapper, KeyMapper

logger = logging.getLogger(__name__)


class _BaseDirct(Mapping[str, Any]):
    def __init__(
        self,
        path: str | PathLike[str],
        parsers: Mapping[str, Callable[[str], Any]] = {},
    ) -> None:
        if not (path := Path(path)).is_dir():
            raise NotADirectoryError(path)
        self._path = path
        self._parsers: Mapping[str, Callable[[str], Any]] = {
            "toml": tomllib.loads,
            "yaml": yaml.safe_load,
            "yml": yaml.safe_load,
            "json": json.loads,
            **parsers,
        }

    def to_dict(self) -> dict[str, Any]:
        """Convert this Dirct to a plain dict, recursively converting all subdirectories to dicts as well."""
        return {
            key: value.to_dict() if isinstance(value, _BaseDirct) else value
            for key, value in self.items()
        }

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._path!r})"

    def _get_parser(self, path: Path) -> Callable[[str], Any]:
        """Get a parser for the file extension of the given path, trying the longest extension first."""
        suffixes = path.suffixes
        while suffixes:
            parser = self._parsers.get("".join(suffixes).lstrip("."))
            if parser:
                return parser
            suffixes.pop(0)
        return lambda text: text


class FilesystemDirct(_BaseDirct):
    """A dict that reflects the contents of a directory on the filesystem.

    The keys are the names of the files/subdirectories in the directory (subject to the rules imposed by the given `key_mapper`). The values are the parsed contents of the files, or nested Dirct objects for subdirectories.

    This class does no caching, so it will reflect any changes to the directory's contents. If you want to load the contents of the directory once and then use them, use `to_dict()` method.

    Args:
        path: The path to the directory.
        parsers: A mapping of additional file extensions to parse functions.
        key_mapper: A key converter to use to convert keys to paths and vice versa. Defaults to a BasenameConverter, which ignores leading dots and trailing file extensions.
    """

    def __init__(
        self,
        path: str | PathLike[str],
        parsers: Mapping[str, Callable[[str], Any]] = {},
        key_mapper: KeyMapper = BasenameKeyMapper(),
    ) -> None:
        super().__init__(path, parsers)
        self._key_mapper = key_mapper

    def __getitem__(self, key: str) -> Any:
        path = self._get_path(key)
        if path.is_dir():
            return Dirct(path)
        return self._get_parser(path)(path.read_text())

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


class _SelfDirct(_BaseDirct):
    def to_dict(self) -> dict[str, Any]:
        """Load the contents of this Dirct's __self__.* file or return an empty dict if it doesn't exist, or raise an InvalidSelfError if there are multiple or the contents aren't a dict."""
        if self_file := self._self_file():
            data = self._get_parser(self_file)(self_file.read_text())
            if not isinstance(data, dict):
                raise InvalidSelfError(f"{self_file} does not contain a dict.")
            return cast(dict[str, Any], data)
        return {}

    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict().keys())

    def _self_file(self) -> Path | None:
        """Get this Dirct's __self__.* file, or None if it doesn't exist, or raise an MultipleSelfError if there are multiple __self__.* files."""
        files = tuple(
            f
            for f in self._path.glob("__self__.*")
            if f.is_file() and f.suffix.lstrip(".") in self._parsers
        )
        if len(files) > 1:
            raise MultipleSelfError(
                f"{self._path} has multiple __self__.* files: ({', '.join(f.name for f in files)})."
            )
        return files[0] if files else None


class Dirct(_BaseDirct):
    """A dict that reflects the contents of a directory.

    The keys are the names of the files/subdirectories in the directory (subject to the rules imposed by the given `key_mapper`). The values are the parsed contents of the files, or nested Dirct objects for subdirectories.

    This class does no caching, so it will reflect any changes to the directory's contents. If you want to load the contents of the directory once and then use them, use `to_dict()` method.

    Additionally, if the directory contains a file named __self__.* (where * is any file extension supported by the parsers), the contents of that file will be added to the Dirct as well. This allows you to keep some of the keys in a single file and the rest in separate files or subdirectories.

    Args:
        path: The path to the directory.
        parsers: A mapping of additional file extensions to parse functions.
        key_converter: A key converter to use to convert keys to paths and vice versa. Defaults to a BasenameConverter, which ignores leading dots and trailing file extensions.
    """

    def __init__(
        self,
        path: str | PathLike[str],
        parsers: Mapping[str, Callable[[str], Any]] = {},
        key_mapper: KeyMapper = BasenameKeyMapper(),
    ) -> None:
        super().__init__(path, parsers)
        self._fs_dirct = FilesystemDirct(path, parsers, key_mapper)
        self._self_dirct = _SelfDirct(path, parsers)

    def to_dict(self) -> dict[str, Any]:
        """Convert this Dirct to a plain dict, recursively converting all subdirectories to dicts as well."""
        return {**self._self_dirct.to_dict(), **self._fs_dirct.to_dict()}

    def __getitem__(self, key: str) -> Any:
        with suppress(KeyError):
            return self._fs_dirct[key]
        with suppress(KeyError):
            return self._self_dirct.get(key)
        raise KeyError(
            f"'{key}' does not match any file in {self._path} or any key in {self._path}/__self__.*"
        )

    def __iter__(self) -> Iterator[str]:
        return unique_everseen(chain(self._fs_dirct, self._self_dirct))
