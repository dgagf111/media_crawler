"""
pythonProjectTemplate 主包

对外提供常用的入口和工具, 如全局配置、日志和 FastAPI 应用工厂。
"""
import sys

# 兼容旧的 pythonprojecttemplate 导入路径
sys.modules.setdefault("pythonprojecttemplate", sys.modules[__name__])

__all__ = ["config", "get_logger", "create_application"]


def __getattr__(name):
    if name == "config":
        from .config.config import config as _config

        return _config
    if name == "get_logger":
        from .log.logHelper import get_logger as _get_logger

        return _get_logger
    if name == "create_application":
        from .api.main import create_application as _create_application

        return _create_application
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
