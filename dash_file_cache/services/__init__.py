# -*- coding: UTF-8 -*-
"""
Services
========
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
The flask services. Bind these services to the dash/flask apps to provide extra
functionalities.
"""

from pkgutil import extend_path

# Import sub-modules.
from . import utilities
from . import reqstream
from . import downloader
from . import data

from .data import ServiceData
from .downloader import ServiceDownloader

__all__ = (
    "utilities",
    "reqstream",
    "downloader",
    "data",
    "ServiceData",
    "ServiceDownloader",
)

# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
