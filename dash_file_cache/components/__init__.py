# -*- coding: UTF-8 -*-
"""
Components
==========
@ Dash File Cache

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Extra components provided by this package. These components provide extensive
functionalities based on the file cache.
"""

from pkgutil import extend_path

import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import PlainDownloader, Downloader
from ._imports_ import __all__ as __import_all__

from . import typehints
from .typehints import DownloaderURL, DownloaderStatus


__all__ = (
    "typehints",
    "PlainDownloader",
    "Downloader",
    "DownloaderURL",
    "DownloaderStatus",
)

if not hasattr(_dash, "__plotly_dash") and not hasattr(_dash, "development"):
    print(
        "Dash was not successfully imported. "
        "Make sure you don't have a file "
        'named \n"dash.py" in your current directory.',
        file=_sys.stderr,
    )
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package-info.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

async_resources = ["PlainDownloader", "Downloader"]

_js_dist = []

_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js".format(async_resource),
            "external_url": ("https://unpkg.com/{0}@{2}" "/{1}/async-{3}.js").format(
                package_name, __name__, __version__, async_resource
            ),
            "namespace": package_name,
            "async": True,
        }
        for async_resource in async_resources
    ]
)

# TODO: Figure out if unpkg link works
_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js.map".format(async_resource),
            "external_url": (
                "https://unpkg.com/{0}@{2}" "/{1}/async-{3}.js.map"
            ).format(package_name, __name__, __version__, async_resource),
            "namespace": package_name,
            "dynamic": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {"relative_package_path": "dash_file_cache.min.js", "namespace": package_name},
        {
            "relative_package_path": "dash_file_cache.min.js.map",
            "namespace": package_name,
            "dynamic": True,
        },
    ]
)

_css_dist = []

for _component in __import_all__:
    _component_obj = locals()[_component]
    setattr(
        _component_obj,
        "_namespace",
        getattr(_component_obj, "_namespace").replace("_component", ""),
    )
    setattr(_component_obj, "_js_dist", _js_dist)
    setattr(_component_obj, "_css_dist", _css_dist)

# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
