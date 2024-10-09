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

# Import sub-modules.
from . import downloader


from .downloader import Downloader


__all__ = (
    "downloader",
    "Downloader",
)

# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
