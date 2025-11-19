"""
兼容层: 为旧的 `pythonprojecttemplate.core.config` 导入路径提供支持,
直接复用新的配置实现。
"""

from pythonprojecttemplate.config.config import Config, config  # noqa: F401

__all__ = ["Config", "config"]
