"""Custom errors.

This module contains custom exceptions that are used throughout the package.
"""


class WVUtilsError(Exception):
    """Base class for all wvutils exceptions."""


class JSONError(Exception):
    """Base class for all JSON exceptions."""


class JSONEncodeError(JSONError, TypeError):
    """Raised when JSON serializing fails."""


class JSONDecodeError(JSONError, ValueError):
    """Raised when JSON deserializing fails."""


class PickleError(Exception):
    """Base class for all pickle exceptions."""


class PickleEncodeError(PickleError, TypeError):
    """Raised when pickle serializing fails."""


class PickleDecodeError(PickleError, ValueError):
    """Raised when unpickling fails."""


class HashError(Exception):
    """Base class for all hashing exceptions."""


class HashEncodeError(HashError, TypeError):
    """Raised when hashing fails."""


__all__ = []
