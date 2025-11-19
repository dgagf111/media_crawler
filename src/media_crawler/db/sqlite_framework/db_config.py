"""
SQLite数据库配置模块
管理所有数据库相关的配置信息
"""

import os
from pathlib import Path

# 数据库目录路径
DB_DIR = Path(__file__).parent / "data"
DB_DIR.mkdir(exist_ok=True)

# 数据库文件路径
DB_FILE = DB_DIR / "app.db"

# 数据库连接配置
DB_CONFIG = {
    "database": str(DB_FILE),
    "timeout": 30.0,  # 连接超时时间（秒）
    "check_same_thread": False,  # 允许多线程访问
    "isolation_level": None,  # 自动提交模式
}

# SQL文件路径
SQL_SCHEMA_FILE = DB_DIR / "sql_schema.sql"
SQL_DATA_FILE = DB_DIR / "sql_data.sql"

# 日志配置
LOG_QUERIES = True  # 是否记录SQL查询日志
LOG_FILE = DB_DIR / "db.log"


def get_db_path():
    """获取数据库文件路径"""
    return str(DB_FILE)


def get_sql_schema_path():
    """获取SQL架构文件路径"""
    return str(SQL_SCHEMA_FILE)


def get_sql_data_path():
    """获取SQL数据文件路径"""
    return str(SQL_DATA_FILE)


def ensure_db_directory():
    """确保数据库目录存在"""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return str(DB_DIR)
