# WVUtils

[WVUtils](https://github.com/Phosmic/wvutils) is a collection of utilities that are shared across multiple [Phosmic](https://phosmic.com) projects.

---

## Requirements:

**WVUtils** requires Python 3.10 or higher and is platform independent.

## Issue reporting

If you discover an issue with WVUtils, please report it at [https://github.com/Phosmic/wvutils/issues](https://github.com/Phosmic/wvutils/issues).

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

---

-   [Requirements](#requirements)
-   [Installing](#installing)
-   [Library](#library)

## Installing

Most stable version from [**PyPi**](https://pypi.org/project/wvutils/):

[![PyPI](https://img.shields.io/pypi/v/wvutils?style=flat-square)](https://pypi.org/project/wvutils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wvutils?style=flat-square)](https://pypi.org/project/wvutils/)
[![PyPI - License](https://img.shields.io/pypi/l/wvutils?style=flat-square)](https://pypi.org/project/wvutils/)

```bash
python3 -m pip install wvutils
```

Development version from [**GitHub**](https://github.com/Phosmic/wvutils):


![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Phosmic/wvutils/ubuntu.yml?style=flat-square)
![Codecov](https://img.shields.io/codecov/c/github/Phosmic/wvutils/master?flag=unittests&style=flat-square&token=t9poCrjbiR)
![GitHub](https://img.shields.io/github/license/Phosmic/wvutils?style=flat-square)


```bash
git clone git+https://github.com/Phosmic/wvutils.git
cd wvutils
python3 -m pip install -e .
```

---

## Library

<a id="wvutils.aws"></a>

# `wvutils.aws`

Utilities for interacting with AWS services.

This module provides utilities for interacting with AWS services.

<a id="wvutils.aws.get_boto3_session"></a>

#### `get_boto3_session`

```python
def get_boto3_session(region_name: AWSRegion) -> Session
```

Get the globally shared Boto3 session for a region (thread-safe).

**Todo**:

  * Add support for other session parameters.

**Arguments**:

- `region_name` _AWSRegion_ - Region name for the session.

**Returns**:

- _Session_ - Boto3 session.

<a id="wvutils.aws.clear_boto3_sessions"></a>

#### `clear_boto3_sessions`

```python
def clear_boto3_sessions() -> int
```

Clear all globally shared Boto3 sessions (thread-safe).

**Returns**:

- _int_ - Number of sessions cleared.

<a id="wvutils.aws.boto3_client_ctx"></a>

#### `boto3_client_ctx`

```python
@contextmanager
def boto3_client_ctx(service_name: str, region_name: AWSRegion)
```

Context manager for a Boto3 client (thread-safe).

**Todo**:

  * Add support for other session parameters.

**Arguments**:

- `service_name` _str_ - Name of the service.
- `region_name` _AWSRegion_ - Region name for the service.

**Yields**:

- _Any_ - Boto3 client.

**Raises**:

- `ClientError` - If an error occurs.

<a id="wvutils.aws.parse_s3_uri"></a>

#### `parse_s3_uri`

```python
def parse_s3_uri(s3_uri: str) -> tuple[str, str]
```

Parse the bucket name and path from a S3 URI.

**Arguments**:

- `s3_uri` _str_ - S3 URI to parse.

**Returns**:

- _tuple[str, str]_ - Bucket name and path.

<a id="wvutils.aws.download_from_s3"></a>

#### `download_from_s3`

```python
def download_from_s3(file_path: FilePath,
                     bucket_name: str,
                     bucket_path: str,
                     region_name: AWSRegion,
                     overwrite: bool = False) -> None
```

Download a file from S3.

**Arguments**:

- `file_path` _FilePath_ - Output path to use while downloading the file.
- `bucket_name` _str_ - Name of the S3 bucket containing the file.
- `bucket_path` _str_ - Path of the S3 bucket containing the file.
- `region_name` _AWSRegion_ - Region name for S3.
- `overwrite` _bool_ - Overwrite file on disk if already exists. Defaults to False.

**Raises**:

- `FileExistsError` - If the file already exists and overwrite is False.

<a id="wvutils.aws.upload_file_to_s3"></a>

#### `upload_file_to_s3`

```python
def upload_file_to_s3(file_path: FilePath, bucket_name: str, bucket_path: str,
                      region_name: AWSRegion) -> None
```

Upload a file to S3.

**Arguments**:

- `file_path` _FilePath_ - Path of the file to upload.
- `bucket_name` _str_ - Name of the S3 bucket to upload the file to.
- `bucket_path` _str_ - Path in the S3 bucket to upload the file to.
- `region_name` _AWSRegion_ - Region name for S3.

**Raises**:

- `FileNotFoundError` - If the file does not exist.

<a id="wvutils.aws.upload_bytes_to_s3"></a>

#### `upload_bytes_to_s3`

```python
def upload_bytes_to_s3(raw_b: bytes, bucket_name: str, bucket_path: str,
                       region_name: AWSRegion) -> None
```

Write bytes to a file in S3.

**Arguments**:

- `raw_b` _bytes_ - Bytes of the file to be written.
- `bucket_name` _str_ - Name of the S3 bucket to upload the file to.
- `bucket_path` _str_ - Path in the S3 bucket to upload the file to.
- `region_name` _AWSRegion_ - Region name for S3.

<a id="wvutils.aws.secrets_fetch"></a>

#### `secrets_fetch`

```python
def secrets_fetch(
        secret_name: str,
        region_name: AWSRegion) -> str | int | float | list | dict | None
```

Request and decode a secret from Secrets.

**Arguments**:

- `secret_name` _str_ - Secret name to use.
- `region_name` _AWSRegion_ - Region name for Secrets.

**Returns**:

- _str | int | float | list | dict | None_ - Secret string.

**Raises**:

- `ClientError` - If an error occurs while fetching the secret.
- `ValueError` - If the secret is not valid JSON.

<a id="wvutils.aws.athena_execute_query"></a>

#### `athena_execute_query`

```python
def athena_execute_query(query: str, database_name: str,
                         region_name: AWSRegion) -> str | None
```

Execute a query in Athena.

**Arguments**:

- `query` _str_ - Query to execute.
- `database_name` _str_ - Name of database to execute the query against.
- `region_name` _AWSRegion_ - Region name for Athena.

**Returns**:

- _str | None_ - Query execution ID of the query.

<a id="wvutils.aws.athena_retrieve_query"></a>

#### `athena_retrieve_query`

```python
def athena_retrieve_query(qeid: str, database_name: str,
                          region_name: AWSRegion) -> str | None
```

Retrieve the S3 URI for results of a query in Athena.

**Arguments**:

- `qeid` _str_ - Query execution ID of the query to fetch.
- `database_name` _str_ - Name of the database the query is running against (for debugging).
- `region_name` _AWSRegion_ - Region name for Athena.

**Returns**:

- _str | None_ - Current status of the query, or S3 URI where results are stored.

**Raises**:

- `ValueError` - If the query execution ID is unknown or missing.

<a id="wvutils.aws.athena_stop_query"></a>

#### `athena_stop_query`

```python
def athena_stop_query(qeid: str, region_name: AWSRegion) -> None
```

Stop the execution of a query in Athena.

**Arguments**:

- `qeid` _str_ - Query execution ID of the query to stop.
- `region_name` _AWSRegion_ - Region name for Athena.

<a id="wvutils.errors"></a>

# `wvutils.errors`

Custom errors.

This module contains custom exceptions that are used throughout the package.

<a id="wvutils.errors.WVUtilsError"></a>

## `WVUtilsError` Objects

```python
class WVUtilsError(Exception)
```

Base class for all wvutils exceptions.

<a id="wvutils.errors.JSONError"></a>

## `JSONError` Objects

```python
class JSONError(Exception)
```

Base class for all JSON exceptions.

<a id="wvutils.errors.JSONEncodeError"></a>

## `JSONEncodeError` Objects

```python
class JSONEncodeError(JSONError, TypeError)
```

Raised when JSON serializing fails.

<a id="wvutils.errors.JSONDecodeError"></a>

## `JSONDecodeError` Objects

```python
class JSONDecodeError(JSONError, ValueError)
```

Raised when JSON deserializing fails.

<a id="wvutils.errors.PickleError"></a>

## `PickleError` Objects

```python
class PickleError(Exception)
```

Base class for all pickle exceptions.

<a id="wvutils.errors.PickleEncodeError"></a>

## `PickleEncodeError` Objects

```python
class PickleEncodeError(PickleError, TypeError)
```

Raised when pickle serializing fails.

<a id="wvutils.errors.PickleDecodeError"></a>

## `PickleDecodeError` Objects

```python
class PickleDecodeError(PickleError, ValueError)
```

Raised when unpickling fails.

<a id="wvutils.errors.HashError"></a>

## `HashError` Objects

```python
class HashError(Exception)
```

Base class for all hashing exceptions.

<a id="wvutils.errors.HashEncodeError"></a>

## `HashEncodeError` Objects

```python
class HashEncodeError(HashError, TypeError)
```

Raised when hashing fails.

<a id="wvutils.path"></a>

# `wvutils.path`

Utilities for working with paths.

This module provides utilities for working with paths.

<a id="wvutils.path.is_pathlike"></a>

#### `is_pathlike`

```python
def is_pathlike(potential_path: Any) -> bool
```

Check if an object is path-like.

An object is path-like if it is a string or has a `__fspath__` method.

**Arguments**:

- `potential_path` _Any_ - Object to check.

**Returns**:

- _bool_ - True if the object is path-like, otherwise False.

<a id="wvutils.path.stringify_path"></a>

#### `stringify_path`

```python
def stringify_path(file_path: FilePath) -> str
```

Stringify a path-like object.

The path-like object is first converted to a string, then the user directory is expanded.
> An object is path-like if it is a string or has a `__fspath__` method.

**Arguments**:

- `file_path` _FilePath_ - Path-like object to stringify.

**Returns**:

- _str_ - Path-like object as a string.

**Raises**:

- `TypeError` - If the object is not path-like.

<a id="wvutils.path.ensure_abspath"></a>

#### `ensure_abspath`

```python
def ensure_abspath(file_path: str) -> str
```

Make a path absolute if it is not already.

**Arguments**:

- `file_path` _str_ - Path to ensure is absolute.

**Returns**:

- _str_ - Absolute path.

<a id="wvutils.path.resolve_path"></a>

#### `resolve_path`

```python
def resolve_path(file_path: FilePath) -> str
```

Stringify and resolve a path-like object.

The path-like object is first converted to a string, then the user directory is expanded, and finally the path is resolved to an absolute path.
> An object is path-like if it is a string or has a `__fspath__` method.

**Arguments**:

- `file_path` _FilePath_ - Path-like object to resolve.

**Returns**:

- _str_ - Absolute path of the path-like object as a string.

**Raises**:

- `TypeError` - If the object is not path-like.

<a id="wvutils.path.xdg_cache_path"></a>

#### `xdg_cache_path`

```python
def xdg_cache_path() -> str
```

Base directory to store user-specific non-essential data files.

This should be '${HOME}/.cache', but the 'HOME' environment variable may not exist on non-POSIX-compliant systems.
On POSIX-compliant systems, the XDG base directory specification is followed exactly since '~' expands to '$HOME' if it is present.

**Returns**:

- _str_ - Path for XDG cache.

<a id="wvutils.proxies"></a>

# `wvutils.proxies`

Utilities for working with proxies.

This module provides utilities for working with proxies.

<a id="wvutils.proxies.ProxyManager"></a>

## `ProxyManager` Objects

```python
class ProxyManager()
```

Manages a list of proxies.

This class manages a list of proxies, allowing for randomization, re-use, etc.

<a id="wvutils.proxies.ProxyManager.add_proxies"></a>

#### `ProxyManager.add_proxies`

```python
def add_proxies(proxies: list[str], include_duplicates: bool = False) -> None
```

Add additional proxy addresses.

All proxy addresses added will be added to the end of the list.

**Arguments**:

- `proxies` _list[str]_ - List of proxy addresses.
- `include_duplicates` _bool, optional_ - Whether to include duplicates. Defaults to False.

<a id="wvutils.proxies.ProxyManager.set_proxies"></a>

#### `ProxyManager.set_proxies`

```python
def set_proxies(proxies: list[str]) -> None
```

Set the proxy addresses.

Note: This will clear all existing proxies.

**Arguments**:

- `proxies` _list[str]_ - List of proxy addresses.

<a id="wvutils.proxies.ProxyManager.can_cycle"></a>

#### `ProxyManager.can_cycle`

```python
@property
def can_cycle() -> bool
```

Check if can cycle to the next proxy address.

**Returns**:

- _bool_ - True if can cycle, False otherwise.

<a id="wvutils.proxies.ProxyManager.cycle"></a>

#### `ProxyManager.cycle`

```python
def cycle() -> None
```

Attempt to cycle to the next proxy address.

<a id="wvutils.proxies.ProxyManager.proxy"></a>

#### `ProxyManager.proxy`

```python
@property
def proxy() -> str | None
```

Current proxy address.

**Returns**:

- _str | None_ - Current proxy, or None if no proxies.

<a id="wvutils.proxies.https_to_http"></a>

#### `https_to_http`

```python
def https_to_http(address: str) -> str
```

Convert a HTTPS proxy address to HTTP.

**Arguments**:

- `address` _str_ - HTTPS proxy address.

**Returns**:

- _str_ - HTTP proxy address.

**Raises**:

- `ValueError` - If the address does not start with 'http://' or 'https://'.

<a id="wvutils.proxies.prepare_http_proxy_for_requests"></a>

#### `prepare_http_proxy_for_requests`

```python
def prepare_http_proxy_for_requests(address: str) -> dict[str, str]
```

Prepare a HTTP(S) proxy address for use with the 'requests' library.

**Arguments**:

- `address` _str_ - HTTP(S) proxy address.

**Returns**:

- _dict[str, str]_ - Dictionary of HTTP and HTTPS proxy addresses.

**Raises**:

- `ValueError` - If the address does not start with 'http://' or 'https://'.

<a id="wvutils.args"></a>

# `wvutils.args`

Utilities for parsing arguments from the command line.

This module provides utilities for parsing arguments from the command line.

<a id="wvutils.args.nonempty_string"></a>

#### `nonempty_string`

```python
def nonempty_string(name: str) -> Callable[[str], str]
```

Ensure a string is non-empty.

**Example**:

```python
subparser.add_argument(
    "hashtag",
    type=nonempty_string("hashtag"),
    help="A hashtag (without #)",
)
```

**Arguments**:

- `name` _str_ - Name of the function, used for debugging.

**Returns**:

- _Callable[[str], str]_ - The decorated function.

<a id="wvutils.args.safechars_string"></a>

#### `safechars_string`

```python
def safechars_string(
        name: str,
        allowed_chars: Collection[str] | None = None) -> Callable[[str], str]
```

Ensure a string contains only safe characters.

**Example**:

```python
subparser.add_argument(
    "--session-key",
    type=safechars_string,
    help="Key to share a single token across processes",
)
```

**Arguments**:

- `name` _str_ - Name of the function, used for debugging.
- `allowed_chars` _Collection[str] | None, optional_ - Custom characters used to validate the function name. Defaults to None.

**Returns**:

- _Callable[[str], str]_ - The decorated function.

**Raises**:

- `ValueError` - If empty collection of allowed characters is provided.

<a id="wvutils.general"></a>

# `wvutils.general`

General utilities for working with Python.

This module provides general utilities for working with Python.

<a id="wvutils.general.is_readable_iolike"></a>

#### `is_readable_iolike`

```python
def is_readable_iolike(potential_io: Any) -> bool
```

Check if an object is a readable IO-like.

An object is readable IO-like if it has one of the following:
* callable `readable` method that returns True

Or if it has all of the following:
* callable `read` method.
* string attribute `mode` that contains "r".
* callable `seek` method.
* callable `close` method.
* callable `__enter__` method.
* callable `__exit__` method.

**Arguments**:

- `potential_io` _Any_ - Object to check.

**Returns**:

- _bool_ - True if the object is a readable IO-like, otherwise False.

<a id="wvutils.general.is_writable_iolike"></a>

#### `is_writable_iolike`

```python
def is_writable_iolike(potential_io: Any) -> bool
```

Check if an object is a writable IO-like.

An object is writable IO-like if it has one of the following:
* callable `writable` method that returns True

Or if it has all of the following:
* callable `write` method.
* string attribute `mode` that contains "w".
* callable `seek` method.
* callable `close` method.
* callable `__enter__` method.
* callable `__exit__` method.

**Arguments**:

- `potential_io` _Any_ - Object to check.

**Returns**:

- _bool_ - True if the object is a writable IO-like, otherwise False.

<a id="wvutils.general.is_iolike"></a>

#### `is_iolike`

```python
def is_iolike(potential_io: Any) -> bool
```

Check if an object is IO-like.

An object is IO-like if it has one of the following:
* `io.IOBase` base class
* Calling `is_readable_iolike` returns True. (see [is_readable_iolike](#wvutils.general.is_readable_iolike))
* Calling `is_writable_iolike` returns True. (see [is_writable_iolike](#wvutils.general.is_writable_iolike))

**Arguments**:

- `potential_io` _Any_ - Object to check.

**Returns**:

- _bool_ - True if the object is IO-like, otherwise False.

<a id="wvutils.general.count_lines_in_file"></a>

#### `count_lines_in_file`

```python
def count_lines_in_file(file_path: FilePath) -> int
```

Count the number of lines in a file.

**Notes**:

  All files have at least 1 line (# of lines = # of newlines + 1).

**Arguments**:

- `file_path` _FilePath_ - Path of the file to count lines in.

**Returns**:

- _int_ - Total number of lines in the file.

<a id="wvutils.general.sys_set_recursion_limit"></a>

#### `sys_set_recursion_limit`

```python
def sys_set_recursion_limit() -> None
```

Raise recursion limit to allow for more recurse.

<a id="wvutils.general.gc_set_threshold"></a>

#### `gc_set_threshold`

```python
def gc_set_threshold() -> None
```

Reduce Number of GC Runs to Improve Performance

**Notes**:

  Only applies to CPython.

<a id="wvutils.general.chunker"></a>

#### `chunker`

```python
def chunker(seq: Sequence[Any],
            n: int) -> Generator[Sequence[Any], None, None]
```

Iterate a sequence in size `n` chunks.

**Arguments**:

- `seq` _Sequence[Any]_ - Sequence of values.
- `n` _int_ - Number of values per chunk.

**Yields**:

- _Sequence[Any]_ - Chunk of values with length <= n.

**Raises**:

- `ValueError` - If `n` is 0 or negative.

<a id="wvutils.general.is_iterable"></a>

#### `is_iterable`

```python
def is_iterable(obj: Any) -> bool
```

Check if an object is iterable.

**Arguments**:

- `obj` _Any_ - Object to check.

**Returns**:

- _bool_ - Whether the object is iterable.

<a id="wvutils.general.rename_key"></a>

#### `rename_key`

```python
def rename_key(obj: dict,
               src_key: str,
               dest_key: str,
               in_place: bool = False) -> dict | None
```

Rename a dictionary key.

**Todo**:

  * Add support for nested keys.
  * Add support for renaming multiple keys at once.
  * Add support for non-string (built-in) key types.

  All of the following are True:

  ```python
  isinstance(True, bool)
  isinstance(True, int)
  1 == True
  1 in {1: "a"}
  True in {1: "a"}
  1 in {True: "a"}
  True in {True: "a"}
  1 in {1: "a", True: "b"}
  True in {1: "a", True: "b"}
  ```

**Arguments**:

- `obj` _dict_ - Reference to the dictionary to modify.
- `src` _str_ - Name of the key to rename.
- `dest` _str_ - Name of the key to change to.
- `in_place` _bool, optional_ - Perform in-place using the provided reference. Defaults to False.

**Returns**:

- _dict | None_ - Copy of the dictionary if in_place is False, otherwise None.

<a id="wvutils.general.unnest_key"></a>

#### `unnest_key`

```python
def unnest_key(obj: dict, *keys: str) -> Any | None
```

Fetch a value from a deeply nested dictionary.

**Arguments**:

- `obj` _dict_ - Dictionary to recursively iterate.
- `*keys` _str_ - Ordered keys to fetch.

**Returns**:

- _Any | None_ - The result of the provided keys, or None if any key is not found.

<a id="wvutils.general.sort_dict_by_key"></a>

#### `sort_dict_by_key`

```python
def sort_dict_by_key(obj: dict,
                     reverse: bool = False,
                     deep_copy: bool = False) -> dict | None
```

Sort a dictionary by key.

**Arguments**:

- `obj` _dict_ - Dictionary to sort.
- `reverse` _bool, optional_ - Sort in reverse order. Defaults to False.
- `deep_copy` _bool, optional_ - Return a deep copy of the dictionary. Defaults to False.

**Returns**:

- _dict | None_ - Dictionary sorted by key. If `in_place` is True, None is returned.

**Raises**:

- `ValueError` - If the dictionary keys are not of the same type.

<a id="wvutils.general.dedupe_list"></a>

#### `dedupe_list`

```python
def dedupe_list(values: list[Any], raise_on_dupe: bool = False) -> list[Any]
```

Remove duplicate values from a list.

**Example**:

```python
dedupe_list([1, 2, 3, 1, 2, 3])
# [1, 2, 3]
```

**Arguments**:

- `values` _list[Any]_ - List of values to dedupe.
- `raise_on_dupe` _bool, optional_ - Raise an error if a duplicate is found. Defaults to False.

**Returns**:

- _list[Any]_ - List of unique values.

**Raises**:

- `ValueError` - If a duplicate is found and `raise_on_dupe` is True.

<a id="wvutils.general.dupe_in_list"></a>

#### `dupe_in_list`

```python
def dupe_in_list(values: list[Any]) -> bool
```

Check if a list has duplicate values.

**Arguments**:

- `values` _list[Any]_ - List of values to check.

**Returns**:

- _bool_ - Whether the list has duplicate values.

<a id="wvutils.general.invert_dict_of_str"></a>

#### `invert_dict_of_str`

```python
def invert_dict_of_str(obj: dict[Any, str],
                       deep_copy: bool = False,
                       raise_on_dupe: bool = False) -> dict
```

Invert a dictionary of strings.

**Notes**:

  The value of the last key with a given value will be used.

**Example**:

```python
invert_dict_of_str({"a": "b", "c": "d"})
# {"b": "a", "d": "c"}
```

**Arguments**:

- `obj` _dict[Any, str]_ - Dictionary to invert.
- `deep_copy` _bool, optional_ - Return a deep copy of the dictionary. Defaults to False.
- `raise_on_dupe` _bool, optional_ - Raise an error if a duplicate is found. Defaults to False.

**Returns**:

- _dict_ - Inverted dictionary.

**Raises**:

- `ValueError` - If a duplicate is found and `raise_on_dupe` is True.

<a id="wvutils.general.get_all_subclasses"></a>

#### `get_all_subclasses`

```python
def get_all_subclasses(cls: type) -> list[type]
```

Get all subclasses of a class.

**Arguments**:

- `cls` _type_ - Class to get subclasses of.

**Returns**:

- _list[type]_ - List of subclasses.

<a id="wvutils.dt"></a>

# `wvutils.dt`

Datetime utilities.

This module contains functions and classes that are used to work with datetimes.

<a id="wvutils.dt.dtformats"></a>

## `dtformats` Objects

```python
class dtformats()
```

Datetime formats.

**Attributes**:

- `twitter` _str_ - Twitter datetime format.
- `reddit` _str_ - Reddit datetime format.
- `general` _str_ - General datetime format.
- `db` _str_ - Database datetime format.
- `date` _str_ - Date format.
- `time_12h` _str_ - 12-hour time format with timezone.
- `time_24h` _str_ - 24-hour time format with timezone.

<a id="wvutils.dt.num_days_in_month"></a>

#### `num_days_in_month`

```python
def num_days_in_month(year: int, month: int) -> int
```

Determine the number of days in a month.

**Arguments**:

- `year` _int_ - Year to check.
- `month` _int_ - Month to check.

**Returns**:

- _int_ - Number of days in the month.

<a id="wvutils.parquet"></a>

# `wvutils.parquet`

Parquet utilities.

This module provides utilities for working with Parquet files.

<a id="wvutils.parquet.get_parquet_session"></a>

#### `get_parquet_session`

```python
def get_parquet_session(use_s3: bool,
                        region_name: AWSRegion | None = None) -> fs.FileSystem
```

Get the globally shared Parquet filesystem session.

**Todo**:

  * Add support for other session parameters.

**Arguments**:

- `use_s3` _bool_ - Use S3 if True, otherwise uses local filesystem.
- `region_name` _AWSRegion | None, optional_ - AWS region name. Defaults to None.

  

**Returns**:

- _pyarrow.fs.FileSystem_ - The filesystem session.

<a id="wvutils.parquet.clear_parquet_sessions"></a>

#### `clear_parquet_sessions`

```python
def clear_parquet_sessions() -> int
```

Clear all globally shared Parquet filesystem sessions.

**Returns**:

- _int_ - Number of sessions cleared.

<a id="wvutils.parquet.create_pa_schema"></a>

#### `create_pa_schema`

```python
def create_pa_schema(schema_template: dict[str, str]) -> pa.schema
```

Create a parquet schema from a template.

**Example**:

```python
{
    "key_a": "string",
    "key_b": "integer",
    "key_c": "float",
    "key_d": "bool",
    "key_e": "timestamp[s]",
    "key_f": "timestamp[ms]",
    "key_g": "timestamp[ns]",
}
```

  becomes

```python
pa.schema([
    ("key_a", pa.string()),
    ("key_b", pa.int64()),
    ("key_c", pa.float64()),
    ("key_d", pa.bool_()),
    ("key_e", pa.timestamp("s",  tz=utc)),
    ("key_f", pa.timestamp("ms", tz=utc)),
    ("key_g", pa.timestamp("ns", tz=utc)),
])
```

**Arguments**:

- `schema_template` _Sequence[Sequence[str]]_ - Data names and parquet types for creating the schema.

**Returns**:

- _pa.schema_ - Final parquet schema.

**Raises**:

- `ValueError` - If an unknown type name is encountered.

<a id="wvutils.parquet.force_dataframe_dtypes"></a>

#### `force_dataframe_dtypes`

```python
def force_dataframe_dtypes(dataframe: pd.DataFrame,
                           template: dict[str, str]) -> pd.DataFrame
```

Force the data types of a dataframe using a template.

**Arguments**:

- `dataframe` _pd.DataFrame_ - Dataframe to force types.
- `template` _dict[str, str]_ - Template to use for forcing types.

**Returns**:

- _pd.DataFrame_ - Dataframe with forced types.

**Raises**:

- `ValueError` - If an unknown type name is encountered.

<a id="wvutils.parquet.export_dataset"></a>

#### `export_dataset`

```python
def export_dataset(data: list[dict] | deque[dict] | pd.DataFrame,
                   output_location: str | FilePath,
                   primary_template: dict[str, str],
                   partitions_template: dict[str, str],
                   *,
                   basename_template: str | None = None,
                   use_s3: bool = False,
                   region_name: AWSRegion | None = None,
                   use_threads: bool = False,
                   overwrite: bool = False) -> None
```

Write to dataset to local filesystem or AWS S3.

**Arguments**:

- `data` _list[dict] | deque[dict] | pd.DataFrame]_ - List, deque, or dataframe of objects to be written.
- `output_location` _str | FilePath_ - Location to write the dataset to.
- `primary_template` _dict[str, str]_ - Parquet schema template to use for the table (excluding partitions).
  partitions_template(dict[str, str]): Parquet schema template to use for the partitions.
- `basename_template` _str, optional_ - Filename template to use when writing to S3 or locally. Defaults to None.
- `use_s3` _bool, optional_ - Use S3 as the destination when exporting parquet files. Defaults to False.
- `region_name` _AWSRegion, optional_ - AWS region to use when exporting to S3. Defaults to None.
- `use_threads` _bool, optional_ - Use multiple threads when exporting. Defaults to False.
- `overwrite` _bool, optional_ - Overwrite existing files. Defaults to False.

<a id="wvutils.restruct"></a>

# `wvutils.restruct`

Utilities for restructuring data.

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

<a id="wvutils.restruct.json_dumps"></a>

#### `json_dumps`

```python
def json_dumps(obj: JSONSerializable) -> str
```

Encode an object as JSON.

**Arguments**:

- `obj` _JSONSerializable_ - Object to encode.

**Returns**:

- _str_ - Object encoded as JSON.

**Raises**:

- `JSONEncodeError` - If the object could not be encoded.

<a id="wvutils.restruct.jsonl_dumps"></a>

#### `jsonl_dumps`

```python
def jsonl_dumps(objs: Iterable[JSONSerializable]) -> str
```

Encode objects as JSONL.

**Arguments**:

- `objs` _Iterable[JSONSerializable]_ - Objects to encode.

**Returns**:

- _str_ - Objects encoded as JSONL.

**Raises**:

- `JSONEncodeError` - If the objects could not be encoded.

<a id="wvutils.restruct.json_dump"></a>

#### `json_dump`

```python
def json_dump(obj: JSONSerializable, file_path: str) -> None
```

Encode an object as JSON and write it to a file.

**Arguments**:

- `file_path` _str_ - Path of the file to open.

**Raises**:

- `JSONEncodeError` - If the object could not be encoded.

<a id="wvutils.restruct.jsonl_dump"></a>

#### `jsonl_dump`

```python
def jsonl_dump(objs: Iterable[JSONSerializable], file_path: str) -> None
```

Encode objects as JSONL and write them to a file.

**Arguments**:

- `objs` _Iterable[JSONSerializable]_ - Objects to encode.
- `file_path` _str_ - Path of the file to open.

**Raises**:

- `JSONEncodeError` - If the objects could not be encoded.

<a id="wvutils.restruct.json_loads"></a>

#### `json_loads`

```python
def json_loads(encoded_obj: str) -> JSONSerializable
```

Decode a JSON-encoded object.

**Arguments**:

- `encoded_obj` _str_ - Object to decode.

**Returns**:

- _JSONSerializable_ - Decoded object.

**Raises**:

- `JSONDecodeError` - If the object could not be decoded.

<a id="wvutils.restruct.json_load"></a>

#### `json_load`

```python
def json_load(file_path: FilePath) -> JSONSerializable
```

Decode a file containing a JSON-encoded object.

**Arguments**:

- `file_path` _FilePath_ - Path of the file to open.

**Returns**:

- _JSONSerializable_ - Decoded object.

**Raises**:

- `JSONDecodeError` - If the file could not be decoded.

<a id="wvutils.restruct.jsonl_loader"></a>

#### `jsonl_loader`

```python
def jsonl_loader(
    file_path: FilePath,
    *,
    allow_empty_lines: bool = False
) -> Generator[JSONSerializable, None, None]
```

Decode a file containing JSON-encoded objects, one per line.

**Arguments**:

- `file_path` _FilePath_ - Path of the file to open.
- `allow_empty_lines` _bool, optional_ - Whether to allow (skip) empty lines. Defaults to False.

**Yields**:

- _JSONSerializable_ - Decoded object.

**Raises**:

- `JSONDecodeError` - If the line could not be decoded, or if an empty line was found and `allow_empty_lines` is False.

<a id="wvutils.restruct.squeegee_loader"></a>

#### `squeegee_loader`

```python
def squeegee_loader(
        file_path: FilePath) -> Generator[JSONSerializable, None, None]
```

Automatically decode a file containing JSON-encoded objects.

Supports multiple formats (JSON, JSONL, JSONL of JSONL, etc).

**Todo**:

  * Add support for pretty-printed JSON that has been appended to a file.

  

**Arguments**:

- `file_path` _FilePath_ - Path of the file to open.

**Yields**:

- _JSONSerializable_ - Decoded object.

**Raises**:

- `JSONDecodeError` - If the line could not be decoded.

<a id="wvutils.restruct.gen_hash"></a>

#### `gen_hash`

```python
def gen_hash(obj: MD5Hashable) -> str
```

Create an MD5 hash from a hashable object.

Note: Tuples and deques are not hashable, so they are converted to lists.

**Arguments**:

- `obj` _MD5Hashable_ - Object to hash.

**Returns**:

- _str_ - MD5 hash of the object.

**Raises**:

- `HashEncodeError` - If the object could not be encoded.

<a id="wvutils.restruct.pickle_dump"></a>

#### `pickle_dump`

```python
def pickle_dump(obj: PickleSerializable, file_path: FilePath) -> None
```

Serialize an object as a pickle and write it to a file.

**Arguments**:

- `obj` _JSONSerializable_ - Object to serialize.
- `file_path` _FilePath_ - Path of the file to write.

**Raises**:

- `PickleEncodeError` - If the object could not be encoded.

<a id="wvutils.restruct.pickle_dumps"></a>

#### `pickle_dumps`

```python
def pickle_dumps(obj: PickleSerializable) -> bytes
```

Serialize an object as a pickle.

**Arguments**:

- `obj` _PickleSerializable_ - Object to serialize.

**Returns**:

- _bytes_ - Serialized object.

**Raises**:

- `PickleEncodeError` - If the object could not be encoded.

<a id="wvutils.restruct.pickle_load"></a>

#### `pickle_load`

```python
def pickle_load(file_path: FilePath) -> PickleSerializable
```

Deserialize a pickle-serialized object from a file.

Note: Not safe for large files.

**Arguments**:

- `file_path` _FilePath_ - Path of the file to open.

**Returns**:

- _PickleSerializable_ - Deserialized object.

**Raises**:

- `PickleDecodeError` - If the object could not be decoded.

<a id="wvutils.restruct.pickle_loads"></a>

#### `pickle_loads`

```python
def pickle_loads(serialized_obj: bytes) -> PickleSerializable
```

Deserialize a pickle-serialized object.

**Arguments**:

- `serialized_obj` _bytes_ - Object to deserialize.

**Returns**:

- _PickleSerializable_ - Deserialized object.

**Raises**:

- `PickleDecodeError` - If the object could not be decoded.


---

