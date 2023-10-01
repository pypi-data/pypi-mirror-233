import os
from collections.abc import Generator
from contextlib import contextmanager

import pytest

from wvutils.path import (
    ensure_abspath,
    is_pathlike,
    resolve_path,
    stringify_path,
    xdg_cache_path,
)


class PathLike:
    def __init__(self, path):
        self._path = path

    def __fspath__(self):
        return self._path


class NonPathLike:
    pass


@pytest.mark.parametrize(
    "potential_path, expected",
    [("path/to/file", True), (PathLike("path/to/file"), True), (NonPathLike(), False)],
)
def test_is_pathlike(potential_path, expected):
    assert is_pathlike(potential_path) is expected


@pytest.mark.parametrize(
    "path, expected",
    [("path/to/file", "path/to/file"), (PathLike("path/to/file"), "path/to/file")],
)
def test_stringify_path(path, expected):
    assert stringify_path(path) == expected


@pytest.mark.parametrize("path", [set(), list(), dict(), 1, 1.0, NonPathLike()])
def test_stringify_path_raises_on_non_pathlike(path):
    with pytest.raises(TypeError, match=r"Object is not path-like: .+"):
        stringify_path(path)


@pytest.mark.parametrize(
    "path, expected",
    [
        ("path/to/file", os.path.abspath("path/to/file")),
        ("/path/to/file", "/path/to/file"),
    ],
)
def test_ensure_abspath(path, expected):
    assert ensure_abspath(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("path/to/file", os.path.abspath("path/to/file")),
        ("/path/to/file", "/path/to/file"),
        (PathLike("path/to/file"), os.path.abspath("path/to/file")),
        (PathLike("/path/to/file"), "/path/to/file"),
    ],
)
def test_resolve_path(path, expected):
    assert resolve_path(path) == expected


@pytest.mark.parametrize("path", [set(), list(), dict(), 1, 1.0, NonPathLike()])
def test_resolve_path_raises_on_non_pathlike(path):
    with pytest.raises(TypeError, match=r"Object is not path-like: .+"):
        resolve_path(path)


@contextmanager
def set_xdg_cache_path(path: str | None) -> Generator[None, None, None]:
    """Context manager for temporarily setting the XDG_CACHE_HOME environment variable.

    Example:

    ```python
    from wvutils.path import set_xdg_cache_path
    from pathlib import Path

    path = Path('US/Eastern')
    with set_xdg_cache_path(path):
        # Do something that uses the XDG_CACHE_HOME environment variable
        pass
    ```

    Args:
        path (str): The path to set the environment variable to.
    """

    def setXDG(p) -> None:
        if p is None:
            try:
                del os.environ["XDG_CACHE_HOME"]
            except KeyError:
                pass
        else:
            os.environ["XDG_CACHE_HOME"] = p

    orig_path = os.environ.get("XDG_CACHE_HOME")
    setXDG(path)
    try:
        yield
    finally:
        setXDG(orig_path)


@pytest.mark.parametrize(
    "path, expected",
    [
        (None, os.path.join(os.path.expanduser("~"), ".cache")),
        ("", os.path.join(os.path.expanduser("~"), ".cache")),
        (" ", os.path.join(os.path.expanduser("~"), ".cache")),
        ("path/to/cache", os.path.join(os.path.expanduser("~"), ".cache")),
    ],
)
def test_xdg_cache_path(path, expected):
    with set_xdg_cache_path(path):
        assert xdg_cache_path() == expected


def test_xdg_cache_path_with_path(temp_dir):
    with set_xdg_cache_path(temp_dir):
        assert xdg_cache_path() == temp_dir
