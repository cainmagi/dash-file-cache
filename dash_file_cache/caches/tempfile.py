# -*- coding: UTF-8 -*-
"""
Temporary file
==============
@ Dash File Cache: caches

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The cache implemented by temporary directories. Since the data is maintained as files,
currently, the implementation in this module can be only used for caching the file-like
objects. The cached files are stored in a temorary directory and can be accessed by
any programs as long as the files do not reach the end of life.

Note that this module is totally implemented by the Python Standard Library (PySTL).
It has some limitations. For example,
1. All files will not be deleted until the program exit. The temporary folder is
   removed only at the exit of the main process.
2. During the running of the program, the files will not be deleted even if they are
   manually marked as end-of-life. These files are simply truncated as empty files.
"""

import os
import json

from typing import Union, Any, TypeVar

try:
    from typing import Mapping
    from typing import Tuple
except ImportError:
    from collections.abc import Mapping
    from builtins import tuple as Tuple

from .. import utilities as utils
from . import typehints as th
from .abstract import CacheAbstract


Info = TypeVar("Info", bound=Mapping[str, Any])
Data = TypeVar("Data")

__all__ = ("CacheFile",)


class CacheFile(CacheAbstract[th.CachedFileInfo, th.CachedData]):
    """The cache implementation based on a temporary folder.

    Different from a memory-based cache like `CachePlain` and `CacheQueue`, this
    `CacheFile` is purely implemented by file I/O. Therefore, it will not automatically
    delete expired file. Users need to take responsibility of managing the files by
    themselves.

    However, when the quit of the running program is catched by `atexit`, the entire
    temporary folder should be removed.
    """

    def __init__(
        self,
        cache_dir: Union[str, os.PathLike, utils.TempDir, None],
        chunk_size: int = 1,
    ) -> None:
        """Initialization.

        Arguments
        ---------
        cache_dir: `str | PathLike | TempDir | None`
            The path of the temporary directory used by this cache.

            If a `str` or `PathLike` is used, `cache_dir` is the path to the folder.
            It means that this folder will be managed by this `CacheFile`. The path
            will be converted to `TempDir`.

            If a `TempDir` is used, it means that this cache is sharing a temporary
            folder with other files. The folder will be managed by the given
            `cache_dir`.

            If `None` is used, a temporary folder will be created by `tempfile.mkdtemp`
            and the folder will be managed by a `TempDir` created by this `CacheFile`.

        chunk_size: `int`
            The chunk size when streaming the cached file to users. The unit is `MB`.
        """
        super().__init__()
        if chunk_size < 1:
            raise ValueError('cache: The argument "chunk_size" needs to be >=1.')
        self.__dir: utils.TempDir = (
            cache_dir
            if isinstance(cache_dir, utils.TempDir)
            else (utils.TempDir(cache_dir))
        )
        self.__chunk_size: int = chunk_size * 1024 * 1024

    def __repr__(self) -> str:
        return "<{0} dir={1}>".format(self.__class__.__name__, repr(self.__dir.path))

    def __str__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, str(self.__dir.path))

    @property
    def chunk_size(self) -> int:
        """The chunk size when saving a large file. The unit is `MB`."""
        return int(round(self.__chunk_size / (1024 * 1024)))

    @chunk_size.setter
    def chunk_size(self, val: int) -> None:
        """The chunk size when saving a large file. The unit is `MB`."""
        self.__chunk_size = int(val) * 1024 * 1024

    @property
    def dir(self) -> utils.TempDir:
        """Property: Get the temporary dir of this cache. Exporting this value to other
        `CacheFile` instances can make the temporary directory shared."""
        return self.__dir

    def key_to_path(self, key) -> str:
        """Given the key of the file, return the file path without extensions."""
        return os.path.join(self.__dir.path, key)

    def is_in(self, key: str) -> bool:
        """Check whether `key` is registered in the cache.

        The `__contains__` operator is delegated to this method.
        """
        path = self.key_to_path(key)
        return os.path.isfile(path + ".tmp") and os.path.isfile(path + ".json")

    def remove(self, key: str) -> th.CachedFileInfo:
        """Remove the info of one cached item from this cache.

        Using this method implies that the data in the cache reaches its end of life.
        Only the cache item information will still be usable.

        Returns
        -------
        #1: `{str: Any}`
            The light-weighted meta-data queried in the cache.
        """
        path = self.key_to_path(key)
        with open(path + ".json", "r") as fobj:
            info: th.CachedFileInfo = json.load(fobj)
        try:
            os.remove(path + ".json")
        except OSError:
            pass
        if os.path.isfile(path + ".tmp"):
            try:
                os.remove(path + ".tmp")
            except OSError:
                pass
        return info

    def dump(self, key: str, info: th.CachedFileInfo, data: th.CachedData) -> None:
        """Dump data to the cache.

        Arguments
        ---------
        key: `str`
            The key value of this new data. If the `key` exists in the cache, will
            replace the original value.

        info: `CachedFileInfo`
            The meta-data of the cached file.

        data: `CachedData`
            The data (that may be large-amount) of the cached file.
        """
        path = self.key_to_path(key)
        with open(path + ".json", "w") as fobj:
            json.dump(info, fobj, ensure_ascii=False)
        if data["type"] == "path":
            with open(path + ".tmp", "w") as fobj:
                fobj.write(str(data["path"]))
        elif data["type"] == "str":
            _data = data["data"]
            chunk = _data.read(self.__chunk_size)
            with open(path + ".tmp", "w") as fobj:
                while chunk:
                    fobj.write(chunk)
                    chunk = _data.read(self.__chunk_size)
        elif data["type"] == "bytes":
            _data = data["data"]
            chunk = _data.read(self.__chunk_size)
            with open(path + ".tmp", "wb") as fobj:
                while chunk:
                    fobj.write(chunk)
                    chunk = _data.read(self.__chunk_size)
        else:
            raise TypeError(
                "cache: The value to be dumped is not recognized: {0}".format(data)
            )

    def load(self, key: str) -> Tuple[th.CachedFileInfo, th.Deferred[th.CachedData]]:
        """Load the data by a specific keyword.

        Arguments
        ---------
        key: `str`
            The key value of to be queried. If `key` does not exist in the cache, will
            raise a `FileNotFoundError`.

        Returns
        -------
        #1: `th.CachedFileInfo`
            The preloaded meta-data of the file.

        #1: `() -> th.CachedData`
            The lazy loader for the data. This function implements a deferred loading
            mechanism allowing that the large-size data to be actually loaded when this
            method is called.
        """
        path = self.key_to_path(key)
        with open(path + ".json", "r") as fobj:
            info: th.CachedFileInfo = json.load(fobj)
        file_type = info["type"]

        def _deferred():
            if file_type == "path":
                with open(path + ".tmp", "r") as fobj:
                    _path: str = fobj.read()
                return th.CachedPath(type=file_type, path=_path)
            elif file_type == "str":
                fobj = open(path + ".tmp", "r")
                return th.CachedStringIO(type=file_type, data=fobj)
            elif file_type == "bytes":
                fobj = open(path + ".tmp", "rb")
                return th.CachedBytesIO(type=file_type, data=fobj)
            else:
                raise TypeError(
                    "cache: The type {0} of the key to be loaded is not "
                    "recognized: {1}".format(file_type, key)
                )

        return info, _deferred


if __name__ == "__main__":
    pass
