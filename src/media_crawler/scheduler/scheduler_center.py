import sys
import os
import threading
import signal
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore

# 添加项目根目录到Python路径，确保可以导入其他模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from pythonprojecttemplate.config.config import config
from pythonprojecttemplate.log.logHelper import get_logger
import importlib
import time

logger = get_logger()

def retry_decorator(max_attempts, delay):
    """
    重试装饰器：用于包装任务函数，提供自动重试功能。

    :param max_attempts: 最大重试次数
    :param delay: 重试之间的延迟时间（秒）
    :return: 装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"任务执行失败 (尝试 {attempts}/{max_attempts}): {str(e)}")
                    if attempts < max_attempts:
                        logger.info(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)
                    else:
                        logger.error(f"任务在 {max_attempts} 次尝试后仍然失败")
                        raise
        return wrapper
    return decorator

class SchedulerCenter:
    """
    调度中心类：管理和执行定时任务。
    """

    def __init__(self):
        """
        初始化调度中心。
        从配置文件加载调度器配置和任务配置。
        """
        self.scheduler = None
        self.config = config.get_scheduler_config()
        self.tasks_config = config.get_tasks_config()
        self._is_running = False

    @property
    def is_running(self):
        """检查调度器是否正在运行"""
        return self._is_running and self.scheduler and self.scheduler.running

    def initialize(self):
        """
        初始化调度器。
        设置作业存储、执行器和默认作业配置。
        """
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(self.config['executors']['default_threads']),
            'processpool': ProcessPoolExecutor(self.config['executors']['process_pool'])
        }
        job_defaults = {
            'coalesce': self.config['job_defaults']['coalesce'],
            'max_instances': self.config['job_defaults']['max_instances']
        }

        self.scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults
        )

    def add_task_from_config(self, task_name, task_config):
        """
        从配置添加任务到调度器。

        :param task_name: 任务名称
        :param task_config: 任务配置
        """
        return self._add_job_from_config(task_name, task_config)

    def add_job(self, func=None, trigger=None, id=None, **kwargs):
        """
        通用的添加任务方法，支持直接传入函数和触发器参数
        
        :param func: 要执行的函数
        :param trigger: 触发器类型
        :param id: 任务ID
        :param kwargs: 其他参数
        """
        if func is None:
            # 使用原有的任务配置方式
            return self._add_job_from_config(kwargs.get('task_name'), kwargs.get('task_config'))
        else:
            # 直接添加函数任务
            if self.scheduler is None:
                self.initialize()
            return self.scheduler.add_job(func, trigger=trigger, id=id, **kwargs)

    def _add_job_from_config(self, task_name, task_config):
        """从配置添加任务的内部方法"""
        try:
            # 动态导入任务模块
            module = importlib.import_module(f'pythonprojecttemplate.scheduler.tasks.{task_name}')
            job_func = getattr(module, 'run')

            # 应用重试装饰器
            max_attempts = task_config.get('max_attempts', 3)
            delay = task_config.get('retry_delay', 1)
            job_func_with_retry = retry_decorator(max_attempts, delay)(job_func)

            # 使用线程包装任务函数，确保任务在单独的线程中执行
            def wrapper():
                thread = threading.Thread(target=job_func_with_retry)
                thread.start()

            # 添加任务到调度器
            job = self.scheduler.add_job(
                wrapper,
                trigger=task_config['trigger'],
                **task_config['args'],
                id=task_name
            )
            logger.info(f"添加任务成功: {task_name}")
            return job
        except Exception as e:
            logger.error(f"添加任务失败: {task_name}, 错误: {str(e)}")
            return None

    def start(self):
        """
        启动调度中心。
        初始化调度器，添加所有配置的任务，并启动调度器。
        """
        self.initialize()
        logger.info("初始化调度器完成")
        for task_name, task_config in self.tasks_config.items():
            self.add_task_from_config(task_name, task_config)
        logger.info(f"已添加 {len(self.tasks_config)} 个任务")
        self.scheduler.start()
        self._is_running = True
        logger.info("调度器已启动")
        self.print_jobs()

    def shutdown(self, wait=True):
        """
        关闭调度中心。
        停止调度器并释放资源。
        
        :param wait: 是否等待任务完成（默认True）
        """
        logger.info("正在关闭调度器...")
        if self.scheduler and self.scheduler.running:
            try:
                self.scheduler.shutdown(wait=wait)
            except Exception as e:
                logger.error(f"关闭调度器时发生错误: {e}")
        self._is_running = False
        logger.info("调度器已关闭")

    def print_jobs(self):
        """
        打印当前调度的所有任务信息。
        """
        logger.info("当前调度的任务:")
        for job in self.scheduler.get_jobs():
            logger.info(f"- {job.id}: 下次运行时间 {job.next_run_time}")

    def get_jobs(self):
        """获取所有任务"""
        if self.scheduler:
            return self.scheduler.get_jobs()
        return []

    def pause_job(self, job_id):
        """暂停任务"""
        if self.scheduler:
            self.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        """恢复任务"""
        if self.scheduler:
            self.scheduler.resume_job(job_id)

    def remove_job(self, job_id):
        """移除任务"""
        if self.scheduler:
            self.scheduler.remove_job(job_id)

    def _wrap_task_with_retry(self, func, retry_config):
        """包装任务函数以支持重试机制"""
        max_attempts = retry_config.get('max_attempts', 3)
        retry_delay = retry_config.get('retry_delay', 1)
        return retry_decorator(max_attempts, retry_delay)(func)

# 创建调度中心实例
scheduler_center = SchedulerCenter()

def signal_handler(signum, frame):
    """
    信号处理函数：用于处理中断信号，确保调度器正常关闭。
    """
    logger.info("接收到关闭信号，正在关闭调度器...")
    scheduler_center.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # 启动调度中心
        scheduler_center.start()
        
        # 使用 signal.pause() 保持主程序运行，等待信号
        signal.pause()
    except (KeyboardInterrupt, SystemExit):
        pass
