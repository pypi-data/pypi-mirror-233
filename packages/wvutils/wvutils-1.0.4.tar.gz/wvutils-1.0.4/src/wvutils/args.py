"""Utilities for parsing arguments from the command line.

This module provides utilities for parsing arguments from the command line.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from wvutils.constants import DEFAULT_SAFECHARS_ALLOWED_CHARS

if TYPE_CHECKING:
    from collections.abc import Callable, Collection

__all__ = [
    "nonempty_string",
    "safechars_string",
]

logger: logging.Logger = logging.getLogger(__name__)


def nonempty_string(name: str) -> Callable[[str], str]:
    """Ensure a string is non-empty.

    Example:

    ```python
    subparser.add_argument(
        "hashtag",
        type=nonempty_string("hashtag"),
        help="A hashtag (without #)",
    )
    ```

    Args:
        name (str): Name of the function, used for debugging.

    Returns:
        Callable[[str], str]: The decorated function.
    """

    def func(text):
        text = text.strip()
        if not text:
            raise ValueError("Must not be an empty string")
        return text

    func.__name__ = name
    return func


def safechars_string(
    name: str,
    allowed_chars: Collection[str] | None = None,
) -> Callable[[str], str]:
    """Ensure a string contains only safe characters.

    Example:

    ```python
    subparser.add_argument(
        "--session-key",
        type=safechars_string,
        help="Key to share a single token across processes",
    )
    ```

    Args:
        name (str): Name of the function, used for debugging.
        allowed_chars (Collection[str] | None, optional): Custom characters used to validate the function name. Defaults to None.

    Returns:
        Callable[[str], str]: The decorated function.

    Raises:
        ValueError: If empty collection of allowed characters is provided.
    """
    if allowed_chars is None:
        # Default to alphanum
        allowed_chars = DEFAULT_SAFECHARS_ALLOWED_CHARS
    else:
        # Prepare user-provided chars
        allowed_chars = set(allowed_chars)

    if len(allowed_chars) == 0:
        raise ValueError("Must provide at least one character")

    def func(text):
        text = text.strip()
        for char in text:
            if char not in allowed_chars:
                msg = ""
                msg += "Must consist of characters ["
                if allowed_chars:
                    msg += "'"
                    msg += "', '".join(allowed_chars)
                    msg += "'"
                msg += "]"
                raise ValueError(msg)
        return text

    func.__name__ = name
    return func
