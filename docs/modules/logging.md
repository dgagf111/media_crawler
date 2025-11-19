# 📝 日志系统文档

Python Project Template 提供了功能完善的日志系统，支持多级别日志记录、文件轮转、结构化输出等企业级功能。

## 📋 目录

- [日志系统概览](#日志系统概览)
- [核心功能](#核心功能)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [高级特性](#高级特性)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 🏗️ 日志系统概览

### 系统架构

```
log/
├── __init__.py              # 日志模块入口
├── logHelper.py             # 核心日志助手
└── test_log_module.py       # 完整测试套件
```

### 核心特性

- **🎯 多级别日志**: DEBUG、INFO、WARNING、ERROR、CRITICAL
- **📁 文件轮转**: 自动按大小和时间轮转日志文件
- **📊 结构化输出**: JSON格式日志，便于日志分析
- **🎨 彩色输出**: 控制台彩色日志，提升可读性
- **⚡ 高性能**: 异步写入，支持高频日志记录
- **🔒 线程安全**: 支持多线程并发日志记录
- **🎛️ 灵活配置**: 支持多种配置方式和输出格式

## ⚙️ 核心功能

### 日志助手 (logHelper.py)

```python
from log.logHelper import get_logger

# 获取日志实例
logger = get_logger()

# 或获取指定名称的日志器
logger = get_logger('my_module')
```

### 日志级别说明

| 级别 | 数值 | 用途 | 示例场景 |
|------|------|------|----------|
| DEBUG | 10 | 详细诊断信息 | 变量值、函数调用跟踪 |
| INFO | 20 | 一般信息记录 | 操作成功、状态变更 |
| WARNING | 30 | 警告信息 | 配置缺失、性能问题 |
| ERROR | 40 | 错误信息 | 操作失败、异常捕获 |
| CRITICAL | 50 | 严重错误 | 系统崩溃、致命错误 |

### 输出格式

#### 控制台输出格式
```
2025-09-01 10:30:45 [INFO] [module_name] - 操作成功完成
2025-09-01 10:30:46 [ERROR] [database] - 数据库连接失败: Connection timeout
```

#### 文件输出格式 (JSON)
```json
{
    "timestamp": "2025-09-01T10:30:45.123456",
    "level": "INFO",
    "logger": "module_name", 
    "message": "操作成功完成",
    "module": "user_service",
    "function": "create_user",
    "line": 45
}
```

## 🔧 配置说明

### 环境配置

```yaml
# config/env.yaml
log:
  level: INFO                    # 日志级别
  format: structured            # 输出格式: simple/structured
  console_output: true          # 控制台输出
  file_output: true             # 文件输出
  log_dir: logs                 # 日志目录
  max_file_size: 10MB           # 最大文件大小
  backup_count: 5               # 备份文件数量
  encoding: utf-8               # 文件编码
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| level | str | INFO | 日志级别 |
| format | str | structured | 输出格式 |
| console_output | bool | true | 控制台输出开关 |
| file_output | bool | true | 文件输出开关 |
| log_dir | str | logs | 日志文件目录 |
| max_file_size | str | 10MB | 单个日志文件最大大小 |
| backup_count | int | 5 | 保留的备份文件数量 |

## 📖 使用指南

### 基础用法

```python
from log.logHelper import get_logger

# 获取日志器
logger = get_logger()

# 记录不同级别的日志
logger.debug("调试信息：变量值为 {}", variable_value)
logger.info("用户登录成功：用户ID {}", user_id)
logger.warning("配置项缺失：{}, 使用默认值", config_key)
logger.error("数据库操作失败：{}", error_message)
logger.critical("系统致命错误：{}", critical_error)
```

### 模块化日志记录

```python
# 在不同模块中使用专属日志器
class UserService:
    def __init__(self):
        self.logger = get_logger('user_service')
    
    def create_user(self, user_data):
        self.logger.info("开始创建用户：{}", user_data['username'])
        try:
            # 创建用户逻辑
            user = self._create_user_in_db(user_data)
            self.logger.info("用户创建成功：ID {}", user.id)
            return user
        except Exception as e:
            self.logger.error("用户创建失败：{}", str(e))
            raise
```

### 结构化日志

```python
import threading
from log.logHelper import get_logger

logger = get_logger()

def process_order(order_id):
    # 添加上下文信息
    logger.info(
        "开始处理订单",
        extra={
            'order_id': order_id,
            'thread_id': threading.current_thread().ident,
            'user_id': get_current_user_id(),
            'action': 'process_order'
        }
    )
```

### 异常日志记录

```python
import traceback
from log.logHelper import get_logger

logger = get_logger()

def handle_api_request(request):
    try:
        result = process_request(request)
        logger.info("API请求处理成功", extra={
            'endpoint': request.path,
            'method': request.method,
            'status_code': 200
        })
        return result
        
    except Exception as e:
        logger.error("API请求处理失败", extra={
            'endpoint': request.path,
            'error': str(e),
            'stack_trace': traceback.format_exc()
        })
        raise
```

## 🚀 高级特性

### 性能监控装饰器

```python
import time
from functools import wraps

def log_performance(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = time.time()
        
        logger.debug(f"开始执行 {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(f"{func.__name__} 执行完成", extra={
                'function': func.__name__,
                'execution_time': execution_time,
                'success': True
            })
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} 执行失败", extra={
                'function': func.__name__,
                'execution_time': execution_time,
                'error': str(e),
                'success': False
            })
            raise
            
    return wrapper

# 使用示例
@log_performance
def complex_calculation(data):
    return process_data(data)
```

### 日志分析器

```python
import json
from collections import Counter
from datetime import datetime, timedelta

class LogAnalyzer:
    """日志分析器"""
    
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        
    def analyze_logs(self, hours=24):
        """分析最近N小时的日志"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        stats = {
            'total_logs': 0,
            'level_distribution': Counter(),
            'error_count': 0,
            'warning_count': 0
        }
        
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    log_entry = json.loads(line.strip())
                    log_time = datetime.fromisoformat(log_entry['timestamp'])
                    
                    if log_time < cutoff_time:
                        continue
                    
                    stats['total_logs'] += 1
                    stats['level_distribution'][log_entry['level']] += 1
                    
                    if log_entry['level'] == 'ERROR':
                        stats['error_count'] += 1
                    elif log_entry['level'] == 'WARNING':
                        stats['warning_count'] += 1
                        
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return stats

# 使用示例
analyzer = LogAnalyzer('logs/app.log')
stats = analyzer.analyze_logs()
print(f"错误日志数: {stats['error_count']}")
```

## 🎯 最佳实践

### 1. 日志级别使用建议

- **DEBUG**: 开发调试时使用，生产环境通常关闭
- **INFO**: 记录重要的业务流程和状态变化
- **WARNING**: 记录可能的问题，但不影响正常运行
- **ERROR**: 记录错误信息，需要关注和处理
- **CRITICAL**: 记录严重错误，可能导致应用崩溃

### 2. 性能考虑

```python
# ✅ 推荐：使用延迟格式化
logger.debug("处理用户 %s 的请求", user_id)

# ❌ 避免：提前格式化字符串
# logger.debug(f"处理用户 {user_id} 的请求")  # 即使DEBUG级别关闭也会执行格式化

# ✅ 推荐：条件日志
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("复杂的调试信息: %s", expensive_debug_function())
```

### 3. 安全考虑

```python
import re

def sanitize_log_message(message):
    """清理敏感信息"""
    # 移除密码
    message = re.sub(r'"password":\s*"[^"]*"', '"password": "***"', message)
    # 移除信用卡号
    message = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '****-****-****-****', message)
    return message

# 使用示例
logger.info(sanitize_log_message("用户注册: {}".format(user_data)))
```

## 🔧 故障排除

### 常见问题

#### 1. 日志文件权限问题

```bash
# 创建日志目录并设置权限
mkdir -p logs
chmod 755 logs

# 检查文件权限
ls -la logs/
```

#### 2. 日志文件过大

```python
# 配置更激进的日志轮转
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3          # 只保留3个备份
)
```

#### 3. 中文编码问题

```python
# 确保使用UTF-8编码
import logging

handler = logging.FileHandler('logs/app.log', encoding='utf-8')
logger.addHandler(handler)
```

### 测试验证

```bash
# 运行日志模块测试
python log/test_log_module.py

# 通过测试控制器运行
python run_module_tests.py log

# 验证日志输出
tail -f logs/app.log
```

## 📚 参考资源

### 相关文档
- [测试指南](../guides/testing-guide.md) - 日志系统测试说明
- [监控系统](monitoring.md) - 集成监控和日志
- [配置管理](../config/README.md) - 日志配置说明

### 外部资源
- [Python logging 官方文档](https://docs.python.org/3/library/logging.html)
- [结构化日志最佳实践](https://12factor.net/logs)

---

**最后更新**: 2025-09-01  
**文档版本**: v3.0.0  
**模块版本**: v3.0.0

> 💡 **提示**: 日志系统支持运行时动态调整日志级别，便于生产环境调试。