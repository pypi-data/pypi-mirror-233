"""Constant values.

This module contains constants that are used throughout the package.
"""
from __future__ import annotations

from string import ascii_letters, digits
from sys import maxsize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

__all__ = [
    "DEFAULT_SAFECHARS_ALLOWED_CHARS",
    "IS_64_BIT",
]

DEFAULT_SAFECHARS_ALLOWED_CHARS: Final[set[str]] = {"-", "_", *ascii_letters, *digits}


IS_64_BIT: Final[bool] = maxsize > 2**32
