from pathlib import Path
from typing import Any, Iterator, cast

from dirct._base_dirct import BaseDirct
from dirct.exceptions import InvalidSelfError, MultipleSelfError


class SelfDirct(BaseDirct):
    def to_dict(self) -> dict[str, Any]:
        """Load the contents of this Dirct's __self__.* file or return an empty dict if it doesn't exist, or raise an InvalidSelfError if there are multiple or the contents aren't a dict."""
        if self_file := self._self_file():
            data = self._load(self_file)
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
        files = tuple(f for f in self._path.glob("__self__.*") if f.is_file())
        if len(files) > 1:
            raise MultipleSelfError(
                f"{self._path} has multiple __self__.* files: ({', '.join(f.name for f in files)})."
            )
        return files[0] if files else None
