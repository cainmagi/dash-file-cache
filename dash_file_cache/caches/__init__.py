# -*- coding: UTF-8 -*-
"""
Caches
======
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
The implementation of caches. The caches are used for storing the temporary files that
are served to the frontend. Different kinds of caches can be used in different cases.
"""

from pkgutil import extend_path

# Import sub-modules.
from . import abstract
from . import lrudict
from . import memory
from . import tempfile

from .memory import CachePlain, CacheQueue
from .tempfile import CacheFile

__all__ = (
    "abstract",
    "lrudict",
    "memory",
    "tempfile",
    "CachePlain",
    "CacheQueue",
    "CacheFile",
)

# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
