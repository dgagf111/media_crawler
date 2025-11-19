"""
SQLite工具函数集（修复版）
提供全面的SQLite数据库操作功能，采用函数式API设计
包含数据库初始化、CRUD操作、事务处理、批量操作、复杂查询、错误处理、备份恢复等功能

使用方法：
1. 导入该模块
2. 初始化数据库连接
3. 使用函数式API进行数据库操作
import sqlite_toolkit as stk

# 初始化配置
stk.init_db_config({
    "db_path": "my_app.db",
    "backup_dir": "backups"
})

# 初始化数据库
stk.initialize_database(schema_sql, data_sql)

# 基本CRUD操作
with stk.get_db_connection() as conn:
    # 插入记录
    user_id = stk.insert_record("users", {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    }, conn)

    # 查询记录
    user = stk.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,), conn)

    # 更新记录
    stk.update_record("users", {"age": 26}, "id = ?", (user_id,), conn)

    # 删除记录
    stk.delete_record("users", "id = ?", (user_id,), conn)

# 事务操作
with stk.get_db_connection() as conn:
    with stk.transaction(conn):
        # 在事务中执行多个操作
        order_id = stk.insert_record("orders", order_data, conn)
        stk.insert_records("order_items", order_items, conn)

# 复杂查询
result = stk.execute_query_with_pagination(
    "SELECT * FROM users WHERE age > ? ORDER BY name",
    (20,), page=1, page_size=10
)

# 数据库备份
backup_path = stk.backup_database("my_backup")
stk.restore_database(backup_path)

# 数据导出
stk.export_table_to_json("users", "users_backup.json")
"""

"""
这个SQLite工具函数集提供了全面的SQLite数据库操作功能，采用函数式API设计，不使用class包装。它包含了以下主要功能：

 数据库初始化和连接管理：
 init_db_config() - 初始化数据库配置
 get_db_config() - 获取当前数据库配置
 get_db_connection() - 获取数据库连接的上下文管理器
 initialize_database() - 初始化数据库
 reset_database() - 重置数据库（删除所有表和数据）
 destroy_database() - 销毁数据库（删除数据库文件）
 表操作：
 table_exists() - 检查表是否存在
 create_table() - 创建表
 drop_table() - 删除表
 get_table_info() - 获取表结构信息
 add_column() - 添加列
 数据操作 - CRUD：
 insert_record() - 插入单条记录
 insert_records() - 批量插入记录
 fetch_one() - 执行查询并返回单条记录
 fetch_all() - 执行查询并返回所有记录
 update_record() - 更新记录
 delete_record() - 删除记录
 事务处理：
 transaction() - 事务上下文管理器
 execute_in_transaction() - 在事务中执行多个操作
 复杂查询支持：
 execute_query_with_pagination() - 执行分页查询
 execute_join_query() - 执行多表连接查询
 execute_aggregate_query() - 执行聚合查询
 数据库统计信息：
 get_database_stats() - 获取数据库统计信息
 get_table_stats() - 获取表统计信息
 数据库备份和恢复：
 backup_database() - 备份数据库
 restore_database() - 从备份恢复数据库
 list_backups() - 列出所有备份
 delete_backup() - 删除备份
 日志和错误处理：
 log_error() - 记录错误日志
 log_query() - 记录查询日志
 clear_log() - 清空日志文件
 get_log_entries() - 获取日志条目
 数据导入导出：
 export_table_to_csv() - 导出表数据到CSV文件
 import_csv_to_table() - 从CSV文件导入数据到表
 export_table_to_json() - 导出表数据到JSON文件
 import_json_to_table() - 从JSON文件导入数据到表
 数据库优化：
 optimize_database() - 优化数据库
 create_index() - 创建索引
 drop_index() - 删除索引
 list_indexes() - 列出索引
 辅助函数：
 execute_sql_file() - 执行SQL文件
 execute_sql_script() - 执行SQL脚本
 get_table_names() - 获取所有表名
 get_view_names() - 获取所有视图名
 get_trigger_names() - 获取所有触发器名
 create_view() - 创建视图
 drop_view() - 删除视图
 create_trigger() - 创建触发器
 drop_trigger() - 删除触发器
"""

import os
import sqlite3
import shutil
import datetime
import json
from typing import Dict, List, Any, Optional, Union, Tuple, ContextManager
from contextlib import contextmanager

# ===== 配置部分 =====

# 默认数据库配置
DEFAULT_DB_CONFIG = {
    "db_path": "data/app.db",  # 数据库文件路径
    "log_path": "data/db.log",  # 日志文件路径
    "backup_dir": "data/backups",  # 备份目录
    "timeout": 30.0,  # 连接超时时间(秒)
    "check_same_thread": False,  # 是否允许跨线程访问
    "enable_foreign_keys": True,  # 是否启用外键约束
    "enable_wal": True,  # 是否启用WAL模式
}

# 全局配置变量
_db_config = DEFAULT_DB_CONFIG.copy()

# ===== 数据库初始化和连接管理 =====


def init_db_config(config: Dict[str, Any] = None) -> None:
    """
    初始化数据库配置
    参数:
        config: 配置字典，如果为None则使用默认配置
    返回值:
        None
    """
    global _db_config
    if config:
        _db_config.update(config)

    # 确保数据目录存在
    os.makedirs(os.path.dirname(_db_config["db_path"]), exist_ok=True)
    os.makedirs(_db_config["backup_dir"], exist_ok=True)


def get_db_config() -> Dict[str, Any]:
    """
    获取当前数据库配置
    返回值:
        数据库配置字典
    """
    return _db_config.copy()


@contextmanager
def get_db_connection(db_path: str = None) -> ContextManager[sqlite3.Connection]:
    """
    获取数据库连接的上下文管理器
    参数:
        db_path: 数据库文件路径，如果为None则使用配置中的路径
    返回值:
        数据库连接对象
    """
    if db_path is None:
        db_path = _db_config["db_path"]

    conn = None
    try:
        # 创建数据库连接
        conn = sqlite3.connect(
            db_path,
            timeout=_db_config["timeout"],
            check_same_thread=_db_config["check_same_thread"],
        )

        # 配置连接
        if _db_config["enable_foreign_keys"]:
            conn.execute("PRAGMA foreign_keys = ON")

        if _db_config["enable_wal"]:
            conn.execute("PRAGMA journal_mode = WAL")

        # 设置行工厂，使结果以字典形式返回
        conn.row_factory = sqlite3.Row

        yield conn

        # 提交事务
        conn.commit()
    except Exception as e:
        # 发生错误时回滚
        if conn:
            conn.rollback()
        raise e
    finally:
        # 关闭连接
        if conn:
            conn.close()


def initialize_database(schema_sql: str = None, data_sql: str = None) -> bool:
    """
    初始化数据库
    参数:
        schema_sql: 数据库架构SQL，如果为None则尝试从默认路径加载
        data_sql: 初始数据SQL，如果为None则尝试从默认路径加载
    返回值:
        bool: 初始化是否成功
    """
    try:
        with get_db_connection() as conn:
            # 检查数据库是否已初始化
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            if tables:
                # 数据库已存在表，跳过初始化
                return False

            # 执行架构SQL
            if schema_sql:
                conn.executescript(schema_sql)
            elif os.path.exists("data/sql_schema.sql"):
                with open("data/sql_schema.sql", "r", encoding="utf-8") as f:
                    conn.executescript(f.read())

            # 执行数据SQL
            if data_sql:
                conn.executescript(data_sql)
            elif os.path.exists("data/sql_data.sql"):
                with open("data/sql_data.sql", "r", encoding="utf-8") as f:
                    conn.executescript(f.read())

            return True
    except Exception as e:
        log_error(f"初始化数据库失败: {e}")
        return False


def reset_database() -> bool:
    """
    重置数据库（删除所有表和数据）
    返回值:
        bool: 重置是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()

            # 禁用外键约束
            cursor.execute("PRAGMA foreign_keys = OFF")

            # 删除所有表
            for table in tables:
                table_name = table[0]
                if table_name != "sqlite_sequence":  # 保留系统表
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

            # 重新启用外键约束
            cursor.execute("PRAGMA foreign_keys = ON")

            return True
    except Exception as e:
        log_error(f"重置数据库失败: {e}")
        return False


def destroy_database() -> bool:
    """
    销毁数据库（删除数据库文件）
    返回值:
        bool: 销毁是否成功
    """
    try:
        db_path = _db_config["db_path"]
        if os.path.exists(db_path):
            os.remove(db_path)
        return True
    except Exception as e:
        log_error(f"销毁数据库失败: {e}")
        return False


# ===== 表操作 =====


def table_exists(table_name: str, conn: sqlite3.Connection = None) -> bool:
    """
    检查表是否存在
    参数:
        table_name: 表名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 表是否存在
    """

    def _check_table_exists(conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return cursor.fetchone() is not None

    if conn:
        return _check_table_exists(conn)
    else:
        with get_db_connection() as conn:
            return _check_table_exists(conn)


def create_table(
    table_name: str,
    columns: Dict[str, str],
    primary_key: str = None,
    foreign_keys: Dict[str, Tuple[str, str]] = None,
    conn: sqlite3.Connection = None,
) -> bool:
    """
    创建表
    参数:
        table_name: 表名
        columns: 列定义字典 {列名: 列类型}
        primary_key: 主键列名
        foreign_keys: 外键定义 {列名: (引用表, 引用列)}
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 创建是否成功
    """

    def _create_table(conn):
        try:
            cursor = conn.cursor()

            # 构建列定义SQL
            column_defs = []
            for col_name, col_type in columns.items():
                if col_name == primary_key:
                    column_defs.append(f"{col_name} {col_type} PRIMARY KEY")
                else:
                    column_defs.append(f"{col_name} {col_type}")

            # 添加外键约束
            if foreign_keys:
                for col_name, (ref_table, ref_col) in foreign_keys.items():
                    column_defs.append(
                        f"FOREIGN KEY ({col_name}) REFERENCES {ref_table}({ref_col})"
                    )

            # 创建表
            create_sql = (
                f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)})"
            )
            cursor.execute(create_sql)

            return True
        except Exception as e:
            log_error(f"创建表 {table_name} 失败: {e}")
            return False

    if conn:
        return _create_table(conn)
    else:
        with get_db_connection() as conn:
            return _create_table(conn)


def drop_table(table_name: str, conn: sqlite3.Connection = None) -> bool:
    """
    删除表
    参数:
        table_name: 表名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 删除是否成功
    """

    def _drop_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            return True
        except Exception as e:
            log_error(f"删除表 {table_name} 失败: {e}")
            return False

    if conn:
        return _drop_table(conn)
    else:
        with get_db_connection() as conn:
            return _drop_table(conn)


def get_table_info(
    table_name: str, conn: sqlite3.Connection = None
) -> List[Dict[str, Any]]:
    """
    获取表结构信息
    参数:
        table_name: 表名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        表结构信息列表
    """

    def _get_table_info(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            # 转换为字典列表
            result = []
            for col in columns:
                result.append(
                    {
                        "cid": col[0],
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "primary_key": bool(col[5]),
                    }
                )

            return result
        except Exception as e:
            log_error(f"获取表 {table_name} 信息失败: {e}")
            return []

    if conn:
        return _get_table_info(conn)
    else:
        with get_db_connection() as conn:
            return _get_table_info(conn)


def add_column(
    table_name: str,
    column_name: str,
    column_type: str,
    default_value: Any = None,
    conn: sqlite3.Connection = None,
) -> bool:
    """
    添加列
    参数:
        table_name: 表名
        column_name: 列名
        column_type: 列类型
        default_value: 默认值
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 添加是否成功
    """

    def _add_column(conn):
        try:
            cursor = conn.cursor()

            # 构建添加列SQL
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"

            # 添加默认值
            if default_value is not None:
                if isinstance(default_value, str):
                    sql += f" DEFAULT '{default_value}'"
                elif isinstance(default_value, (int, float)):
                    sql += f" DEFAULT {default_value}"
                else:
                    sql += f" DEFAULT '{str(default_value)}'"

            cursor.execute(sql)
            return True
        except Exception as e:
            log_error(f"添加列 {column_name} 到表 {table_name} 失败: {e}")
            return False

    if conn:
        return _add_column(conn)
    else:
        with get_db_connection() as conn:
            return _add_column(conn)


# ===== 数据操作 - CRUD =====


def insert_record(
    table_name: str, data: Dict[str, Any], conn: sqlite3.Connection = None
) -> Optional[int]:
    """
    插入单条记录
    参数:
        table_name: 表名
        data: 数据字典 {列名: 值}
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        新记录的ID，如果失败则返回None
    """

    def _insert_record(conn):
        try:
            cursor = conn.cursor()

            # 构建SQL
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # 执行插入
            cursor.execute(sql, list(data.values()))

            # 返回新记录ID
            return cursor.lastrowid
        except Exception as e:
            # 不记录日志，让异常向上传播以便事务处理
            raise e

    if conn:
        return _insert_record(conn)
    else:
        with get_db_connection() as conn:
            return _insert_record(conn)


def insert_records(
    table_name: str, data_list: List[Dict[str, Any]], conn: sqlite3.Connection = None
) -> List[int]:
    """
    批量插入记录
    参数:
        table_name: 表名
        data_list: 数据字典列表
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        新记录ID列表
    """

    def _insert_records(conn):
        try:
            cursor = conn.cursor()

            # 获取所有列名
            all_columns = set()
            for data in data_list:
                all_columns.update(data.keys())
            all_columns = sorted(all_columns)

            # 构建SQL
            columns = ", ".join(all_columns)
            placeholders = ", ".join(["?"] * len(all_columns))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # 准备数据
            values_list = []
            for data in data_list:
                values = [data.get(col) for col in all_columns]
                values_list.append(values)

            # 执行批量插入
            cursor.executemany(sql, values_list)

            # 获取插入的ID范围
            # SQLite的executemany不返回lastrowid，需要查询获取
            if data_list:
                cursor.execute(f"SELECT last_insert_rowid()")
                last_id = cursor.fetchone()[0]
                first_id = last_id - len(data_list) + 1
                return list(range(first_id, last_id + 1))
            else:
                return []
        except Exception as e:
            log_error(f"批量插入记录到表 {table_name} 失败: {e}")
            return []

    if conn:
        return _insert_records(conn)
    else:
        with get_db_connection() as conn:
            return _insert_records(conn)


def fetch_one(
    query: str, params: Tuple = None, conn: sqlite3.Connection = None
) -> Optional[Dict[str, Any]]:
    """
    执行查询并返回单条记录
    参数:
        query: SQL查询语句
        params: 查询参数元组
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        记录字典，如果没有结果则返回None
    """

    def _fetch_one(conn):
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            log_error(f"执行查询失败: {e}, SQL: {query}")
            return None

    if conn:
        return _fetch_one(conn)
    else:
        with get_db_connection() as conn:
            return _fetch_one(conn)


def fetch_all(
    query: str, params: Tuple = None, conn: sqlite3.Connection = None
) -> List[Dict[str, Any]]:
    """
    执行查询并返回所有记录
    参数:
        query: SQL查询语句
        params: 查询参数元组
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        记录字典列表
    """

    def _fetch_all(conn):
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            log_error(f"执行查询失败: {e}, SQL: {query}")
            return []

    if conn:
        return _fetch_all(conn)
    else:
        with get_db_connection() as conn:
            return _fetch_all(conn)


def update_record(
    table_name: str,
    data: Dict[str, Any],
    where_clause: str,
    where_params: Tuple = None,
    conn: sqlite3.Connection = None,
) -> int:
    """
    更新记录
    参数:
        table_name: 表名
        data: 要更新的数据字典 {列名: 新值}
        where_clause: WHERE条件子句
        where_params: WHERE条件参数
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        受影响的行数
    """

    def _update_record(conn):
        try:
            cursor = conn.cursor()

            # 构建SET子句
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])

            # 构建完整SQL
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            # 合并参数
            params = list(data.values())
            if where_params:
                params.extend(where_params)

            # 执行更新
            cursor.execute(sql, params)

            # 返回受影响的行数
            return cursor.rowcount
        except Exception as e:
            log_error(f"更新表 {table_name} 记录失败: {e}")
            return 0

    if conn:
        return _update_record(conn)
    else:
        with get_db_connection() as conn:
            return _update_record(conn)


def delete_record(
    table_name: str,
    where_clause: str,
    where_params: Tuple = None,
    conn: sqlite3.Connection = None,
) -> int:
    """
    删除记录
    参数:
        table_name: 表名
        where_clause: WHERE条件子句
        where_params: WHERE条件参数
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        受影响的行数
    """

    def _delete_record(conn):
        try:
            cursor = conn.cursor()

            # 构建SQL
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"

            # 执行删除
            if where_params:
                cursor.execute(sql, where_params)
            else:
                cursor.execute(sql)

            # 返回受影响的行数
            return cursor.rowcount
        except Exception as e:
            log_error(f"删除表 {table_name} 记录失败: {e}")
            return 0

    if conn:
        return _delete_record(conn)
    else:
        with get_db_connection() as conn:
            return _delete_record(conn)


# ===== 事务处理 =====


@contextmanager
def transaction(conn: sqlite3.Connection) -> ContextManager[None]:
    """
    事务上下文管理器
    参数:
        conn: 数据库连接
    """
    try:
        # 开始事务
        conn.execute("BEGIN")
        yield
        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        raise e


def execute_in_transaction(operations: List[Tuple[str, Tuple]]) -> bool:
    """
    在事务中执行多个操作
    参数:
        operations: 操作列表，每个元素是(SQL语句, 参数)元组
    返回值:
        bool: 是否全部成功
    """
    try:
        with get_db_connection() as conn:
            with transaction(conn):
                cursor = conn.cursor()
                for sql, params in operations:
                    if params:
                        cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)
            return True
    except Exception as e:
        log_error(f"事务执行失败: {e}")
        return False


# ===== 复杂查询支持 =====


def execute_query_with_pagination(
    query: str,
    params: Tuple = None,
    page: int = 1,
    page_size: int = 10,
    conn: sqlite3.Connection = None,
) -> Dict[str, Any]:
    """
    执行分页查询
    参数:
        query: 基础查询语句(不包含LIMIT和OFFSET)
        params: 查询参数
        page: 页码(从1开始)
        page_size: 每页记录数
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        包含分页结果和统计信息的字典
    """

    def _execute_query_with_pagination(conn):
        try:
            cursor = conn.cursor()

            # 获取总记录数
            count_query = f"SELECT COUNT(*) FROM ({query})"
            if params:
                cursor.execute(count_query, params)
            else:
                cursor.execute(count_query)

            total_count = cursor.fetchone()[0]

            # 计算分页参数
            offset = (page - 1) * page_size
            total_pages = (total_count + page_size - 1) // page_size

            # 执行分页查询
            paginated_query = f"{query} LIMIT ? OFFSET ?"
            paginated_params = list(params) if params else []
            paginated_params.extend([page_size, offset])

            cursor.execute(paginated_query, paginated_params)
            rows = cursor.fetchall()

            return {
                "data": [dict(row) for row in rows],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_count": total_count,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1,
                },
            }
        except Exception as e:
            log_error(f"分页查询失败: {e}")
            return {"data": [], "pagination": {}}

    if conn:
        return _execute_query_with_pagination(conn)
    else:
        with get_db_connection() as conn:
            return _execute_query_with_pagination(conn)


def execute_join_query(
    tables: List[str],
    columns: List[str],
    join_conditions: List[str],
    where_clause: str = None,
    where_params: Tuple = None,
    order_by: str = None,
    limit: int = None,
    conn: sqlite3.Connection = None,
) -> List[Dict[str, Any]]:
    """
    执行多表连接查询
    参数:
        tables: 表名列表
        columns: 要查询的列名列表
        join_conditions: 连接条件列表
        where_clause: WHERE条件子句
        where_params: WHERE条件参数
        order_by: 排序子句
        limit: 限制返回记录数
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        查询结果列表
    """

    def _execute_join_query(conn):
        try:
            cursor = conn.cursor()

            # 构建SELECT子句
            select_clause = ", ".join(columns)

            # 构建FROM和JOIN子句
            from_clause = tables[0]
            for i in range(1, len(tables)):
                from_clause += f" JOIN {tables[i]} ON {join_conditions[i-1]}"

            # 构建完整SQL
            sql = f"SELECT {select_clause} FROM {from_clause}"

            # 添加WHERE子句
            if where_clause:
                sql += f" WHERE {where_clause}"

            # 添加ORDER BY子句
            if order_by:
                sql += f" ORDER BY {order_by}"

            # 添加LIMIT子句
            if limit:
                sql += f" LIMIT {limit}"

            # 执行查询
            if where_params:
                cursor.execute(sql, where_params)
            else:
                cursor.execute(sql)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            log_error(f"连接查询失败: {e}")
            return []

    if conn:
        return _execute_join_query(conn)
    else:
        with get_db_connection() as conn:
            return _execute_join_query(conn)


def execute_aggregate_query(
    table_name: str,
    group_by: str,
    aggregations: Dict[str, str],
    where_clause: str = None,
    where_params: Tuple = None,
    having_clause: str = None,
    having_params: Tuple = None,
    order_by: str = None,
    conn: sqlite3.Connection = None,
) -> List[Dict[str, Any]]:
    """
    执行聚合查询
    参数:
        table_name: 表名
        group_by: 分组列
        aggregations: 聚合函数字典 {别名: 聚合函数}
        where_clause: WHERE条件子句
        where_params: WHERE条件参数
        having_clause: HAVING条件子句
        having_params: HAVING条件参数
        order_by: 排序子句
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        聚合查询结果列表
    """

    def _execute_aggregate_query(conn):
        try:
            cursor = conn.cursor()

            # 构建SELECT子句
            select_items = [group_by]
            for alias, func in aggregations.items():
                select_items.append(f"{func} AS {alias}")
            select_clause = ", ".join(select_items)

            # 构建基础SQL
            sql = f"SELECT {select_clause} FROM {table_name} GROUP BY {group_by}"

            # 添加WHERE子句
            if where_clause:
                sql += f" WHERE {where_clause}"

            # 添加HAVING子句
            if having_clause:
                sql += f" HAVING {having_clause}"

            # 添加ORDER BY子句
            if order_by:
                sql += f" ORDER BY {order_by}"

            # 执行查询
            if where_params and having_params:
                cursor.execute(sql, where_params + having_params)
            elif where_params:
                cursor.execute(sql, where_params)
            elif having_params:
                cursor.execute(sql, having_params)
            else:
                cursor.execute(sql)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            log_error(f"聚合查询失败: {e}")
            return []

    if conn:
        return _execute_aggregate_query(conn)
    else:
        with get_db_connection() as conn:
            return _execute_aggregate_query(conn)


# ===== 数据库统计信息 =====


def get_database_stats(conn: sqlite3.Connection = None) -> Dict[str, Any]:
    """
    获取数据库统计信息
    参数:
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        数据库统计信息字典
    """

    def _get_database_stats(conn):
        try:
            cursor = conn.cursor()

            # 获取数据库文件大小
            db_path = _db_config["db_path"]
            size_mb = 0
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                size_mb = size_bytes / (1024 * 1024)

            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            # 获取每个表的记录数
            table_counts = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                table_counts[table] = count

            # 获取数据库版本信息
            cursor.execute("SELECT sqlite_version()")
            sqlite_version = cursor.fetchone()[0]

            return {
                "size_mb": round(size_mb, 2),
                "table_counts": table_counts,
                "sqlite_version": sqlite_version,
                "tables": tables,
            }
        except Exception as e:
            log_error(f"获取数据库统计信息失败: {e}")
            return {}

    if conn:
        return _get_database_stats(conn)
    else:
        with get_db_connection() as conn:
            return _get_database_stats(conn)


def get_table_stats(table_name: str, conn: sqlite3.Connection = None) -> Dict[str, Any]:
    """
    获取表统计信息
    参数:
        table_name: 表名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        表统计信息字典
    """

    def _get_table_stats(conn):
        try:
            cursor = conn.cursor()

            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            # 获取记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            record_count = cursor.fetchone()[0]

            # 获取索引信息
            cursor.execute(f"PRAGMA index_list({table_name})")
            indexes = cursor.fetchall()

            # 获取外键信息
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            foreign_keys = cursor.fetchall()

            return {
                "name": table_name,
                "columns": [dict(col) for col in columns],
                "record_count": record_count,
                "indexes": [dict(idx) for idx in indexes],
                "foreign_keys": [dict(fk) for fk in foreign_keys],
            }
        except Exception as e:
            log_error(f"获取表 {table_name} 统计信息失败: {e}")
            return {}

    if conn:
        return _get_table_stats(conn)
    else:
        with get_db_connection() as conn:
            return _get_table_stats(conn)


# ===== 数据库备份和恢复 =====


def backup_database(backup_name: str = None) -> Optional[str]:
    """
    备份数据库
    参数:
        backup_name: 备份名称，如果为None则使用时间戳
    返回值:
        备份文件路径，如果失败则返回None
    """
    try:
        # 生成备份文件名
        if not backup_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"db_backup_{timestamp}"

        backup_path = os.path.join(_db_config["backup_dir"], f"{backup_name}.db")

        # 确保备份目录存在
        os.makedirs(_db_config["backup_dir"], exist_ok=True)

        # 复制数据库文件
        shutil.copy2(_db_config["db_path"], backup_path)

        return backup_path
    except Exception as e:
        log_error(f"备份数据库失败: {e}")
        return None


def restore_database(backup_path: str) -> bool:
    """
    从备份恢复数据库
    参数:
        backup_path: 备份文件路径
    返回值:
        bool: 恢复是否成功
    """
    try:
        # 检查备份文件是否存在
        if not os.path.exists(backup_path):
            log_error(f"备份文件不存在: {backup_path}")
            return False

        # 关闭所有数据库连接
        # 注意: 在实际应用中，可能需要更复杂的连接管理

        # 恢复数据库文件
        shutil.copy2(backup_path, _db_config["db_path"])

        return True
    except Exception as e:
        log_error(f"恢复数据库失败: {e}")
        return False


def list_backups() -> List[Dict[str, Any]]:
    """
    列出所有备份
    返回值:
        备份信息列表
    """
    try:
        backups = []
        backup_dir = _db_config["backup_dir"]

        if not os.path.exists(backup_dir):
            return backups

        for filename in os.listdir(backup_dir):
            if filename.endswith(".db"):
                filepath = os.path.join(backup_dir, filename)
                stat = os.stat(filepath)

                backups.append(
                    {
                        "name": filename[:-3],  # 去掉.db后缀
                        "path": filepath,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "created_time": datetime.datetime.fromtimestamp(
                            stat.st_ctime
                        ).isoformat(),
                        "modified_time": datetime.datetime.fromtimestamp(
                            stat.st_mtime
                        ).isoformat(),
                    }
                )

        # 按创建时间降序排序
        backups.sort(key=lambda x: x["created_time"], reverse=True)

        return backups
    except Exception as e:
        log_error(f"列出备份失败: {e}")
        return []


def delete_backup(backup_name: str) -> bool:
    """
    删除备份
    参数:
        backup_name: 备份名称
    返回值:
        bool: 删除是否成功
    """
    try:
        backup_path = os.path.join(_db_config["backup_dir"], f"{backup_name}.db")

        if not os.path.exists(backup_path):
            log_error(f"备份不存在: {backup_name}")
            return False

        os.remove(backup_path)
        return True
    except Exception as e:
        log_error(f"删除备份失败: {e}")
        return False


# ===== 日志和错误处理 =====


def log_error(message: str) -> None:
    """
    记录错误日志
    参数:
        message: 错误消息
    """
    try:
        log_path = _db_config["log_path"]
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] ERROR: {message}\n")
    except Exception:
        # 如果日志记录失败，忽略错误以避免无限循环
        pass


def log_query(query: str, params: Tuple = None, execution_time: float = None) -> None:
    """
    记录查询日志
    参数:
        query: SQL查询语句
        params: 查询参数
        execution_time: 执行时间(毫秒)
    """
    try:
        log_path = _db_config["log_path"]
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] QUERY: {query}\n")
            if params:
                f.write(f"[{timestamp}] PARAMS: {params}\n")
            if execution_time:
                f.write(f"[{timestamp}] EXECUTION TIME: {execution_time}ms\n")
    except Exception:
        # 如果日志记录失败，忽略错误以避免无限循环
        pass


def clear_log() -> bool:
    """
    清空日志文件
    返回值:
        bool: 清空是否成功
    """
    try:
        log_path = _db_config["log_path"]
        if os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("")
        return True
    except Exception as e:
        log_error(f"清空日志失败: {e}")
        return False


def get_log_entries(limit: int = 100) -> List[str]:
    """
    获取日志条目
    参数:
        limit: 返回的最大条目数
    返回值:
        日志条目列表
    """
    try:
        log_path = _db_config["log_path"]
        if not os.path.exists(log_path):
            return []

        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 返回最后limit行
        return lines[-limit:] if limit > 0 else lines
    except Exception as e:
        log_error(f"获取日志条目失败: {e}")
        return []


# ===== 数据导入导出 =====


def export_table_to_csv(
    table_name: str, csv_path: str = None, include_header: bool = True
) -> bool:
    """
    导出表数据到CSV文件
    参数:
        table_name: 表名
        csv_path: CSV文件路径，如果为None则使用表名作为文件名
        include_header: 是否包含表头
    返回值:
        bool: 导出是否成功
    """
    try:
        import csv

        # 确定CSV文件路径
        if csv_path is None:
            csv_path = f"{table_name}.csv"

        # 获取表数据
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # 获取列名
            if include_header:
                column_names = [description[0] for description in cursor.description]
            else:
                column_names = None

        # 写入CSV文件
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # 写入表头
            if include_header:
                writer.writerow(column_names)

            # 写入数据
            for row in rows:
                writer.writerow(row)

        return True
    except Exception as e:
        log_error(f"导出表 {table_name} 到CSV失败: {e}")
        return False


def import_csv_to_table(
    csv_path: str,
    table_name: str,
    columns: List[str] = None,
    include_header: bool = True,
    delimiter: str = ",",
) -> bool:
    """
    从CSV文件导入数据到表
    参数:
        csv_path: CSV文件路径
        table_name: 表名
        columns: 列名列表，如果为None则使用CSV文件中的表头
        include_header: CSV文件是否包含表头
        delimiter: CSV分隔符
    返回值:
        bool: 导入是否成功
    """
    try:
        import csv

        # 读取CSV文件
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)

            # 读取表头
            if include_header:
                header = next(reader)
                if columns is None:
                    columns = header

            # 读取数据
            data = []
            for row in reader:
                if columns and len(row) == len(columns):
                    data.append(dict(zip(columns, row)))

        # 导入数据到表
        if data:
            with get_db_connection() as conn:
                return len(insert_records(table_name, data, conn)) > 0

        return True
    except Exception as e:
        log_error(f"从CSV导入数据到表 {table_name} 失败: {e}")
        return False


def export_table_to_json(table_name: str, json_path: str = None) -> bool:
    """
    导出表数据到JSON文件
    参数:
        table_name: 表名
        json_path: JSON文件路径，如果为None则使用表名作为文件名
    返回值:
        bool: 导出是否成功
    """
    try:
        # 确定JSON文件路径
        if json_path is None:
            json_path = f"{table_name}.json"

        # 获取表数据
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # 转换为字典列表
            data = [dict(row) for row in rows]

        # 写入JSON文件
        with open(json_path, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)

        return True
    except Exception as e:
        log_error(f"导出表 {table_name} 到JSON失败: {e}")
        return False


def import_json_to_table(json_path: str, table_name: str) -> bool:
    """
    从JSON文件导入数据到表
    参数:
        json_path: JSON文件路径
        table_name: 表名
    返回值:
        bool: 导入是否成功
    """
    try:
        # 读取JSON文件
        with open(json_path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)

        # 确保数据是列表
        if not isinstance(data, list):
            data = [data]

        # 导入数据到表
        if data:
            with get_db_connection() as conn:
                return len(insert_records(table_name, data, conn)) > 0

        return True
    except Exception as e:
        log_error(f"从JSON导入数据到表 {table_name} 失败: {e}")
        return False


# ===== 数据库优化 =====


def optimize_database() -> bool:
    """
    优化数据库
    返回值:
        bool: 优化是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 执行VACUUM命令重建数据库
            cursor.execute("VACUUM")

            # 执行ANALYZE命令更新统计信息
            cursor.execute("ANALYZE")

            return True
    except Exception as e:
        log_error(f"优化数据库失败: {e}")
        return False


def create_index(
    table_name: str,
    index_name: str,
    columns: List[str],
    unique: bool = False,
    conn: sqlite3.Connection = None,
) -> bool:
    """
    创建索引
    参数:
        table_name: 表名
        index_name: 索引名
        columns: 列名列表
        unique: 是否创建唯一索引
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 创建是否成功
    """

    def _create_index(conn):
        try:
            cursor = conn.cursor()

            # 构建创建索引SQL
            unique_str = "UNIQUE " if unique else ""
            columns_str = ", ".join(columns)
            sql = f"CREATE {unique_str}INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns_str})"

            # 执行创建索引
            cursor.execute(sql)

            return True
        except Exception as e:
            log_error(f"创建索引 {index_name} 失败: {e}")
            return False

    if conn:
        return _create_index(conn)
    else:
        with get_db_connection() as conn:
            return _create_index(conn)


def drop_index(index_name: str, conn: sqlite3.Connection = None) -> bool:
    """
    删除索引
    参数:
        index_name: 索引名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 删除是否成功
    """

    def _drop_index(conn):
        try:
            cursor = conn.cursor()

            # 执行删除索引
            cursor.execute(f"DROP INDEX IF EXISTS {index_name}")

            return True
        except Exception as e:
            log_error(f"删除索引 {index_name} 失败: {e}")
            return False

    if conn:
        return _drop_index(conn)
    else:
        with get_db_connection() as conn:
            return _drop_index(conn)


def list_indexes(
    table_name: str = None, conn: sqlite3.Connection = None
) -> List[Dict[str, Any]]:
    """
    列出索引
    参数:
        table_name: 表名，如果为None则列出所有索引
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        索引信息列表
    """

    def _list_indexes(conn):
        try:
            cursor = conn.cursor()

            if table_name:
                # 获取指定表的索引
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()

                result = []
                for idx in indexes:
                    index_name = idx[1]
                    unique = bool(idx[2])

                    # 获取索引列信息
                    cursor.execute(f"PRAGMA index_info({index_name})")
                    columns = cursor.fetchall()

                    result.append(
                        {
                            "name": index_name,
                            "table": table_name,
                            "unique": unique,
                            "columns": [col[2] for col in columns],
                        }
                    )

                return result
            else:
                # 获取所有索引
                cursor.execute(
                    "SELECT name, tbl_name FROM sqlite_master WHERE type='index'"
                )
                indexes = cursor.fetchall()

                result = []
                for idx in indexes:
                    index_name = idx[0]
                    table_name = idx[1]

                    # 获取索引详细信息
                    cursor.execute(f"PRAGMA index_list({table_name})")
                    table_indexes = cursor.fetchall()

                    unique = False
                    for table_idx in table_indexes:
                        if table_idx[1] == index_name:
                            unique = bool(table_idx[2])
                            break

                    # 获取索引列信息
                    cursor.execute(f"PRAGMA index_info({index_name})")
                    columns = cursor.fetchall()

                    result.append(
                        {
                            "name": index_name,
                            "table": table_name,
                            "unique": unique,
                            "columns": [col[2] for col in columns],
                        }
                    )

                return result
        except Exception as e:
            log_error(f"列出索引失败: {e}")
            return []

    if conn:
        return _list_indexes(conn)
    else:
        with get_db_connection() as conn:
            return _list_indexes(conn)


# ===== 辅助函数 =====


def execute_sql_file(sql_file_path: str, conn: sqlite3.Connection = None) -> bool:
    """
    执行SQL文件
    参数:
        sql_file_path: SQL文件路径
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 执行是否成功
    """

    def _execute_sql_file(conn):
        try:
            with open(sql_file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            cursor = conn.cursor()
            cursor.executescript(sql_script)

            return True
        except Exception as e:
            log_error(f"执行SQL文件 {sql_file_path} 失败: {e}")
            return False

    if conn:
        return _execute_sql_file(conn)
    else:
        with get_db_connection() as conn:
            return _execute_sql_file(conn)


def execute_sql_script(sql_script: str, conn: sqlite3.Connection = None) -> bool:
    """
    执行SQL脚本
    参数:
        sql_script: SQL脚本
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 执行是否成功
    """

    def _execute_sql_script(conn):
        try:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            return True
        except Exception as e:
            log_error(f"执行SQL脚本失败: {e}")
            return False

    if conn:
        return _execute_sql_script(conn)
    else:
        with get_db_connection() as conn:
            return _execute_sql_script(conn)


def get_table_names(conn: sqlite3.Connection = None) -> List[str]:
    """
    获取所有表名
    参数:
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        表名列表
    """

    def _get_table_names(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            log_error(f"获取表名失败: {e}")
            return []

    if conn:
        return _get_table_names(conn)
    else:
        with get_db_connection() as conn:
            return _get_table_names(conn)


def get_view_names(conn: sqlite3.Connection = None) -> List[str]:
    """
    获取所有视图名
    参数:
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        视图名列表
    """

    def _get_view_names(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            log_error(f"获取视图名失败: {e}")
            return []

    if conn:
        return _get_view_names(conn)
    else:
        with get_db_connection() as conn:
            return _get_view_names(conn)


def get_trigger_names(conn: sqlite3.Connection = None) -> List[str]:
    """
    获取所有触发器名
    参数:
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        触发器名列表
    """

    def _get_trigger_names(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            log_error(f"获取触发器名失败: {e}")
            return []

    if conn:
        return _get_trigger_names(conn)
    else:
        with get_db_connection() as conn:
            return _get_trigger_names(conn)


def create_view(
    view_name: str, view_query: str, conn: sqlite3.Connection = None
) -> bool:
    """
    创建视图
    参数:
        view_name: 视图名
        view_query: 视图查询语句
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 创建是否成功
    """

    def _create_view(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE VIEW IF NOT EXISTS {view_name} AS {view_query}")
            return True
        except Exception as e:
            log_error(f"创建视图 {view_name} 失败: {e}")
            return False

    if conn:
        return _create_view(conn)
    else:
        with get_db_connection() as conn:
            return _create_view(conn)


def drop_view(view_name: str, conn: sqlite3.Connection = None) -> bool:
    """
    删除视图
    参数:
        view_name: 视图名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 删除是否成功
    """

    def _drop_view(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
            return True
        except Exception as e:
            log_error(f"删除视图 {view_name} 失败: {e}")
            return False

    if conn:
        return _drop_view(conn)
    else:
        with get_db_connection() as conn:
            return _drop_view(conn)


def create_trigger(
    trigger_name: str,
    trigger_event: str,
    trigger_table: str,
    trigger_condition: str,
    trigger_action: str,
    conn: sqlite3.Connection = None,
) -> bool:
    """
    创建触发器
    参数:
        trigger_name: 触发器名
        trigger_event: 触发事件 (INSERT, UPDATE, DELETE)
        trigger_table: 触发表
        trigger_condition: 触发条件
        trigger_action: 触发动作
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 创建是否成功
    """

    def _create_trigger(conn):
        try:
            cursor = conn.cursor()

            # 构建创建触发器SQL
            sql = f"""
            CREATE TRIGGER IF NOT EXISTS {trigger_name}
            {trigger_event} ON {trigger_table}
            {trigger_condition}
            BEGIN
                {trigger_action}
            END
            """

            cursor.execute(sql)
            return True
        except Exception as e:
            log_error(f"创建触发器 {trigger_name} 失败: {e}")
            return False

    if conn:
        return _create_trigger(conn)
    else:
        with get_db_connection() as conn:
            return _create_trigger(conn)


def drop_trigger(trigger_name: str, conn: sqlite3.Connection = None) -> bool:
    """
    删除触发器
    参数:
        trigger_name: 触发器名
        conn: 数据库连接，如果为None则创建新连接
    返回值:
        bool: 删除是否成功
    """

    def _drop_trigger(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
            return True
        except Exception as e:
            log_error(f"删除触发器 {trigger_name} 失败: {e}")
            return False

    if conn:
        return _drop_trigger(conn)
    else:
        with get_db_connection() as conn:
            return _drop_trigger(conn)
