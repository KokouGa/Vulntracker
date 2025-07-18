from cachetools import TTLCache
from typing import Any, Optional

# Cache with a maximum size of 1000 items and a time-to-live of 1 hour (3600 seconds)
cache: TTLCache[str, Any] = TTLCache(maxsize=1000, ttl=3600)


def get_from_cache(key: str) -> Optional[Any]:
    return cache.get(key)


def set_to_cache(key: str, value: Any) -> None:
    cache[key] = value
