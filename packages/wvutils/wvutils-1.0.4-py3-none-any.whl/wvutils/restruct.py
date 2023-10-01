"""Utilities for restructuring data.

This module provides utilities for restructuring data, including serialization and hashing.

JSON

| Python                                 | JSON   |
| :------------------------------------- | :----- |
| dict                                   | object |
| list, tuple                            | array  |
| str                                    | string |
| int, float, int- & float-derived enums | number |
| True                                   | true   |
| False                                  | false  |
| None                                   | null   |

Hash

> No content.

Pickle

> An important difference between cloudpickle and pickle is that cloudpickle can serialize a function or class by value, whereas pickle can only serialize it by reference.
> Serialization by reference treats functions and classes as attributes of modules, and pickles them through instructions that trigger the import of their module at load time.
> Serialization by reference is thus limited in that it assumes that the module containing the function or class is available/importable in the unpickling environment.
> This assumption breaks when pickling constructs defined in an interactive session, a case that is automatically detected by cloudpickle, that pickles such constructs by value.

Read more: https://github.com/cloudpipe/cloudpickle/blob/master/README.md#overriding-pickles-serialization-mechanism-for-importable-constructs
"""
from __future__ import annotations

import json
import logging
from collections import deque
from hashlib import md5
from typing import TYPE_CHECKING

import cloudpickle
import rapidjson

from wvutils.errors import (
    HashEncodeError,
    JSONDecodeError,
    JSONEncodeError,
    PickleDecodeError,
    PickleEncodeError,
)

from wvutils.path import resolve_path

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from wvutils.type_aliases import (
        FilePath,
        JSONSerializable,
        MD5Hashable,
        PickleSerializable,
    )


__all__ = [
    "gen_hash",
    "json_dump",
    "json_dumps",
    "json_load",
    "json_loads",
    "jsonl_dump",
    "jsonl_dumps",
    "jsonl_loader",
    "pickle_dump",
    "pickle_dumps",
    "pickle_load",
    "pickle_loads",
    "squeegee_loader",
]

logger: logging.Logger = logging.getLogger(__name__)


def json_dumps(obj: JSONSerializable) -> str:
    """Encode an object as JSON.

    Args:
        obj (JSONSerializable): Object to encode.

    Returns:
        str: Object encoded as JSON.

    Raises:
        JSONEncodeError: If the object could not be encoded.
    """
    try:
        return rapidjson.dumps(obj, default=str, number_mode=rapidjson.NM_NATIVE)
    except (TypeError, ValueError) as err:
        raise JSONEncodeError("Could not encode object") from err


def jsonl_dumps(objs: Iterable[JSONSerializable]) -> str:
    """Encode objects as JSONL.

    Args:
        objs (Iterable[JSONSerializable]): Objects to encode.

    Returns:
        str: Objects encoded as JSONL.

    Raises:
        JSONEncodeError: If the objects could not be encoded.
    """
    try:
        return "\n".join(map(json_dumps, objs))
    except JSONEncodeError as err:
        raise JSONEncodeError("Could not encode objects") from err


def json_dump(obj: JSONSerializable, file_path: str) -> None:
    """Encode an object as JSON and write it to a file.

    Args:
        file_path (str): Path of the file to open.

    Raises:
        JSONEncodeError: If the object could not be encoded.
    """
    file_path = resolve_path(file_path)
    try:
        with open(file_path, mode="w", encoding="utf-8") as wf:
            rapidjson.dump(obj, wf, default=str, number_mode=rapidjson.NM_NATIVE)
    except (TypeError, ValueError) as err:
        raise JSONEncodeError("Could not encode object") from err


def jsonl_dump(objs: Iterable[JSONSerializable], file_path: str) -> None:
    """Encode objects as JSONL and write them to a file.

    Args:
        objs (Iterable[JSONSerializable]): Objects to encode.
        file_path (str): Path of the file to open.

    Raises:
        JSONEncodeError: If the objects could not be encoded.
    """
    file_path = resolve_path(file_path)
    try:
        with open(file_path, mode="w", encoding="utf-8") as wf:
            wf.write(jsonl_dumps(objs))
    except JSONEncodeError as err:
        raise JSONEncodeError("Could not encode objects") from err


def json_loads(encoded_obj: str) -> JSONSerializable:
    """Decode a JSON-encoded object.

    Args:
        encoded_obj (str): Object to decode.

    Returns:
        JSONSerializable: Decoded object.

    Raises:
        JSONDecodeError: If the object could not be decoded.
    """
    try:
        return rapidjson.loads(encoded_obj, number_mode=rapidjson.NM_NATIVE)
    except (TypeError, rapidjson.JSONDecodeError) as err:  # OverflowError)
        raise JSONDecodeError("Could not decode object") from err


def json_load(file_path: FilePath) -> JSONSerializable:
    """Decode a file containing a JSON-encoded object.

    Args:
        file_path (FilePath): Path of the file to open.

    Returns:
        JSONSerializable: Decoded object.

    Raises:
        JSONDecodeError: If the file could not be decoded.
    """
    file_path = resolve_path(file_path)
    try:
        with open(file_path, mode="r", encoding="utf-8") as rf:
            return rapidjson.load(rf, number_mode=rapidjson.NM_NATIVE)
    except (TypeError, rapidjson.JSONDecodeError) as err:  # OverflowError)
        raise JSONDecodeError(f"Could not decode file '{file_path}'") from err


def jsonl_loader(
    file_path: FilePath,
    *,
    allow_empty_lines: bool = False,
) -> Generator[JSONSerializable, None, None]:
    """Decode a file containing JSON-encoded objects, one per line.

    Args:
        file_path (FilePath): Path of the file to open.
        allow_empty_lines (bool, optional): Whether to allow (skip) empty lines. Defaults to False.

    Yields:
        JSONSerializable: Decoded object.

    Raises:
        JSONDecodeError: If the line could not be decoded, or if an empty line was found and `allow_empty_lines` is False.
    """
    file_path = resolve_path(file_path)
    with open(file_path, mode="r", encoding="utf-8") as rf:
        for line in rf:
            # Remove trailing whitespace
            line = line.rstrip()
            # Handle empty lines
            if not line:
                if allow_empty_lines:
                    continue
                else:
                    raise JSONDecodeError(f"Could not decode file '{file_path}'")
            try:
                decoded_obj = json_loads(line)
            except JSONDecodeError as err:
                raise JSONDecodeError(f"Could not decode file '{file_path}'") from err
            yield decoded_obj


def squeegee_loader(file_path: FilePath) -> Generator[JSONSerializable, None, None]:
    """Automatically decode a file containing JSON-encoded objects.

    Supports multiple formats (JSON, JSONL, JSONL of JSONL, etc).

    Todo:
        * Add support for pretty-printed JSON that has been appended to a file.


    Args:
        file_path (FilePath): Path of the file to open.

    Yields:
        JSONSerializable: Decoded object.

    Raises:
        JSONDecodeError: If the line could not be decoded.
    """
    file_path = resolve_path(file_path)

    # Try to decode as JSON standard
    try:
        decoded_obj = json_load(file_path)
    except JSONDecodeError:
        decoded_obj = None

    if decoded_obj is not None:
        # Recognized as JSON (JSON standard)
        if isinstance(decoded_obj, list):
            # List of objects on multiple lines
            for single_content in decoded_obj:
                yield single_content
        else:
            # Single object on multiple lines
            yield decoded_obj
    else:
        # Recognized as JSONL (JSON line)
        for decoded_obj in jsonl_loader(file_path, allow_empty_lines=True):
            if isinstance(decoded_obj, list):
                # List of objects on single line
                for single_content in decoded_obj:
                    yield single_content
            else:
                # Single object on single line
                yield decoded_obj
    # TODO: Add support for mix of pretty-printed JSON and JSONL


def gen_hash(obj: MD5Hashable) -> str:
    """Create an MD5 hash from a hashable object.

    Note: Tuples and deques are not hashable, so they are converted to lists.

    Args:
        obj (MD5Hashable): Object to hash.

    Returns:
        str: MD5 hash of the object.

    Raises:
        HashEncodeError: If the object could not be encoded.
    """
    obj_b = None
    try:
        if isinstance(obj, bytes):
            obj_b = obj
        elif isinstance(obj, str):
            obj_b = obj.encode("utf-8")
        elif isinstance(obj, (dict, int, float, bool, list)):
            obj_b = json_dumps(obj).encode("utf-8")
        elif isinstance(obj, (tuple, deque)):
            obj_list = list(obj)
            obj_b = json_dumps(obj_list).encode("utf-8")
    except (TypeError, json.JSONDecodeError) as err:
        raise HashEncodeError("Could not hash object") from err
    if obj_b is None:
        raise HashEncodeError("Could not hash object")
    return md5(obj_b).hexdigest()


def pickle_dump(obj: PickleSerializable, file_path: FilePath) -> None:
    """Serialize an object as a pickle and write it to a file.

    Args:
        obj (JSONSerializable): Object to serialize.
        file_path (FilePath): Path of the file to write.

    Raises:
        PickleEncodeError: If the object could not be encoded.
    """
    with open(file_path, mode="wb") as wb:
        try:
            cloudpickle.dump(obj, wb)
        except (TypeError, cloudpickle.pickle.PicklingError) as err:
            raise PickleEncodeError("Could not pickle object") from err


def pickle_dumps(obj: PickleSerializable) -> bytes:
    """Serialize an object as a pickle.

    Args:
        obj (PickleSerializable): Object to serialize.

    Returns:
        bytes: Serialized object.

    Raises:
        PickleEncodeError: If the object could not be encoded.
    """
    try:
        return cloudpickle.dumps(obj)
    except (TypeError, cloudpickle.pickle.PicklingError) as err:
        raise PickleEncodeError("Could not pickle object") from err


def pickle_load(file_path: FilePath) -> PickleSerializable:
    """Deserialize a pickle-serialized object from a file.

    Note: Not safe for large files.

    Args:
        file_path (FilePath): Path of the file to open.

    Returns:
        PickleSerializable: Deserialized object.

    Raises:
        PickleDecodeError: If the object could not be decoded.
    """
    with open(file_path, mode="rb") as rb:
        try:
            return cloudpickle.load(rb)
        except (TypeError, cloudpickle.pickle.UnpicklingError) as err:
            raise PickleDecodeError("Could not unpickle object") from err


def pickle_loads(serialized_obj: bytes) -> PickleSerializable:
    """Deserialize a pickle-serialized object.

    Args:
        serialized_obj (bytes): Object to deserialize.

    Returns:
        PickleSerializable: Deserialized object.

    Raises:
        PickleDecodeError: If the object could not be decoded.
    """
    try:
        return cloudpickle.loads(serialized_obj)
    except (TypeError, cloudpickle.pickle.UnpicklingError) as err:
        raise PickleDecodeError("Could not unpickle object") from err
