from cachetools import TTLCache
from .cache_manager import BaseCacheManager
import time

class MemoryCacheManager(BaseCacheManager):
    def __init__(self, ttl, max_size):
        self.default_ttl = ttl
        self.cache = TTLCache(maxsize=max_size, ttl=ttl)

    def get(self, key):
        item = self.cache.get(key)
        if item is None:
            return None
        value, expiration, *_ = item
        if expiration is None or time.time() < expiration:
            return value
        else:
            del self.cache[key]
            return None

    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.default_ttl
        expiration = time.time() + ttl if ttl is not None else None
        self.cache[key] = (value, expiration)

    def delete(self, key):
        self.cache.pop(key, None)

    def exists(self, key):
        """检查键是否存在"""
        return self.get(key) is not None

    def clear(self):
        self.cache.clear()

    def set_list(self, key, value_list, ttl=None):
        self.set(key, value_list, ttl)

    def get_list(self, key):
        return self.get(key)

    def set_hash(self, key, value_dict, ttl=None):
        self.set(key, value_dict, ttl)

    def get_hash(self, key):
        return self.get(key)
