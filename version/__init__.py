# -*- coding: UTF-8 -*-
"""
Version
=======
@ Dash File Cache

Author
------
Yuchen Jin @ AIT, Aramco Research Center
Yuchen.Jin@aramcoamericas.com

Description
-----------

Use this module to get the version number without importing `rdash`.
"""

import os
import sys
import importlib
import importlib.util
import types

from typing import Union, Optional


__all__ = ("import_dummy", "__version__")


def import_dummy(
    module_path: Union[str, os.PathLike], module_name: Optional[str] = None
) -> types.ModuleType:
    """Get a module without importing its parent.

    This dummy import should be only used when the module to be import does not rely
    on any other modules in its package.

    Arguments:
        module_path: The path of the module file.
        module_name: The module name registered in the system global list. If not
            provided, will specify the `module_name` using the file name.
    """
    module_path = str(os.path.normpath(module_path))
    if not os.path.isfile(module_path):
        raise ImportError(
            'version: The required module file is missing: "{0}".'.format(module_path)
        )
    if (not isinstance(module_name, str)) or (not module_name):
        module_name = os.path.splitext(os.path.split(module_path)[-1])[0].replace(
            "-", "_"
        )
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(
            'version: Fail to import the module "{0}". Maybe the module path does not '
            'refer to a valid module: "{1}".'.format(module_name, module_path)
        )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    if spec.loader is None:
        raise ImportError(
            'version: Fail to import the module "{0}", because the module loader '
            "cannot be automatically generated.".format(module_name)
        )
    spec.loader.exec_module(module)
    return module


version = import_dummy(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "dash_file_cache", "version.py"
    ),
    "dash_file_cache.version",
)
__version__ = version.__version__
