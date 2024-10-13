# -*- coding: UTF-8 -*-
"""
Abstract
========
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
The abstract class definition of caches. The abstract class is the base class of all
implementations.
"""

import abc

from typing import Any, Generic, TypeVar

try:
    from typing import Mapping
    from typing import Tuple
except ImportError:
    from collections.abc import Mapping
    from builtins import tuple as Tuple

from typing_extensions import final

from . import typehints as th


Info = TypeVar("Info", bound=Mapping[str, Any])
Data = TypeVar("Data")

__all__ = ("CacheAbstract",)


class CacheAbstract(abc.ABC, Generic[Info, Data]):
    """The abstract cache class."""

    def __contains__(self, key: str) -> bool:
        return self.is_in(key)

    @abc.abstractmethod
    def is_in(self, key: str) -> bool:
        """Abstract method checking whether `key` is registered in the cache.

        The `__contains__` operator is delegated to this method.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, key: str) -> Info:
        """Abstract method for removing the info of one cached item from this cache.

        Using this method implies that the data in the cache reaches its end of life.
        Only the cache item information will still be usable.

        Returns
        -------
        #1: `{str: Any}`
            The light-weighted meta-data queried in the cache.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def dump(self, key: str, info: Info, data: Data) -> None:
        """Abstract method for dumping data to the cache.

        Arguments
        ---------
        key: `str`
            The key value of this new data. If the `key` exists in the cache, will
            replace the original value.

        info: `{str: Any}`
            The light-weighted meta-data to be dumped into the cache.

        data: `Any`
            The data to be dumped into the cache.
        """
        raise NotImplementedError

    @final
    def load_info(self, key: str) -> Info:
        """Load the meta-data by a specific keyword.

        This method is implemented by fetching the returned value `load(key)[0]`.

        Arguments
        ---------
        key: `str`
            The key value of to be queried. If `key` does not exist in the cache, will
            raise a `FileNotFoundError`.

        Returns
        -------
        #1: `{str: Any}`
            The light-weighted meta-data queried in the cache.
        """
        return self.load(key)[0]

    @final
    def load_data(self, key: str) -> Data:
        """Load the data by a specific keyword.

        This method is implemented by fetching and calling `load(key)[1]()`.

        Arguments
        ---------
        key: `str`
            The key value of to be queried. If `key` does not exist in the cache, will
            raise a `FileNotFoundError`.

        Returns
        -------
        #1: `Any`
            The data object queried in the cache. Since `data` may be large, this value
            should be a file-like object in most cases.
        """
        return self.load(key)[1]()

    @abc.abstractmethod
    def load(self, key: str) -> Tuple[Info, th.Deferred[Data]]:
        """Abstract method for loading the data by a specific keyword.

        Arguments
        ---------
        key: `str`
            The key value of to be queried. If `key` does not exist in the cache, will
            raise a `FileNotFoundError`.

        Returns
        -------
        #1: `{str: Any}`
            The light-weighted meta-data queried in the cache.

        #2: `() -> Any`:
            The lazy loader for the data. This function implements a deferred loading
            mechanism allowing that the large-size data to be actually loaded when this
            method is called.
        """
        raise NotImplementedError
