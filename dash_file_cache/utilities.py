"""
Utilities
=========
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
Shared utilities used for handling the files and requests.
"""

import os
import sys
import weakref
import shutil
import tempfile
import contextlib
import multiprocessing as mproc
import types
import io

from typing import Union, Optional, Generic, TypeVar, IO

try:
    from typing import Callable
    from typing import Type
except ImportError:
    from collections.abc import Callable
    from builtins import type as Type


__all__ = (
    "is_in_main_process",
    "remove_temp_dir",
    "TempDir",
    "StreamFinalizer",
)
_IO = TypeVar("_IO", bound=IO)
_BaseException = TypeVar("_BaseException", bound=BaseException)


if sys.version_info >= (3, 8):

    def is_in_main_process() -> bool:
        """Check whether the current process is the main process."""
        return mproc.parent_process() is None

else:

    def is_in_main_process() -> bool:
        """Check whether the current process is the main process."""
        return mproc.current_process().name.casefold() == "mainprocess"


def remove_temp_dir(path: Union[str, os.PathLike]) -> None:
    """Remove the temporary directory.

    Note that this method only works if it is called by the main process.

    The exception caused by file occupation is suppressed.
    """
    if not is_in_main_process():
        return
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)


class TempDir:
    """Temporary directory.

    Will remove the entire directory when this instance is destructed.

    Acquired from
    https://docs.python.org/3/library/weakref.html#comparing-finalizers-with-del-methods
    """

    def __init__(self, path: Union[str, os.PathLike, None] = None) -> None:
        """Initialzation.

        Arguments
        ---------
        path: `str | os.PathLike | None`
            The path to the temporary directory. If this path is absent, will use
            `tempfile.mkdtemp()` to create a file in the temporary folder.
        """
        if path is None:
            self.__path = str(tempfile.mkdtemp())
        else:
            os.makedirs(path, exist_ok=True)
            self.__path = str(path)
        self._finalizer = weakref.finalize(self, remove_temp_dir, self.__path)

    def remove(self) -> None:
        """Remove this folder explicitly.

        Note that this method only works if it is called by the main process.
        """
        if is_in_main_process():
            self._finalizer()

    @property
    def path(self) -> str:
        """Property: The path of this temporary folder."""
        return self.__path

    @property
    def is_removed(self) -> bool:
        """Property: Check whether this temporary folder has been removed."""
        return not self._finalizer.alive


class StreamFinalizer(contextlib.ContextDecorator, Generic[_IO]):
    """Finalizer for a stream IO when the stream has been delivered.

    This class will be used by `ServiceData` for safely maintain the file object while
    serving the file stream.
    """

    def __init__(
        self,
        fobj: _IO,
        truncate: bool = False,
        close: bool = False,
        callback_on_exit: Optional[Callable[[_IO], None]] = None,
    ) -> None:
        """Initialization.

        Arguments
        ---------
        fobj: `IO[Any]`
            The file-like object to be managed whent the exiting the finalizer
            environment.

        truncate: `bool`
            If set, will trucate the file when exiting the context. This flag needs
            cannot be used when the IO is read-only.

        close: `bool`
            If set, will close the file handle when exiting the context.

        callback_on_exit: `((IO[Any]) -> None) | None`
            The callback function that will be called when exiting from the context.
            This method will be called before the file is truncated or closed.
        """
        self.__fobj = fobj
        self.__truncate = bool(truncate)
        self.__close = bool(close)
        self.__callback_on_exit = (
            callback_on_exit if callable(callback_on_exit) else None
        )

    def __enter__(self) -> _IO:
        """Entering the context, reset the file cursor."""
        self.__fobj.seek(0, io.SEEK_SET)
        return self.__fobj

    def __exit__(
        self,
        exc_type: Optional[Type[_BaseException]],
        exc_value: Optional[_BaseException],
        exc_traceback: Optional[types.TracebackType],
    ) -> None:
        """Exiting the context, clear the related file-like object."""
        if self.__callback_on_exit is not None:
            self.__fobj.seek(0, io.SEEK_SET)
            self.__callback_on_exit(self.__fobj)
        if self.__truncate:
            self.__fobj.seek(0, io.SEEK_SET)
            self.__fobj.truncate(0)
        if self.__close:
            self.__fobj.close()
