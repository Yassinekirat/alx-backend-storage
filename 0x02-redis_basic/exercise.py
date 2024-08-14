#!/usr/bin/env python3
""" Writing strings to Redis"""
import redis
import uuid
from typing import Union
from typing import Callable, Optional, Any
import functools
import redis


def call_history(method: Callable) -> Callable:
    """Decorator to store function call history in Redis"""
    @functools.wraps(method)
    def wrapper(self: Any, *args) -> str:
        """Decorator to store function call history in Redis"""
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called"""
    @functools.wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """ Wraps called method and adds its call count redis before execution
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def replay(fn: Callable) -> None:
    """Display the history of calls for a particular method"""
    client = redis.Redis()
    
    calls = client.get(fn.__qualname__)
    calls = int(calls.decode('utf-8')) if calls else 0
    
    inputs = [input.decode('utf-8') for input in client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')



class Cache:
    def __init__(self):
        """Starting constructor method python"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
