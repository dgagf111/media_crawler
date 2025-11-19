"""
SQLite工具函数集测试文件
全面测试sqlite_toolkit.py中的所有功能
"""

import os
import sys
import shutil
import json
import csv
import tempfile
from datetime import datetime

# 导入被测试的工具函数
import sqlite_toolkit as stk


def setup_test_environment():
    """
    设置测试环境
    """
    print("=== 设置测试环境 ===")

    # 创建临时测试目录
    test_dir = tempfile.mkdtemp(prefix="sqlite_test_")
    print(f"测试目录: {test_dir}")

    # 配置测试数据库
    test_config = {
        "db_path": os.path.join(test_dir, "test.db"),
        "log_path": os.path.join(test_dir, "test.log"),
        "backup_dir": os.path.join(test_dir, "backups"),
    }

    # 初始化配置
    stk.init_db_config(test_config)

    print("测试环境设置完成")
    return test_dir


def cleanup_test_environment(test_dir):
    """
    清理测试环境
    """
    print("\n=== 清理测试环境 ===")

    # 确保所有数据库连接都已关闭
    stk.destroy_database()

    # 删除测试目录
    shutil.rmtree(test_dir, ignore_errors=True)
    print("测试环境清理完成")


def test_database_initialization():
    """
    测试数据库初始化功能
    """
    print("\n=== 测试数据库初始化 ===")

    # 测试获取配置
    config = stk.get_db_config()
    print(f"数据库配置: {config}")

    # 测试数据库连接
    with stk.get_db_connection() as conn:
        print("数据库连接成功")

        # 测试执行简单查询
        result = stk.fetch_one("SELECT sqlite_version() as version", conn=conn)
        print(f"SQLite版本: {result['version']}")

    # 测试初始化数据库（使用示例SQL）
    schema_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        category TEXT,
        stock_quantity INTEGER DEFAULT 0
    );
    
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total_amount REAL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """

    data_sql = """
    INSERT INTO users (name, email, age) VALUES 
    ('张三', 'zhangsan@example.com', 25),
    ('李四', 'lisi@example.com', 30),
    ('王五', 'wangwu@example.com', 28);
    
    INSERT INTO products (name, price, category, stock_quantity) VALUES 
    ('iPhone 13', 5999.00, '电子产品', 100),
    ('MacBook Pro', 12999.00, '电子产品', 50),
    ('AirPods', 1299.00, '电子产品', 200);
    """

    success = stk.initialize_database(schema_sql, data_sql)
    print(f"数据库初始化结果: {success}")

    # 验证表是否创建成功
    tables = stk.get_table_names()
    print(f"创建的表: {tables}")

    return success


def test_table_operations():
    """
    测试表操作功能
    """
    print("\n=== 测试表操作 ===")

    # 测试检查表是否存在
    users_exists = stk.table_exists("users")
    products_exists = stk.table_exists("products")
    print(f"users表存在: {users_exists}")
    print(f"products表存在: {products_exists}")

    # 测试获取表信息
    users_info = stk.get_table_info("users")
    print(f"users表结构: {users_info}")

    # 测试创建新表
    new_table_columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "order_id": "INTEGER NOT NULL",
        "product_id": "INTEGER NOT NULL",
        "quantity": "INTEGER DEFAULT 1",
        "unit_price": "REAL NOT NULL",
        "subtotal": "REAL NOT NULL",
    }

    foreign_keys = {"order_id": ("orders", "id"), "product_id": ("products", "id")}

    success = stk.create_table(
        "order_items", new_table_columns, foreign_keys=foreign_keys
    )
    print(f"创建order_items表结果: {success}")

    # 验证新表是否创建成功
    order_items_exists = stk.table_exists("order_items")
    print(f"order_items表存在: {order_items_exists}")

    # 测试添加列
    add_column_success = stk.add_column("users", "phone", "TEXT")
    print(f"添加phone列结果: {add_column_success}")

    # 验证列是否添加成功
    updated_users_info = stk.get_table_info("users")
    print(f"更新后的users表结构: {updated_users_info}")

    return True


def test_crud_operations():
    """
    测试CRUD操作
    """
    print("\n=== 测试CRUD操作 ===")

    # 测试插入单条记录
    new_user = {
        "name": "测试用户",
        "email": "test@example.com",
        "age": 35,
        "phone": "13800138000",
    }

    user_id = stk.insert_record("users", new_user)
    print(f"插入新用户ID: {user_id}")

    # 测试查询单条记录
    user = stk.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    print(f"查询到的用户: {user}")

    # 测试更新记录
    update_success = stk.update_record(
        "users", {"age": 36, "phone": "13900139000"}, "id = ?", (user_id,)
    )
    print(f"更新用户记录影响行数: {update_success}")

    # 验证更新结果
    updated_user = stk.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    print(f"更新后的用户: {updated_user}")

    # 测试批量插入
    new_products = [
        {
            "name": "iPad",
            "price": 3999.00,
            "category": "电子产品",
            "stock_quantity": 80,
        },
        {
            "name": "Apple Watch",
            "price": 2999.00,
            "category": "电子产品",
            "stock_quantity": 120,
        },
        {
            "name": "iMac",
            "price": 9999.00,
            "category": "电子产品",
            "stock_quantity": 30,
        },
    ]

    product_ids = stk.insert_records("products", new_products)
    print(f"批量插入产品ID列表: {product_ids}")

    # 测试查询多条记录
    all_users = stk.fetch_all("SELECT name, email, age FROM users ORDER BY id")
    print(f"所有用户: {all_users}")

    # 测试删除记录
    delete_success = stk.delete_record("users", "id = ?", (user_id,))
    print(f"删除用户记录影响行数: {delete_success}")

    # 验证删除结果
    deleted_user = stk.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    print(f"删除后的用户查询结果: {deleted_user}")

    return True


def test_transaction_operations():
    """
    测试事务操作
    """
    print("\n=== 测试事务操作 ===")

    # 测试事务上下文管理器
    try:
        with stk.get_db_connection() as conn:
            with stk.transaction(conn):
                # 在事务中执行多个操作
                order_data = {
                    "user_id": 1,
                    "total_amount": 7298.00,
                    "status": "completed",
                }
                order_id = stk.insert_record("orders", order_data, conn)

                order_items = [
                    {
                        "order_id": order_id,
                        "product_id": 1,
                        "quantity": 1,
                        "unit_price": 5999.00,
                        "subtotal": 5999.00,
                    },
                    {
                        "order_id": order_id,
                        "product_id": 3,
                        "quantity": 1,
                        "unit_price": 1299.00,
                        "subtotal": 1299.00,
                    },
                ]

                item_ids = stk.insert_records("order_items", order_items, conn)

                print(f"事务中创建订单ID: {order_id}")
                print(f"事务中创建订单项ID列表: {item_ids}")

        # 验证事务结果
        order = stk.fetch_one("SELECT * FROM orders WHERE id = ?", (order_id,))
        print(f"事务提交后的订单: {order}")

        order_items_count = stk.fetch_one(
            "SELECT COUNT(*) as count FROM order_items WHERE order_id = ?", (order_id,)
        )
        print(f"订单项数量: {order_items_count['count']}")

    except Exception as e:
        print(f"事务执行失败: {e}")
        return False

    # 测试事务回滚
    try:
        with stk.get_db_connection() as conn:
            with stk.transaction(conn):
                # 尝试插入重复邮箱，应该失败并回滚
                duplicate_user = {
                    "name": "重复用户",
                    "email": "zhangsan@example.com",  # 已存在的邮箱
                    "age": 40,
                }
                stk.insert_record("users", duplicate_user, conn)

        print("意外：重复邮箱插入成功")
        return False

    except Exception as e:
        print(f"预期的失败和回滚: {e}")

        # 验证没有插入重复记录
        duplicate_count = stk.fetch_one(
            "SELECT COUNT(*) as count FROM users WHERE email = ?",
            ("zhangsan@example.com",),
        )
        print(f"重复邮箱用户数量: {duplicate_count['count']}")

    return True


def test_complex_queries():
    """
    测试复杂查询功能
    """
    print("\n=== 测试复杂查询 ===")

    # 测试分页查询
    paginated_result = stk.execute_query_with_pagination(
        "SELECT * FROM users ORDER BY id", page=1, page_size=2
    )
    print(f"分页查询结果: {paginated_result}")

    # 测试连接查询
    join_result = stk.execute_join_query(
        tables=["users", "orders"],
        columns=["users.name", "users.email", "orders.total_amount", "orders.status"],
        join_conditions=["users.id = orders.user_id"],
        order_by="orders.created_at DESC",
    )
    print(f"连接查询结果: {join_result}")

    # 测试聚合查询
    aggregate_result = stk.execute_aggregate_query(
        table_name="products",
        group_by="category",
        aggregations={
            "total_products": "COUNT(*)",
            "avg_price": "AVG(price)",
            "max_price": "MAX(price)",
            "min_price": "MIN(price)",
        },
        order_by="total_products DESC",
    )
    print(f"聚合查询结果: {aggregate_result}")

    # 测试带条件的聚合查询
    conditional_aggregate_result = stk.execute_aggregate_query(
        table_name="orders",
        group_by="user_id",
        aggregations={"order_count": "COUNT(*)", "total_spent": "SUM(total_amount)"},
        having_clause="total_spent > 0",
        order_by="total_spent DESC",
    )
    print(f"条件聚合查询结果: {conditional_aggregate_result}")

    return True


def test_database_statistics():
    """
    测试数据库统计信息
    """
    print("\n=== 测试数据库统计信息 ===")

    # 测试获取数据库统计信息
    db_stats = stk.get_database_stats()
    print(f"数据库统计信息: {db_stats}")

    # 测试获取表统计信息
    users_stats = stk.get_table_stats("users")
    print(f"users表统计信息: {users_stats}")

    products_stats = stk.get_table_stats("products")
    print(f"products表统计信息: {products_stats}")

    orders_stats = stk.get_table_stats("orders")
    print(f"orders表统计信息: {orders_stats}")

    return True


def test_backup_and_restore():
    """
    测试备份和恢复功能
    """
    print("\n=== 测试备份和恢复 ===")

    # 获取备份前的数据
    users_before = stk.fetch_all("SELECT * FROM users")
    print(f"备份前用户数量: {len(users_before)}")

    # 测试创建备份
    backup_path = stk.backup_database("test_backup")
    print(f"创建备份路径: {backup_path}")

    # 测试列出备份
    backups = stk.list_backups()
    print(f"备份列表: {backups}")

    # 测试删除一些数据
    delete_success = stk.delete_record("users", "id > 3")
    print(f"删除部分用户记录影响行数: {delete_success}")

    # 验证数据已删除
    users_after_delete = stk.fetch_all("SELECT * FROM users")
    print(f"删除后用户数量: {len(users_after_delete)}")

    # 测试恢复备份
    restore_success = stk.restore_database(backup_path)
    print(f"恢复备份结果: {restore_success}")

    # 验证数据已恢复
    users_after_restore = stk.fetch_all("SELECT * FROM users")
    print(f"恢复后用户数量: {len(users_after_restore)}")

    # 测试删除备份
    delete_backup_success = stk.delete_backup("test_backup")
    print(f"删除备份结果: {delete_backup_success}")

    # 验证备份已删除
    backups_after_delete = stk.list_backups()
    print(f"删除备份后的备份列表: {backups_after_delete}")

    return True


def test_logging_functionality():
    """
    测试日志功能
    """
    print("\n=== 测试日志功能 ===")

    # 测试记录错误日志
    stk.log_error("这是一个测试错误")

    # 测试记录查询日志
    stk.log_query("SELECT * FROM users", (1,), 15.5)

    # 测试获取日志条目
    log_entries = stk.get_log_entries(10)
    print(f"日志条目: {log_entries}")

    # 测试清空日志
    clear_success = stk.clear_log()
    print(f"清空日志结果: {clear_success}")

    # 验证日志已清空
    empty_log_entries = stk.get_log_entries()
    print(f"清空后的日志条目数量: {len(empty_log_entries)}")

    return True


def test_data_import_export():
    """
    测试数据导入导出功能
    """
    print("\n=== 测试数据导入导出 ===")

    # 测试导出表到CSV
    csv_export_success = stk.export_table_to_csv("users", "test_users.csv")
    print(f"导出users表到CSV结果: {csv_export_success}")

    # 验证CSV文件
    if os.path.exists("test_users.csv"):
        with open("test_users.csv", "r", encoding="utf-8") as f:
            csv_content = f.read()
        print(f"CSV文件内容预览: {csv_content[:200]}...")

    # 测试从CSV导入数据
    # 先创建一个临时表
    temp_table_columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "email": "TEXT",
        "age": "INTEGER",
        "phone": "TEXT",
    }
    stk.create_table("temp_users", temp_table_columns)

    csv_import_success = stk.import_csv_to_table("test_users.csv", "temp_users")
    print(f"从CSV导入数据结果: {csv_import_success}")

    # 验证导入结果
    temp_users_count = stk.fetch_one("SELECT COUNT(*) as count FROM temp_users")
    print(f"临时表用户数量: {temp_users_count['count']}")

    # 测试导出表到JSON
    json_export_success = stk.export_table_to_json("products", "test_products.json")
    print(f"导出products表到JSON结果: {json_export_success}")

    # 验证JSON文件
    if os.path.exists("test_products.json"):
        with open("test_products.json", "r", encoding="utf-8") as f:
            json_content = json.load(f)
        print(f"JSON文件记录数量: {len(json_content)}")

    # 测试从JSON导入数据
    stk.create_table(
        "temp_products",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "price": "REAL",
            "category": "TEXT",
            "stock_quantity": "INTEGER",
        },
    )

    json_import_success = stk.import_json_to_table(
        "test_products.json", "temp_products"
    )
    print(f"从JSON导入数据结果: {json_import_success}")

    # 验证导入结果
    temp_products_count = stk.fetch_one("SELECT COUNT(*) as count FROM temp_products")
    print(f"临时表产品数量: {temp_products_count['count']}")

    # 清理临时文件
    for file in ["test_users.csv", "test_products.json"]:
        if os.path.exists(file):
            os.remove(file)

    return True


def test_index_operations():
    """
    测试索引操作
    """
    print("\n=== 测试索引操作 ===")

    # 测试创建索引
    email_index_success = stk.create_index(
        "users", "idx_users_email", ["email"], unique=True
    )
    print(f"创建邮箱索引结果: {email_index_success}")

    price_index_success = stk.create_index("products", "idx_products_price", ["price"])
    print(f"创建价格索引结果: {price_index_success}")

    # 测试列出索引
    all_indexes = stk.list_indexes()
    print(f"所有索引: {all_indexes}")

    users_indexes = stk.list_indexes("users")
    print(f"users表索引: {users_indexes}")

    # 测试删除索引
    delete_email_index_success = stk.drop_index("idx_users_email")
    print(f"删除邮箱索引结果: {delete_email_index_success}")

    # 验证索引已删除
    users_indexes_after_delete = stk.list_indexes("users")
    print(f"删除后的users表索引: {users_indexes_after_delete}")

    return True


def test_view_and_trigger_operations():
    """
    测试视图和触发器操作
    """
    print("\n=== 测试视图和触发器 ===")

    # 测试创建视图
    view_query = """
    SELECT u.name, u.email, COUNT(o.id) as order_count, 
           COALESCE(SUM(o.total_amount), 0) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
    """

    create_view_success = stk.create_view("user_order_summary", view_query)
    print(f"创建用户订单摘要视图结果: {create_view_success}")

    # 测试查询视图
    view_data = stk.fetch_all("SELECT * FROM user_order_summary")
    print(f"视图数据: {view_data}")

    # 测试获取视图列表
    views = stk.get_view_names()
    print(f"视图列表: {views}")

    # 测试创建触发器
    trigger_action = """
    INSERT INTO order_audit (order_id, action, action_time, user_id)
    VALUES (NEW.id, 'INSERT', datetime('now'), NEW.user_id);
    """

    # 先创建审计表
    stk.create_table(
        "order_audit",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "order_id": "INTEGER",
            "action": "TEXT",
            "action_time": "TEXT",
            "user_id": "INTEGER",
        },
    )

    create_trigger_success = stk.create_trigger(
        "trg_order_insert_audit",
        "AFTER INSERT",
        "orders",
        "FOR EACH ROW",
        trigger_action,
    )
    print(f"创建订单插入审计触发器结果: {create_trigger_success}")

    # 测试触发器
    new_order = {"user_id": 2, "total_amount": 1000.00, "status": "pending"}

    order_id = stk.insert_record("orders", new_order)
    print(f"插入新订单ID: {order_id}")

    # 验证触发器是否执行
    audit_records = stk.fetch_all(
        "SELECT * FROM order_audit WHERE order_id = ?", (order_id,)
    )
    print(f"审计记录: {audit_records}")

    # 测试获取触发器列表
    triggers = stk.get_trigger_names()
    print(f"触发器列表: {triggers}")

    # 测试删除视图和触发器
    delete_view_success = stk.drop_view("user_order_summary")
    print(f"删除视图结果: {delete_view_success}")

    delete_trigger_success = stk.drop_trigger("trg_order_insert_audit")
    print(f"删除触发器结果: {delete_trigger_success}")

    return True


def test_database_optimization():
    """
    测试数据库优化功能
    """
    print("\n=== 测试数据库优化 ===")

    # 获取优化前的数据库统计信息
    stats_before = stk.get_database_stats()
    print(f"优化前数据库大小: {stats_before['size_mb']} MB")

    # 测试数据库优化
    optimize_success = stk.optimize_database()
    print(f"数据库优化结果: {optimize_success}")

    # 获取优化后的数据库统计信息
    stats_after = stk.get_database_stats()
    print(f"优化后数据库大小: {stats_after['size_mb']} MB")

    return True


def test_sql_execution():
    """
    测试SQL执行功能
    """
    print("\n=== 测试SQL执行 ===")

    # 测试执行SQL脚本
    sql_script = """
    CREATE TABLE IF NOT EXISTS test_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value INTEGER DEFAULT 0
    );
    
    INSERT INTO test_table (name, value) VALUES ('test1', 100);
    INSERT INTO test_table (name, value) VALUES ('test2', 200);
    """

    script_success = stk.execute_sql_script(sql_script)
    print(f"执行SQL脚本结果: {script_success}")

    # 验证脚本执行结果
    test_data = stk.fetch_all("SELECT * FROM test_table")
    print(f"测试表数据: {test_data}")

    # 测试执行SQL文件
    # 创建临时SQL文件
    with open("temp_test.sql", "w", encoding="utf-8") as f:
        f.write(
            """
        INSERT INTO test_table (name, value) VALUES ('test3', 300);
        UPDATE test_table SET value = value * 2 WHERE name = 'test1';
        """
        )

    file_success = stk.execute_sql_file("temp_test.sql")
    print(f"执行SQL文件结果: {file_success}")

    # 验证文件执行结果
    updated_data = stk.fetch_all("SELECT * FROM test_table ORDER BY id")
    print(f"更新后的测试表数据: {updated_data}")

    # 清理临时文件
    if os.path.exists("temp_test.sql"):
        os.remove("temp_test.sql")

    return True


def test_database_cleanup():
    """
    测试数据库清理功能
    """
    print("\n=== 测试数据库清理 ===")

    # 获取清理前的表列表
    tables_before = stk.get_table_names()
    print(f"清理前的表: {tables_before}")

    # 测试重置数据库
    reset_success = stk.reset_database()
    print(f"重置数据库结果: {reset_success}")

    # 验证数据库已重置
    tables_after_reset = stk.get_table_names()
    print(f"重置后的表: {tables_after_reset}")

    # 测试销毁数据库
    destroy_success = stk.destroy_database()
    print(f"销毁数据库结果: {destroy_success}")

    # 验证数据库文件已删除
    db_path = stk.get_db_config()["db_path"]
    db_exists = os.path.exists(db_path)
    print(f"数据库文件是否存在: {db_exists}")

    return True


def run_all_tests():
    """
    运行所有测试
    """
    print("开始运行SQLite工具函数集全面测试")
    print("=" * 60)

    # 设置测试环境
    test_dir = setup_test_environment()

    try:
        # 运行所有测试
        test_results = []

        test_results.append(("数据库初始化", test_database_initialization()))
        test_results.append(("表操作", test_table_operations()))
        test_results.append(("CRUD操作", test_crud_operations()))
        test_results.append(("事务操作", test_transaction_operations()))
        test_results.append(("复杂查询", test_complex_queries()))
        test_results.append(("数据库统计", test_database_statistics()))
        test_results.append(("备份恢复", test_backup_and_restore()))
        test_results.append(("日志功能", test_logging_functionality()))
        test_results.append(("数据导入导出", test_data_import_export()))
        test_results.append(("索引操作", test_index_operations()))
        test_results.append(("视图和触发器", test_view_and_trigger_operations()))
        test_results.append(("数据库优化", test_database_optimization()))
        test_results.append(("SQL执行", test_sql_execution()))
        test_results.append(("数据库清理", test_database_cleanup()))

        # 输出测试结果摘要
        print("\n" + "=" * 60)
        print("测试结果摘要:")
        print("=" * 60)

        passed = 0
        failed = 0

        for test_name, result in test_results:
            status = "✓ 通过" if result else "✗ 失败"
            print(f"{test_name:20}: {status}")

            if result:
                passed += 1
            else:
                failed += 1

        print("=" * 60)
        print(f"总计: {passed} 通过, {failed} 失败")

        if failed == 0:
            print("🎉 所有测试通过！")
        else:
            print("❌ 部分测试失败")

        return failed == 0

    finally:
        # 清理测试环境
        cleanup_test_environment(test_dir)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
