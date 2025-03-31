# -*- coding: UTF-8 -*-
"""
Dash File Cache
===============

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Utilities for providing convenient methods to serve cached data in Plotly-Dash or
Flask.
"""

from pkgutil import extend_path

# Import the version module.
from . import version
from .version import __version__

# Import sub-modules.
from . import utilities
from . import caches
from . import components
from . import services

# Import frequently-used classes.
from .caches import CachePlain, CacheQueue, CacheFile
from .services import ServiceData, ServiceDownloader
from .components import PlainDownloader, Downloader, DownloaderURL, DownloaderStatus

__all__ = (
    "__version__",
    "version",
    "utilities",
    "caches",
    "components",
    "services",
    "CachePlain",
    "CacheQueue",
    "CacheFile",
    "ServiceData",
    "ServiceDownloader",
    "PlainDownloader",
    "Downloader",
    "DownloaderURL",
    "DownloaderStatus",
)

_js_dist = []

for item in components._js_dist:
    _item = item.copy()
    if "relative_package_path" in _item:
        _item["relative_package_path"] = components._os.path.join(
            "components", _item["relative_package_path"]
        )
    _js_dist.append(_item)

_css_dist = []

for item in components._css_dist:
    _item = item.copy()
    if "relative_package_path" in _item:
        _item["relative_package_path"] = components._os.path.join(
            "components", _item["relative_package_path"]
        )
    _css_dist.append(_item)


# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
