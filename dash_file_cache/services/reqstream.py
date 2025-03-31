"""
Deferred request streamer
=========================
@ Dash File Cache: services

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Deferred data stream forwarding mechanism used for implementing the proxy-based
data access.
"""

import contextlib
import types

from typing import Optional, Any, TypeVar

try:
    from typing import Iterator, Mapping
    from typing import Type
except ImportError:
    from collections.abc import Iterator, Mapping
    from builtins import type as Type

from typing_extensions import Protocol

import urllib3
import urllib3.util

from ..caches.typehints import CachedFileInfo, CachedRequest


_BaseException = TypeVar("_BaseException", bound=BaseException)
__all__ = ("ProtocolResponse", "DeferredRequestStream")


class ProtocolResponse(Protocol):
    """The protocol of an HTTP response. This protocol is defined for the
    compatibility of different `urllib3` versions."""

    def close(self) -> None: ...

    def release_conn(self) -> None: ...

    def read(self, amt: Optional[int] = None) -> Any: ...

    @property
    def headers(self) -> Mapping[Any, Any]: ...


class DeferredRequestStream(contextlib.AbstractContextManager):
    """Deferred data stream forwarded from the response of a pre-configured request.

    By entering the context of this class, a connection to the remote resource will
    be established. Within this context, a data stream can be read and forwarded.
    """

    __slots__ = ("info", "data", "__pool", "__request")

    def __init__(self, info: CachedFileInfo, data: CachedRequest) -> None:
        """Initialization.

        Arguments
        ---------
        info: `CachedFileInfo`
        data: `CachedRequest`
            The information and the request configuration loaded from the cache.
        """
        self.info: CachedFileInfo = info
        self.data: CachedRequest = data

        urllib3.HTTPResponse().headers

        self.__pool: Optional[urllib3.PoolManager] = None
        self.__request: Optional[ProtocolResponse] = None

    def close(self) -> None:
        """Close all connections if they exist."""
        if self.__request is not None:
            _rel_con = getattr(self.__request, "release_conn", None)
            if _rel_con is not None:
                _rel_con()
            _close = getattr(self.__request, "close", None)
            if _close is not None:
                _close()
            self.__request = None
        if self.__pool is not None:
            self.__pool.clear()
            self.__pool = None

    def __enter__(self) -> ProtocolResponse:
        """Create the connection, and enter the context."""
        self.close()
        # Create the pool.
        if self.__pool is not None:
            pool = self.__pool
        else:
            pool = urllib3.PoolManager(
                retries=urllib3.util.Retry(connect=5, read=2, redirect=5),
                timeout=urllib3.util.Timeout(connect=5.0),
            )
            self.__pool = pool
        # Create the response.
        headers = self.data["headers"]
        req = pool.request(
            url=self.data["url"],
            headers=headers if headers else None,
            method="get",
            preload_content=False,
        )
        self.__request = req
        return req

    def __exit__(
        self,
        exc_type: Optional[Type[_BaseException]],
        exc_value: Optional[_BaseException],
        exc_traceback: Optional[types.TracebackType],
    ) -> None:
        self.close()

    def __update_info(self, headers: Mapping[Any, Any]) -> None:
        """Given a collection of headers of the service response. Use the information
        to update the file information of the cached data."""
        if "Content-Length" in headers:
            self.info["data_size"] = int(headers["Content-Length"])
        _file_name = headers.get("Content-Disposition")
        _file_name_fallback = self.data["file_name_fallback"]
        if isinstance(_file_name, str) and ("filename=" in _file_name):
            self.info["file_name"] = _file_name.rsplit("filename=", maxsplit=1)[-1]
        elif _file_name_fallback:
            self.info["file_name"] = _file_name_fallback
        if "Content-Type" in headers:
            _content_type = str(headers["Content-Type"]).strip()
            _mimetype = _content_type.split(";", maxsplit=1)[0].strip()
            self.info["content_type"] = _content_type
            self.info["mime_type"] = _mimetype

    def provide(self, chunk_size: int = 1024 * 1024) -> Iterator[bytes]:
        """Create the data provider of this deferred request stream.

        Note that this method is designed for being used outside the context. When
        using this method, it will maintain the context within this stream provider.
        In other words, the context will be exited when this method get finalized.

        Arguments
        ---------
        chunk_size: `int`
            The chunk size used for forwarding the data.

        Returns
        -------
        #1: `Iterator[bytes]`
            A stream created by this method.
        """
        fobj = self.__enter__()
        self.__update_info(fobj.headers)

        def provider() -> Iterator[bytes]:
            with contextlib.closing(self):
                data = fobj.read(chunk_size)
                while data:
                    yield data
                    data = fobj.read(chunk_size)

        return provider()
