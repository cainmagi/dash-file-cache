"""
Data
=====
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
Service(s) related to the data exchanges.
"""

import os
import io
import uuid

from typing import Union, Optional, IO, AnyStr, Any

try:
    from typing import Iterator, Callable
except ImportError:
    from collections.abc import Iterator, Callable

from typing_extensions import ClassVar, Literal

import dash
import flask
import flask.views

from ..caches.typehints import (
    CachedFileInfo,
    CachedData,
    CachedPath,
    CachedStringIO,
    CachedBytesIO,
)
from ..caches.abstract import CacheAbstract
from ..caches.memory import CacheQueue
from .utilities import no_cache, get_server
from ..utilities import StreamFinalizer


__all__ = ("ServiceData",)


class ServiceData:
    """Service provider for streaming data.

    This instance provides a cache for storing temporary data. A temporary data item
    will be accessed by the directly or downloaded.
    """

    def __init__(
        self,
        cache: CacheAbstract[CachedFileInfo, CachedData],
        service_name: str = "/cached-data",
        chunk_size: int = 1,
    ) -> None:
        """Initialization.

        Arguments
        ---------
        cache: `Cache[CachedFileInfo, CachedData]`
            The cache instance hosting the temporary data.

        service_name: `str`
            The name of this service.

        chunk_size: `int`
            The chunk size when streaming the cached file to users. The unit is `MB`.
        """
        if chunk_size < 1:
            raise ValueError('services: The argument "chunk_size" needs to be >=1.')
        if not isinstance(cache, CacheAbstract):
            raise TypeError(
                'services: The argument "cache" needs to be a cache object.'
            )
        self.__cache = cache
        self.__addr: str = service_name.strip()
        self.__chunk_size: int = chunk_size * 1024 * 1024

    @property
    def cache(self) -> CacheAbstract[CachedFileInfo, CachedData]:
        """Property: The cache of this service."""
        return self.__cache

    @property
    def chunk_size(self) -> int:
        """The chunk size when streaming the cached file to users. The unit is `MB`."""
        return int(round(self.__chunk_size / (1024 * 1024)))

    @chunk_size.setter
    def chunk_size(self, val: int) -> None:
        """The chunk size when streaming the cached file to users. The unit is `MB`."""
        self.__chunk_size = int(val) * 1024 * 1024

    def register(
        self,
        fobj: Union[str, os.PathLike, io.StringIO, io.BytesIO],
        file_name: str = "",
        content_type: str = "",
        mime_type: str = "image/jpeg",
        one_time_service: bool = False,
        download: bool = False,
    ) -> str:
        """Register the a new file (a path or a file-like object) to the cache.

        Arguments
        ---------
        fobj: `str | os.PathLike | io.StringIO | io.BytesIO`
            The path or a file-io object of a specific file to be registered.

        file_name: `str`
            The file name of `fobj`. If not provided, will attempt to
            1. solve the name from `fobj` if it is a path.
            2. randomly generate a dummy file name.
            Note that this value is used only when the file will be streamed as a
            downloadable file.

        content_type: `str`
            The content-type in the response. An optional encoding can be provided
            here. If this value is not specified, will use `mime_type` to fill this
            value.

        mime_type: `str`
            The mime-type of the response. Typically, it is only determined by the type
            of the file.

        one_time_service: `bool`
            A flag. When it is enabled, will use the on-exit mechanism to remove this
            cached data once it is served for once.

            This option is recommended if this cached item is used for one-time
            downloading.

        download: `bool`
            If specified, will mark the returned address as a downloadable link.

        Returns
        -------
        #1: `str`
            The URL that would be used for accessing this temporarily cached file.
        """

        def get_file_info(
            type: Literal["path", "str", "bytes"], data_size: int, file_name: str
        ) -> CachedFileInfo:
            return CachedFileInfo(
                type=type,
                data_size=data_size,
                file_name=file_name,
                content_type=content_type if content_type else mime_type,
                mime_type=mime_type,
                one_time_service=one_time_service,
            )

        uid = uuid.uuid4().hex

        if isinstance(fobj, (str, os.PathLike)):
            with open(fobj, "rb") as _fobj:
                _fobj.seek(0, io.SEEK_END)
                file_size = _fobj.tell()
            file_name = file_name if file_name else os.path.split(str(fobj))[-1]
            file_name = file_name if file_name else uid
            info = get_file_info("path", file_size, file_name)
            data = CachedPath(type="path", path=fobj)
        elif isinstance(fobj, io.StringIO):
            fobj.seek(0, io.SEEK_END)
            file_size = fobj.tell()
            fobj.seek(0, io.SEEK_SET)
            file_name = file_name if file_name else uid
            info = get_file_info("str", file_size, file_name)
            data = CachedStringIO(type="str", data=fobj)
        elif isinstance(fobj, io.BytesIO):
            fobj.seek(0, io.SEEK_END)
            file_size = fobj.tell()
            fobj.seek(0, io.SEEK_SET)
            file_name = file_name if file_name else uid
            info = get_file_info("bytes", file_size, file_name)
            data = CachedBytesIO(type="bytes", data=fobj)
        else:
            raise TypeError(
                'service: Cannot recognize the type of the argument "fobj": {0}'.format(
                    fobj.__class__.__name__
                )
            )

        if isinstance(self.__cache, CacheQueue):
            cache = self.__cache.mirror
        else:
            cache = self.__cache
        cache.dump(key=uid, info=info, data=data)
        return "{0}?uid={1}{2}".format(
            self.__addr, uid, "&download=true" if download else ""
        )

    @staticmethod
    def _stream_data_to_loader(data: Callable[[], CachedData]) -> Callable[[], IO[Any]]:
        """Private method of `stream()`

        A post-processor for ensuring that the loaded data is interpreted as a
        file-like object."""

        def loader() -> IO[Any]:
            _data = data()
            if _data["type"] == "path":
                fobj = open(_data["path"], "rb")
            else:
                fobj = _data["data"]
            fobj.seek(0, io.SEEK_SET)
            return fobj

        return loader

    @staticmethod
    def _stream_get_at_closed(
        cache: CacheAbstract[CachedFileInfo, CachedData], uid: str
    ) -> Callable[[IO[Any]], None]:
        """Private method of `stream()`

        Get the `at_closed()` method used by `stream()`."""

        def at_closed(_ctx_fobj: IO[Any]) -> None:
            """Remove the cache data when the file is not used any more."""
            if isinstance(_ctx_fobj, (io.StringIO, io.BytesIO)):
                _ctx_fobj.truncate(0)
            if isinstance(_ctx_fobj, (io.BufferedIOBase, io.TextIOBase, io.RawIOBase)):
                _ctx_fobj.close()
            cache.remove(uid)

        return at_closed

    def stream(self, uid: str, download: bool = False) -> flask.Response:
        """Wrap a cached data item with streaming data provider.

        Arguments
        ---------
        uid: `str`
            The UUID used for accessing the cached item. If not hit, raise
            `FileNotFoundError`.

        download: `bool`
            A flag. If enabled, will mark the streamed data as the data to be
            downloaded.

        Returns
        -------
        #1: `Response`
            The flask Response used for forwarding the data to the frontend.
        """
        if uid not in self.__cache:
            raise FileNotFoundError(
                "services: The requested file {0} has expired.".format(uid)
            )

        info, deferred = self.__cache.load(uid)

        if info["data_size"] <= 0:
            raise FileNotFoundError(
                "services: The requested file {0} is empty.".format(uid)
            )

        file_type = info["type"]
        if file_type not in ("path", "str", "bytes"):
            raise TypeError(
                "service: Cannot recognize the type of fobj: " "{0}".format(file_type)
            )

        one_time_service = info["one_time_service"]
        at_closed = self._stream_get_at_closed(cache=self.cache, uid=uid)

        def provider(_deferred: Callable[[], IO[AnyStr]]) -> Iterator[AnyStr]:
            """Streaming data provider."""

            with StreamFinalizer(
                _deferred(), callback_on_exit=at_closed if one_time_service else None
            ) as _fobj:
                data = _fobj.read(self.__chunk_size)
                while data:
                    yield data
                    data = _fobj.read(self.__chunk_size)

        resp = flask.Response(
            flask.stream_with_context(provider(self._stream_data_to_loader(deferred))),
            content_type=(
                "application/octet-stream" if download else info["content_type"]
            ),
            mimetype=info["mime_type"],
        )
        resp.headers["Content-Length"] = str(info["data_size"])
        if download:
            file_name = info["file_name"]
            file_name = file_name if isinstance(file_name, str) and file_name else uid
            resp.headers["Content-Disposition"] = "attachment; filename={0}".format(
                file_name
            )

        return resp

    def serve(
        self, app: Union[dash.Dash, flask.Flask], endpoint: Optional[str] = None
    ) -> None:
        """Serve the page to the flask app."""

        server = get_server(app)

        rself = self

        class ViewCachedData(flask.views.MethodView):
            """Service for the raw HTML page"""

            init_every_request: ClassVar[bool] = False

            @no_cache
            def get(self) -> flask.Response:
                req = flask.request
                uid = req.args.get("uid", type=str, default="")
                download = req.args.get("download", type=bool, default=False)
                if (not isinstance(uid, str)) or (not uid):
                    raise TypeError("services: The required raw page UID is unknown.")

                return rself.stream(uid, download=download)

        endpoint = (
            endpoint.strip() if (isinstance(endpoint, str) and endpoint) else None
        )
        endpoint = endpoint if endpoint else self.__addr.strip("/\\ ")
        endpoint = endpoint.replace("/", ".").replace("\\", ".")
        server.add_url_rule(
            rule=rself.__addr,
            endpoint=endpoint,
            view_func=ViewCachedData.as_view("View.{0}".format(endpoint)),
        )
