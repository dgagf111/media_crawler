"""
SQLite框架简明使用示例
展示如何使用函数式API进行常见的数据库操作
每个函数都包含详细注释，说明操作目的和实现方法
"""

import db_utils
import db_config
from db_tests import run_sql_tests


def initialize_database():
    """
    初始化数据库和表结构

    功能说明：
    - 检查数据库是否已存在，避免重复初始化
    - 创建必要的表结构
    - 插入初始测试数据

    返回值：
    - 无返回值

    异常处理：
    - 自动处理数据库连接和关闭
    """
    print("正在初始化数据库...")
    with db_utils.get_db_connection() as conn:
        # 检查users表是否已存在，避免重复初始化
        if db_utils.table_exists(conn, "users"):
            print("数据库已存在，跳过初始化")
            return

        # 执行SQL架构文件，创建表结构
        db_utils.execute_sql_file(conn, db_config.get_sql_schema_path())

        # 执行数据文件，插入初始测试数据
        db_utils.execute_sql_file(conn, db_config.get_sql_data_path())

        print("数据库初始化完成！")


def basic_crud_operations():
    """
    演示基本的CRUD（创建、读取、更新、删除）操作

    功能说明：
    - 插入新记录（Create）
    - 查询单条记录（Read）
    - 更新现有记录（Update）
    - 查询多条记录
    - 删除记录（Delete）

    返回值：
    - 无返回值，但会打印操作结果

    注意事项：
    - 所有操作都在事务中执行，确保数据一致性
    - 使用参数化查询防止SQL注入
    """
    print("\n=== 基本CRUD操作演示 ===")

    with db_utils.get_db_connection() as conn:
        # 1. 创建（Create）- 插入新用户
        print("1. 插入新用户...")
        new_user = {
            "name": "测试用户",
            "email": "test@example.com",
            "age": 28,
            "phone": "13900139000",
            "address": "北京市朝阳区",
        }
        # insert_record返回新记录的ID
        user_id = db_utils.insert_record(conn, "users", new_user)
        print(f"   新用户ID: {user_id}")

        # 2. 读取（Read）- 查询单个用户
        print("2. 查询单个用户...")
        # 使用参数化查询，防止SQL注入
        user = db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (user_id,))
        print(f"   用户信息: {user}")

        # 3. 更新（Update）- 修改用户信息
        print("3. 更新用户信息...")
        # 更新指定记录的字段
        affected_rows = db_utils.update_record(
            conn, "users", {"age": 29, "address": "北京市海淀区"}, "id = ?", (user_id,)
        )
        print(f"   更新了 {affected_rows} 行")

        # 4. 读取多条记录
        print("4. 查询多个用户...")
        # 限制返回数量，避免数据过多
        all_users = db_utils.fetch_all(
            conn, "SELECT name, email, age FROM users LIMIT 5"
        )
        for i, user in enumerate(all_users, 1):
            print(f"   {i}. {user['name']} ({user['email']}) - {user['age']}岁")

        # 5. 删除（Delete）- 移除用户记录
        print("5. 删除用户...")
        affected_rows = db_utils.delete_record(conn, "users", "id = ?", (user_id,))
        print(f"   删除了 {affected_rows} 行")


def advanced_database_operations():
    """
    演示高级数据库操作

    功能说明：
    - 批量插入数据
    - 执行复杂查询（多表连接、分组、聚合）
    - 事务处理（原子操作）
    - 获取数据库统计信息

    返回值：
    - 无返回值，但会打印操作结果

    注意事项：
    - 事务处理确保操作的原子性
    - 复杂查询展示了SQL的强大功能
    """
    print("\n=== 高级数据库操作演示 ===")

    with db_utils.get_db_connection() as conn:
        # 1. 批量插入数据
        print("1. 批量插入产品...")
        new_products = [
            {
                "name": "智能手机",
                "description": "高性能智能手机",
                "price": 3999.00,
                "category": "电子产品",
                "stock_quantity": 30,
            },
            {
                "name": "蓝牙耳机",
                "description": "降噪蓝牙耳机",
                "price": 599.00,
                "category": "电子产品",
                "stock_quantity": 80,
            },
            {
                "name": "平板电脑",
                "description": "轻薄平板电脑",
                "price": 2599.00,
                "category": "电子产品",
                "stock_quantity": 40,
            },
        ]
        # 批量插入比单条插入效率更高
        product_ids = db_utils.insert_records(conn, "products", new_products)
        print(f"   插入了 {len(product_ids)} 个产品")

        # 2. 复杂查询示例
        print("2. 复杂查询示例...")
        # 查询订单总额超过5000的用户，使用多表连接和分组
        query = """
            SELECT u.name, u.email, COUNT(o.id) as order_count, SUM(o.total_amount) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            HAVING total_spent > 5000
            ORDER BY total_spent DESC
        """
        big_spenders = db_utils.fetch_all(conn, query)
        print("   高消费用户:")
        for spender in big_spenders:
            print(
                f"     {spender['name']} - 订单数: {spender['order_count']}, 总消费: ¥{spender['total_spent']:.2f}"
            )

        # 3. 事务操作演示
        print("3. 事务操作演示...")
        try:
            # 使用事务上下文管理器，确保操作的原子性
            with db_utils.transaction(conn):
                # 创建订单
                order_data = {
                    "user_id": 1,
                    "total_amount": 4598.00,
                    "status": "pending",
                    "shipping_address": "上海市浦东新区xxx路xxx号",
                }
                order_id = db_utils.insert_record(conn, "orders", order_data)

                # 添加订单项
                order_items = [
                    {
                        "order_id": order_id,
                        "product_id": 1,
                        "quantity": 1,
                        "unit_price": 3999.00,
                        "subtotal": 3999.00,
                    },
                    {
                        "order_id": order_id,
                        "product_id": 2,
                        "quantity": 1,
                        "unit_price": 599.00,
                        "subtotal": 599.00,
                    },
                ]
                db_utils.insert_records(conn, "order_items", order_items)
                print(f"   事务提交成功，订单ID: {order_id}")
        except Exception as e:
            # 如果事务中任何操作失败，所有更改都会回滚
            print(f"   事务回滚: {e}")

        # 4. 获取数据库统计信息
        print("4. 数据库统计信息...")
        stats = db_utils.get_database_stats(conn)
        print(f"   数据库大小: {stats.get('size_mb', 0)} MB")
        print("   表统计:")
        for table, count in stats["table_counts"].items():
            print(f"     {table}: {count} 条记录")


def error_handling_examples():
    """
    演示错误处理机制

    功能说明：
    - 处理唯一约束冲突（如重复邮箱）
    - 处理查询不存在的记录
    - 处理无效SQL语句

    返回值：
    - 无返回值，但会打印错误处理结果

    注意事项：
    - 展示了如何优雅地处理常见数据库错误
    - 使用try-except捕获并处理异常
    """
    print("\n=== 错误处理演示 ===")

    with db_utils.get_db_connection() as conn:
        # 1. 处理唯一约束冲突
        print("1. 尝试插入重复邮箱...")
        try:
            # 尝试插入已存在的邮箱，应该失败
            duplicate_user = {
                "name": "重复用户",
                "email": "zhangsan@example.com",  # 假设此邮箱已存在
                "age": 30,
            }
            db_utils.insert_record(conn, "users", duplicate_user)
            print("   意外成功！")
        except Exception as e:
            # 捕获并处理唯一约束冲突异常
            print(f"   预期失败: {e}")

        # 2. 处理查询不存在的记录
        print("2. 查询不存在的记录...")
        # 查询一个不存在的ID
        non_existent_user = db_utils.fetch_one(
            conn, "SELECT * FROM users WHERE id = ?", (99999,)
        )
        if non_existent_user is None:
            print("   正确处理了不存在的记录")

        # 3. 处理无效SQL语句
        print("3. 尝试执行无效SQL...")
        try:
            # 尝试查询不存在的表
            db_utils.fetch_all(conn, "SELECT * FROM non_existent_table")
        except Exception as e:
            # 捕获并处理SQL语法错误
            print(f"   正确捕获了SQL错误: {e}")


def main():
    """
    主函数，组织并执行所有示例

    功能说明：
    - 按顺序执行所有示例函数
    - 运行测试验证框架功能
    - 输出执行结果

    返回值：
    - 无返回值

    执行流程：
    1. 初始化数据库
    2. 演示基本CRUD操作
    3. 演示高级数据库操作
    4. 演示错误处理
    5. 运行测试套件
    """
    print("SQLite框架简明使用示例")
    print("=" * 50)

    # 1. 初始化数据库
    initialize_database()

    # 2. 演示基本CRUD操作
    basic_crud_operations()

    # 3. 演示高级数据库操作
    advanced_database_operations()

    # 4. 演示错误处理
    error_handling_examples()

    # 5. 运行测试套件验证框架功能
    print("\n=== 运行测试套件 ===")
    success = run_sql_tests()

    if success:
        print("\n🎉 所有示例和测试都成功完成！")
    else:
        print("\n❌ 部分测试失败，请检查代码。")


# 当脚本直接运行时，执行主函数
if __name__ == "__main__":
    main()
