import logging
import os
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler

from pythonprojecttemplate.config.settings import settings

__all__ = ['get_logger']

"""
LogHelper 类：日志辅助工具

这个类提供了一个集中的日志管理解决方案，具有以下特点：
1. 单例模式：确保整个应用程序中只有一个日志实例，避免资源浪费和日志混乱。
2. 配置灵活：支持从配置文件加载设置，也可以通过参数自定义。
3. 双重输出：同时支持控制台和文件日志输出。
4. 文件日志管理：
   - 按日期自动组织日志文件（年/月/日）。
   - 支持日志文件大小限制和备份。
5. 日志级别控制：支持设置全局日志级别。
6. 简单API：提供常用的日志方法（debug, info, warning, error, critical）。

使用方法：
1. 获取日志实例：
   logger = get_logger()

2. 记录日志：
   logger.info("这是一条信息日志")
   logger.error("这是一条错误日志")

3. 自定义配置（可选）：
   custom_logger = LogHelper(project_name="MyProject", log_level="DEBUG")

注意：
- 首次使用时会自动初始化并加载配置。
- 日志文件默认保存在 '../log' 目录下，可通过配置文件或初始化参数修改。
- 默认的日志级别是 INFO，可以通过配置文件或初始化参数修改。
"""

class LogHelper:
    """
    日志辅助类，用于创建和管理日志实例。
    使用单例模式确保全局只有一个日志实例。
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, project_name=None, base_log_directory=None, log_level=None, max_bytes=10*1024*1024, backup_count=5):
        """
        初始化日志辅助类。
        
        :param project_name: 项目名称，用于日志文件夹命名
        :param base_log_directory: 基础日志目录
        :param log_level: 日志级别
        :param max_bytes: 单个日志文件的最大字节数
        :param backup_count: 保留的日志文件数量
        """
        if not hasattr(self, 'initialized'):
            self.load_config(project_name, base_log_directory, log_level)
            self.max_bytes = max_bytes
            self.backup_count = backup_count
            self.logger = logging.getLogger(self.project_name)
            # 确保日志级别设置为 DEBUG
            self.logger.setLevel(logging.DEBUG)
            self.setup_handlers()
            self.initialized = True

    def load_config(self, project_name=None, base_log_directory=None, log_level=None):
        """
        从配置文件加载日志配置。
        如果传入参数，则优先使用传入的参数。
        """
        log_config = settings.logging
        self.project_name = project_name or log_config.project_name
        self.base_log_directory = base_log_directory or log_config.base_log_directory
        log_level_str = (log_level or log_config.log_level).upper()
        # 确保默认日志级别为 DEBUG
        self.log_level = getattr(logging, log_level_str, logging.DEBUG)

    def setup_handlers(self):
        """
        设置日志处理器，包括控制台输出和文件输出。
        """
        # 设置控制台处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)  # 确保控制台处理器也设置为 DEBUG 级别
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 设置文件处理器
        try:
            self.create_log_file_handler()
        except Exception as e:
            print(f"Error creating log file handler: {e}")

    def create_log_file_handler(self):
        """
        创建文件日志处理器，支持按大小和时间轮转。
        """
        current_date = datetime.now()
        year, month, day = current_date.strftime('%Y'), current_date.strftime('%Y-%m'), current_date.strftime('%Y-%m-%d')
        
        month_dir = os.path.join(self.base_log_directory, self.project_name, year, month)
        os.makedirs(month_dir, exist_ok=True)
        
        log_file_path = os.path.join(month_dir, f'{day}.log')
        
        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=self.max_bytes, backupCount=self.backup_count
        )
        file_handler.setLevel(logging.DEBUG)  # 确保文件处理器也设置为 DEBUG 级别
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        
        self.logger.addHandler(file_handler)

    def debug(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', None)
        if exc_info:
            if isinstance(exc_info, BaseException):
                message += f"\n{traceback.format_exc()}"
            elif exc_info is True:
                message += f"\n{traceback.format_exc()}"
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', None)
        if exc_info:
            if isinstance(exc_info, BaseException):
                message += f"\n{traceback.format_exc()}"
            elif exc_info is True:
                message += f"\n{traceback.format_exc()}"
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', None)
        if exc_info:
            if isinstance(exc_info, BaseException):
                message += f"\n{traceback.format_exc()}"
            elif exc_info is True:
                message += f"\n{traceback.format_exc()}"
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', None)
        if exc_info:
            if isinstance(exc_info, BaseException):
                message += f"\n{traceback.format_exc()}"
            elif exc_info is True:
                message += f"\n{traceback.format_exc()}"
        self.logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        exc_info = kwargs.pop('exc_info', None)
        if exc_info:
            if isinstance(exc_info, BaseException):
                message += f"\n{traceback.format_exc()}"
            elif exc_info is True:
                message += f"\n{traceback.format_exc()}"
        self.logger.critical(message, *args, **kwargs)

def get_logger():
    """
    获取日志实例的全局方法。
    :return: LogHelper实例
    """
    return LogHelper()

if __name__ == '__main__':
    import shutil

    # 测试设置
    test_project_name = "TestProject"
    test_log_dir = "./test_logs"
    
    # 创建测试用的 logger，并明确设置日志级别为 DEBUG
    logger = LogHelper(project_name=test_project_name, base_log_directory=test_log_dir, log_level="DEBUG")

    # 测试日志创建
    logger.info("测试日志信息")
    current_date = datetime.now()
    year, month, day = current_date.strftime('%Y'), current_date.strftime('%Y-%m'), current_date.strftime('%Y-%m-%d')
    expected_log_path = os.path.join(test_log_dir, test_project_name, year, month, f"{day}.log")
    
    if os.path.exists(expected_log_path):
        print("测试通过：日志文件已成功创建")
    else:
        print("测试失败：日志文件未被创建")

    # 测试不同级别的日志
    test_messages = {
        "debug": "这是一条调试日志",
        "info": "这是一条信息日志",
        "warning": "这是一条警告日志",
        "error": "这是一条错误日志",
        "critical": "这是一条严重错误日志"
    }

    for level, message in test_messages.items():
        getattr(logger, level)(message)

    # 测试带异常信息的日志
    try:
        raise ValueError("测试异常")
    except ValueError as e:
        logger.error("发生了一个错误", exc_info=e)
        logger.critical("发生了一个严重错误", exc_info=True)

    # 测试带额外参数的日志
    extra_data = {"user": "测试用户", "action": "登录"}
    logger.info("用户操作", extra=extra_data)

    # 检查日志文件内容
    with open(expected_log_path, 'r', encoding='utf-8') as log_file:
        content = log_file.read()
        for message in test_messages.values():
            if message in content:
                print(f"测试通过：日志消息 '{message}' 已成功记录")
            else:
                print(f"测试失败：日志消息 '{message}' 未在日志文件中找到")
        
        if "ValueError: 测试异常" in content and "Traceback (most recent call last):" in content:
            print("测试通过：异常信息已成功记录")
        else:
            print("测试失败：异常信息未在日志文件中找到")
        
        if "用户操作" in content and "测试用户" in content and "登录" in content:
            print("测试通过：带额外参数的日志已成功记录")
        else:
            print("测试失败：带额外参数的日志未在日志文件中找到")

    # 测试单例模式
    logger1 = get_logger()
    logger2 = get_logger()
    if logger1 is logger2:
        print("测试通过：get_logger() 返回了相同的实例")
    else:
        print("测试失败：get_logger() 没有返回相同的实例")

    # 清理测试生成的日志文件和目录
    if os.path.exists(test_log_dir):
        shutil.rmtree(test_log_dir)
        print("测试日志目录已清理")

    print("所有测试完成")
