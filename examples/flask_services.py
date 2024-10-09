# -*- coding: UTF-8 -*-
"""
Flask services
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
The demo for the cache APIs served by a pure Flask application.
"""

import os

from typing import Union, Optional

try:
    from typing import Mapping
    from typing import Tuple, Dict
except ImportError:
    from collections.abc import Mapping
    from builtins import tuple as Tuple, dict as Dict

from typing import TypedDict, overload

import flask
from flask import request

if __name__ == "__main__":
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dash_file_cache import ServiceData, CachePlain


class MethodError(Exception):
    """The error is raised when an invalid method is used."""


class AppData:
    """The management of application data."""

    class DataItem(TypedDict):
        """A registered data item."""

        path: str
        """The full path to the file."""

        content_type: str
        """The content type of the file. If an empty string is specified, will use the
        mime type."""

        mime_type: str
        """The mime type of the file."""

    def __init__(self, files: Optional[Mapping[str, DataItem]] = None) -> None:
        """Initialization.

        Arguments
        ---------
        files: `{str: }`
        """
        self.root_dir = os.path.dirname(__file__)
        self.files: Dict[str, AppData.DataItem] = (
            dict((key, self.norm_path(file)) for key, file in files.items())
            if files
            else dict()
        )
        self.service = ServiceData(CachePlain(1))

    @overload
    def norm_path(self, path: str) -> str: ...

    @overload
    def norm_path(self, path: DataItem) -> DataItem: ...

    def norm_path(self, path: Union[str, DataItem]) -> Union[str, DataItem]:
        """Normalize the path. Will

        1. If the given value is a `DataItem`, will try to return a new `DataItem` with
           the keyword `path` modified.
        2. Search whether `path` refers to a file. If so, return it directly.
        3. Search whether `path` specifies a file name in the same folder of this
           script. If so, return the full path of the file.
        4. If nothing can be found, return `path` directly.

        Arguments
        ---------
        path: `str`
            The path to be normalized.

        Returns
        -------
        #1: `str`
            The normalized path.
        """
        if not isinstance(path, str):
            content_type = path["content_type"]
            content_type = content_type if content_type else path["mime_type"]
            return self.DataItem(
                path=self.norm_path(path["path"]),
                content_type=content_type,
                mime_type=path["mime_type"],
            )
        if os.path.isfile(path):
            return path
        _path = os.path.join(self.root_dir, path)
        if os.path.isfile(_path):
            return _path
        return path

    def list_files(self) -> Tuple[str, ...]:
        """Return the list of available files."""
        return tuple(self.files.keys())

    def add_file(
        self, key: str, path: str, mime_type: str, content_type: Optional[str] = None
    ):
        """Add one file to the file manager."""
        content_type = content_type if content_type else mime_type
        self.files[key] = self.DataItem(
            path=self.norm_path(path), mime_type=mime_type, content_type=content_type
        )

    def serve(self, app: flask.Flask) -> None:
        """Provide all services related to this file manager."""

        self.service.serve(app)

        @app.route("/", endpoint="index")
        def index():
            return flask.jsonify({"files": self.list_files()})

        @app.route("/file", methods=["GET", "POST"], endpoint="file")
        def file_config():
            file_name = request.args.get("name", type=str)
            if file_name is None:
                raise TypeError(
                    'Needs to specify the argument "name" when accessing this API.'
                )
            if file_name not in self.files:
                raise FileNotFoundError(
                    'The requeste file name "{0}" does not exist in the file '
                    "list.".format(file_name)
                )
            if request.method == "GET":
                return flask.jsonify(self.files[file_name])
            elif request.method == "POST":
                file_item = self.files[file_name]
                use_download = request.args.get("download", type=bool, default=False)
                addr = self.service.register(
                    file_item["path"],
                    content_type=file_item["content_type"],
                    mime_type=file_item["mime_type"],
                    one_time_service=True,
                    download=use_download,
                )
                return flask.jsonify({"addr": addr})
            else:
                raise MethodError(
                    "The requested method {0} is not supported.".format(request.method)
                )


app = flask.Flask("test-flask-services")
appdata = AppData(
    {
        "test1": {
            "path": "test_image.svg",
            "content_type": "",
            "mime_type": "image/svg+xml",
        },
        "test2": {
            "path": "test_philips_PM5544.svg",
            "content_type": "",
            "mime_type": "image/svg+xml",
        },
    }
)


@app.errorhandler(MethodError)
def error_method(error):
    resp = flask.jsonify(
        {
            "code": 405,
            "message": "The method is not allowed for this API.",
            "error": str(error),
        }
    )
    resp.status_code = 405
    return resp


@app.errorhandler(TypeError)
def error_argument(error):
    resp = flask.jsonify(
        {
            "code": 422,
            "message": "The usage of the API is not correct.",
            "error": str(error),
        }
    )
    resp.status_code = 422
    return resp


@app.errorhandler(FileNotFoundError)
def error_data_not_found(error):
    resp = flask.jsonify(
        {"code": 404, "message": "The requested file is missing.", "error": str(error)}
    )
    resp.status_code = 404
    return resp


appdata.serve(app)


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

    app.run(host=get_ip(), port=8080, debug=False)
