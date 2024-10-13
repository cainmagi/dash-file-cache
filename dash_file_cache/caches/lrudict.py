# -*- coding: UTF-8 -*-
"""
LRUDict
=======
@ Dash File Cache: caches

License
-------
End-User License Agreement (EULA) of AIT-PDF-ANNOTATOR

Author
------
Yuchen Jin @ AIT, Aramco Research Center
Yuchen.Jin@aramcoamericas.com

Description
-----------
Implemation of the LRU Dictionary.
"""

import sys
import itertools
import collections
import collections.abc
import threading

from typing import Union, Optional, Any, Generic, TypeVar

try:
    from typing import Sequence, Mapping, Hashable, Iterable, Iterator
    from typing import List, Tuple, Dict
except ImportError:
    from collections.abc import Sequence, Mapping, Hashable, Iterable, Iterator
    from builtins import list as List, tuple as Tuple, dict as Dict

from typing_extensions import Self, overload


__all__ = ("MutableMapping", "LRUDict")

K = TypeVar("K", bound=Hashable)
T = TypeVar("T")
KS = TypeVar("KS")
S = TypeVar("S")


if sys.version_info >= (3, 9):
    from collections.abc import Mapping as _Mapping, MutableMapping
else:

    class _Mapping(collections.abc.Mapping, Generic[K, T]):
        """Dummy Compatible version of typehint available `Mapping`."""

    class MutableMapping(collections.abc.MutableMapping, Generic[K, T]):
        """Dummy Compatible version of typehint available `MutableMapping`.

        Since Python 3.9, it is allowed to specify the typhint of `MutableMapping`
        like this:
        ```python
        MutableMapping[K, V]
        ```
        However, before this version (including Python<=3.8), the above typehint is
        not an approved usage. This class use Generic class to add "dummy" typehint
        interface to the non-compatible `MutableMapping` version for ensuring that the
        package is compatible with older python versions.

        Note that the added dummy typehint will not take effect like a real typehint.
        The editor cannot infer anything from it. It is only a trick used for ensuring
        the compatibility.
        """


class LRUDictView(_Mapping[K, T]):
    """Internal class. The read-only proxy used by `MappingView` of `LRUDict`.

    Note that the methods of this class is not protected by the threading lock.
    """

    def __init__(self, keys: Sequence[K], storage: Mapping[K, T]) -> None:
        """Initialization.

        This class should be initialized by methods of `LRUDict`. Users should not
        explicitly initialize it.

        Arguments
        ---------
        keys: `[K]`
            The ordered keywords of the `LRUDict`.

        storage: `{K: T}`
            The internal storage of `LRUDict`. Accessing this storage will not trigger
            the priority change of `LRUDict`.
        """
        self.__keys = keys
        self.__storage = storage

    def __len__(self) -> int:
        return len(self.__keys)

    def __iter__(self) -> Iterator[K]:
        return iter(self.__keys)

    def __getitem__(self, key: K) -> T:
        return self.__storage[key]


class LRUDict(MutableMapping[K, T]):
    """The dictionary powered by the least recently used cache.

    Limit size, evicting the least recently looked-up key when full.

    This LRUDict is also ensured to be thread-safe.

    This LRUDict would not allow the implicit releasing of the buffer by default.
    Users need to use pop() method to release the buffer explictly.
    """

    @overload
    def __init__(self, *, maxsize: int = 10) -> None: ...

    @overload
    def __init__(self, *, maxsize: int = 10, **kwargs: T) -> None: ...

    @overload
    def __init__(self, data: Mapping[K, T], *, maxsize: int = 10) -> None: ...

    @overload
    def __init__(
        self, data: Mapping[str, T], *, maxsize: int = 10, **kwargs: T
    ) -> None: ...

    @overload
    def __init__(self, data: Iterable[Tuple[K, T]], *, maxsize: int = 10) -> None: ...

    @overload
    def __init__(
        self, data: Iterable[Tuple[str, T]], *, maxsize: int = 10, **kwargs: T
    ) -> None: ...

    # Next overload is for dict(string.split(sep) for string in iterable)
    # Cannot be Iterable[Sequence[_T]] or otherwise dict(["foo", "bar", "baz"]) is not
    # an error
    @overload
    def __init__(self: Mapping[str, str], data: Iterable[List[str]]) -> None: ...

    def __init__(self, *args, **kwargs) -> None:
        """Initialization.

        Arguments
        ---------
        data: `{K: T} | [(K, T)]`, **kwargs:
            The data used for creating the dictionary.

            The usage of the initialization is totally the same as that of a ordinary
            dictionary.

        maxsize: `int`
            The size of the cache.
        """
        super().__init__()
        self.__maxsize = kwargs.pop("maxsize", 10)
        if self.__maxsize <= 0:
            raise ValueError(
                'lrudict: The argument "maxsize" need to be a postive integer.'
            )
        self.__lock = threading.RLock()
        __storage = collections.OrderedDict(*args, **kwargs)
        self.__curkeys: "collections.deque[K]" = collections.deque(
            __storage.keys(), maxlen=self.__maxsize
        )
        self.__curkeys.reverse()
        self.__storage: Dict[K, T] = dict(
            (key, __storage[key]) for key in self.__curkeys
        )
        self.__view = LRUDictView(self.__curkeys, self.__storage)

    # Core properties and functionalities of LRUDict.
    @property
    def maxsize(self) -> int:
        """Property: The maximal size of the LRU dictionary cache."""
        return self.__maxsize

    @property
    def is_full(self) -> bool:
        """Property: Whether the dict is full."""
        with self.__lock:
            return len(self.__curkeys) >= self.maxsize

    def move_to_recent(self, key: K) -> None:
        """Move a specific key to the most recent place of the `LRUDict`."""
        with self.__lock:
            idx = self.__curkeys.index(key)
            if idx == 0:
                return
            cur_len = len(self.__curkeys)
            idx = -idx if (idx < cur_len // 2) else cur_len - idx
            self.__curkeys.rotate(idx)
            key_ = self.__curkeys.popleft()
            idx = idx - 1 if idx > 0 else idx + 1
            self.__curkeys.rotate(-idx)
            self.__curkeys.appendleft(key_)

    def __repr__(self) -> str:
        with self.__lock:
            return "<{0} {{{1}}}>".format(
                self.__class__.__name__,
                ", ".join(
                    "{0}: {1}".format(key, self.__storage[key])
                    for key in self.__curkeys
                ),
            )

    def __str__(self) -> str:
        with self.__lock:
            keys = tuple(self.__curkeys)
            if len(keys) > 1:
                contents = ", ".join(
                    itertools.chain(
                        (
                            "{0}: {1}".format(key, self.__storage[key])
                            for key in keys[:1]
                        ),
                        ("{0}".format(key) for key in keys[1:-1]),
                        (
                            "{0}: {1}".format(key, self.__storage[key])
                            for key in keys[-1:]
                        ),
                    )
                )
            elif len(keys) == 1:
                contents = "{0}: {1}".format(keys[0], self.__storage[keys[0]])
            else:
                contents = ""
            return "{0}{{{1}}}".format(self.__class__.__name__[0:1], contents)

    def __len__(self) -> int:
        """Number of items in this `LRUDict`."""
        with self.__lock:
            return len(self.__curkeys)

    def __contains__(self, key: Any) -> bool:
        with self.__lock:
            is_in = key in self.__storage
        return is_in

    def __iter__(self) -> Iterator[K]:
        with self.__lock:
            keys = iter(self.__curkeys)
        return keys

    def __getitem__(self, key: K) -> T:
        with self.__lock:
            value = self.__storage[key]
            self.move_to_recent(key)
        return value

    def __setitem__(self, key: K, value: T) -> None:
        with self.__lock:
            if key in self:
                self.move_to_recent(key)
                self.__storage[key] = value
            elif len(self.__curkeys) >= self.maxsize:
                # FIFO
                old_key = self.__curkeys.pop()
                del self.__storage[old_key]
                self.__curkeys.appendleft(key)
                self.__storage[key] = value
            else:
                self.__curkeys.appendleft(key)
                self.__storage[key] = value

    def __delitem__(self, key: K) -> None:
        with self.__lock:
            if key in self:
                self.__curkeys.remove(key)
                del self.__storage[key]
            else:
                raise KeyError(
                    "lrudict: The key {0} does not exist in the LRUDict.".format(key)
                )

    # Inherit from the deque
    def back_index(self, idx: int) -> K:
        """Given the priority index, get the corresponding keyword in the `LRUDict`.

        This method will not influence the order of keys.
        """
        with self.__lock:
            return self.__curkeys[idx]

    def index(self, key: K) -> int:
        """Given the keyword, return the priority index of this keyword in the
        `LRUDict`.

        This method will not influence the order of keys.
        """
        with self.__lock:
            return self.__curkeys.index(key)

    def reverse(self) -> None:
        """Revert the priority order of keys in this `LRUDict`."""
        with self.__lock:
            self.__curkeys.reverse()

    def rotate(self, n: int) -> None:
        """Rotate the priority order of keys in this `LRUDict` n steps to the lower
        priority direction. If n is negative, rotate to the higher priority direction.
        """
        with self.__lock:
            self.__curkeys.rotate(n)

    # Inherit from the Dict
    def __or__(self: Self, val: Mapping[K, T]) -> Self:
        """Create a new `LRUDict` with the merged keys and values of this `LRUDict` and
        other, which can be an arbitrary mapping type. The values of other take
        priority when the keys are shared.
        """
        return self.__class__(
            itertools.chain(self.items(), val.items()),
            maxsize=self.__maxsize,
        )

    def __ror__(self, val: Mapping[K, T]) -> Self:
        """Create a new `LRUDict` with the merged keys and values of this `LRUDict` and
        other, which can be an arbitrary mapping type. The values of this `LRUDict`
        take priority when the keys are shared.

        Note that this method is used only when `val` does not implement the `__or__`
        operator.
        """
        return self.__class__(
            itertools.chain(val.items(), self.items()),
            maxsize=self.__maxsize,
        )

    def __ior__(self: Self, val: Union[Mapping[K, T], Iterable[Tuple[K, T]]]) -> Self:
        """Update this `LRUDict` with keys and values from other, which may be either
        a mapping or an iterable of key/value pairs. The values of other take priority
        when keys are shared.
        """
        self.update(val)
        return self

    def clear(self) -> None:
        """Make this `LRUDict` empty."""
        with self.__lock:
            self.__curkeys.clear()
            self.__storage.clear()

    def copy(self) -> Self:
        """Make a shallow copy of this `LRUDict`."""
        res = self.__class__(maxsize=self.__maxsize)
        res.__curkeys.extend(self.__curkeys)
        res.__storage.update(self.__storage)
        return res

    def reversed(self) -> Iterator[K]:
        """Return a reverse iterator over the keys of the dictionary. This is a
        shortcut for `reversed(LRUDict.keys())`."""
        return iter(reversed(self.__curkeys))

    def keys(self):
        """`LRUDict(...).keys()` -> a set-like object providing a view on
        `LRUDict`'s keys."""
        return collections.abc.KeysView(self.__view)

    def items(self):
        """`LRUDict(...).items()` -> a set-like object providing a view on
        `LRUDict`'s items."""
        return collections.abc.ItemsView(self.__view)

    def values(self):
        """`LRUDict(...).values()` -> an object providing a view on `LRUDict`'s
        values."""
        return collections.abc.ValuesView(self.__view)

    # @overload
    # @classmethod
    # def fromkeys(
    #     cls: Type["LRUDict[KS, Any]"],
    #     iterable: Iterable[KS],
    #     value: None = None,
    #     maxsize: int = 10,
    # ) -> "LRUDict[KS, Optional[Any]]": ...

    # @overload
    # @classmethod
    # def fromkeys(
    #     cls: Type["LRUDict[KS, Any]"], iterable: Iterable[KS], value: S, maxsize: int = 10
    # ) -> "LRUDict[KS, S]": ...

    @overload
    @classmethod
    def fromkeys(
        cls,
        iterable: Iterable[KS],
        value: None = None,
        maxsize: int = 10,
    ) -> "LRUDict[KS, Optional[Any]]": ...

    @overload
    @classmethod
    def fromkeys(
        cls, iterable: Iterable[KS], value: S, maxsize: int = 10
    ) -> "LRUDict[KS, S]": ...

    @classmethod
    def fromkeys(
        cls: Any,
        iterable: Iterable[KS],
        value: Optional[S] = None,
        maxsize: int = 10,
    ) -> "LRUDict[KS, Any]":
        """Create a new ordered dictionary with keys from iterable and values
        set to value.

        Arguments
        ---------
        iterable: `[KS]`
            An iterable object that will be used as the key values of the newly
            created dictionary.

        value: `S`
            The value that will be assigned to all keywords in the created dictionary.

        maxsize: `int`
            The size of the cache.
        """
        return cls(((key, value) for key in iterable), maxsize=maxsize)

    # Extra functionalities.
    @property
    def recent(self) -> K:
        """Get the keyword of the recent item."""
        with self.__lock:
            return self.__curkeys[0]

    @property
    def eldest(self) -> K:
        """Get the keyword of the eldest item, i.e. the item to be removed if the
        dict is full and the new value arrives."""
        with self.__lock:
            return self.__curkeys[-1]

    @property
    def recent_val(self) -> T:
        """Get the value of the recent item."""
        with self.__lock:
            return self.__storage[self.__curkeys[0]]

    @property
    def eldest_val(self) -> T:
        """Get the value of the eldest item, i.e. the item to be removed if the
        dict is full and the new value arrives."""
        with self.__lock:
            return self.__storage[self.__curkeys[-1]]

    @property
    def recent_item(self) -> Tuple[K, T]:
        """Get the recent (key, val) item."""
        with self.__lock:
            key = self.__curkeys[0]
            return key, self.__storage[key]

    @property
    def eldest_item(self) -> Tuple[K, T]:
        """Get the eldest (key, val) item, i.e. the item to be removed if the
        dict is full and the new value arrives."""
        with self.__lock:
            key = self.__curkeys[-1]
            return key, self.__storage[key]

    def recent_popitem(self) -> Tuple[K, T]:
        """The same as `popitem()`."""
        with self.__lock:
            return self.popitem()

    def eldest_popitem(self) -> Tuple[K, T]:
        """Run `popitem()` but pop the eldest item."""
        with self.__lock:
            key = self.__curkeys.pop()
            val = self.__storage.pop(key)
        return key, val
