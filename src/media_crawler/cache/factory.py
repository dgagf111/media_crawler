"""
缓存工厂模块

负责根据配置创建合适的缓存管理器实例，支持内存缓存和Redis缓存的切换。
"""

from typing import Any, Dict, Tuple

from pythonprojecttemplate.config.config import Config
from pythonprojecttemplate.log.logHelper import get_logger

from .memory_cache import MemoryCacheManager
from .redis_cache import RedisCacheManager

logger = get_logger()


class CacheFactory:
    """缓存工厂类"""

    DEFAULT_TTL = 3600
    DEFAULT_MAX_SIZE = 1000

    _cached_config: Dict[str, Any] | None = None
    _config_signature: int | None = None

    @classmethod
    def _resolve_cache_config(cls, force_reload: bool = False) -> Dict[str, Any]:
        """
        统一解析缓存配置，确保 Redis 嵌套配置被正确读取，并缓存结果。

        Returns:
            Dict[str, Any]: 包含缓存类型、TTL、redis配置与加载来源的字典
        """
        config = Config()
        settings_obj = getattr(config, "_settings", None)
        signature = id(settings_obj) if settings_obj is not None else None

        if not force_reload and cls._cached_config is not None and cls._config_signature == signature:
            return cls._cached_config

        cache_config: Dict[str, Any] = config.get_cache_config() or {}
        redis_config_raw = cache_config.get("redis") or {}
        if not isinstance(redis_config_raw, dict):
            redis_config_raw = {}

        defaults_used = []

        def _resolve_redis_value(key: str, default: Any) -> Any:
            value = redis_config_raw.get(key)
            if isinstance(value, str):
                value = value.strip() or None
            if value is None:
                defaults_used.append(key)
                return default
            return value

        redis_config = {
            "host": _resolve_redis_value("host", "localhost"),
            "port": _resolve_redis_value("port", 6379),
            "db": _resolve_redis_value("db", 0),
        }

        origin = getattr(settings_obj, "load_origin", {})
        resolved = {
            "type": (cache_config.get("type") or "memory").lower(),
            "ttl": cache_config.get("ttl", CacheFactory.DEFAULT_TTL),
            "max_size": cache_config.get("max_size", CacheFactory.DEFAULT_MAX_SIZE),
            "redis": redis_config,
            "redis_defaults": defaults_used,
            "origin": origin,
        }
        cls._cached_config = resolved
        cls._config_signature = signature
        return resolved

    @classmethod
    def clear_cache(cls) -> None:
        """手动清空缓存，供测试或配置热加载场景使用。"""
        cls._cached_config = None
        cls._config_signature = None

    @staticmethod
    def _create_memory_cache(ttl: int, max_size: int) -> MemoryCacheManager:
        """
        根据提供的 TTL 和容量创建内存缓存实例。
        """
        return MemoryCacheManager(ttl=ttl, max_size=max_size)

    @staticmethod
    def _create_redis_cache(
        redis_cfg: Dict[str, Any],
        ttl: int,
        origin: Dict[str, Any],
        defaults: Tuple[str, ...],
    ):
        """
        使用解析后的 redis 配置初始化 Redis 缓存管理器，并输出配置来源。
        """
        logger.info(
            "Redis cache configuration resolved from %s (env=%s): host=%s port=%s db=%s ttl=%s defaults=%s",
            origin.get("source", "unknown"),
            origin.get("env_name", "n/a"),
            redis_cfg["host"],
            redis_cfg["port"],
            redis_cfg["db"],
            ttl,
            defaults or "none",
        )
        return RedisCacheManager(
            host=redis_cfg["host"],
            port=redis_cfg["port"],
            db=redis_cfg["db"],
            ttl=ttl,
        )

    @classmethod
    def create_cache_manager(cls, cache_type: str | None = None):
        """
        创建缓存管理器
        """
        resolved = cls._resolve_cache_config()
        selected_type = (cache_type or resolved["type"]).lower()

        if selected_type == "redis":
            try:
                return cls._create_redis_cache(
                    resolved["redis"],
                    resolved["ttl"],
                    resolved["origin"],
                    tuple(resolved["redis_defaults"]),
                )
            except Exception:
                origin = resolved["origin"]
                logger.exception(
                    "Redis缓存初始化失败，降级到内存缓存 (env=%s, source=%s)",
                    origin.get("env_name", "n/a"),
                    origin.get("source", "unknown"),
                )
                return cls._create_memory_cache(resolved["ttl"], resolved["max_size"])
        return cls._create_memory_cache(resolved["ttl"], resolved["max_size"])

    @classmethod
    def create_memory_cache(cls):
        """创建内存缓存管理器"""
        resolved = cls._resolve_cache_config()
        return cls._create_memory_cache(resolved["ttl"], resolved["max_size"])

    @classmethod
    def create_redis_cache(cls):
        """创建Redis缓存管理器"""
        resolved = cls._resolve_cache_config()
        return cls._create_redis_cache(
            resolved["redis"],
            resolved["ttl"],
            resolved["origin"],
            tuple(resolved["redis_defaults"]),
        )


# 提供便捷的工厂函数
def get_cache_manager(cache_type=None):
    """获取缓存管理器的便捷函数"""
    return CacheFactory.create_cache_manager(cache_type)


def get_memory_cache():
    """获取内存缓存管理器的便捷函数"""
    return CacheFactory.create_memory_cache()


def get_redis_cache():
    """获取Redis缓存管理器的便捷函数"""
    return CacheFactory.create_redis_cache()
