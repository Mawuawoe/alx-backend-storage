#!/usr/bin/env python3
"""
implement a cache class, store data to redisRAM
"""
import redis
import uuid
from typing import Union


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
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data to redis,
        set key value
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return(key)
