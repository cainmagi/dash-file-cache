# -*- coding: UTF-8 -*-
"""
Download file
=============
@ Dash File Cache - demo

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The demo for downloading a file served by the cache.
"""

import os
import time

from typing import Optional

try:
    from typing import Callable
    from typing import Tuple
except ImportError:
    from collections.abc import Callable
    from builtins import tuple as Tuple

import dash
from dash import html
from dash import Output, Input

import diskcache

if __name__ == "__main__":
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dash_file_cache import CacheFile
from dash_file_cache import Downloader, DownloaderStatus
from dash_file_cache import ServiceData, ServiceDownloader


app = dash.Dash("test-tempfile-cache")
cache = diskcache.Cache("./cache")
background_callback_manager = dash.DiskcacheManager(cache)


class Demo:
    def __init__(self) -> None:
        self.service = ServiceData(CacheFile(None))
        self.root = os.path.dirname(__file__)

    def layout(self) -> html.Div:
        return html.Div(
            (
                html.Div(
                    html.P(
                        (
                            html.Span(
                                "Download a image:", style={"paddingRight": "0.5rem"}
                            ),
                            html.Button(id="btn", children="Start"),
                        )
                    )
                ),
                html.Div((html.P(("Progress:", html.Span(id="prog"))))),
                html.Div((html.P("Cache type:"), html.P(id="type"))),
                html.Div((html.P("Cache address:"), html.P(id="addr"))),
                html.Div((html.P("Downloader status:"), html.P(id="dlstats"))),
                Downloader(id="download", mitm="/dfc-downloader"),
            ),
        )

    def bind(self, app: dash.Dash):
        @app.callback(
            Output("type", "children"),
            Output("addr", "children"),
            Input("btn", "n_clicks"),
            background=True,
            running=[
                (Output("btn", "disabled"), True, False),
            ],
            progress=[Output("prog", "children")],
            manager=background_callback_manager,
            prevent_initial_call=True,
        )
        def click_get_image(
            set_progress: Callable[[Tuple[str]], None], n_clicks: Optional[int]
        ):
            if not n_clicks:
                return dash.no_update, dash.no_update
            file_path = os.path.join(self.root, "test_image.svg")
            n = 10
            for i in range(n):
                time.sleep(0.1)

                set_progress(("{0}%".format(int(round((i + 1) / n * 100))),))
            addr = self.service.register(
                file_path,
                content_type="image/svg+xml; charset=utf-8",
                mime_type="image/svg+xml",
                one_time_service=True,
                download=True,
            )
            return str(file_path.__class__.__name__), addr

        @app.callback(
            Output("download", "url"),
            Input("addr", "children"),
            prevent_initial_call=True,
        )
        def trigger_downloading_event(addr):
            if not addr:
                return dash.no_update
            return addr

        @app.callback(
            Output("dlstats", "children"),
            Input("download", "status"),
            prevent_initial_call=True,
        )
        def trigger_downloading_status(status: Optional[DownloaderStatus]):
            if not status:
                return ""
            return str(status)


class WrappedApp:
    """A wrapped app. This wrapped app is accessed by the tests."""

    def __init__(self, app: dash.Dash) -> None:
        self.app = app

    def load(self) -> None:
        demo = Demo()
        app.layout = demo.layout()
        demo.bind(app)
        demo.service.serve(app)
        ServiceDownloader("/dfc-downloader").serve(app)


wrapped_app = WrappedApp(app)


if __name__ == "__main__":
    import socket

    def get_ip(method: str = "broadcast") -> str:
        """Detect the IP address of this device."""
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            if method == "broadcast":
                s_socket.connect(("10.255.255.255", 1))
                ip_value = s_socket.getsockname()[0]
            elif method == "udp":
                s_socket.connect(("8.8.8.8", 1))
                ip_value = s_socket.getsockname()[0]
            elif method == "host":
                ip_value = socket.gethostbyname(socket.gethostname())
            else:
                raise ConnectionError
        except Exception:  # pylint: disable=broad-except
            ip_value = "localhost"
        finally:
            s_socket.close()
        return ip_value

    wrapped_app.load()
    wrapped_app.app.run(host=get_ip(), port="8080", debug=False)
