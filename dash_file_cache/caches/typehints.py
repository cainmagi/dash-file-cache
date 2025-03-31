"""
Typehints
=========
@ Dash File Cache: caches

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Extra typehints used by the definition of caches.
"""

import os

from typing import Union, Optional, IO, TypeVar

try:
    from typing import Callable
    from typing import Dict
except ImportError:
    from collections.abc import Callable
    from builtins import dict as Dict

from typing_extensions import Literal, TypedDict


T = TypeVar("T")

Deferred = Callable[[], T]
"""A deferred value. This value is lazy-loaded by a function. Only when this function
gets called, the value will be produced."""


__all__ = (
    "Deferred",
    "CachedFileInfo",
    "CachedPath",
    "CachedStringIO",
    "CachedBytesIO",
    "CachedData",
)


class CachedFileInfo(TypedDict):
    """The metadata of the cached file."""

    type: Literal["path", "str", "bytes", "request"]
    """The type os this cached data."""

    data_size: int
    """The length of the cached data, representing the number of bytes or characters.
    This value is acquired by preloading the file."""

    file_name: str
    """The file name. This value needs to be used when the data is prepared for
    streaming."""

    content_type: str
    """The content-type in the response. An optional encoding can be provided here.
    For an HTML page, this value should be `"text/html; charset=utf-8"`."""

    mime_type: str
    """The mime-type of the response. Typically, it is only determined by the type
    of the file. For an HTML page, this value should be `"text/html"`."""

    one_time_service: bool
    """A flag. When it is enabled, will use the on-exit mechanism to remove this cached
    data once it is served for once.

    This option is recommended if this cached item is used for one-time downloading.
    """


class CachedPath(TypedDict):
    """The string path or the path-like object specifying a file existing on the disk.

    In this case, the `CachedPath` will only store the path. The file will be always
    read and streamed as binary file stream.
    """

    type: Literal["path"]
    """The type os this cached data."""

    path: Union[str, os.PathLike]
    """The path to the file on the local disk."""


class CachedRequest(TypedDict):
    """The URL and request configuration specifying a remote file. This configuration
    is mainly used when a cross-domain URL needs to be accessed or an authentication
    protected file is to be read.

    In this case, the `CachedRequest` will only store the URL and the request
    configurations. The request stream will be established and forwarded to the
    users when this cached data item is to be streamed.
    """

    type: Literal["request"]
    """The type os this cached data."""

    url: str
    """The URL referring to the remote file."""

    headers: Dict[str, str]
    """A collection of headers to be used when accessing the remote file."""

    file_name_fallback: Optional[str]
    """A fall-back file name. It is used when the response of the request does not
    provide a file name. If this valus is not specified, will use the URL to guess
    the file name."""


class CachedStringIO(TypedDict):
    """The data of one cached `StringIO` data."""

    type: Literal["str"]
    """The type os this cached data."""

    data: IO[str]
    """The text data to be cached, the type of the file can be determined by the
    file name and the `mime_type`."""


class CachedBytesIO(TypedDict):
    """The data of one cached `BytesIO` data."""

    type: Literal["bytes"]
    """The type os this cached data."""

    data: IO[bytes]
    """The binary data to be cached, the type of the file can be determined by the
    file name and the `mime_type`."""


CachedData = Union[CachedPath, CachedRequest, CachedStringIO, CachedBytesIO]
"""The typehint of the cached data."""
