#!/usr/bin/env python3
"""
implement a cache class, store data to redisRAM
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method in Cache."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        # Use the qualified name of the method as the Redis key
        key = f"{method.__qualname__}"
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Define keys for storing inputs and outputs in Redis
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        # Store input arguments as a string in Redis
        self._redis.rpush(inputs_key, str(args))

        # Execute the method and capture the output
        result = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(outputs_key, str(result))

        # Return the result of the original method
        return result
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
    @call_history
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


def replay(method: Callable):
    """Displays the history of calls for a specific method."""
    redis_client = method.__self__._redis
    method_name = method.__qualname__

    # Fetch number of times the method was called
    call_count = redis_client.get(method_name)
    call_count = int(call_count) if call_count else 0
    print(f"{method_name} was called {call_count} times:")

    # Get input and output history
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    # Display each call's inputs and outputs
    for i, (input_data, output_data) in enumerate(zip(inputs, outputs), start=1):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")
