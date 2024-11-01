#!/usr/bin/env python3
'''This module with tools for request caching and tracking.'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.'''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.'''
        redis_store.incr(f'count:{url}')  # Increment the count for the URL
        result = redis_store.get(f'result:{url}')
        if result:
            # Decode the result if it exists in cache
            return result.decode('utf-8')
        try:
            response = requests.get(url)
            # Raise an HTTPError if the status is 4xx, 5xx
            response.raise_for_status()
            result = response.text
            # Store the result in cache
            redis_store.setex(f'result:{url}', 10, result.encode('utf-8'))
            return result
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return ""
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.'''
    pass  # The actual implementation is handled by the data_cacher decorator
