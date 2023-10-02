"""
.. include:: ../README.md
"""


import importlib.metadata as metadata

__version__ = metadata.version(__package__ or __name__)

from .dirct import Dirct, FilesystemDirct
from .key_mappers import BasenameKeyMapper, ExactKeyMapper, KeyMapper

__all__ = (
    "Dirct",
    "FilesystemDirct",
    "KeyMapper",
    "BasenameKeyMapper",
    "ExactKeyMapper",
)
