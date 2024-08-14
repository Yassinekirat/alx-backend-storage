#!/usr/bin/env python3
""" Writing strings to Redis"""
import redis
import uuid
from typing import Union
from typing import Callable, Optional, Union


class Cache:
    def __init__(self):
        """Starting constructor method python"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """Retrieve data from Redis and apply an optional function"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis"""
        return self.get(key, fn=int)
