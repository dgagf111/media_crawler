# 任务调度系统文档

## 概述

任务调度系统基于APScheduler构建，提供了灵活的定时任务管理功能，支持多种触发器类型、重试机制、并发控制等企业级特性。系统采用插件化架构，易于扩展和维护。

## 架构设计

### 核心组件

```
scheduler/
├── scheduler_center.py       # 调度中心主控制器
├── tasks/                   # 任务模块目录
│   ├── __init__.py
│   ├── task1.py            # 任务实现示例
│   ├── task2.py
│   └── base_task.py        # 任务基类
├── triggers/               # 自定义触发器
│   └── custom_trigger.py
└── decorators/            # 任务装饰器
    └── task_decorators.py
```

### 设计特点

1. **插件化架构**: 任务模块可以独立开发和部署
2. **多种触发器**: 支持interval、cron、date等触发方式
3. **重试机制**: 任务失败时自动重试，支持退避策略
4. **并发控制**: 控制任务的并发执行数量
5. **监控集成**: 内置监控指标和日志记录
6. **优雅关闭**: 支持任务的优雅停止和清理

## 功能特性

### 1. 触发器类型

#### Interval触发器 (间隔执行)

```yaml
# config/dev.yaml
tasks:
  data_sync:
    trigger: interval
    args:
      seconds: 30        # 每30秒执行一次
      # minutes: 5       # 每5分钟执行一次
      # hours: 2         # 每2小时执行一次
      # days: 1          # 每天执行一次
    max_attempts: 3
    retry_delay: 5
```

#### Cron触发器 (定时执行)

```yaml
tasks:
  daily_report:
    trigger: cron
    args:
      hour: 9           # 每天9点执行
      minute: 0
      # day_of_week: 1-5  # 周一到周五
      # month: 1-12      # 指定月份
    max_attempts: 5
    retry_delay: 10
```

#### Date触发器 (一次性执行)

```yaml
tasks:
  one_time_migration:
    trigger: date
    args:
      run_date: "2023-12-25 10:00:00"  # 指定时间执行一次
    max_attempts: 1
```

### 2. 任务实现

#### 基础任务类

```python
# scheduler/tasks/base_task.py
from abc import ABC, abstractmethod
from log.logHelper import get_logger

logger = get_logger()

class BaseTask(ABC):
    """任务基类"""
    
    def __init__(self):
        self.logger = logger
        self.task_name = self.__class__.__name__
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """执行任务的抽象方法"""
        pass
    
    def on_success(self, result):
        """任务成功完成时的回调"""
        self.logger.info(f"任务 {self.task_name} 执行成功")
    
    def on_failure(self, exception):
        """任务失败时的回调"""
        self.logger.error(f"任务 {self.task_name} 执行失败: {exception}")
    
    def on_retry(self, attempt, max_attempts):
        """任务重试时的回调"""
        self.logger.warning(f"任务 {self.task_name} 第 {attempt}/{max_attempts} 次重试")
    
    def validate_params(self, **kwargs):
        """参数验证"""
        return True
    
    def cleanup(self):
        """任务清理工作"""
        pass
```

#### 任务实现示例

```python
# scheduler/tasks/data_sync_task.py
import requests
from typing import Dict, Any
from .base_task import BaseTask
from cache.cache_manager import get_cache_manager
from config.config import config

class DataSyncTask(BaseTask):
    """数据同步任务"""
    
    def __init__(self):
        super().__init__()
        self.cache = get_cache_manager(config.get_cache_config())
        self.api_url = "https://api.example.com/data"
    
    def execute(self, source="api", batch_size=100):
        """执行数据同步"""
        self.logger.info(f"开始数据同步任务 - 来源: {source}, 批次大小: {batch_size}")
        
        try:
            # 验证参数
            self.validate_params(source=source, batch_size=batch_size)
            
            # 获取数据
            data = self._fetch_data(source, batch_size)
            
            # 处理数据
            processed_count = self._process_data(data)
            
            # 更新缓存
            self._update_cache(processed_count)
            
            result = {
                "processed_count": processed_count,
                "source": source,
                "batch_size": batch_size
            }
            
            self.on_success(result)
            return result
            
        except Exception as e:
            self.on_failure(e)
            raise
    
    def _fetch_data(self, source: str, batch_size: int) -> list:
        """获取数据"""
        if source == "api":
            response = requests.get(
                self.api_url,
                params={"limit": batch_size},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("data", [])
        elif source == "database":
            # 从数据库获取数据的逻辑
            pass
        else:
            raise ValueError(f"不支持的数据源: {source}")
    
    def _process_data(self, data: list) -> int:
        """处理数据"""
        processed_count = 0
        
        for item in data:
            try:
                # 数据处理逻辑
                processed_item = self._transform_item(item)
                
                # 保存或更新数据
                self._save_item(processed_item)
                
                processed_count += 1
                
            except Exception as e:
                self.logger.error(f"处理数据项失败: {item}, 错误: {e}")
                continue
        
        return processed_count
    
    def _transform_item(self, item: dict) -> dict:
        """转换数据项"""
        return {
            "id": item.get("id"),
            "name": item.get("name", "").strip(),
            "created_at": item.get("timestamp"),
            "processed_at": datetime.utcnow()
        }
    
    def _save_item(self, item: dict):
        """保存数据项"""
        # 实际的保存逻辑
        pass
    
    def _update_cache(self, count: int):
        """更新缓存统计"""
        cache_key = "data_sync:stats"
        stats = self.cache.get(cache_key) or {"total_processed": 0}
        stats["total_processed"] += count
        stats["last_sync"] = datetime.utcnow().isoformat()
        self.cache.set(cache_key, stats, ttl=86400)  # 缓存24小时
    
    def validate_params(self, **kwargs):
        """参数验证"""
        source = kwargs.get("source")
        batch_size = kwargs.get("batch_size")
        
        if source not in ["api", "database"]:
            raise ValueError("source参数必须是'api'或'database'")
        
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size必须是正整数")
        
        return True

# 任务入口函数
def run():
    """任务入口点 - 由调度器调用"""
    task = DataSyncTask()
    return task.execute()
```

### 3. 调度中心

```python
# scheduler/scheduler_center.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from log.logHelper import get_logger
from config.config import config
import importlib
import inspect

logger = get_logger()

class SchedulerCenter:
    """调度中心 - 管理所有定时任务"""
    
    def __init__(self):
        self.scheduler = None
        self.is_running = False
        self._setup_scheduler()
    
    def _setup_scheduler(self):
        """配置调度器"""
        # 获取配置
        scheduler_config = config.get_scheduler_config()
        tasks_config = config.get_tasks_config()
        
        # 配置执行器
        executors = {
            'default': ThreadPoolExecutor(
                max_workers=scheduler_config.get('executors', {}).get('default_threads', 20)
            ),
            'processpool': ProcessPoolExecutor(
                max_workers=scheduler_config.get('executors', {}).get('process_pool', 5)
            )
        }
        
        # 配置作业存储
        job_stores = {
            'default': MemoryJobStore()
        }
        
        # 配置作业默认值
        job_defaults = scheduler_config.get('job_defaults', {
            'coalesce': False,
            'max_instances': 3,
            'misfire_grace_time': 30
        })
        
        # 创建调度器
        self.scheduler = BackgroundScheduler(
            executors=executors,
            job_stores=job_stores,
            job_defaults=job_defaults,
            timezone='Asia/Shanghai'
        )
        
        # 添加事件监听器
        self._setup_event_listeners()
    
    def _setup_event_listeners(self):
        """设置事件监听器"""
        from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
        
        def job_executed(event):
            """任务执行成功"""
            logger.info(f"任务 {event.job_id} 执行成功")
        
        def job_error(event):
            """任务执行失败"""
            logger.error(f"任务 {event.job_id} 执行失败: {event.exception}")
        
        self.scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(job_error, EVENT_JOB_ERROR)
    
    def start(self):
        """启动调度器"""
        if self.is_running:
            logger.warning("调度器已经在运行中")
            return
        
        try:
            # 加载所有任务
            self._load_tasks()
            
            # 启动调度器
            self.scheduler.start()
            self.is_running = True
            
            logger.info("调度器启动成功")
            
        except Exception as e:
            logger.error(f"调度器启动失败: {e}")
            raise
    
    def shutdown(self, wait=True):
        """关闭调度器"""
        if not self.is_running:
            return
        
        try:
            self.scheduler.shutdown(wait=wait)
            self.is_running = False
            logger.info("调度器已关闭")
            
        except Exception as e:
            logger.error(f"调度器关闭失败: {e}")
    
    def _load_tasks(self):
        """加载所有任务"""
        tasks_config = config.get_tasks_config()
        
        for task_name, task_config in tasks_config.items():
            try:
                self._add_task(task_name, task_config)
                logger.info(f"成功加载任务: {task_name}")
                
            except Exception as e:
                logger.error(f"加载任务失败 {task_name}: {e}")
                continue
    
    def _add_task(self, task_name: str, task_config: dict):
        """添加单个任务"""
        # 导入任务模块
        task_module = importlib.import_module(f"scheduler.tasks.{task_name}")
        
        # 获取任务函数
        if hasattr(task_module, 'run'):
            task_func = task_module.run
        else:
            raise ImportError(f"任务模块 {task_name} 没有 'run' 函数")
        
        # 包装任务函数以添加重试机制
        wrapped_func = self._wrap_task_with_retry(task_func, task_config)
        
        # 获取触发器配置
        trigger_type = task_config.get('trigger', 'interval')
        trigger_args = task_config.get('args', {})
        
        # 添加任务到调度器
        self.scheduler.add_job(
            func=wrapped_func,
            trigger=trigger_type,
            id=task_name,
            name=f"Task_{task_name}",
            replace_existing=True,
            **trigger_args
        )
    
    def _wrap_task_with_retry(self, task_func, task_config):
        """为任务添加重试机制"""
        max_attempts = task_config.get('max_attempts', 1)
        retry_delay = task_config.get('retry_delay', 0)
        
        def wrapped_task(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return task_func(*args, **kwargs)
                
                except Exception as e:
                    if attempt == max_attempts - 1:
                        # 最后一次尝试失败，重新抛出异常
                        raise
                    
                    logger.warning(f"任务执行失败 (第{attempt + 1}次尝试): {e}")
                    
                    if retry_delay > 0:
                        import time
                        time.sleep(retry_delay)
        
        return wrapped_task
    
    def add_job(self, func, trigger, **kwargs):
        """动态添加任务"""
        if not self.is_running:
            raise RuntimeError("调度器未运行")
        
        return self.scheduler.add_job(func, trigger, **kwargs)
    
    def remove_job(self, job_id):
        """移除任务"""
        if not self.is_running:
            raise RuntimeError("调度器未运行")
        
        self.scheduler.remove_job(job_id)
    
    def get_jobs(self):
        """获取所有任务"""
        if not self.is_running:
            return []
        
        return self.scheduler.get_jobs()
    
    def pause_job(self, job_id):
        """暂停任务"""
        if not self.is_running:
            raise RuntimeError("调度器未运行")
        
        self.scheduler.pause_job(job_id)
    
    def resume_job(self, job_id):
        """恢复任务"""
        if not self.is_running:
            raise RuntimeError("调度器未运行")
        
        self.scheduler.resume_job(job_id)

# 全局调度器实例
scheduler_center = SchedulerCenter()
```

## 任务装饰器

### 1. 任务监控装饰器

```python
# scheduler/decorators/task_decorators.py
from functools import wraps
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge
import time

# Prometheus指标
task_executions = Counter('scheduler_task_executions_total', 
                         'Total task executions', 
                         ['task_name', 'status'])

task_duration = Histogram('scheduler_task_duration_seconds',
                         'Task execution duration',
                         ['task_name'])

active_tasks = Gauge('scheduler_active_tasks',
                    'Number of currently active tasks',
                    ['task_name'])

def monitor_task(task_name: str = None):
    """任务监控装饰器"""
    def decorator(func):
        name = task_name or func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # 增加活跃任务计数
            active_tasks.labels(task_name=name).inc()
            
            try:
                result = func(*args, **kwargs)
                
                # 记录成功执行
                task_executions.labels(task_name=name, status='success').inc()
                
                return result
                
            except Exception as e:
                # 记录失败执行
                task_executions.labels(task_name=name, status='failure').inc()
                raise
                
            finally:
                # 记录执行时间
                duration = time.time() - start_time
                task_duration.labels(task_name=name).observe(duration)
                
                # 减少活跃任务计数
                active_tasks.labels(task_name=name).dec()
        
        return wrapper
    return decorator

def rate_limit(max_calls: int, time_window: int):
    """任务频率限制装饰器"""
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # 清理过期的调用记录
            calls[:] = [call_time for call_time in calls 
                       if now - call_time < time_window]
            
            # 检查是否超过限制
            if len(calls) >= max_calls:
                raise RuntimeError(
                    f"任务 {func.__name__} 超过速率限制: "
                    f"{max_calls} calls per {time_window} seconds"
                )
            
            # 记录当前调用
            calls.append(now)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def timeout(seconds: int):
    """任务超时装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"任务 {func.__name__} 执行超时 ({seconds}秒)")
            
            # 设置信号处理器
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            
            try:
                return func(*args, **kwargs)
            finally:
                # 恢复原来的信号处理器
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        
        return wrapper
    return decorator

def log_execution(logger=None):
    """任务执行日志装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = logger or get_logger()
            task_name = func.__name__
            
            log.info(f"开始执行任务: {task_name}")
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                
                duration = (datetime.now() - start_time).total_seconds()
                log.info(f"任务 {task_name} 执行成功，耗时: {duration:.2f}秒")
                
                return result
                
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                log.error(f"任务 {task_name} 执行失败，耗时: {duration:.2f}秒，错误: {e}")
                raise
        
        return wrapper
    return decorator
```

### 2. 使用装饰器的任务示例

```python
# scheduler/tasks/enhanced_task.py
from ..decorators.task_decorators import monitor_task, rate_limit, timeout, log_execution
from log.logHelper import get_logger

@monitor_task("enhanced_data_process")
@rate_limit(max_calls=5, time_window=60)  # 每分钟最多5次
@timeout(300)  # 5分钟超时
@log_execution()
def run():
    """增强的任务示例"""
    logger = get_logger()
    
    logger.info("开始处理数据...")
    
    # 模拟耗时操作
    import time
    time.sleep(2)
    
    # 实际业务逻辑
    result = {
        "processed_records": 1000,
        "status": "success",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(f"数据处理完成: {result}")
    return result
```

## 配置管理

### 1. 环境配置

```yaml
# env.yaml
scheduler:
  timezone: "Asia/Shanghai"
  executors:
    default_threads: 20
    process_pool: 5
  job_defaults:
    coalesce: false
    max_instances: 3
    misfire_grace_time: 30
```

### 2. 任务配置

```yaml
# config/dev.yaml
tasks:
  # 数据同步任务
  data_sync:
    trigger: interval
    args:
      minutes: 30
    max_attempts: 3
    retry_delay: 10
    executor: default
    
  # 每日报告任务
  daily_report:
    trigger: cron
    args:
      hour: 9
      minute: 0
      day_of_week: "mon-fri"
    max_attempts: 5
    retry_delay: 30
    executor: processpool
    
  # 系统清理任务
  system_cleanup:
    trigger: cron
    args:
      hour: 2
      minute: 0
    max_attempts: 2
    retry_delay: 60
    
  # 监控检查任务
  health_check:
    trigger: interval
    args:
      seconds: 30
    max_attempts: 1
    retry_delay: 0
```

## 监控和管理

### 1. 任务状态监控

```python
# 获取任务状态API
from fastapi import APIRouter
from scheduler.scheduler_center import scheduler_center

router = APIRouter()

@router.get("/scheduler/status")
async def get_scheduler_status():
    """获取调度器状态"""
    return {
        "is_running": scheduler_center.is_running,
        "jobs_count": len(scheduler_center.get_jobs()),
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            }
            for job in scheduler_center.get_jobs()
        ]
    }

@router.post("/scheduler/jobs/{job_id}/pause")
async def pause_job(job_id: str):
    """暂停任务"""
    scheduler_center.pause_job(job_id)
    return {"message": f"任务 {job_id} 已暂停"}

@router.post("/scheduler/jobs/{job_id}/resume")
async def resume_job(job_id: str):
    """恢复任务"""
    scheduler_center.resume_job(job_id)
    return {"message": f"任务 {job_id} 已恢复"}
```

### 2. Prometheus指标

```python
# 暴露调度器指标
from prometheus_client import Info, Enum

scheduler_info = Info('scheduler_info', 'Scheduler information')
scheduler_state = Enum('scheduler_state', 'Scheduler state', 
                      states=['stopped', 'running', 'paused'])

# 更新指标
def update_scheduler_metrics():
    scheduler_info.info({
        'version': '1.0.0',
        'timezone': 'Asia/Shanghai',
        'jobs_count': str(len(scheduler_center.get_jobs()))
    })
    
    if scheduler_center.is_running:
        scheduler_state.state('running')
    else:
        scheduler_state.state('stopped')
```

## 最佳实践

### 1. 任务设计原则

```python
# 好的任务设计
class GoodTask(BaseTask):
    def execute(self):
        # 1. 幂等性：重复执行产生相同结果
        # 2. 原子性：要么全部成功，要么全部失败
        # 3. 状态检查：检查前置条件
        # 4. 进度跟踪：记录执行进度
        # 5. 资源清理：确保资源正确释放
        pass
```

### 2. 错误处理策略

```python
def robust_task():
    """健壮的任务处理"""
    try:
        # 主要业务逻辑
        result = main_business_logic()
        
        # 验证结果
        if not validate_result(result):
            raise ValueError("结果验证失败")
        
        return result
        
    except RetryableError as e:
        # 可重试的错误
        logger.warning(f"可重试错误: {e}")
        raise  # 让调度器重试
        
    except FatalError as e:
        # 致命错误，不要重试
        logger.error(f"致命错误: {e}")
        send_alert(e)  # 发送告警
        return None  # 不抛出异常，避免重试
        
    except Exception as e:
        # 未知错误
        logger.error(f"未知错误: {e}")
        raise  # 重新抛出，让调度器决定
```

### 3. 性能优化

```python
# 批处理优化
def batch_processing_task():
    """批处理任务优化"""
    batch_size = 100
    total_processed = 0
    
    while True:
        # 分批获取数据
        batch_data = get_batch_data(batch_size, offset=total_processed)
        
        if not batch_data:
            break
        
        # 批量处理
        process_batch(batch_data)
        total_processed += len(batch_data)
        
        # 定期检查是否需要停止
        if should_stop():
            logger.info(f"任务被请求停止，已处理 {total_processed} 条记录")
            break
    
    return {"total_processed": total_processed}
```

### 4. 资源管理

```python
class ResourceManagedTask(BaseTask):
    """资源管理任务示例"""
    
    def __init__(self):
        super().__init__()
        self.db_connection = None
        self.file_handles = []
    
    def execute(self):
        try:
            # 获取资源
            self.db_connection = get_db_connection()
            
            # 执行业务逻辑
            return self._do_work()
            
        finally:
            # 确保资源清理
            self.cleanup()
    
    def cleanup(self):
        """资源清理"""
        if self.db_connection:
            self.db_connection.close()
            
        for handle in self.file_handles:
            try:
                handle.close()
            except:
                pass
```

## 故障排除

### 常见问题

1. **任务不执行**
   ```python
   # 检查任务是否正确加载
   jobs = scheduler_center.get_jobs()
   print([job.id for job in jobs])
   
   # 检查触发器配置
   for job in jobs:
       print(f"{job.id}: {job.trigger}")
   ```

2. **任务重复执行**
   ```yaml
   # 设置coalesce防止任务堆积
   job_defaults:
     coalesce: true
     max_instances: 1
   ```

3. **内存泄漏**
   ```python
   # 在任务中注意资源清理
   def memory_safe_task():
       try:
           large_data = load_large_data()
           process_data(large_data)
       finally:
           # 显式删除大对象
           del large_data
           import gc
           gc.collect()
   ```

4. **死锁问题**
   ```python
   # 使用锁时注意顺序
   import threading
   
   lock1 = threading.Lock()
   lock2 = threading.Lock()
   
   def safe_task():
       # 总是按相同顺序获取锁
       with lock1:
           with lock2:
               # 执行需要同步的操作
               pass
   ```

通过合理使用任务调度系统，可以实现复杂的定时任务管理，提高系统的自动化程度和可靠性。关键是要根据业务需求设计合适的任务结构和调度策略。