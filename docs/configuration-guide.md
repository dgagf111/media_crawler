# 配置管理指南

本项目采用基于YAML的分层配置管理系统，支持开发、测试、生产等多个环境的配置分离。

## 📁 配置文件结构

```
├── env.yaml              # 全局非敏感配置
├── config/
│   ├── config.py         # 配置管理核心代码
│   ├── dev.yaml          # 开发环境配置
│   ├── test.yaml         # 测试环境配置
│   └── prod.yaml         # 生产环境配置
```

## 🏗️ 配置分层设计

### 1. env.yaml（全局配置）
存储**非敏感的统一配置**，不随环境变化：
- 环境选择配置
- 日志配置
- 调度器配置
- 模块配置
- 公共参数（时区、API版本、默认端口等）

### 2. config/{env}.yaml（环境配置）
存储**环境相关的配置**，包含敏感信息：
- 数据库连接信息
- API密钥
- 缓存配置
- 监控配置
- API服务器配置

## 🔧 环境切换

### 方法1：修改 env.yaml
```yaml
env:
  dev    # 开发环境
  #test  # 测试环境  
  #prod  # 生产环境
```

### 方法2：环境变量
```bash
# 开发环境
ENV=dev python main.py

# 测试环境
ENV=test python main.py

# 生产环境
ENV=prod python main.py
```

## 📋 配置示例

### env.yaml（全局配置）
```yaml
env:
  dev  # 当前环境

module_config:
  base_path: modules
  modules:
    - test

logging:
  project_name: project_name
  base_log_directory: ../log
  log_level: INFO 

scheduler:
  executors:
    default_threads: 20
    process_pool: 5
  job_defaults:
    coalesce: false
    max_instances: 3

# 非敏感的统一配置
common:
  time_zone: Asia/Shanghai
  api_version: v1
  ports:
    redis_default: 6379
    mysql_default: 3306
```

### config/dev.yaml（开发环境）
```yaml
# 开发环境配置文件
database:
  username: your_username
  password: your_password
  host: localhost
  port: 3306
  database: your_database

cache:
  type: memory  # 开发环境使用内存缓存
  ttl: 3600
  max_size: 1000
  redis:
    host: localhost
    port: 6379
    db: 0

api:
  host: "0.0.0.0"
  port: 8000
  loop: "asyncio"
  open_api_on_startup: true  # 开发环境自动打开文档
  docs_url: "/docs"
  cors_origins: ["*"]
  max_concurrency: 100
  request_timeout: 30
  api_version: v1
  
security:
  token:
    secret_key: your-secret-key-for-development
    algorithm: HS256
    access_token_expire_minutes: 180  # 3小时
    refresh_token_expire_days: 7
  revocation:
    backend: memory
    key_prefix: ppt:security
    default_ttl_seconds: 604800
    memory_cleanup_interval_seconds: 120
    redis:
      host: localhost
      port: 6379
      db: 2
      username:
      password:
      ssl: false
  audit:
    enabled: true
    include_username: true
```

### config/prod.yaml（生产环境）
```yaml
# 生产环境配置文件
database:
  username: ${PPT_DATABASE__USERNAME}
  password: ${PPT_DATABASE__PASSWORD}
  host: ${PPT_DATABASE__HOST}
  port: ${PPT_DATABASE__PORT}
  database: ${PPT_DATABASE__DATABASE}

cache:
  type: redis  # 生产环境优先使用Redis缓存
  ttl: 3600
  max_size: 1000
  redis:
    host: ${PPT_CACHE__REDIS__HOST}
    port: ${PPT_CACHE__REDIS__PORT}
    db: 0

monitoring:
  prometheus_port: 9966
  cpu_threshold: 70  # 生产环境设置更低的阈值
  memory_threshold: 70

api:
  host: "0.0.0.0"
  port: 8000
  loop: "uvloop"  # 生产环境使用更高性能的事件循环
  open_api_on_startup: false
  docs_url: null  # 生产环境禁用文档
  cors_origins: ["https://your-domain.com", "https://api.your-domain.com"]
  max_concurrency: 500  # 生产环境更高的并发数
  request_timeout: 15   # 生产环境更短的超时时间
  api_version: v1
  
security:
  token:
    secret_key: ${PPT_SECURITY__TOKEN__SECRET_KEY}
    algorithm: HS256
    access_token_expire_minutes: 30   # 30分钟
    refresh_token_expire_days: 3   # 天
  revocation:
    backend: redis
    key_prefix: ppt:security
    default_ttl_seconds: 259200
    memory_cleanup_interval_seconds: 45
    redis:
      host: ${PPT_SECURITY__REVOCATION__REDIS__HOST:-redis}
      port: ${PPT_SECURITY__REVOCATION__REDIS__PORT:-6379}
      db: 2
      username:
      password:
      ssl: false
  audit:
    enabled: true
    include_username: true
```

## 💻 使用方法

### 基本用法
```python
from config.config import config

# 获取MySQL配置
mysql_config = config.get_mysql_config()
print(f"数据库主机: {mysql_config['host']}")

# 获取API配置
api_config = config.get_api_config()
print(f"API端口: {api_config['port']}")

# 获取公共配置
print(f"时区: {config.get_time_zone()}")
print(f"API版本: {config.get_api_version()}")
```

### 配置方法一览
```python
config.get_env_config()        # 环境配置
config.get_common_config()     # 公共配置
config.get_mysql_config()      # MySQL配置
config.get_api_config()        # API配置
config.get_cache_config()      # 缓存配置
config.get_monitoring_config() # 监控配置
config.get_log_config()        # 日志配置
config.get_scheduler_config()  # 调度器配置
config.get_tasks_config()      # 任务配置
config.get_time_zone()         # 时区
config.get_api_version()       # API版本
```

## 🔐 环境变量支持

配置文件中可以使用环境变量：

```yaml
database:
  username: ${PPT_DATABASE__USERNAME}
  password: ${PPT_DATABASE__PASSWORD}
  host: ${PPT_DATABASE__HOST:-localhost}  # 带默认值
  port: ${PPT_DATABASE__PORT:-3306}
  database: ${PPT_DATABASE__DATABASE}
security:
  token:
    secret_key: ${PPT_SECURITY__TOKEN__SECRET_KEY}
```

### 生产环境变量设置
```bash
export PPT_DATABASE__USERNAME=prod_user
export PPT_DATABASE__PASSWORD=secure_password
export PPT_DATABASE__HOST=prod-db.example.com
export PPT_DATABASE__PORT=3306
export PPT_DATABASE__DATABASE=prod_database
export PPT_CACHE__REDIS__HOST=redis.example.com
export PPT_CACHE__REDIS__PORT=6379
export PPT_SECURITY__TOKEN__SECRET_KEY=your-super-secret-production-key
export PPT_SECURITY__REVOCATION__REDIS__HOST=redis.example.com
export PPT_SECURITY__REVOCATION__REDIS__PORT=6379
```

## 🌍 环境配置对比

| 配置项 | 开发环境 | 测试环境 | 生产环境 |
|--------|---------|---------|---------|
| 缓存类型 | memory | memory | redis |
| API文档 | 启用 | 启用 | 禁用 |
| 事件循环 | asyncio | asyncio | uvloop |
| CORS | 允许所有 | 允许所有 | 限制域名 |
| 令牌过期时间 | 3小时 | 15分钟 | 30分钟 |
| 数据库 | 本地测试库 | 测试专用库 | 生产数据库 |
| 监控阈值 | 80% | 80% | 70% |
| 并发数 | 100 | 50 | 500 |

## 🔧 配置最佳实践

### 1. 敏感信息管理
- ✅ 生产环境敏感信息使用环境变量
- ✅ 开发环境可以直接写在配置文件中
- ❌ 不要在代码库中提交生产环境密码

### 2. 环境隔离
- ✅ 每个环境使用独立的数据库和Redis
- ✅ 测试环境使用较小的资源限制
- ✅ 生产环境禁用调试功能

### 3. 配置验证
```python
# 配置验证示例
def validate_config():
    api_config = config.get_api_config()
    
    # 验证必需的配置项
    required_fields = ['host', 'port', 'secret_key']
    for field in required_fields:
        if not api_config.get(field):
            raise ValueError(f"Missing required API config: {field}")
    
    # 验证端口范围
    port = api_config.get('port')
    if not (1024 <= port <= 65535):
        raise ValueError(f"Invalid port number: {port}")
```

### 4. 配置热重载
```python
# 重新加载配置（慎用于生产环境）
def reload_config():
    config._initialized = False
    config._load_config()
```

## 🚀 部署配置

### Docker部署
```dockerfile
# Dockerfile中设置环境
ENV ENV=prod
ENV PPT_DATABASE__USERNAME=prod_user
ENV PPT_SECURITY__TOKEN__SECRET_KEY=your-production-secret

# 复制配置文件
COPY env.yaml /app/
COPY config/ /app/config/
```

### 容器编排
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - ENV=prod
      - PPT_DATABASE__USERNAME=${PPT_DATABASE__USERNAME}
      - PPT_DATABASE__PASSWORD=${PPT_DATABASE__PASSWORD}
      - PPT_SECURITY__TOKEN__SECRET_KEY=${PPT_SECURITY__TOKEN__SECRET_KEY}
    env_file:
      - .env.prod
```

## 🐛 故障排除

### 常见问题

1. **配置文件找不到**
   ```
   FileNotFoundError: config file not found
   ```
   确保在项目根目录运行程序，检查env.yaml和config/{env}.yaml文件是否存在。

2. **环境变量未解析**
   ```
   api_version: ${API_VERSION}
   ```
   检查环境变量是否正确设置，或使用带默认值的语法：`${API_VERSION:-v1}`

3. **配置值类型错误**
   ```
   TypeError: port must be integer
   ```
   检查配置文件中的数值类型是否正确，特别是端口号等数字配置。

### 调试配置
```python
# 打印所有配置用于调试
def debug_config():
    print("=== 调试配置信息 ===")
    print("环境配置:", config.get_env_config())
    print("API配置:", config.get_api_config())
    print("MySQL配置:", config.get_mysql_config())
    print("缓存配置:", config.get_cache_config())
```

---

**最后更新**: 2025-09-01  
**配置系统版本**: v3.1.0

> 💡 **提示**: 配置更改后建议运行测试确保系统正常工作：`python tests/test_framework_integration.py`
