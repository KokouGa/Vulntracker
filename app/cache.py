
from cachetools import TTLCache

#Cache with a maximum size of 1000 items and a time-to-live of 1 hour (3600 seconds)
cache = TTLCache(maxsize=1000, ttl=3600)

def get_from_cache(key: str):
    return cache.get(key)

def set_to_cache(key: str, value):
    cache[key] = value