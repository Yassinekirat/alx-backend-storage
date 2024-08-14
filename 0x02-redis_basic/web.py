#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
import functools
from typing import Callable

client = redis.Redis()


def cache_result(expiration: int):
    """Implementing an expiring web cache and tracker"""
    def decorator(fn: Callable) -> Callable:
        """Implementing an expiring web cache and tracker"""
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            cache_key = f"{fn.__name__}:{args[0]}"
            count_key = f"count:{args[0]}"
            client.incr(count_key)
            cached_result = client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')
            result = fn(*args, **kwargs)
            client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


@cache_result(expiration=10)
def get_page(url: str) -> str:
    """Implementing an expiring web cache and tracker"""
    response = requests.get(url)
    return response.text
