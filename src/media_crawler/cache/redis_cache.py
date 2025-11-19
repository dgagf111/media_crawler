import redis
from .cache_manager import BaseCacheManager
import json
import logging

logger = logging.getLogger(__name__)

class RedisCacheManager(BaseCacheManager):
    def __init__(self, host, port, db, ttl):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.default_ttl = ttl
        self.redis.ping()  # 尝试连接 Redis

    def get(self, key):
        try:
            self.redis.ping()  # 检查连接状态
            value = self.redis.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value.decode()
            return None
        except redis.ConnectionError:
            raise
        except Exception as e:
            raise redis.ConnectionError(f"Redis connection error: {str(e)}")

    def _convert_lists_to_tuples(self, obj):
        if isinstance(obj, list):
            return tuple(self._convert_lists_to_tuples(item) for item in obj)
        elif isinstance(obj, dict):
            return {key: self._convert_lists_to_tuples(value) for key, value in obj.items()}
        return obj

    def _convert_tuples_to_lists(self, obj):
        if isinstance(obj, tuple):
            return [self._convert_tuples_to_lists(item) for item in obj]
        elif isinstance(obj, list):
            return [self._convert_tuples_to_lists(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._convert_tuples_to_lists(value) for key, value in obj.items()}
        return obj

    def set(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl
        
        if isinstance(value, tuple) or self._contains_tuple(value):
            raise ValueError("Redis缓存不支持存储元组类型。请使用列表代替。")
        
        serialized_value = json.dumps(value)
        self.redis.setex(key, ttl, serialized_value)

    def _contains_tuple(self, obj):
        if isinstance(obj, tuple):
            return True
        elif isinstance(obj, list):
            return any(self._contains_tuple(item) for item in obj)
        elif isinstance(obj, dict):
            return any(self._contains_tuple(v) for v in obj.values())
        return False

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        """检查键是否存在"""
        return self.redis.exists(key) > 0

    def clear(self):
        self.redis.flushdb()

    def set_list(self, key, value_list, ttl=None):
        self.set(key, value_list, ttl)

    def get_list(self, key):
        return self.get(key)

    def set_hash(self, key, value_dict, ttl=None):
        self.set(key, value_dict, ttl)

    def get_hash(self, key):
        return self.get(key)

