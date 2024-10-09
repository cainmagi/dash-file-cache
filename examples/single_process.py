# -*- coding: UTF-8 -*-
"""
Single process
==============
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
The demo for preparing and serving the data dynamically in the same process.
"""

import os
import io

from typing import Optional

import dash
from dash import html
from dash import Output, Input

if __name__ == "__main__":
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dash_file_cache import CachePlain
from dash_file_cache import ServiceData


app = dash.Dash("test-single-process")


class Demo:
    def __init__(self) -> None:
        self.service = ServiceData(CachePlain(cache_size=1))
        self.root = os.path.dirname(__file__)

    def layout(self) -> html.Div:
        return html.Div(
            (
                html.Div(
                    (
                        html.P("Get Image by:"),
                        html.Button(id="btn-strio", children="StringIO"),
                        html.Button(id="btn-bytesio", children="BytesIO"),
                        html.Button(id="btn-path", children="Path"),
                    )
                ),
                html.Div((html.P("Cache type:"), html.P(id="type"))),
                html.Div((html.P("Cache address:"), html.P(id="addr"))),
                html.Div((html.P("Cached Image:"), html.Img(id="cache"))),
            ),
        )

    def bind(self, app: dash.Dash):
        @app.callback(
            Output("type", "children"),
            Output("addr", "children"),
            Input("btn-strio", "n_clicks"),
            Input("btn-bytesio", "n_clicks"),
            Input("btn-path", "n_clicks"),
            prevent_initial_call=True,
        )
        def click_get_image(
            n_clicks_strio: Optional[int],
            n_clicks_bytesio: Optional[int],
            n_clicks_path: Optional[int],
        ):
            prop_id = str(dash.callback_context.triggered[0]["prop_id"])
            file_path = os.path.join(self.root, "test_image.svg")
            if prop_id.startswith("btn-strio") and n_clicks_strio:
                with open(file_path, "r") as fobj:
                    fio = io.StringIO(fobj.read())
            elif prop_id.startswith("btn-bytesio") and n_clicks_bytesio:
                with open(file_path, "rb") as fobj:
                    fio = io.BytesIO(fobj.read())
            elif prop_id.startswith("btn-path") and n_clicks_path:
                fio = file_path
            else:
                return dash.no_update, dash.no_update
            addr = self.service.register(
                fio,
                content_type="image/svg+xml",
                mime_type="image/svg+xml",
                one_time_service=True,
            )
            return str(fio.__class__.__name__), addr

        @app.callback(
            Output("cache", "src"),
            Input("addr", "children"),
            prevent_initial_call=True,
        )
        def update_cache(addr):
            if not addr:
                return dash.no_update
            return addr


demo = Demo()

app.layout = demo.layout()
demo.bind(app)
demo.service.serve(app)


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

    app.run(host=get_ip(), port="8080", debug=False)
