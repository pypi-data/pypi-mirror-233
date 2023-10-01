"""Custom type aliases and type variables.

This module contains custom type aliases and type variables used throughout the package.
"""
from __future__ import annotations

import collections
import io
import os
from collections.abc import Hashable
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from typing import TypeAlias

__all__ = [
    "AWSRegion",
    "FileObject",
    "FilePath",
    "JSONSerializable",
    "MD5Hashable",
    "Mask",
    "Masks",
    "PickleSerializable",
    "Span",
    "Spans",
]


# Python types
# DictKey: TypeAlias = str | int | float | bool | object | None
FilePath: TypeAlias = str | os.PathLike[str]
# FileObject: TypeAlias = io.IOBase | io.RawIOBase | io.BufferedIOBase | io.TextIOBase
FileObject: TypeAlias = io.TextIOBase | io.BytesIO

# Spans and masks
Span: TypeAlias = list[int] | tuple[int, int]
Spans: TypeAlias = list[Span] | collections.deque[Span]
Mask: TypeAlias = str
Masks: TypeAlias = list[Mask] | collections.deque[Mask]

# Serialization
JSONSerializable: TypeAlias = str | int | float | bool | list | dict | None
PickleSerializable: TypeAlias = object
MD5Hashable: TypeAlias = JSONSerializable | tuple | Hashable

# AWS
# TODO: Consider making this an enum or directly pulling from boto3. Either way switch to Literal or string.
AWSRegion: TypeAlias = Literal[
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "ca-central-1",
    "eu-north-1",
    "eu-west-3",
    "eu-west-2",
    "eu-west-1",
    "eu-central-1",
    "eu-south-1",
    "ap-south-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-east-1",
    "sa-east-1",
    "cn-north-1",
    "cn-northwest-1",
    "us-gov-east-1",
    "us-gov-west-1",
    "us-gov-secret-1",
    "us-gov-topsecret-1",
    "us-gov-topsecret-2",
    "me-south-1",
    "af-south-1",
    "eu-east-1",
    "eu-central-2",
    "ap-south-2",
    "ap-southeast-3",
    "me-south-2",
    "eu-north-1",
    "eu-south-1",
    "me-west-1",
    "ru-central-1",
    "ap-southeast-4",
    "ca-west-1",
]
