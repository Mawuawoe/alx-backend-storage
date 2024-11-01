#!/usr/bin/env python3
"""
implement a cache class, store data to redisRAM
"""
import requests
import redis
from typing import Callable
from functools import wraps


# Initialize Redis client
r = redis.Redis()


def count_access(method: Callable) -> Callable:
    """Decorator to count and track URL accesses in Redis."""
    @wraps(method)
    def wrapper(url: str) -> str:
        # Increment the counter in Redis for the URL
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_result(timeout: int = 10) -> Callable:
    """Decorator to cache the result of the method in Redis with a timeout."""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            # Check if the content is already cached
            cached_content = r.get(f"cached:{url}")
            if cached_content:
                return cached_content.decode("utf-8")

            # Otherwise, fetch the content and cache it
            content = method(url)
            r.setex(f"cached:{url}", timeout, content)
            return content
        return wrapper
    return decorator


@count_access
@cache_result(timeout=10)
def get_page(url: str) -> str:
    """
    Fetches HTML content of a URL,
    caching it in Redis with an expiration of 10 seconds.
    """
    response = requests.get(url)
    return response.text
