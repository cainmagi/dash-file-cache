# -*- coding: UTF-8 -*-
"""
Memory
======
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
The caches implemented by the data exchanges in the memory. Since the data is
maintained in the memory. A very large file (for example, a file exceeding the size of
the memory) may cause such caches to fail.

A good thing is that such caches can be used for storing any kinds of data. Note that
sharing data among processes needs the data to support `pickle`.

This module provides two implementations:

1. CachePlain: Share data within the same process. It will not work if the background
   callbacks are used.
2. CacheQueue: Share data based on a queue shared by multiple processes. It can work
   among threads or processes. Therefore, it is compatible with the background
   callbacks.
"""

import uuid
import weakref

from typing import Union, Optional, Any, TypeVar

try:
    from typing import Mapping
    from typing import Tuple, Dict
except ImportError:
    from collections.abc import Mapping
    from builtins import tuple as Tuple, dict as Dict

from typing_extensions import ClassVar, Literal, Never

import threading
import queue

from . import typehints as th
from .lrudict import LRUDict
from .. import utilities as utils
from .abstract import CacheAbstract


Info = TypeVar("Info", bound=Mapping[str, Any])
Data = TypeVar("Data")

_Info = TypeVar("_Info", bound=Mapping[str, Any])
_Data = TypeVar("_Data")

__all__ = ("CachePlain", "CacheQueue")


class CachePlain(CacheAbstract[Info, Data]):
    """The plain implementation of the cache.

    This `CachePlain` instance can only share the cached data among threads. It can
    be used in normal callbacks. However, in background callbacks, any modifications
    on`CachePlain` will be aborted when the callback gets finalized.

    Manipulation of this cache is threading-safe.
    """

    def __init__(self, cache_size: int) -> None:
        """Initialization.

        Arguments
        ---------
        cache_size: `int`
            The size of the cache, i.e. the maximum of items in the cache. When the
            cache is full, adding more data in the cache will cause the eldest data
            to quit from the cache.
        """
        super().__init__()
        if cache_size < 1:
            raise ValueError('cache: The argument "cache_size" needs to be >=1.')
        self.__cache: LRUDict[str, Tuple[Info, Data]] = LRUDict(maxsize=cache_size)

    def __repr__(self) -> str:
        return "<{0} cache={1}>".format(self.__class__.__name__, repr(self.__cache))

    def __str__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, str(self.__cache))

    @property
    def cache(self) -> LRUDict[str, Tuple[Info, Data]]:
        """Property: Get the low-level LRU cache object of this instance."""
        return self.__cache

    def is_in(self, key: str) -> bool:
        """Check whether `key` is registered in the cache.

        The `__contains__` operator is delegated to this method.
        """
        return key in self.__cache

    def remove(self, key: str) -> Info:
        """Remove the info of one cached item from this cache.

        Using this method implies that the data in the cache reaches its end of life.
        Only the cache item information will still be usable.

        Returns
        -------
        #1: `{str: Any}`
            The light-weighted meta-data queried in the cache.
        """
        info = self.load_info(key)
        del self.__cache[key]
        return info

    def dump(self, key: str, info: Info, data: Data) -> None:
        """Dump data to the cache.

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
        self.__cache[key] = (info, data)

    def load(self, key: str) -> Tuple[Info, th.Deferred[Data]]:
        """Load the data by a specific keyword.

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
        info, value = self.__cache[key]

        def _deferred() -> Data:
            return value

        return info, _deferred


class CacheQueue(CacheAbstract[Info, Data]):
    """The cache implementation based on process-sharable `Queue()`.

    Note that a threading queue can be also used here. But it is recommended to use
    `multiprocessing.get_context(...).Manager().Queue()`.

    This `CacheQueue` instance is designed for caching the data among processes. This
    cache can be accessed by the background callbacks.

    Any instance of this class will create a daemon thread if it is in the main
    process. This daemon thread keeps listening to the queue.

    Manipulation of this cache is processing-safe.

    Example
    -------
    ``` python
    import multiprocessing as mproc
    from concurrent.futures import ProcessPoolExecutor

    ctx = mproc.get_context("spawn")
    man = ctx.Manager()

    cache = CacheQueue(3, man.Queue())
    cache_m = cache.mirror  # `cache` cannot be directly sent to the process pool.

    with ProcessPoolExecutor(mp_context=ctx) as exe:
        exe.submit(cache_m.dump, "a", 1).result()
        exe.submit(cache_m.dump, "b", 2).result()
        exe.submit(cache_m.dump, "c", 3).result()
        exe.submit(cache_m.dump, "d", 4).result()

    print(dict(cache.cache.items()))
    # {'d': 4, 'c': 3, 'b': 2}
    ```
    """

    threads: ClassVar[Dict[str, threading.Thread]] = dict()

    class CacheQueueMirror(CacheAbstract[_Info, _Data]):
        """The process-compatible instance of `CacheQueue`."""

        def __init__(self, qobj: queue.Queue) -> None:
            """Initialization.

            Arguments
            ---------
            qobj: `Queue`
                Acquired from the parent `CacheQueue` instance.
            """
            super().__init__()
            self.__qobj = qobj

        def is_in(self, key: str) -> Literal[False]:
            """Check whether `key` is registered in the cache.

            Not accessible for this mirror instance.
            """
            return False

        def remove(self, key: str) -> Never:
            """Remove one cached item from this cache.

            Not accessible for this mirror instance.
            """
            raise NotImplementedError('cache: Should not use "pop()" in a sub-process.')

        def dump(self, key: str, info: _Info, data: _Data) -> None:
            """Dump data to the cache.

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
            self.__qobj.put((key, info, data))

        def load(self, key: str) -> Never:
            """Load the data by a specific keyword.

            Not accessible for this mirror instance.
            """
            raise NotImplementedError(
                'cache: Should not use "load()" in a sub-process.'
            )

    def __init__(
        self,
        cache_size: int,
        qobj: Union[queue.Queue, th.Deferred[queue.Queue], None] = None,
    ) -> None:
        """Initialization.

        Arguments
        ---------
        cache_size: `int`
            The size of the cache, i.e. the maximum of items in the cache. When the
            cache is full, adding more data in the cache will cause the eldest data
            to quit from the cache.

        qobj: `Queue | (() -> Queue) | None`
            The queue object provided by either of `queue.Queue()` or the
            `multiprocessing.get_context(...).Manager().Queue()`.

            It is used for synchronize the data from the sub-processes to the main
            process.

            If this value is `None`, it means that the property `CacheQueue().qobj`
            will be implemented later. This property needs to be configured before
            the first time when this cache is used.

            If this value is a function returning a queue. It means that the function
            will be used for deferred loading. In other words, the queue will be
            initialized when it is actually used for the first time.
        """
        super().__init__()
        if cache_size < 1:
            raise ValueError('cache: The argument "cache_size" needs to be >=1.')
        self.__cache: LRUDict[str, Tuple[Info, Data]] = LRUDict(maxsize=cache_size)
        self.__qobj_func: Optional[th.Deferred[queue.Queue]] = (
            qobj if callable(qobj) else None
        )
        self.__qobj: Optional[queue.Queue] = None if callable(qobj) else qobj
        self.__finalizer: Optional[weakref.finalize] = None
        if self.__qobj is not None:
            self.__init_listener(self.__qobj)

    def __repr__(self) -> str:
        return "<{0} cache={1}>".format(self.__class__.__name__, repr(self.__cache))

    def __str__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, str(self.__cache))

    @staticmethod
    def __get_listener(
        cache: LRUDict[str, Tuple[Info, Data]], qobj: queue.Queue
    ) -> None:
        """The implementation of the process listener.

        This method is used for initializing a thread in the main process.
        """
        while True:
            data = qobj.get()
            if data is None:
                break
            (key, info, value) = data
            cache[key] = (info, value)

    @classmethod
    def __get_finalizer(cls, listener_name: str, qobj: queue.Queue):
        """The finalizer of the listener.

        This method should be called when this object is destructed. It will attempt
        to finalize the listener thread.
        """
        qobj.put(None)
        listener = cls.threads.pop(listener_name, None)
        if isinstance(listener, threading.Thread):
            listener.join()

    def __init_listener(self, qobj: queue.Queue) -> None:
        """Initialize the listener event.

        This method will be called only when this cache is initialized in the main
        process.
        """
        if utils.is_in_main_process():
            listener = threading.Thread(
                target=self.__get_listener,
                args=(self.__cache, qobj),
                daemon=True,
                name="proc-{0}".format(uuid.uuid4()),
            )
            listener.start()
            self.threads[listener.name] = listener
            self.__finalizer = weakref.finalize(
                self, self.__get_finalizer, listener.name, qobj
            )

    @property
    def qobj(self) -> queue.Queue:
        """Property: The queue object used for sharing data among processes."""
        if self.__qobj is None:
            if self.__qobj_func is None:
                raise ValueError(
                    'Need to specify the property "qobj" before using {0}.'.format(
                        self.__class__.__name__
                    )
                )
            else:
                if self.__finalizer is not None:
                    raise ValueError(
                        "cache: By somehow, the finalizer has been pre-configured. "
                        "This situation should not happen, please submit an issue to "
                        "report this behavior."
                    )
                self.__qobj = self.__qobj_func()
                self.__init_listener(self.__qobj)
                self.__qobj_func = None
        return self.__qobj

    @qobj.setter
    def qobj(self, val: Optional[queue.Queue]) -> None:
        """Property: The queue object used for sharing data among processes."""
        if self.__qobj is not None:
            raise ValueError(
                'cache: The property "qobj" has been configured. Should not configure '
                "it again."
            )
        if self.__finalizer is not None:
            raise ValueError(
                "cache: By somehow, the finalizer has been pre-configured. This "
                "situation should not happen, please submit an issue to report this "
                "behavior."
            )
        self.__qobj = val
        if val is not None:
            self.__qobj_func = None
            self.__init_listener(val)

    @property
    def mirror(self) -> CacheQueueMirror[Info, Data]:
        """Property: The queue mirror. This method should be used when `dump()`
        needs to be called in sub-processes."""
        return self.CacheQueueMirror(self.qobj)

    @property
    def cache(self) -> LRUDict[str, Tuple[Info, Data]]:
        """Property: Get the low-level LRU cache object of this instance.

        Note that this property is not accessible in a sub-process.
        """
        if not utils.is_in_main_process():
            raise NotImplementedError(
                'cache: Should not access "cache" in a sub-process.'
            )
        return self.__cache

    def is_in(self, key: str) -> bool:
        """Check whether `key` is registered in the cache.

        Please only use this method in the main process. It will not work in any
        subprocess.

        The `__contains__` operator is delegated to this method.
        """
        if not utils.is_in_main_process():
            return False
        return key in self.__cache

    def remove(self, key: str) -> Info:
        """Remove the info of one cached item from this cache.

        Using this method implies that the data in the cache reaches its end of life.
        Only the cache item information will still be usable.

        Returns
        -------
        #1: `{str: Any}`
            The light-weighted meta-data queried in the cache.
        """
        info = self.load_info(key)
        del self.__cache[key]
        return info

    def dump(self, key: str, info: Info, data: Data) -> None:
        """Dump data to the cache.

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
        self.qobj.put((key, info, data))

    def load(self, key: str) -> Tuple[Info, th.Deferred[Data]]:
        """Load the data by a specific keyword.

        Please only use this method in the main process. It will not work in any
        subprocess.

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
        if not utils.is_in_main_process():
            raise NotImplementedError(
                'cache: Should not use "load()" in a sub-process.'
            )
        info, value = self.__cache[key]

        def _deferred() -> Data:
            return value

        return info, _deferred
