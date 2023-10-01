"""Laroux: a simple, friendly LRU cache.

Copyright (c) 2022 by William Ellison.

Laroux is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

Laroux is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for details.

You should have received a copy of the GNU Affero General Public License
along with Laroux.  If not, see <https://www.gnu.org/licenses>.
"""
from typing import Union, Generic, TypeVar, List

_K = TypeVar("k")
_V = TypeVar("v")


class LarouxCache(Generic[_K, _V]):
    """A general-purpose LRU cache class.

    Defaults to 32 members upon creation but this may be customized at
    the time of instantiation.

    LRU caches work by promoting the most recently used items and
    evicting the least recently used ones.  This can be a cheap, easy
    way to improve performance on heavily trafficked websites.
    """

    def __init__(self, max_size: int = 32):
        """Create a new Laroux cache.

        The maximum size defaults to 32 members but may be customized by
        the user of this library.

        Params:
        - max_size [int]: the maximum size of the cache, defaults to 32
          members.
        """
        self._max_size: int = max_size
        self._hash_table = {}
        self._cache_list: _LarouxCacheList[_K, _V] = _LarouxCacheList[_K, _V]()
        self._length: int = 0

    def __len__(self) -> int:
        """Returns the length of a Laroux cache."""
        return self._length

    def resize(self, new_size: int) -> None:
        """Changes the size of a Laroux cache.

        Params:
        - new_size [int]: the new size of the cache.
        """
        self._max_size = new_size
        while len(self._cache_list) > new_size:
            _ = self._cache_list.pop()

    def push(self, key: _K, value: _V) -> None:
        """Add a new element to a Laroux cache as a key-value pair.

        Params:
        - key [_K]: the key
        - value [_V]: the value

        Raises:
          ValueError - if the passed key is of a non-hashable type
        """
        if "__hash__" not in dir(key):
            raise ValueError("key type of Laroux cache must be hashable")

        self._hash_table[key] = value
        self._cache_list.push(key, value)
        self._length += 1
        self._evict()

    def _evict(self) -> None:
        """Evict the least-recently-used member of a Laroux cache.

        This method is not meant to be called publicly.

        Params:
          None.
        """
        if len(self) > self._max_size:
            last = self._cache_list.head.prev
            self._hash_table.pop(last.key, "oops")
            self._cache_list.pop()
            self._length -= 1

    def peek(self) -> Union[_V, None]:
        """Return the most-recently-used member of a Laroux cache."""
        return self._cache_list.peek().value

    def __getitem__(self, key: _K) -> Union[_V, None]:
        """Retrieve the item matching a specific key, or None if it doesn't exist."""
        retval = self._hash_table.get(key, None)

        if retval:
            connected_node = self._cache_list.find(retval, value_search=True)
            _ = self._cache_list.remove(connected_node)
            self._cache_list.push(key, retval)

        return retval

    def __str__(self):
        """Stringize a Laroux cache to visualize its contents."""
        return str([str(n) for n in self._cache_list])


class _ListNode(Generic[_K, _V]):
    def __init__(self, key: _K, value: Union[_V, None]):
        self.value = value
        self.key = key
        self.prev: Union[_ListNode[_K, _V], None] = None
        self.next: Union[_ListNode[_K, _V], None] = None

    def __str__(self) -> str:
        return str(self.value)


class _ListIterator(Generic[_V]):
    def __init__(self, linked_list):
        self.current = linked_list.head.next
        self.sentinel = linked_list.head

    def __next__(self):
        if self.current == self.sentinel:
            raise StopIteration
        retval = self.current
        self.current = self.current.next
        return retval


class _LarouxCacheList(Generic[_K, _V]):
    def __init__(self):
        self.head: _ListNode[_K, _V] = _ListNode[_K, _V](None, None)
        self.head.prev: _ListNode[_K, _V] = self.head
        self.head.next: _ListNode[_K, _V] = self.head
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def peek(self) -> _ListNode[_K, _V]:
        return self.head.next

    def push(self, key: _V, value: _V) -> None:
        node = _ListNode[_K, _V](key, value)
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self._length += 1

    def __iter__(self) -> _ListIterator:
        return _ListIterator(self)

    def find(self, needle: Union[_K, _V], value_search: bool = False) -> Union[_ListNode[_K, _V], None]:
        here: _ListNode[_K, _V] = self.head.next

        while here != self.head:
            if value_search and here.value == needle:
                return here
            elif here.key == needle:
                return here
            else:
                here = here.next

        return None

    def remove(self, node: Union[_ListNode[_K, _V], None]) -> Union[_V, None]:
        if node:
            previous = node.prev
            following = node.next
            previous.next = following
            following.prev = previous
            node.next = None
            node.prev = None
            self._length -= 1
            return node.value
        return None

    def pop(self) -> _V:
        retval: _V = self.head.prev.value
        last = self.head.prev.prev
        last.next = self.head
        self.head.prev = last
        return retval

    def arrayize(self) -> List[_V]:
        return [i.value for i in self]

    def __str__(self) -> str:
        return str(self.arrayize())
