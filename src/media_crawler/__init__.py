"""
pythonProjectTemplate 主包

对外提供常用的入口和工具, 如全局配置、日志和 FastAPI 应用工厂。
"""

from .config.config import config
from .log.logHelper import get_logger
from .api.main import create_application

__all__ = ["config", "get_logger", "create_application"]
