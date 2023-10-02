"""
.. include:: ../README.md
"""


import importlib.metadata as metadata

__version__ = metadata.version(__package__ or __name__)
__all__ = ("InsensitiveStrEnum",)


from enum import StrEnum
from typing import Any


class InsensitiveStrEnum(StrEnum):
    """A case-insensitive string enum."""

    @classmethod
    def _missing_(cls, value: object) -> Any:
        value = value.lower() if isinstance(value, str) else value
        for member in cls:
            if member == value:
                return member
        return None
