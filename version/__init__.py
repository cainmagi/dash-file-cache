# -*- coding: UTF-8 -*-
"""
Version
=======
@ Dash File Cache

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Version resolver for building the package. This package is only included in the wheel.
It is used for dynamically extracting the package version from `package.json`.
"""

import os
import json


__all__ = ("__version__",)

_basepath = "."
_filepath = os.path.abspath(os.path.join(_basepath, "package.json"))
with open(_filepath) as f:
    __version__ = str(json.load(f)["version"])
