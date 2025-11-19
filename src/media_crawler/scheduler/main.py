"""
任务调度主模块

提供任务调度管理器的统一接口
"""

from .scheduler_center import SchedulerCenter

# 创建调度管理器别名，与测试期望的名称一致
SchedulerManager = SchedulerCenter

# 创建默认实例
default_scheduler = SchedulerCenter()

def get_scheduler():
    """获取默认调度器实例"""
    return default_scheduler

def create_scheduler():
    """创建新的调度器实例"""
    return SchedulerCenter()

# 导出主要类和函数
__all__ = ['SchedulerManager', 'SchedulerCenter', 'default_scheduler', 'get_scheduler', 'create_scheduler']