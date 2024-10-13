"""
Utilities
=========
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
Utilities related to the Flask services.
"""

import functools

from typing import Union, Any

try:
    from typing import Callable
except ImportError:
    from collections.abc import Callable

from typing_extensions import ParamSpec

import dash
import flask

P = ParamSpec("P")


__all__ = ("no_cache", "get_server")


def no_cache(func: Callable[P, Any]) -> Callable[P, flask.Response]:
    """A deocrator adding no_cache property to the flask services.

    This decorator will mark the response of a service by `no_cache`. It is useful
    when the same value needs to be triggered for multiple times. For example, in some
    cases, users may need to click a button to download a file. If `no_cache` is not
    configured, clicking the button for the second time will not trigger any events
    unless the file to be served is changed.

    In other words, this decorator is used for disabling the cache for some specific
    services.
    """

    def new_func(*args: P.args, **kwargs: P.kwargs) -> flask.Response:
        resp = flask.make_response(func(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp

    return functools.update_wrapper(new_func, func)


def get_server(app: Union[dash.Dash, flask.Flask]) -> flask.Flask:
    """Get the Flask server instance from the application.

    Arguments
    ---------
    app: `Dash | Flask`
        Can be either a dash or a flask app. If it is a dash app, try to fetch the
        flask server instance. Otherwise, return the flask app directly.

    Returns
    -------
    #1: `Flask`
        The Flask server instance of the given `app`.
    """
    server = app.server if isinstance(app, dash.Dash) else app
    if not isinstance(server, flask.Flask):
        raise TypeError(
            "Fail to fetch the server from the app. The fetched instance is: "
            "{0}".format(app)
        )
    return server
