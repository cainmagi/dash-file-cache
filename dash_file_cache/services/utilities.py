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

from typing import Union

try:
    from typing import Callable
except ImportError:
    from collections.abc import Callable

import dash
import flask


__all__ = ("no_cache", "get_server")


def no_cache(func: Callable):
    def new_func(*args, **kwargs) -> flask.Response:
        resp = flask.make_response(func(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp

    return functools.update_wrapper(new_func, func)


def get_server(app: Union[dash.Dash, flask.Flask]) -> flask.Flask:
    """Get the Flask server instance from the app.

    Arguments
    ---------
    app: `Dash | Flask`
        Can be either a dash or a flask app. If it is a dash app, try to fetch the
        flask server instance. Otherwise, return the flask app directly.

    Returns
    -------
    #1: `Flask`
        The flask server.
    """
    server = app.server if isinstance(app, dash.Dash) else app
    if not isinstance(server, flask.Flask):
        raise TypeError(
            "Fail to fetch the server from the app. The fetched instance is: "
            "{0}".format(app)
        )
    return server
