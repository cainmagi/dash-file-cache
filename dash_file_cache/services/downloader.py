"""
Services used by Downloader
===========================
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
Service(s) related to the downloader.
"""

import os

from typing import Union, Optional, TypeVar

from typing_extensions import ClassVar

import dash
import flask
import flask.views
from werkzeug.wrappers.response import Response as WzResponse

from .utilities import get_server


__all__ = ("ServiceDownloader",)
_Response = TypeVar("_Response", bound=(Union[flask.Response, WzResponse]))


class ServiceDownloader:
    """Service provider for optional features of the downloader.

    This instance provides some optional features required by the implementation
    of the downloader. The services of this instance do not handle any downloadable
    data.
    """

    def __init__(
        self,
        service_name: str = "/dfc-downloader",
        allowed_cross_origin: Optional[str] = None,
    ) -> None:
        """Initialization.

        Arguments
        ---------
        service_name: `str`
            The name of this service.

        allowed_cross_origin: `str | None`
            The allowed cross origin when serving the files. The usage should be the
            same as `"Access-Control-Allow-Origin"`. If this value is empty or `None`,
            the cross-origin will not be configured.
        """
        self.__addr: str = service_name.strip()
        self.__allowed_cross_origin: str = (
            allowed_cross_origin.strip()
            if isinstance(allowed_cross_origin, str)
            else ""
        )
        self.path_local = os.path.dirname(__file__)

    @property
    def allowed_cross_origin(self) -> str:
        """Property: The allowed cross origin. If this value is an empty string, the
        cross-origin data delivery will not be used."""
        return self.__allowed_cross_origin

    def _stream_add_headers(self, resp: _Response) -> _Response:
        """Private method of `stream()`

        Add customized headers to the data service response."""
        if self.__allowed_cross_origin:
            resp.headers["Access-Control-Allow-Origin"] = self.__allowed_cross_origin
            resp.headers["Access-Control-Allow-Credentials"] = "true"
        return resp

    def serve(
        self, app: Union[dash.Dash, flask.Flask], endpoint: Optional[str] = None
    ) -> None:
        """Serve the page to the flask app."""

        server = get_server(app)

        rself = self

        endpoint = (
            endpoint.strip() if (isinstance(endpoint, str) and endpoint) else None
        )
        endpoint = endpoint if endpoint else self.__addr.strip("/\\ ")
        endpoint = endpoint.replace("/", ".").replace("\\", ".")

        class ViewDownloaderMITM(flask.views.MethodView):
            """Service script pages used by the downloader."""

            init_every_request: ClassVar[bool] = False
            path_mitm: ClassVar[str] = os.path.join(rself.path_local, "dfc_mitm.html")

            def get(self):
                if os.path.isfile(self.path_mitm):
                    with open(self.path_mitm, "r", encoding="utf-8") as fobj:
                        resp = flask.make_response(fobj.read())
                        resp.headers["Content-Type"] = "text/html"
                else:
                    resp = flask.redirect(
                        "https://jimmywarting.github.io/StreamSaver.js/"
                        "mitm.html?version=2.0.0"
                    )
                resp = rself._stream_add_headers(resp)

                return resp

        server.add_url_rule(
            rule=rself.__addr + "/mitm",
            endpoint=endpoint + ".mitm",
            view_func=ViewDownloaderMITM.as_view("View.{0}.mitm".format(endpoint)),
        )

        class ViewDownloaderSWJs(flask.views.MethodView):
            """Service script pages used by the downloader."""

            init_every_request: ClassVar[bool] = False
            path_sw: ClassVar[str] = os.path.join(rself.path_local, "dfc_sw.js")

            def get(self):
                if os.path.isfile(self.path_sw):
                    with open(self.path_sw, "r", encoding="utf-8") as fobj:
                        resp = flask.make_response(fobj.read())
                        resp.headers["Content-Type"] = "application/javascript"
                else:
                    resp = flask.redirect(
                        "https://jimmywarting.github.io/StreamSaver.js/sw.js"
                    )
                resp = rself._stream_add_headers(resp)

                return resp

        server.add_url_rule(
            rule=rself.__addr + "/sw.js",
            endpoint=endpoint + ".sw",
            view_func=ViewDownloaderSWJs.as_view("View.{0}.sw".format(endpoint)),
        )
