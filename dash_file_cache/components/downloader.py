# -*- coding: UTF-8 -*-
"""
Downloader
==========
@ Dash File Cache: components

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The downloader component implemented by Python.
"""

from typing import Optional

try:
    from typing import Callable
except ImportError:
    from collections.abc import Callable

from typing_extensions import ClassVar

import dash
from dash import html
from dash import Input, Output, State


__all__ = ("Downloader",)


class Downloader:
    """Purely Python-Dash implemented downloader component.

    This component is purely implemented by python codes. The usage is like this:
    ``` python
    app = dash.Dash(...)

    downloader = Downloader(id="downloader")

    app.layout = html.Div(
        (
            html.Button(id="btn")
            downloader.layout()
        )
    )

    downloader.use_callbacks(app)

    @app.callback(
        downloader.as_output,
        Input("btn", "n_clicks")
    )
    def trigger_get_file(n_clicks: Optional[int]):
        if not n_clicks:
            return dash.no_update
        return "/file.txt"
    ```
    """

    callback_js: ClassVar[str] = (
        """
        function (uri) {
            var link = document.createElement("a");
            link.setAttribute("download", "");
            link.setAttribute("target", "_blank");
            link.setAttribute("rel", "no-refresh");
            link.href = uri;
            document.body.appendChild(link);
            link.click();
            link.remove();
            return "success";
        }
        """
    )

    def __init__(self, id: str, to_addr: Optional[Callable[[str], str]] = None) -> None:
        """Initialization.

        Initialize the basic property of this component.

        Arguments
        ---------
        id: `str`
            The basic id of this component.

        to_addr: `((str) -> str) | None`
            An optional pre-processing function which converts the trigger from the
            callback to the address used for downloading the file.

            If not provided, will use the trigger value directly (equivalent to
            `lambda x: x`).

            If returning an empty string, the downloading event will be prevented.
        """
        self.__id: str = id
        self.__to_addr: Optional[Callable[[str], str]] = (
            to_addr if callable(to_addr) else None
        )

    @property
    def as_input(self) -> Input:
        """Property: Provide the trigger as the callback input. This input should be
        triggered when the address of the downloadable file is prepared."""
        return Input("{0}-trigger".format(self.__id), "children")

    @property
    def as_output(self) -> Output:
        """Property: Provide the trigger as the callback output."""
        return Output("{0}-trigger".format(self.__id), "children")

    @property
    def as_state(self) -> State:
        """Property: Provide the trigger as the callback state. This input should be
        triggered when the address of the downloadable file is prepared."""
        return State("{0}-trigger".format(self.__id), "children")

    def layout(self) -> html.Div:
        """Get the layout of this component."""
        return html.Div(
            hidden=True,
            children=(
                html.Div(id="{0}-js-finish-trigger".format(self.__id), hidden=True),
                html.Div(id="{0}-js-trigger".format(self.__id), hidden=True),
                html.Div(id="{0}-trigger".format(self.__id), hidden=True),
            ),
        )

    def use_callbacks(self, app: dash.Dash) -> None:
        """Use callbacks.

        Bind the automatically generated callbacks used by this components to the given
        `app`.

        Arguments
        ---------
        app: `Dash`
            The dash application.
        """
        if not isinstance(app, dash.Dash):
            raise TypeError('The argument "app" needs to be a Dash instance.')

        # Bind the redirection of the downloading results.
        @app.callback(
            Output("{0}-js-trigger".format(self.__id), "children"),
            [Input("{0}-trigger".format(self.__id), "children")],
            prevent_initial_call=True,
        )
        def download_redirect(trigger: Optional[str]):
            """Trigger of download link redirection."""
            if not trigger:
                return dash.no_update
            if self.__to_addr is None:
                return trigger
            addr = self.__to_addr(trigger)
            if not addr:
                return dash.no_update
            return addr

        # Client-side callback, the downloading is actually fired by this callback.
        app.clientside_callback(
            self.callback_js,
            Output("{0}-js-finish-trigger".format(self.__id), "children"),
            Input("{0}-js-trigger".format(self.__id), "children"),
            prevent_initial_call=True,
        )
