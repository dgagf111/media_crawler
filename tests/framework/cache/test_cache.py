import pytest
import threading
import time
from pythonprojecttemplate.cache.cache_manager import get_cache_manager
import redis
from unittest.mock import patch
from pythonprojecttemplate.cache.memory_cache import MemoryCacheManager
from pythonprojecttemplate.cache.redis_cache import RedisCacheManager

import logging
import io

@pytest.fixture(autouse=True)
def setup_logging():
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    logger = logging.getLogger('cache.redis_cache')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    yield log_capture
    logger.removeHandler(handler)

@pytest.fixture(scope="module")
def cache_manager():
    # 获取缓存管理器实例
    cache = get_cache_manager()
    yield cache
    # 在测试结束后清空缓存
    cache.clear()

def test_basic_operations(cache_manager):
    # 测试基本的设置和获取操作
    cache_manager.set("test_key", "test_value")
    assert cache_manager.get("test_key") == "test_value"

    # 测试更新操作
    cache_manager.set("test_key", "new_value")
    assert cache_manager.get("test_key") == "new_value"

    # 测试删除操作
    cache_manager.delete("test_key")
    assert cache_manager.get("test_key") is None

def test_ttl(cache_manager):
    # 测试 TTL (Time To Live) 功能
    cache_manager.set("ttl_key", "ttl_value", ttl=1)
    assert cache_manager.get("ttl_key") == "ttl_value"
    time.sleep(2)  # 等待超过 TTL 时间
    assert cache_manager.get("ttl_key") is None

def test_non_existent_key(cache_manager):
    # 测试获取不存在的键
    assert cache_manager.get("non_existent_key") is None

def test_clear(cache_manager):
    # 测试清空缓存
    cache_manager.set("key1", "value1")
    cache_manager.set("key2", "value2")
    cache_manager.clear()
    assert cache_manager.get("key1") is None
    assert cache_manager.get("key2") is None

def test_concurrent_access(cache_manager):
    # 测试并发访问
    def worker(worker_id):
        for i in range(100):
            key = f"concurrent_key_{worker_id}_{i}"
            cache_manager.set(key, f"value_{worker_id}_{i}")
            assert cache_manager.get(key) == f"value_{worker_id}_{i}"

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 验证所有键都正确设置
    for i in range(10):
        for j in range(100):
            key = f"concurrent_key_{i}_{j}"
            assert cache_manager.get(key) == f"value_{i}_{j}"

def test_large_data(cache_manager):
    # 测试大量数据
    large_data = "x" * 1000000  # 1MB 的数据
    cache_manager.set("large_key", large_data)
    assert cache_manager.get("large_key") == large_data

def test_connection_failure(cache_manager):
    if isinstance(cache_manager, RedisCacheManager):
        with patch.object(cache_manager.redis, 'get', side_effect=redis.ConnectionError):
            with pytest.raises(redis.ConnectionError):
                cache_manager.get("test_key")
    else:
        pytest.skip("This test is only applicable for Redis cache")

def test_different_data_types(cache_manager):
    # 测试列表
    test_list = ["item1", "item2", "item3"]
    cache_manager.set_list("list_key", test_list)
    retrieved_list = cache_manager.get_list("list_key")
    assert retrieved_list == test_list, "列表数据读写失败"

    # 测试哈希（字典）
    test_hash = {"field1": "value1", "field2": "value2"}
    cache_manager.set_hash("hash_key", test_hash)
    retrieved_hash = cache_manager.get_hash("hash_key")
    assert retrieved_hash == test_hash, "哈希数据读写失败"

    # 测试复杂数据结构
    complex_data = {
        "list": [1, 2, 3],
        "dict": {"a": 1, "b": 2},
    }
    cache_manager.set("complex_key", complex_data)
    retrieved_complex_data = cache_manager.get("complex_key")
    assert retrieved_complex_data == complex_data, "复杂数据结构读写失败"

    # 测试元组（对于Redis缓存应该跳过）
    if isinstance(cache_manager, RedisCacheManager):
        pytest.skip("Redis缓存不支持直接存储元组，跳过元组测试")
    else:
        test_tuple = (1, 2, 3)
        cache_manager.set("tuple_key", test_tuple)
        retrieved_tuple = cache_manager.get("tuple_key")
        assert retrieved_tuple == test_tuple, "元组数据读写失败或数据类型被改变"
        assert isinstance(retrieved_tuple, tuple), "检索到的数据不是元组类型"

    print("不同数据类型测试通过")

def test_expiration_strategy(cache_manager):
    cache_manager.set("expire_key", "expire_value", ttl=1)
    assert cache_manager.get("expire_key") == "expire_value"
    time.sleep(2)
    assert cache_manager.get("expire_key") is None

    # 测试更新 TTL
    cache_manager.set("update_ttl_key", "update_ttl_value", ttl=10)
    time.sleep(1)
    cache_manager.set("update_ttl_key", "new_value", ttl=1)
    time.sleep(2)
    assert cache_manager.get("update_ttl_key") is None

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
