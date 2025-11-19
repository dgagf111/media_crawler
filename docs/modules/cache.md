# 缓存系统文档

## 概述

缓存系统提供了一个灵活、高性能的缓存解决方案，支持内存缓存和Redis缓存，具有优雅降级机制。系统采用工厂模式设计，可以根据配置自动选择合适的缓存实现。

## 架构设计

### 核心组件

```
cache/
├── cache_manager.py        # 缓存管理器工厂
├── memory_cache.py         # 内存缓存实现
├── redis_cache.py         # Redis缓存实现
├── cache_keys_manager.py  # 缓存键管理
└── cache_keys.yaml        # 缓存键配置
```

### 设计模式

1. **工厂模式**: `get_cache_manager()` 根据配置创建相应的缓存实例
2. **策略模式**: 不同的缓存实现提供统一的接口
3. **单例模式**: 确保缓存管理器的全局一致性

## 功能特性

### 1. 多种缓存类型支持

#### 内存缓存 (MemoryCache)
- **优点**: 访问速度极快，无网络延迟
- **适用场景**: 单机应用，临时数据存储
- **数据类型**: 支持所有Python数据类型，包括元组

```python
# 配置示例
cache_config = {
    'type': 'memory',
    'ttl': 3600,
    'max_size': 1000
}
```

#### Redis缓存 (RedisCache)
- **优点**: 支持分布式，数据持久化
- **适用场景**: 分布式应用，需要持久化的缓存数据
- **限制**: 不支持元组类型（会自动转换为列表）

```python
# 配置示例
cache_config = {
    'type': 'redis',
    'ttl': 3600,
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
}
```

### 2. 优雅降级机制

当Redis不可用时，系统会自动降级到内存缓存，确保应用程序的正常运行：

```python
def get_cache_manager(config):
    cache_type = config.get('type', 'memory')
    
    if cache_type == 'redis':
        try:
            return RedisCache(config)
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"Redis连接失败，降级到内存缓存: {e}")
            return MemoryCache(config)
    else:
        return MemoryCache(config)
```

### 3. 统一的API接口

所有缓存实现都提供相同的API接口：

#### 基础操作
```python
# 设置缓存
cache.set(key, value, ttl=None)

# 获取缓存
value = cache.get(key)

# 删除缓存
cache.delete(key)

# 清空所有缓存
cache.clear()

# 检查键是否存在
exists = cache.exists(key)
```

#### 高级操作
```python
# 列表操作
cache.set_list(key, [1, 2, 3], ttl=3600)
items = cache.get_list(key)

# 哈希操作
cache.set_hash(key, {'name': 'John', 'age': 30}, ttl=3600)
data = cache.get_hash(key)

# 批量操作
cache.mset({'key1': 'value1', 'key2': 'value2'})
values = cache.mget(['key1', 'key2'])
```

## 配置指南

### 环境配置

在`config/dev.yaml`中配置缓存系统：

```yaml
cache:
  type: redis  # 或 memory
  ttl: 3600   # 默认过期时间(秒)
  max_size: 1000  # 内存缓存最大条目数
  redis:
    host: ${REDIS_HOST:-localhost}
    port: ${REDIS_PORT:-6379}
    db: 0
    password: ${REDIS_PASSWORD}  # 可选
    socket_timeout: 5
    socket_connect_timeout: 5
```

### 缓存键管理

系统提供了统一的缓存键管理机制：

```yaml
# cache/cache_keys.yaml
user_cache: "user:{user_id}"
session_cache: "session:{session_id}"
product_cache: "product:{product_id}"
```

```python
# 使用缓存键管理器
from cache.cache_keys_manager import CacheKeysManager

keys_manager = CacheKeysManager()
user_key = keys_manager.get_key('user_cache', user_id=123)
# 结果: "user:123"
```

## 使用示例

### 基础使用

```python
from cache.cache_manager import get_cache_manager
from config.config import config

# 获取缓存实例
cache_config = config.get_cache_config()
cache = get_cache_manager(cache_config)

# 基础操作
cache.set("user:123", {"name": "Alice", "age": 30}, ttl=3600)
user_data = cache.get("user:123")

if user_data:
    print(f"用户姓名: {user_data['name']}")
else:
    print("用户不存在或缓存已过期")
```

### 装饰器缓存

```python
from functools import wraps
import json
import hashlib

def cache_result(ttl=3600, key_prefix=""):
    """结果缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{hash_args(args, kwargs)}"
            
            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        return wrapper
    return decorator

def hash_args(args, kwargs):
    """生成参数哈希"""
    content = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(content.encode()).hexdigest()[:8]

# 使用示例
@cache_result(ttl=1800, key_prefix="user_service")
def get_user_profile(user_id):
    # 模拟数据库查询
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}
```

### 分布式锁

```python
import time
import uuid

class DistributedLock:
    def __init__(self, cache, key, timeout=10, retry_interval=0.1):
        self.cache = cache
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.retry_interval = retry_interval
        self.lock_value = str(uuid.uuid4())
    
    def __enter__(self):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self._acquire():
                return self
            time.sleep(self.retry_interval)
        raise TimeoutError(f"无法获取锁: {self.key}")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release()
    
    def _acquire(self):
        # 使用SET NX命令尝试获取锁
        return self.cache.set(self.key, self.lock_value, ttl=self.timeout, nx=True)
    
    def _release(self):
        # 只有锁的持有者才能释放锁
        current_value = self.cache.get(self.key)
        if current_value == self.lock_value:
            self.cache.delete(self.key)

# 使用示例
with DistributedLock(cache, "process_order", timeout=30):
    # 执行需要互斥的操作
    process_critical_section()
```

## 性能优化

### 1. 批量操作

```python
# 批量设置
data = {
    "user:1": {"name": "Alice"},
    "user:2": {"name": "Bob"},
    "user:3": {"name": "Charlie"}
}
cache.mset(data)

# 批量获取
keys = ["user:1", "user:2", "user:3"]
results = cache.mget(keys)
```

### 2. 管道操作 (Redis)

```python
# Redis管道操作提高性能
if hasattr(cache, 'pipeline'):
    with cache.pipeline() as pipe:
        pipe.set("key1", "value1")
        pipe.set("key2", "value2")
        pipe.set("key3", "value3")
        pipe.execute()
```

### 3. 缓存预热

```python
def warm_up_cache():
    """缓存预热"""
    logger.info("开始缓存预热...")
    
    # 预加载热点数据
    hot_users = get_hot_users()
    for user in hot_users:
        cache.set(f"user:{user.id}", user.to_dict(), ttl=7200)
    
    # 预加载配置数据
    config_data = get_system_config()
    cache.set("system:config", config_data, ttl=3600)
    
    logger.info("缓存预热完成")
```

## 监控和指标

### 缓存命中率监控

```python
class CacheMetrics:
    def __init__(self):
        self.hits = 0
        self.misses = 0
    
    def record_hit(self):
        self.hits += 1
    
    def record_miss(self):
        self.misses += 1
    
    def get_hit_ratio(self):
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
    
    def reset(self):
        self.hits = 0
        self.misses = 0

# 集成到缓存类中
class MonitoredCache:
    def __init__(self, cache):
        self.cache = cache
        self.metrics = CacheMetrics()
    
    def get(self, key):
        value = self.cache.get(key)
        if value is not None:
            self.metrics.record_hit()
        else:
            self.metrics.record_miss()
        return value
```

### Prometheus指标

```python
from prometheus_client import Counter, Histogram, Gauge

# 缓存操作计数器
cache_operations = Counter('cache_operations_total', 
                          'Total cache operations', 
                          ['operation', 'cache_type'])

# 缓存响应时间
cache_latency = Histogram('cache_operation_duration_seconds',
                         'Cache operation duration',
                         ['operation', 'cache_type'])

# 缓存大小
cache_size = Gauge('cache_size_bytes',
                  'Current cache size in bytes',
                  ['cache_type'])
```

## 最佳实践

### 1. 键命名规范

```python
# 好的键命名
"user:profile:{user_id}"
"session:data:{session_id}"
"product:details:{product_id}"

# 避免的键命名
"u123"
"temp_data"
"cache1"
```

### 2. TTL设置策略

```python
# 根据数据特性设置不同的TTL
TTL_CONFIG = {
    'user_profile': 3600,      # 1小时 - 相对稳定的数据
    'session_data': 1800,      # 30分钟 - 会话数据
    'hot_products': 600,       # 10分钟 - 热点商品
    'system_config': 86400,    # 24小时 - 系统配置
}
```

### 3. 错误处理

```python
def safe_cache_get(key, default=None):
    """安全的缓存获取"""
    try:
        return cache.get(key)
    except Exception as e:
        logger.error(f"缓存获取失败: {key}, 错误: {e}")
        return default

def safe_cache_set(key, value, ttl=None):
    """安全的缓存设置"""
    try:
        cache.set(key, value, ttl=ttl)
        return True
    except Exception as e:
        logger.error(f"缓存设置失败: {key}, 错误: {e}")
        return False
```

### 4. 缓存更新策略

```python
# Cache-Aside 模式
def get_user_by_id(user_id):
    # 1. 先查缓存
    cache_key = f"user:{user_id}"
    user = cache.get(cache_key)
    
    if user is None:
        # 2. 缓存未命中，查数据库
        user = db.get_user(user_id)
        if user:
            # 3. 更新缓存
            cache.set(cache_key, user, ttl=3600)
    
    return user

def update_user(user_id, user_data):
    # 1. 更新数据库
    db.update_user(user_id, user_data)
    
    # 2. 删除缓存（让下次访问时重新加载）
    cache_key = f"user:{user_id}"
    cache.delete(cache_key)
```

## 故障排除

### 常见问题

1. **Redis连接失败**
   ```bash
   # 检查Redis服务状态
   systemctl status redis
   
   # 测试连接
   redis-cli ping
   ```

2. **内存缓存占用过高**
   ```python
   # 设置合理的max_size
   cache_config = {
       'type': 'memory',
       'max_size': 10000  # 限制最大条目数
   }
   ```

3. **缓存穿透**
   ```python
   # 对空结果也进行缓存
   def get_product(product_id):
       product = cache.get(f"product:{product_id}")
       if product is None:
           product = db.get_product(product_id)
           # 即使是None也缓存，TTL设置较短
           cache.set(f"product:{product_id}", product or "NULL", ttl=300)
       
       return product if product != "NULL" else None
   ```

通过合理使用缓存系统，可以显著提升应用程序的性能和用户体验。关键是要根据业务场景选择合适的缓存策略和配置。