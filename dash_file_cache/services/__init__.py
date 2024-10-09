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
from . import data

from .data import ServiceData

__all__ = ("utilities", "data", "ServiceData")

# Set this local module as the prefered one
__path__ = extend_path(__path__, __name__)

# Delete private sub-modules and objects
del extend_path
