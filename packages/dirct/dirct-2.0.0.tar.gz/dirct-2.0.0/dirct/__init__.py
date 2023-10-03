"""
.. include:: ../README.md
"""


import importlib.metadata as metadata

__version__ = metadata.version(__package__ or __name__)

from .dirct import Dirct

__all__ = ("Dirct",)
