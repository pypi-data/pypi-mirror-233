import json
import tomllib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml

from dirct.exceptions import UnsupportedFileError


class FileExtensionLoader(ABC):
    """A base class for loaders that support specific file extensions."""

    def __init__(self, *extensions: str) -> None:
        self._ext = extensions

    def __call__(self, path: Path) -> Any:
        if any(path.name.endswith(ext) for ext in self._ext):
            return self.load(path)
        raise UnsupportedFileError

    @abstractmethod
    def load(self, path: Path) -> Any:
        ...


class TomlLoader(FileExtensionLoader):
    def __init__(self) -> None:
        super().__init__(".toml")

    def load(self, path: Path) -> dict[str, Any]:
        with path.open("rb") as f:
            return tomllib.load(f)


class YamlLoader(FileExtensionLoader):
    def __init__(self) -> None:
        super().__init__(".yaml", ".yml")

    def load(self, path: Path) -> Any:
        with path.open("rb") as f:
            return yaml.safe_load(f)


class JsonLoader(FileExtensionLoader):
    def __init__(self) -> None:
        super().__init__(".json")

    def load(self, path: Path) -> Any:
        with path.open("rb") as f:
            return json.load(f)


class TextLoader:
    def __call__(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise UnsupportedFileError


class BinaryLoader:
    def __call__(self, path: Path) -> bytes:
        return path.read_bytes()


DEFAULT_LOADERS = (
    TomlLoader(),
    YamlLoader(),
    JsonLoader(),
    TextLoader(),
    BinaryLoader(),
)
