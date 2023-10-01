from laroux.laroux import LarouxCache, _LarouxCacheList, _ListIterator, _ListNode
import pytest


def test_new_cache_is_empty():
    cache = LarouxCache[str, str]()
    assert len(cache) == 0


def test_new_cache_size_is_correct():
    cache = LarouxCache[str, str](max_size=100)
    assert cache._max_size == 100


def test_change_cache_size():
    cache = LarouxCache[str, str](max_size=100)
    cache.resize(128)
    assert cache._max_size == 128


def test_cache_size_set_correctly():
    cache = LarouxCache[str, str]()
    cache.push("foo", "a")
    assert len(cache) == 1


def test_add_and_peek():
    cache = LarouxCache[str, str](max_size=3)
    cache.push("foo", "a")
    assert cache.peek() == "a"


def test_add_and_retrieve():
    cache = LarouxCache[str, str](max_size=3)
    cache.push("foo", "a")
    cache.push("bar", "b")
    assert cache["bar"] == "b"


def test_lru_function():
    cache = LarouxCache[str, str](max_size=10)
    cache.push("a", "foo")
    cache.push("b", "bar")
    cache.push("c", "baz")
    _ = cache["a"]
    assert cache.peek() == "foo"
    _ = cache["b"]
    assert cache.peek() == "bar"


def test_eviction():
    cache = LarouxCache[str, int](max_size=3)
    ltr = ["a", "b", "c"]
    num = [0, 1, 2]
    for k, v in zip(ltr, num):
        cache.push(k, v)
    cache.push("d", 3)
    assert len(cache) == 3
    val = cache["a"]
    assert val is None


def test_stringize_cache():
    cache = LarouxCache[str, str](max_size=1)
    cache.push("foo", "a")
    assert str(cache) == "['a']"


def test_new_list_is_empty():
    lst = _LarouxCacheList[str, str]()
    assert len(lst) == 0


def test_stringize_list_node():
    lst = _LarouxCacheList[str, int]()
    lst.push("a", 42)
    assert str(lst.peek()) == "42"


def test_list_size_set_correctly_on_add():
    lst = _LarouxCacheList[str, str]()
    lst.push("a", "foo")
    assert len(lst) == 1


def test_list_size_set_correctly_on_remove():
    lst = _LarouxCacheList[str, str]()
    lst.push("a", "foo")
    lst.remove(lst.peek())
    assert len(lst) == 0


def test_list_iteration():
    lst = _LarouxCacheList[str, str]()
    lst.push("a", "a")
    lit = iter(lst)
    assert lit.current.value == "a"


def test_list_correct_order():
    lst = _LarouxCacheList[int, int]()
    for i in range(10):
        lst.push(i, i)
    for i, v in zip(range(0, 10, -1), lst):
        assert i == v.value


def test_list_arrayize():
    array = [1, 2, 3]
    lst = _LarouxCacheList[int, int]()
    for i in reversed(range(1, 4)):
        lst.push(i, i)
    lst_array = lst.arrayize()
    assert lst_array == array


def test_list_remove():
    lst = _LarouxCacheList[int, int]()
    for i in reversed(range(0, 10)):
        lst.push(i, i)
    node = lst.find(5)
    if node:
        retval = lst.remove(node)
    assert len(lst) == 9
    assert 5 not in lst.arrayize()


def test_list_find():
    lst = _LarouxCacheList[int, int]()
    for i in range(0, 3):
        lst.push(i, i)
    node = lst.find(38)
    assert node is None


def test_list_pop():
    lst = _LarouxCacheList[int, int]()
    for i in range(0, 3):
        lst.push(i, i)
    assert lst.pop() == 0


def test_list_remove_nonexistent_returns_none():
    lst = _LarouxCacheList[int, int]()
    for i in range(0, 3):
        lst.push(i, i)
    assert lst.remove(None) is None


def test_list_stringize():
    lst = _LarouxCacheList[int, int]()
    for i in range(0, 3):
        lst.push(i, i)
    assert str(lst) == "[2, 1, 0]"
