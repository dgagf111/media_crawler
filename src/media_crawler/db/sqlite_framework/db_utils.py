"""
SQLite数据库操作工具函数
提供函数式API，无需类包装，易用易维护
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path

import db_config

# 配置日志
if db_config.LOG_QUERIES:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(db_config.LOG_FILE), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
else:
    logger = None


def log_query(sql: str, params: Optional[Tuple] = None):
    """记录SQL查询日志"""
    if logger:
        logger.info(f"SQL: {sql}")
        if params:
            logger.info(f"Params: {params}")


def get_connection() -> sqlite3.Connection:
    """
    获取数据库连接
    Returns:
        sqlite3.Connection: 数据库连接对象
    """
    db_config.ensure_db_directory()
    conn = sqlite3.connect(**db_config.DB_CONFIG)

    # 启用外键约束
    conn.execute("PRAGMA foreign_keys = ON")

    # 配置连接参数
    conn.row_factory = sqlite3.Row  # 返回字典样式的行

    return conn


@contextmanager
def get_db_connection():
    """
    数据库连接上下文管理器
    自动处理连接的打开和关闭
    Usage:
        with get_db_connection() as conn:
            # 使用连接执行操作
            pass
    """
    conn = get_connection()
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def execute_query(
    conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None
) -> sqlite3.Cursor:
    """
    执行SQL查询（INSERT, UPDATE, DELETE等）
    Args:
        conn: 数据库连接
        sql: SQL语句
        params: 参数元组
    Returns:
        sqlite3.Cursor: 游标对象
    """
    log_query(sql, params)
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    return cursor


def execute_query_many(
    conn: sqlite3.Connection, sql: str, params_list: List[Tuple]
) -> sqlite3.Cursor:
    """
    批量执行SQL查询
    Args:
        conn: 数据库连接
        sql: SQL语句
        params_list: 参数列表
    Returns:
        sqlite3.Cursor: 游标对象
    """
    log_query(sql, f"BATCH: {len(params_list)} items")
    cursor = conn.cursor()
    cursor.executemany(sql, params_list)
    return cursor


def fetch_all(
    conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None
) -> List[Dict[str, Any]]:
    """
    获取所有查询结果
    Args:
        conn: 数据库连接
        sql: SQL语句
        params: 参数元组
    Returns:
        List[Dict]: 查询结果列表
    """
    log_query(sql, params)
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    return [dict(row) for row in cursor.fetchall()]


def fetch_one(
    conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None
) -> Optional[Dict[str, Any]]:
    """
    获取单个查询结果
    Args:
        conn: 数据库连接
        sql: SQL语句
        params: 参数元组
    Returns:
        Optional[Dict]: 查询结果字典，如果没有结果则返回None
    """
    log_query(sql, params)
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    row = cursor.fetchone()
    return dict(row) if row else None


def fetch_value(
    conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None
) -> Any:
    """
    获取单个值
    Args:
        conn: 数据库连接
        sql: SQL语句
        params: 参数元组
    Returns:
        Any: 查询结果值
    """
    log_query(sql, params)
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    row = cursor.fetchone()
    return row[0] if row else None


def insert_record(conn: sqlite3.Connection, table: str, data: Dict[str, Any]) -> int:
    """
    插入单条记录
    Args:
        conn: 数据库连接
        table: 表名
        data: 数据字典
    Returns:
        int: 插入记录的ID
    """
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    params = tuple(data.values())

    cursor = execute_query(conn, sql, params)
    return cursor.lastrowid


def insert_records(
    conn: sqlite3.Connection, table: str, data_list: List[Dict[str, Any]]
) -> List[int]:
    """
    批量插入记录
    Args:
        conn: 数据库连接
        table: 表名
        data_list: 数据字典列表
    Returns:
        List[int]: 插入记录的ID列表
    """
    if not data_list:
        return []

    columns = ", ".join(data_list[0].keys())
    placeholders = ", ".join(["?" for _ in data_list[0]])
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    params_list = [tuple(data.values()) for data in data_list]

    cursor = execute_query_many(conn, sql, params_list)

    # 获取最后一个插入的ID
    last_row_id = fetch_value(conn, "SELECT last_insert_rowid()")

    if last_row_id is None:
        # 如果无法获取最后一个ID，返回空列表
        return []

    # 计算插入的ID列表
    first_id = last_row_id - len(data_list) + 1
    return list(range(first_id, last_row_id + 1))


def update_record(
    conn: sqlite3.Connection,
    table: str,
    data: Dict[str, Any],
    where_clause: str,
    where_params: Tuple,
) -> int:
    """
    更新记录
    Args:
        conn: 数据库连接
        table: 表名
        data: 要更新的数据
        where_clause: WHERE条件
        where_params: WHERE参数
    Returns:
        int: 受影响的行数
    """
    set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    params = tuple(data.values()) + where_params

    cursor = execute_query(conn, sql, params)
    return cursor.rowcount


def delete_record(
    conn: sqlite3.Connection, table: str, where_clause: str, where_params: Tuple
) -> int:
    """
    删除记录
    Args:
        conn: 数据库连接
        table: 表名
        where_clause: WHERE条件
        where_params: WHERE参数
    Returns:
        int: 受影响的行数
    """
    sql = f"DELETE FROM {table} WHERE {where_clause}"
    cursor = execute_query(conn, sql, where_params)
    return cursor.rowcount


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """
    检查表是否存在
    Args:
        conn: 数据库连接
        table_name: 表名
    Returns:
        bool: 表是否存在
    """
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    result = fetch_one(conn, sql, (table_name,))
    return result is not None


def get_table_info(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    获取表结构信息
    Args:
        conn: 数据库连接
        table_name: 表名
    Returns:
        List[Dict]: 表结构信息列表
    """
    sql = f"PRAGMA table_info({table_name})"
    return fetch_all(conn, sql)


def execute_sql_file(conn: sqlite3.Connection, file_path: str) -> None:
    """
    执行SQL文件
    Args:
        conn: 数据库连接
        file_path: SQL文件路径
    """
    with open(file_path, "r", encoding="utf-8") as file:
        sql_content = file.read()

    # 分割SQL语句（以分号分隔）
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

    for statement in statements:
        if statement:
            execute_query(conn, statement)


def begin_transaction(conn: sqlite3.Connection) -> None:
    """开始事务"""
    conn.execute("BEGIN")


def commit_transaction(conn: sqlite3.Connection) -> None:
    """提交事务"""
    conn.commit()


def rollback_transaction(conn: sqlite3.Connection) -> None:
    """回滚事务"""
    conn.rollback()


@contextmanager
def transaction(conn: sqlite3.Connection):
    """
    事务上下文管理器
    Usage:
        with transaction(conn):
            # 执行多个数据库操作
            pass
    """
    begin_transaction(conn)
    try:
        yield
        commit_transaction(conn)
    except Exception as e:
        rollback_transaction(conn)
        raise e


def backup_database(source_path: str, backup_path: str) -> None:
    """
    备份数据库
    Args:
        source_path: 源数据库路径
        backup_path: 备份数据库路径
    """
    source_conn = sqlite3.connect(source_path)
    backup_conn = sqlite3.connect(backup_path)

    with backup_conn:
        source_conn.backup(backup_conn)

    source_conn.close()
    backup_conn.close()


def get_database_stats(conn: sqlite3.Connection) -> Dict[str, Any]:
    """
    获取数据库统计信息
    Args:
        conn: 数据库连接
    Returns:
        Dict: 数据库统计信息
    """
    stats = {}

    # 获取表列表
    tables = fetch_all(conn, "SELECT name FROM sqlite_master WHERE type='table'")
    stats["tables"] = [table["name"] for table in tables]

    # 获取每个表的记录数
    stats["table_counts"] = {}
    for table in stats["tables"]:
        count = fetch_value(conn, f"SELECT COUNT(*) FROM {table}")
        stats["table_counts"][table] = count

    # 获取数据库大小
    db_path = Path(db_config.get_db_path())
    if db_path.exists():
        stats["size_bytes"] = db_path.stat().st_size
        stats["size_mb"] = round(stats["size_bytes"] / (1024 * 1024), 2)

    return stats
