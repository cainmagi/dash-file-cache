# -*- coding: UTF-8 -*-
"""
Change image
============
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
The demo for serving multiple dynamically loaded images.
"""

import os

from typing import Optional

import dash
from dash import html
from dash import Output, Input

if __name__ == "__main__":
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dash_file_cache import CachePlain
from dash_file_cache import ServiceData


app = dash.Dash("demo-change-image")


class Demo:
    def __init__(self) -> None:
        self.service = ServiceData(CachePlain(cache_size=1))
        self.root = os.path.dirname(__file__)

    def layout(self) -> html.Div:
        return html.Div(
            (
                html.Div(
                    html.P(
                        (
                            html.Span("Get Image:", style={"paddingRight": "0.5rem"}),
                            html.Button(id="btn-img1", children="Image 1"),
                            html.Button(id="btn-img2", children="Image 2"),
                        )
                    )
                ),
                html.Div((html.P("Cache address:"), html.P(id="addr"))),
                html.Div((html.P("Cached Image:"), html.Img(id="cache"))),
            ),
        )

    def bind(self, app: dash.Dash):
        @app.callback(
            Output("addr", "children"),
            Input("btn-img1", "n_clicks"),
            Input("btn-img2", "n_clicks"),
            prevent_initial_call=False,
        )
        def click_get_image(
            n_clicks_img1: Optional[int],
            n_clicks_img2: Optional[int],
        ):
            prop_id = str(dash.callback_context.triggered[0]["prop_id"])
            if prop_id.startswith("btn-img1") and n_clicks_img1:
                file_path = os.path.join(self.root, "test_image.svg")
            elif prop_id.startswith("btn-img2") and n_clicks_img2:
                file_path = os.path.join(self.root, "test_philips_PM5544.svg")
            else:
                file_path = os.path.join(self.root, "test_image.svg")
            addr = self.service.register(
                file_path,
                content_type="image/svg+xml",
                mime_type="image/svg+xml",
                one_time_service=True,
            )
            return addr

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
