#!/usr/bin/env python3
"""
implement a cache class, store data to redisRAM
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method in Cache."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Use the qualified name of the method as the Redis key
        key = f"{method.__qualname__}"
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    the cache class
    """

    def __init__(self):
        """
        connect to redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data to redis,
        set key value
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return (key)

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, float, None]:
        """
        function to decode
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return (data)

    def get_str(self, key: str) -> Optional[str]:
        """
        method to return redis value as str
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        method to return redis value as int
        """
        return self.get(key, fn=int)
