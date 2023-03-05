#
# Copyright (C) 2020-2023 by Ilkka Tuohela <hile@iki.fi>
#
# SPDX-License-Identifier: BSD-3-Clause
#
"""
Abstract base class extensions for cached collections
"""
import time

from collections.abc import MutableSequence, MutableMapping
from typing import Any, Dict, Iterator, List, Optional


# pylint: disable=too-few-public-methods
class ExpiringObjectCache:
    """
    Cache of objects with cache timeout
    """
    __loading__: bool = False
    """Boolean to store cache is being loaded """
    __loaded__: Optional[float] = None
    """Timestamp when cache was last refreshed"""
    __load_duration__: Optional[float] = None
    """Stores duration of data processing in update()"""
    __load_start__: Optional[float] = None
    """Start time for loading data"""
    __max_age_seconds__: Optional[float] = None
    """Age limit for cached items in seconds"""

    def __reset__(self) -> None:
        """
        Reset state. This needs to be called when load errors are handled
        """
        self.__loading__ = False
        self.__loaded__ = None
        self.__load_duration__ = None
        self.__load_start__ = None

    def __start_update__(self) -> None:
        """
        Start updating cached data. This marks cache as loading and sets load time
        to current date
        """
        self.__loading__ = True
        self.__loaded__ = False
        self.__load_start__ = time.time()

    def __finish_update__(self) -> None:
        """
        Set current timestamp to __loaded__ attribute. Also resets __loading__ to False
        """
        now = time.time()
        self.__loaded__ = now
        if self.__load_start__:
            self.__load_duration__ = now - self.__load_start__
        self.__load_start__ = None
        self.__loading__ = False

    @property
    def __requires_reload__(self) -> bool:
        """
        Check if cached data is not yet loaded or requires reloading
        """
        if self.__loading__:
            return False
        if self.__loaded__ is None:
            return True
        if self.__max_age_seconds__ is not None:
            return time.time() > self.__loaded__ + self.__max_age_seconds__
        return False

    def update(self) -> None:
        """
        Update items in object cache
        """
        raise NotImplementedError('update() must be implemented in child class')


class CachedMutableMapping(MutableMapping, ExpiringObjectCache):
    """
    Cached mutable mapping object with maximum lifetime
    """
    __items__: Dict = {}

    def __delitem__(self, index: Any) -> None:
        """
        Delete specified item from cache
        """
        self.__items__.__delitem__(index)

    def __setitem__(self, index: Any, value: Any) -> None:
        """
        Set specified value to given index
        """
        self.__items__.__setitem__(index, value)

    def __getitem__(self, index: Any) -> Any:
        """
        Get specified item from cache
        """
        if self.__requires_reload__:
            self.update()
        return self.__items__.__getitem__(index)

    def __len__(self) -> int:
        """
        Return size of collection
        """
        if self.__requires_reload__:
            self.update()
        return len(self.__items__)

    def __iter__(self) -> Iterator[Any]:
        """
        Set specified value to given index
        """
        if self.__requires_reload__:
            self.update()
        return iter(list(self.__items__))

    # pylint: disable=arguments-differ
    def update(self, **kwargs):
        """
        Update items in object cache

        Child class implementation is expected to call __start_update__ and __finish_update__
        update in beginning and end of updates, and __reset__ in case of errors
        """
        raise NotImplementedError('update() must be implemented in child class')


class CachedMutableSequence(MutableSequence, ExpiringObjectCache):
    """
    Cached mutable sequence with maximum lifetime
    """
    __items__: List[Any] = []
    """List of cached items"""

    def __delitem__(self, index: int) -> None:
        """
        Delete specified item from cache
        """
        self.__items__.__delitem__(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Set specified value to given index
        """
        self.__items__.__setitem__(index, value)

    def insert(self, index: int, value: Any) -> None:
        """
        insert item to specific
        """
        self.__items__.insert(index, value)

    def __getitem__(self, index: int) -> Any:
        """
        Get specified item from cache
        """
        if self.__requires_reload__:
            self.update()
        return self.__items__.__getitem__(index)

    def __len__(self) -> int:
        """
        Return size of collection
        """
        if self.__requires_reload__:
            self.update()
        return len(self.__items__)

    def clear(self) -> None:
        """
        Clear cached data
        """
        self.__items__ = []
        self.__reset__()

    def update(self) -> None:
        """
        Update items in object cache

        Child class implementation is expected to call __start_update__ and __finish_update__
        update in beginning and end of updates, and __reset__ in case of errors
        """
        raise NotImplementedError('update() must be implemented in child class')
