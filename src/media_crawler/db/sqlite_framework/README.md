# SQLite 框架模板 - 详细文档

## 📋 目录

- [项目概述](#项目概述)
- [核心特性](#核心特性)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [详细使用指南](#详细使用指南)
  - [数据库管理](#数据库管理)
  - [表操作](#表操作)
  - [CRUD 操作](#crud操作)
  - [高级功能](#高级功能)
- [API 参考](#api参考)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)
- [示例代码](#示例代码)
- [SQLite 单文件架构详解](#sqlite单文件架构详解)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 📖 项目概述

### 什么是 SQLite 框架模板？

这是一个轻量级、易用、易维护的 SQLite 数据库框架，采用函数式 API 设计，无需类包装。它提供了完整的数据库操作解决方案，包括连接管理、CRUD 操作、事务管理、错误处理等功能。

### 设计理念

- **简洁性**：函数式 API，无需复杂的类继承结构
- **易用性**：直观的接口设计，详细的使用文档
- **可维护性**：模块化设计，清晰的代码结构
- **可扩展性**：易于添加新功能和自定义操作
- **可靠性**：内置完整的测试套件和错误处理

### 适用场景

- ✅ 小型到中型项目的数据库操作
- ✅ 需要快速开发和部署的项目
- ✅ 对性能要求较高的应用
- ✅ 需要详细日志记录的项目
- ✅ 教学和学习 SQLite 的项目
- ✅ 移动应用和桌面应用程序
- ✅ 原型开发和数据验证

---

## ✨ 核心特性

### 🎯 函数式 API 设计

```python
# 无需类包装，直接调用函数
with db_utils.get_db_connection() as conn:
    user_id = db_utils.insert_record(conn, 'users', user_data)
    users = db_utils.fetch_all(conn, "SELECT * FROM users")
```

### 📁 单目录结构

```
sqlite_framework/
├── data/                  # 数据文件目录
│   ├── app.db            # 数据库文件
│   ├── db.log            # 查询日志
│   ├── sql_schema.sql    # 数据库架构
│   └── sql_data.sql      # 测试数据
├── db_config.py          # 配置文件
├── db_utils.py          # 核心工具函数
├── db_tests.py          # 测试文件
├── example_usage.py     # 使用示例
└── README.md           # 说明文档
```

### 🔧 易用易维护

- 详细的代码注释和文档
- 统一的错误处理机制
- 可选的查询日志记录
- 自动连接管理

### 🚀 易扩展

- 模块化设计
- 插件式架构
- 自定义函数支持
- 灵活的配置系统

### 🧪 内置测试

- 完整的单元测试套件
- 测试覆盖率报告
- 持续集成支持
- 性能测试工具

### 💾 事务支持

- 自动事务管理
- 手动事务控制
- 事务回滚机制
- 并发访问支持

### 📊 性能优化

- 批量操作支持
- 连接池管理
- 索引优化建议
- 查询性能分析

---

## 🚀 快速开始

### 环境要求

- Python 3.6+
- SQLite3 (Python 内置，无需额外安装)

### 安装步骤

#### 1. 下载框架文件

```bash
# 克隆项目
git clone <repository-url>
cd sqlite_framework

# 或者直接复制文件到您的项目
cp -r sqlite_framework/ your_project/
```

#### 2. 配置虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# 安装依赖（如果有）
pip install -r requirements.txt
```

#### 3. 验证安装

```bash
# 运行测试
python db_tests.py

# 运行示例
python example_usage.py
```

### 第一个程序

```python
import db_utils

# 创建数据库连接
with db_utils.get_db_connection() as conn:
    # 创建表
    db_utils.execute_query(conn, """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 插入数据
    user_id = db_utils.insert_record(conn, 'users', {
        'name': '张三',
        'email': 'zhangsan@example.com'
    })

    # 查询数据
    user = db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (user_id,))
    print(f"用户信息: {user}")
```

---

## 📁 项目结构

### 目录结构详解

```
sqlite_framework/
├── data/                          # 数据文件目录（自动创建）
│   ├── app.db                    # 主数据库文件
│   ├── db.log                    # SQL查询日志文件
│   ├── sql_schema.sql            # 数据库架构定义
│   ├── sql_data.sql              # 测试数据脚本
│   └── backup_*.db              # 数据库备份文件
├── db_config.py                  # 数据库配置模块
├── db_utils.py                  # 核心数据库操作工具
├── db_tests.py                  # 测试套件
├── example_usage.py             # 使用示例和演示
├── requirements.txt            # 依赖包列表
└── README.md                   # 项目文档
```

### 文件说明

#### `db_config.py` - 配置管理

```python
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
    'database': str(DB_FILE),
    'timeout': 30.0,  # 连接超时时间（秒）
    'check_same_thread': False,  # 允许多线程访问
    'isolation_level': None,  # 自动提交模式
}

# SQL文件路径
SQL_SCHEMA_FILE = DB_DIR / "sql_schema.sql"
SQL_DATA_FILE = DB_DIR / "sql_data.sql"

# 日志配置
LOG_QUERIES = True  # 是否记录SQL查询日志
LOG_FILE = DB_DIR / "db.log"
```

#### `db_utils.py` - 核心工具函数

包含所有数据库操作的核心函数：

- 连接管理
- CRUD 操作
- 事务管理
- 表操作
- 工具函数

#### `db_tests.py` - 测试套件

完整的单元测试，覆盖所有功能：

- 连接测试
- CRUD 操作测试
- 事务测试
- 错误处理测试
- 性能测试

#### `example_usage.py` - 使用示例

详细的使用示例和最佳实践演示。

---

## 📚 详细使用指南

### 数据库管理

#### 创建新数据库

SQLite 框架会自动创建数据库文件，您只需要配置好路径即可。

```python
import db_utils
import db_config

# 方法1：自动创建（推荐）
with db_utils.get_db_connection() as conn:
    print("数据库已自动创建")
    print(f"数据库路径: {db_config.get_db_path()}")

# 方法2：手动创建特定数据库
def create_custom_database(db_path: str):
    """创建自定义数据库"""
    from pathlib import Path

    # 确保目录存在
    db_dir = Path(db_path).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    # 创建数据库连接
    conn = db_utils.get_connection()
    conn.close()

    print(f"数据库已创建: {db_path}")

# 使用示例
create_custom_database("data/my_custom_database.db")
```

#### 数据库连接管理

```python
import db_utils

# 方式1：使用上下文管理器（推荐）
with db_utils.get_db_connection() as conn:
    # 在这里执行数据库操作
    result = db_utils.fetch_all(conn, "SELECT * FROM users")
    print(result)

# 方式2：手动管理连接
conn = db_utils.get_connection()
try:
    # 执行数据库操作
    result = db_utils.fetch_all(conn, "SELECT * FROM users")
    print(result)
finally:
    # 手动关闭连接
    conn.close()
```

#### 数据库备份和恢复

```python
import db_utils
from datetime import datetime

def backup_database():
    """备份数据库"""
    source_path = db_config.get_db_path()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"data/backup_{timestamp}.db"

    try:
        db_utils.backup_database(source_path, backup_path)
        print(f"数据库备份成功: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"数据库备份失败: {e}")
        return None

def restore_database(backup_path: str):
    """恢复数据库"""
    source_path = db_config.get_db_path()

    try:
        db_utils.backup_database(backup_path, source_path)
        print(f"数据库恢复成功: {source_path}")
        return True
    except Exception as e:
        print(f"数据库恢复失败: {e}")
        return False

# 使用示例
backup_file = backup_database()
if backup_file:
    restore_database(backup_file)
```

### 表操作

#### 创建新表

##### 基本表创建

```python
import db_utils

def create_basic_table():
    """创建基本表"""
    with db_utils.get_db_connection() as conn:
        # 创建用户表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("用户表创建成功")

# 使用示例
create_basic_table()
```

##### 使用 SQL 文件创建

```python
import db_utils
import db_config

def create_table_from_sql_file():
    """从SQL文件创建表"""
    with db_utils.get_db_connection() as conn:
        # 执行SQL文件
        db_utils.execute_sql_file(conn, db_config.get_sql_schema_path())
        print("表创建成功")

# 使用示例
create_table_from_sql_file()
```

##### 使用函数封装创建表

```python
import db_utils
from typing import List, Dict, Any

def create_table_with_structure(table_name: str, columns: List[Dict[str, Any]],
                              constraints: List[str] = None):
    """
    使用结构定义创建表
    Args:
        table_name: 表名
        columns: 列定义列表
        constraints: 约束条件列表
    """
    # 构建列定义
    column_defs = []
    for col in columns:
        col_def = f"{col['name']} {col['type']}"

        # 添加约束
        if col.get('primary_key'):
            col_def += " PRIMARY KEY"
        if col.get('autoincrement'):
            col_def += " AUTOINCREMENT"
        if col.get('not_null'):
            col_def += " NOT NULL"
        if col.get('unique'):
            col_def += " UNIQUE"
        if 'default' in col:
            col_def += f" DEFAULT {col['default']}"
        if 'check' in col:
            col_def += f" CHECK ({col['check']})"

        column_defs.append(col_def)

    # 添加表级约束
    if constraints:
        column_defs.extend(constraints)

    # 构建完整SQL
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)})"

    # 执行创建
    with db_utils.get_db_connection() as conn:
        db_utils.execute_query(conn, sql)
        print(f"表 {table_name} 创建成功")

# 使用示例
columns = [
    {'name': 'id', 'type': 'INTEGER', 'primary_key': True, 'autoincrement': True},
    {'name': 'username', 'type': 'TEXT', 'not_null': True, 'unique': True},
    {'name': 'email', 'type': 'TEXT', 'not_null': True, 'unique': True},
    {'name': 'age', 'type': 'INTEGER', 'check': 'age >= 0 AND age <= 150'},
    {'name': 'is_active', 'type': 'BOOLEAN', 'default': 'TRUE'},
    {'name': 'created_at', 'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'}
]

constraints = [
    "CONSTRAINT email_format CHECK (email LIKE '%@%.%')"
]

create_table_with_structure('users', columns, constraints)
```

#### 表结构管理

##### 检查表是否存在

```python
import db_utils

def check_table_exists(table_name: str) -> bool:
    """检查表是否存在"""
    with db_utils.get_db_connection() as conn:
        return db_utils.table_exists(conn, table_name)

# 使用示例
if check_table_exists('users'):
    print("users表已存在")
else:
    print("users表不存在")
```

##### 获取表结构信息

```python
import db_utils

def get_table_structure(table_name: str):
    """获取表结构信息"""
    with db_utils.get_db_connection() as conn:
        if not db_utils.table_exists(conn, table_name):
            print(f"表 {table_name} 不存在")
            return

        # 获取列信息
        columns = db_utils.get_table_info(conn, table_name)

        print(f"表 {table_name} 的结构:")
        for col in columns:
            print(f"  {col['name']} - {col['type']}")
            if col['notnull']:
                print("    NOT NULL")
            if col['dflt_value']:
                print(f"    DEFAULT: {col['dflt_value']}")
            if col['pk']:
                print("    PRIMARY KEY")

# 使用示例
get_table_structure('users')
```

##### 修改表结构

```python
import db_utils

def modify_table_structure():
    """修改表结构"""
    with db_utils.get_db_connection() as conn:

        # 添加新列
        db_utils.execute_query(conn, "ALTER TABLE users ADD COLUMN phone TEXT")

        # SQLite不支持直接修改列名，需要重建表
        # 1. 创建新表
        db_utils.execute_query(conn, """
            CREATE TABLE users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                phone_number TEXT,  # 修改后的列名
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. 复制数据
        db_utils.execute_query(conn, """
            INSERT INTO users_new (id, username, email, phone_number, created_at)
            SELECT id, username, email, phone, created_at FROM users
        """)

        # 3. 删除旧表
        db_utils.execute_query(conn, "DROP TABLE users")

        # 4. 重命名新表
        db_utils.execute_query(conn, "ALTER TABLE users_new RENAME TO users")

        print("表结构修改完成")

# 使用示例
modify_table_structure()
```

##### 删除表

```python
import db_utils

def drop_table_safely(table_name: str):
    """安全删除表"""
    with db_utils.get_db_connection() as conn:
        if db_utils.table_exists(conn, table_name):
            db_utils.execute_query(conn, f"DROP TABLE {table_name}")
            print(f"表 {table_name} 已删除")
        else:
            print(f"表 {table_name} 不存在")

# 使用示例
drop_table_safely('temp_table')
```

#### 完整表创建示例

##### 电商数据库表结构

```python
import db_utils

def create_ecommerce_database():
    """创建完整的电商数据库"""
    print("开始创建电商数据库...")

    with db_utils.get_db_connection() as conn:

        # 1. 用户表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT email_format CHECK (email LIKE '%@%.%')
            )
        """)

        # 2. 产品分类表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                parent_id INTEGER,
                sort_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)

        # 3. 产品表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                sku TEXT UNIQUE NOT NULL,
                category_id INTEGER,
                price REAL NOT NULL CHECK (price >= 0),
                stock_quantity INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)

        # 4. 订单表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                total_amount REAL NOT NULL,
                shipping_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # 5. 订单详情表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,

                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # 创建索引
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku)",
            "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)",
            "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)"
        ]

        for index_sql in indexes:
            db_utils.execute_query(conn, index_sql)

        print("电商数据库创建完成！")

# 使用示例
create_ecommerce_database()
```

### CRUD 操作

#### 创建记录（Create）

##### 单条插入

```python
import db_utils

def insert_single_record():
    """插入单条记录"""
    with db_utils.get_db_connection() as conn:
        # 准备数据
        user_data = {
            'name': '张三',
            'email': 'zhangsan@example.com',
            'age': 25,
            'phone': '13800138001',
            'address': '北京市朝阳区'
        }

        # 插入记录
        user_id = db_utils.insert_record(conn, 'users', user_data)
        print(f"插入的用户ID: {user_id}")

        # 验证插入
        user = db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (user_id,))
        print(f"用户信息: {user}")

# 使用示例
insert_single_record()
```

##### 批量插入

```python
import db_utils

def insert_multiple_records():
    """批量插入记录"""
    with db_utils.get_db_connection() as conn:
        # 准备批量数据
        products_data = [
            {'name': 'iPhone 14', 'price': 5999.00, 'category': '电子产品'},
            {'name': 'MacBook Pro', 'price': 12999.00, 'category': '电子产品'},
            {'name': 'iPad Air', 'price': 3999.00, 'category': '电子产品'}
        ]

        # 批量插入
        product_ids = db_utils.insert_records(conn, 'products', products_data)
        print(f"插入的产品ID列表: {product_ids}")

        # 验证插入
        for i, product_id in enumerate(product_ids):
            product = db_utils.fetch_one(conn, "SELECT * FROM products WHERE id = ?", (product_id,))
            print(f"产品 {i+1}: {product['name']} - ¥{product['price']}")

# 使用示例
insert_multiple_records()
```

#### 读取记录（Read）

##### 获取所有记录

```python
import db_utils

def fetch_all_records():
    """获取所有记录"""
    with db_utils.get_db_connection() as conn:
        # 获取所有用户
        users = db_utils.fetch_all(conn, "SELECT * FROM users")
        print(f"用户总数: {len(users)}")

        # 遍历用户
        for user in users:
            print(f"ID: {user['id']}, 姓名: {user['name']}, 邮箱: {user['email']}")

# 使用示例
fetch_all_records()
```

##### 获取单条记录

```python
import db_utils

def fetch_single_record():
    """获取单条记录"""
    with db_utils.get_db_connection() as conn:
        # 根据ID获取用户
        user = db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (1,))

        if user:
            print(f"用户信息: {user}")
        else:
            print("用户不存在")

        # 根据邮箱获取用户
        user = db_utils.fetch_one(
            conn,
            "SELECT * FROM users WHERE email = ?",
            ('zhangsan@example.com',)
        )

        if user:
            print(f"找到用户: {user['name']}")
        else:
            print("未找到用户")

# 使用示例
fetch_single_record()
```

##### 获取单个值

```python
import db_utils

def fetch_single_value():
    """获取单个值"""
    with db_utils.get_db_connection() as conn:
        # 获取用户总数
        user_count = db_utils.fetch_value(conn, "SELECT COUNT(*) FROM users")
        print(f"用户总数: {user_count}")

        # 获取最大年龄
        max_age = db_utils.fetch_value(conn, "SELECT MAX(age) FROM users")
        print(f"最大年龄: {max_age}")

        # 获取特定用户的年龄
        user_age = db_utils.fetch_value(
            conn,
            "SELECT age FROM users WHERE email = ?",
            ('zhangsan@example.com',)
        )
        print(f"用户年龄: {user_age}")

# 使用示例
fetch_single_value()
```

##### 条件查询

```python
import db_utils

def conditional_query():
    """条件查询"""
    with db_utils.get_db_connection() as conn:
        # 查询年龄大于25的用户
        users = db_utils.fetch_all(
            conn,
            "SELECT * FROM users WHERE age > ? ORDER BY age DESC",
            (25,)
        )
        print(f"年龄大于25的用户: {len(users)} 人")

        # 查询特定邮箱的用户
        user = db_utils.fetch_one(
            conn,
            "SELECT * FROM users WHERE email = ?",
            ('zhangsan@example.com',)
        )

        # 模糊查询
        users = db_utils.fetch_all(
            conn,
            "SELECT * FROM users WHERE name LIKE ?",
            ('%张%',)
        )
        print(f"姓名包含'张'的用户: {len(users)} 人")

        # 多条件查询
        users = db_utils.fetch_all(
            conn,
            "SELECT * FROM users WHERE age > ? AND name LIKE ?",
            (20, '%张%')
        )
        print(f"年龄大于20且姓名包含'张'的用户: {len(users)} 人")

# 使用示例
conditional_query()
```

#### 更新记录（Update）

```python
import db_utils

def update_records():
    """更新记录"""
    with db_utils.get_db_connection() as conn:
        # 更新单个字段
        affected_rows = db_utils.update_record(
            conn,
            'users',
            {'age': 26},  # 要更新的数据
            'id = ?', (1,)  # WHERE条件和参数
        )
        print(f"更新了 {affected_rows} 行")

        # 更新多个字段
        affected_rows = db_utils.update_record(
            conn,
            'users',
            {'age': 27, 'address': '北京市海淀区'},
            'email = ?', ('zhangsan@example.com',)
        )
        print(f"更新了 {affected_rows} 行")

        # 批量更新
        affected_rows = db_utils.update_record(
            conn,
            'users',
            {'is_active': False},
            'age < ?', (18,)
        )
        print(f"批量更新了 {affected_rows} 行")

        # 验证更新
        user = db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (1,))
        print(f"更新后的用户信息: {user}")

# 使用示例
update_records()
```

#### 删除记录（Delete）

```python
import db_utils

def delete_records():
    """删除记录"""
    with db_utils.get_db_connection() as conn:
        # 删除指定用户
        affected_rows = db_utils.delete_record(
            conn,
            'users',
            'id = ?', (1,)  # WHERE条件和参数
        )
        print(f"删除了 {affected_rows} 行")

        # 根据条件删除
        affected_rows = db_utils.delete_record(
            conn,
            'users',
            'age < ? AND is_active = ?', (18, False)
        )
        print(f"删除了 {affected_rows} 行")

        # 验证删除
        user_count = db_utils.fetch_value(conn, "SELECT COUNT(*) FROM users")
        print(f"剩余用户数: {user_count}")

# 使用示例
delete_records()
```

### 高级功能

#### 事务管理

##### 基本事务操作

```python
import db_utils

def basic_transaction():
    """基本事务操作"""
    with db_utils.get_db_connection() as conn:
        try:
            # 开始事务
            db_utils.begin_transaction(conn)

            # 执行多个操作
            order_id = db_utils.insert_record(conn, 'orders', {
                'user_id': 1,
                'total_amount': 999.99,
                'status': 'pending'
            })

            db_utils.insert_record(conn, 'order_items', {
                'order_id': order_id,
                'product_id': 1,
                'quantity': 1,
                'unit_price': 999.99
            })

            # 提交事务
            db_utils.commit_transaction(conn)
            print("事务提交成功")

        except Exception as e:
            # 回滚事务
            db_utils.rollback_transaction(conn)
            print(f"事务回滚: {e}")

# 使用示例
basic_transaction()
```

##### 使用事务上下文管理器（推荐）

```python
import db_utils

def transaction_context_manager():
    """使用事务上下文管理器"""
    with db_utils.get_db_connection() as conn:
        try:
            with db_utils.transaction(conn):
                # 在事务中执行多个操作
                order_id = db_utils.insert_record(conn, 'orders', {
                    'user_id': 1,
                    'total_amount': 1499.99,
                    'status': 'pending'
                })

                # 添加多个订单项
                items = [
                    {'order_id': order_id, 'product_id': 1, 'quantity': 1, 'unit_price': 999.99},
                    {'order_id': order_id, 'product_id': 2, 'quantity': 1, 'unit_price': 499.99}
                ]
                db_utils.insert_records(conn, 'order_items', items)

                # 如果所有操作成功，事务会自动提交
                print("订单创建成功")

        except Exception as e:
            # 如果发生错误，事务会自动回滚
            print(f"订单创建失败: {e}")

# 使用示例
transaction_context_manager()
```

##### 复杂事务示例

```python
import db_utils

def complex_transaction_example():
    """复杂事务示例：银行转账"""
    with db_utils.get_db_connection() as conn:
        try:
            with db_utils.transaction(conn):
                # 检查账户余额
                from_account = db_utils.fetch_one(
                    conn,
                    "SELECT * FROM accounts WHERE id = ? FOR UPDATE",
                    (1,)
                )

                if not from_account:
                    raise ValueError("转出账户不存在")

                if from_account['balance'] < 1000:
                    raise ValueError("余额不足")

                # 转入账户
                to_account = db_utils.fetch_one(
                    conn,
                    "SELECT * FROM accounts WHERE id = ? FOR UPDATE",
                    (2,)
                )

                if not to_account:
                    raise ValueError("转入账户不存在")

                # 执行转账
                transfer_amount = 1000

                # 扣除转出账户余额
                db_utils.update_record(
                    conn, 'accounts',
                    {'balance': from_account['balance'] - transfer_amount},
                    'id = ?', (from_account['id'],)
                )

                # 增加转入账户余额
                db_utils.update_record(
                    conn, 'accounts',
                    {'balance': to_account['balance'] + transfer_amount},
                    'id = ?', (to_account['id'],)
                )

                # 记录转账日志
                db_utils.insert_record(conn, 'transfer_logs', {
                    'from_account_id': from_account['id'],
                    'to_account_id': to_account['id'],
                    'amount': transfer_amount,
                    'status': 'completed'
                })

                print(f"转账成功: {transfer_amount} 元")

        except ValueError as e:
            print(f"转账失败: {e}")
        except Exception as e:
            print(f"转账失败: {e}")

# 使用示例
complex_transaction_example()
```

#### 复杂查询

##### 多表连接查询

```python
import db_utils

def join_query_example():
    """多表连接查询示例"""
    with db_utils.get_db_connection() as conn:
        # 查询用户及其订单信息
        query = """
            SELECT
                u.name as user_name,
                u.email,
                COUNT(o.id) as order_count,
                SUM(o.total_amount) as total_spent,
                MAX(o.created_at) as last_order_date
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.name, u.email
            HAVING order_count > 0
            ORDER BY total_spent DESC
        """

        results = db_utils.fetch_all(conn, query)

        print("用户订单统计:")
        for result in results:
            print(f"用户: {result['user_name']}")
            print(f"  邮箱: {result['email']}")
            print(f"  订单数: {result['order_count']}")
            print(f"  总消费: ¥{result['total_spent']:.2f}")
            print(f"  最后订单: {result['last_order_date']}")
            print()

# 使用示例
join_query_example()
```

##### 子查询示例

```python
import db_utils

def subquery_example():
    """子查询示例"""
    with db_utils.get_db_connection() as conn:
        # 查询消费额高于平均水平的用户
        query = """
            SELECT u.name, u.email,
                   (SELECT SUM(o.total_amount) FROM orders o WHERE o.user_id = u.id) as total_spent
            FROM users u
            WHERE u.id IN (
                SELECT DISTINCT user_id
                FROM orders
                WHERE total_amount > (
                    SELECT AVG(total_amount)
                    FROM orders
                )
            )
        """

        results = db_utils.fetch_all(conn, query)

        print("消费额高于平均水平的用户:")
        for result in results:
            print(f"  {result['name']} ({result['email']}) - ¥{result['total_spent']:.2f}")

# 使用示例
subquery_example()
```

##### 分页查询

```python
import db_utils

def pagination_example():
    """分页查询示例"""
    def get_paginated_results(table, page=1, per_page=10, **conditions):
        """通用分页查询函数"""
        offset = (page - 1) * per_page

        # 构建WHERE条件
        where_clauses = []
        params = []

        for field, value in conditions.items():
            if isinstance(value, (list, tuple)):
                where_clauses.append(f"{field} IN ({','.join(['?']*len(value))})")
                params.extend(value)
            else:
                where_clauses.append(f"{field} = ?")
                params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

        with db_utils.get_db_connection() as conn:
            # 获取总数
            count_query = f"SELECT COUNT(*) FROM {table} WHERE {where_clause}"
            total_count = db_utils.fetch_value(conn, count_query, tuple(params))

            # 获取分页数据
            data_query = f"""
                SELECT * FROM {table}
                WHERE {where_clause}
                ORDER BY id DESC
                LIMIT ? OFFSET ?
            """
            data_params = tuple(params) + (per_page, offset)
            data = db_utils.fetch_all(conn, data_query, data_params)

            return {
                'data': data,
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }

    # 使用分页查询
    page_data = get_paginated_results('users', page=1, per_page=5, is_active=True)

    print(f"第 {page_data['page']} 页 / 共 {page_data['total_pages']} 页")
    print(f"每页 {page_data['per_page']} 条 / 共 {page_data['total_count']} 条")
    print()

    for user in page_data['data']:
        print(f"  {user['name']} ({user['email']})")

# 使用示例
pagination_example()
```

#### 视图和触发器

##### 创建视图

```python
import db_utils

def create_views_example():
    """创建视图示例"""
    with db_utils.get_db_connection() as conn:

        # 创建用户订单汇总视图
        db_utils.execute_query(conn, """
            CREATE VIEW IF NOT EXISTS user_order_summary AS
            SELECT
                u.id as user_id,
                u.username,
                u.email,
                COUNT(o.id) as order_count,
                COALESCE(SUM(o.total_amount), 0) as total_spent,
                MAX(o.created_at) as last_order_date
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.username, u.email
        """)

        # 创建产品库存视图
        db_utils.execute_query(conn, """
            CREATE VIEW IF NOT EXISTS product_inventory_view AS
            SELECT
                p.id,
                p.name,
                p.sku,
                p.price,
                p.stock_quantity,
                c.name as category_name,
                CASE
                    WHEN p.stock_quantity = 0 THEN 'out_of_stock'
                    WHEN p.stock_quantity < 10 THEN 'low_stock'
                    ELSE 'in_stock'
                END as stock_status
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
        """)

        print("视图创建完成")

        # 查询视图
        user_summary = db_utils.fetch_all(conn, "SELECT * FROM user_order_summary")
        print(f"用户订单汇总记录数: {len(user_summary)}")

        inventory = db_utils.fetch_all(conn, "SELECT * FROM product_inventory_view")
        print(f"产品库存记录数: {len(inventory)}")

# 使用示例
create_views_example()
```

##### 创建触发器

```python
import db_utils

def create_triggers_example():
    """创建触发器示例"""
    with db_utils.get_db_connection() as conn:

        # 创建更新时间戳触发器
        db_utils.execute_query(conn, """
            CREATE TRIGGER IF NOT EXISTS update_users_timestamp
            AFTER UPDATE ON users
            FOR EACH ROW
            BEGIN
                UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)

        # 创建库存检查触发器
        db_utils.execute_query(conn, """
            CREATE TRIGGER IF NOT EXISTS check_stock_before_order
            BEFORE INSERT ON order_items
            FOR EACH ROW
            BEGIN
                SELECT CASE
                    WHEN (SELECT stock_quantity FROM products WHERE id = NEW.product_id) < NEW.quantity
                    THEN RAISE(ABORT, 'Insufficient stock')
                END;
            END
        """)

        # 创建审计日志触发器
        db_utils.execute_query(conn, """
            CREATE TRIGGER IF NOT EXISTS log_user_changes
            AFTER UPDATE ON users
            FOR EACH ROW
            BEGIN
                INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, changed_by, changed_at)
                VALUES ('users', NEW.id, 'UPDATE',
                        json_object('username', OLD.username, 'email', OLD.email),
                        json_object('username', NEW.username, 'email', NEW.email),
                        CURRENT_USER, CURRENT_TIMESTAMP);
            END
        """)

        print("触发器创建完成")

# 使用示例
create_triggers_example()
```

#### 数据导入导出

##### CSV 导入导出

```python
import db_utils
import csv

def csv_export_example():
    """CSV导出示例"""
    def export_table_to_csv(table_name, csv_path):
        """导出表到CSV"""
        with db_utils.get_db_connection() as conn:
            # 获取表结构
            table_info = db_utils.get_table_info(conn, table_name)
            columns = [col['name'] for col in table_info]

            # 获取数据
            data = db_utils.fetch_all(conn, f"SELECT * FROM {table_name}")

            # 写入CSV
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                writer.writerows(data)

            print(f"导出完成: {len(data)} 条记录到 {csv_path}")

    # 导出用户表
    export_table_to_csv('users', 'data/users_export.csv')

def csv_import_example():
    """CSV导入示例"""
    def import_csv_to_table(csv_path, table_name):
        """从CSV导入数据"""
        with db_utils.get_db_connection() as conn:
            # 读取CSV
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

            if not data:
                print("CSV文件为空")
                return

            # 批量插入
            with db_utils.transaction(conn):
                for record in data:
                    # 移除空值
                    record = {k: v for k, v in record.items() if v and v.strip()}
                    db_utils.insert_record(conn, table_name, record)

            print(f"导入完成: {len(data)} 条记录")

    # 导入用户数据
    import_csv_to_table('data/users_export.csv', 'users')

# 使用示例
csv_export_example()
csv_import_example()
```

##### JSON 导入导出

```python
import db_utils
import json

def json_export_example():
    """JSON导出示例"""
    def export_table_to_json(table_name, json_path):
        """导出表到JSON"""
        with db_utils.get_db_connection() as conn:
            # 获取数据
            data = db_utils.fetch_all(conn, f"SELECT * FROM {table_name}")

            # 写入JSON
            with open(json_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=2, default=str)

            print(f"导出完成: {len(data)} 条记录到 {json_path}")

    # 导出用户表
    export_table_to_json('users', 'data/users_export.json')

def json_import_example():
    """JSON导入示例"""
    def import_json_to_table(json_path, table_name):
        """从JSON导入数据"""
        with db_utils.get_db_connection() as conn:
            # 读取JSON
            with open(json_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

            if not data:
                print("JSON文件为空")
                return

            # 批量插入
            with db_utils.transaction(conn):
                for record in data:
                    db_utils.insert_record(conn, table_name, record)

            print(f"导入完成: {len(data)} 条记录")

    # 导入用户数据
    import_json_to_table('data/users_export.json', 'users')

# 使用示例
json_export_example()
json_import_example()
```

---

## 🔧 API 参考

### 连接管理

#### `get_connection() -> sqlite3.Connection`

获取数据库连接对象。

**返回值:**

- `sqlite3.Connection`: 数据库连接对象

**示例:**

```python
conn = db_utils.get_connection()
# 使用连接...
conn.close()
```

#### `get_db_connection() -> ContextManager`

数据库连接上下文管理器，自动管理连接的打开和关闭。

**返回值:**

- `ContextManager`: 连接上下文管理器

**示例:**

```python
with db_utils.get_db_connection() as conn:
    # 使用连接...
    pass  # 连接会自动关闭
```

### 基本操作

#### `insert_record(conn: sqlite3.Connection, table: str, data: Dict[str, Any]) -> int`

插入单条记录。

**参数:**

- `conn`: 数据库连接
- `table`: 表名
- `data`: 数据字典

**返回值:**

- `int`: 插入记录的 ID

**示例:**

```python
user_id = db_utils.insert_record(conn, 'users', {
    'name': '张三',
    'email': 'zhangsan@example.com',
    'age': 25
})
```

#### `insert_records(conn: sqlite3.Connection, table: str, data_list: List[Dict[str, Any]]) -> List[int]`

批量插入记录。

**参数:**

- `conn`: 数据库连接
- `table`: 表名
- `data_list`: 数据字典列表

**返回值:**

- `List[int]`: 插入记录的 ID 列表

**示例:**

```python
products = [
    {'name': '产品A', 'price': 99.99},
    {'name': '产品B', 'price': 199.99}
]
product_ids = db_utils.insert_records(conn, 'products', products)
```

#### `update_record(conn: sqlite3.Connection, table: str, data: Dict[str, Any], where_clause: str, where_params: Tuple) -> int`

更新记录。

**参数:**

- `conn`: 数据库连接
- `table`: 表名
- `data`: 要更新的数据
- `where_clause`: WHERE 条件
- `where_params`: WHERE 参数

**返回值:**

- `int`: 受影响的行数

**示例:**

```python
affected = db_utils.update_record(
    conn, 'users',
    {'age': 26},
    'id = ?', (1,)
)
```

#### `delete_record(conn: sqlite3.Connection, table: str, where_clause: str, where_params: Tuple) -> int`

删除记录。

**参数:**

- `conn`: 数据库连接
- `table`: 表名
- `where_clause`: WHERE 条件
- `where_params`: WHERE 参数

**返回值:**

- `int`: 受影响的行数

**示例:**

```python
affected = db_utils.delete_record(
    conn, 'users',
    'id = ?', (1,)
)
```

### 查询操作

#### `fetch_all(conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]`

获取所有查询结果。

**参数:**

- `conn`: 数据库连接
- `sql`: SQL 语句
- `params`: 参数元组（可选）

**返回值:**

- `List[Dict]`: 查询结果列表

**示例:**

```python
users = db_utils.fetch_all(conn, "SELECT * FROM users WHERE age > ?", (25,))
```

#### `fetch_one(conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]`

获取单个查询结果。

**参数:**

- `conn`: 数据库连接
- `sql`: SQL 语句
- `params`: 参数元组（可选）

**返回值:**

- `Optional[Dict]`: 查询结果字典，如果没有结果则返回 None

**示例:**

```python
user = db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (1,))
```

#### `fetch_value(conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None) -> Any`

获取单个值。

**参数:**

- `conn`: 数据库连接
- `sql`: SQL 语句
- `params`: 参数元组（可选）

**返回值:**

- `Any`: 查询结果值

**示例:**

```python
count = db_utils.fetch_value(conn, "SELECT COUNT(*) FROM users")
```

### 表操作

#### `table_exists(conn: sqlite3.Connection, table_name: str) -> bool`

检查表是否存在。

**参数:**

- `conn`: 数据库连接
- `table_name`: 表名

**返回值:**

- `bool`: 表是否存在

**示例:**

```python
if db_utils.table_exists(conn, 'users'):
    print("users表存在")
```

#### `get_table_info(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]`

获取表结构信息。

**参数:**

- `conn`: 数据库连接
- `table_name`: 表名

**返回值:**

- `List[Dict]`: 表结构信息列表

**示例:**

```python
info = db_utils.get_table_info(conn, 'users')
for column in info:
    print(f"{column['name']}: {column['type']}")
```

#### `execute_sql_file(conn: sqlite3.Connection, file_path: str) -> None`

执行 SQL 文件。

**参数:**

- `conn`: 数据库连接
- `file_path`: SQL 文件路径

**示例:**

```python
db_utils.execute_sql_file(conn, 'data/sql_schema.sql')
```

### 事务管理

#### `begin_transaction(conn: sqlite3.Connection) -> None`

开始事务。

**参数:**

- `conn`: 数据库连接

**示例:**

```python
db_utils.begin_transaction(conn)
```

#### `commit_transaction(conn: sqlite3.Connection) -> None`

提交事务。

**参数:**

- `conn`: 数据库连接

**示例:**

```python
db_utils.commit_transaction(conn)
```

#### `rollback_transaction(conn: sqlite3.Connection) -> None`

回滚事务。

**参数:**

- `conn`: 数据库连接

**示例:**

```python
db_utils.rollback_transaction(conn)
```

#### `transaction(conn: sqlite3.Connection) -> ContextManager`

事务上下文管理器。

**参数:**

- `conn`: 数据库连接

**返回值:**

- `ContextManager`: 事务上下文管理器

**示例:**

```python
with db_utils.transaction(conn):
    # 执行事务操作
    pass
```

### 工具函数

#### `get_database_stats(conn: sqlite3.Connection) -> Dict[str, Any]`

获取数据库统计信息。

**参数:**

- `conn`: 数据库连接

**返回值:**

- `Dict`: 数据库统计信息

**示例:**

```python
stats = db_utils.get_database_stats(conn)
print(f"数据库大小: {stats['size_mb']} MB")
```

#### `backup_database(source_path: str, backup_path: str) -> None`

备份数据库。

**参数:**

- `source_path`: 源数据库路径
- `backup_path`: 备份数据库路径

**示例:**

```python
db_utils.backup_database('data/app.db', 'data/backup.db')
```

---

## 🎯 最佳实践

### 连接管理

#### ✅ 推荐做法

```python
# 使用上下文管理器（推荐）
with db_utils.get_db_connection() as conn:
    # 执行数据库操作
    result = db_utils.fetch_all(conn, "SELECT * FROM users")
```

#### ❌ 避免做法

```python
# 避免忘记关闭连接
conn = db_utils.get_connection()
result = db_utils.fetch_all(conn, "SELECT * FROM users")
# 忘记调用 conn.close()
```

### 参数化查询

#### ✅ 推荐做法

```python
# 使用参数化查询防止SQL注入
with db_utils.get_db_connection() as conn:
    user = db_utils.fetch_one(
        conn,
        "SELECT * FROM users WHERE email = ?",
        ('user@example.com',)
    )
```

#### ❌ 避免做法

```python
# 避免字符串拼接（SQL注入风险）
with db_utils.get_db_connection() as conn:
    email = "user@example.com"
    query = f"SELECT * FROM users WHERE email = '{email}'"  # 危险！
    user = db_utils.fetch_one(conn, query)
```

### 事务管理

#### ✅ 推荐做法

```python
# 使用事务上下文管理器
with db_utils.get_db_connection() as conn:
    try:
        with db_utils.transaction(conn):
            # 执行多个相关操作
            order_id = db_utils.insert_record(conn, 'orders', order_data)
            db_utils.insert_record(conn, 'order_items', item_data)
            # 事务会自动提交
    except Exception as e:
        # 事务会自动回滚
        print(f"操作失败: {e}")
```

#### ❌ 避免做法

```python
# 避免手动管理事务（容易出错）
conn = db_utils.get_connection()
try:
    db_utils.begin_transaction(conn)
    # 执行操作...
    db_utils.commit_transaction(conn)
except Exception as e:
    db_utils.rollback_transaction(conn)
finally:
    conn.close()
```

### 错误处理

#### ✅ 推荐做法

```python
# 具体的错误处理
def create_user(user_data):
    try:
        with db_utils.get_db_connection() as conn:
            return db_utils.insert_record(conn, 'users', user_data)
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise ValueError("邮箱已存在")
        else:
            raise
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"数据库操作失败: {e}")
```

#### ❌ 避免做法

```python
# 过于宽泛的错误处理
def create_user(user_data):
    try:
        with db_utils.get_db_connection() as conn:
            return db_utils.insert_record(conn, 'users', user_data)
    except Exception as e:
        print("出错了")  # 没有具体的错误信息
        return None
```

### 性能优化

#### ✅ 推荐做法

```python
# 批量操作
def import_users(users_data):
    with db_utils.get_db_connection() as conn:
        return db_utils.insert_records(conn, 'users', users_data)

# 使用索引
def create_indexes():
    with db_utils.get_db_connection() as conn:
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

# 分页查询
def get_users_page(page=1, per_page=10):
    with db_utils.get_db_connection() as conn:
        offset = (page - 1) * per_page
        return db_utils.fetch_all(
            conn,
            "SELECT * FROM users LIMIT ? OFFSET ?",
            (per_page, offset)
        )
```

#### ❌ 避免做法

```python
# 避免N+1查询问题
def get_users_with_orders():
    with db_utils.get_db_connection() as conn:
        users = db_utils.fetch_all(conn, "SELECT * FROM users")
        for user in users:
            # 每个用户都执行一次查询（N+1问题）
            orders = db_utils.fetch_all(conn, "SELECT * FROM orders WHERE user_id = ?", (user['id'],))
            user['orders'] = orders
        return users

# 应该使用JOIN查询
def get_users_with_orders():
    with db_utils.get_db_connection() as conn:
        return db_utils.fetch_all(conn, """
            SELECT u.*, o.id as order_id, o.total_amount
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
        """)
```

### 数据库设计

#### ✅ 推荐做法

```python
# 使用合适的数据类型
def create_users_table():
    with db_utils.get_db_connection() as conn:
        db_utils.execute_query(conn, """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER CHECK (age >= 0 AND age <= 150),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)

# 使用外键约束
def create_orders_table():
    with db_utils.get_db_connection() as conn:
        db_utils.execute_query(conn, """
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL CHECK (total_amount >= 0),
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
```

#### ❌ 避免做法

```python
# 避免不合适的约束和类型
def create_bad_table():
    with db_utils.get_db_connection() as conn:
        db_utils.execute_query(conn, """
            CREATE TABLE bad_table (
                id TEXT,  # 应该使用INTEGER
                name TEXT,
                age TEXT,  # 应该使用INTEGER
                email TEXT  # 缺少UNIQUE约束
            )
        """)
```

### 测试策略

#### ✅ 推荐做法

```python
# 使用内存数据库进行测试
import unittest
import tempfile

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # 创建临时数据库
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()

        # 修改配置使用临时数据库
        original_db = db_config.DB_CONFIG['database']
        db_config.DB_CONFIG['database'] = self.temp_db.name

        # 创建测试表
        with db_utils.get_db_connection() as conn:
            db_utils.execute_query(conn, """
                CREATE TABLE test_table (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)

    def tearDown(self):
        # 恢复原始配置
        db_config.DB_CONFIG['database'] = original_db
        # 删除临时数据库
        import os
        os.unlink(self.temp_db.name)

    def test_insert(self):
        with db_utils.get_db_connection() as conn:
            test_id = db_utils.insert_record(conn, 'test_table', {'name': 'test'})
            self.assertIsNotNone(test_id)
```

#### ❌ 避免做法

```python
# 避免在生产数据库上测试
def test_insert():
    # 直接在生产数据库上测试（危险！）
    with db_utils.get_db_connection() as conn:
        db_utils.insert_record(conn, 'users', {'name': 'test_user'})
```

---

## ❓ 常见问题

### 连接问题

#### Q: 如何解决 "sqlite3.OperationalError: unable to open database file" 错误？

**A:** 这个错误通常是由于数据库文件路径不正确或权限不足导致的。解决方法：

```python
# 检查数据库路径
import db_config
print(f"数据库路径: {db_config.DB_CONFIG['database']}")

# 确保目录存在
import os
db_dir = os.path.dirname(db_config.DB_CONFIG['database'])
os.makedirs(db_dir, exist_ok=True)

# 检查文件权限
if os.path.exists(db_config.DB_CONFIG['database']):
    print(f"文件可读: {os.access(db_config.DB_CONFIG['database'], os.R_OK)}")
    print(f"文件可写: {os.access(db_config.DB_CONFIG['database'], os.W_OK)}")
```

#### Q: 如何处理多线程访问问题？

**A:** SQLite 默认不支持多线程写入，但可以通过配置支持：

```python
# 在db_config.py中设置
DB_CONFIG = {
    'database': 'app.db',
    'check_same_thread': False,  # 允许多线程访问
    'timeout': 30.0,
    'isolation_level': None,  # 自动提交模式
}

# 或者使用连接池
import threading
from contextlib import contextmanager

# 线程本地存储
thread_local = threading.local()

@contextmanager
def get_thread_connection():
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = db_utils.get_connection()
    try:
        yield thread_local.connection
    finally:
        # 不关闭连接，保持线程本地
        pass
```

### 性能问题

#### Q: 批量插入很慢，如何优化？

**A:** 批量插入性能优化方法：

```python
def optimized_bulk_insert(data_list, batch_size=1000):
    """优化的批量插入"""
    with db_utils.get_db_connection() as conn:
        # 开始事务
        db_utils.begin_transaction(conn)

        try:
            # 分批插入
            for i in range(0, len(data_list), batch_size):
                batch = data_list[i:i + batch_size]
                db_utils.insert_records(conn, 'table_name', batch)

                # 定期提交以避免内存问题
                if i % 5000 == 0:
                    db_utils.commit_transaction(conn)
                    db_utils.begin_transaction(conn)

            # 提交剩余的事务
            db_utils.commit_transaction(conn)

        except Exception as e:
            db_utils.rollback_transaction(conn)
            raise e

# 使用优化插入
large_data = [{'name': f'item_{i}'} for i in range(10000)]
optimized_bulk_insert(large_data)
```

#### Q: 查询很慢，如何优化？

**A:** 查询性能优化方法：

```python
def optimize_queries():
    """优化查询性能"""
    with db_utils.get_db_connection() as conn:
        # 创建索引
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)")

        # 分析数据库
        db_utils.execute_query(conn, "ANALYZE")

        # 使用EXPLAIN分析查询计划
        plan = db_utils.fetch_all(conn, "EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = ?", ('test@example.com',))
        print("查询计划:", plan)

# 使用优化的查询
def get_user_by_email(email):
    with db_utils.get_db_connection() as conn:
        # 只选择需要的列
        return db_utils.fetch_one(
            conn,
            "SELECT id, name, email FROM users WHERE email = ?",
            (email,)
        )
```

### 数据完整性问题

#### Q: 如何处理并发写入冲突？

**A:** 并发写入冲突处理方法：

```python
def safe_update_record(table, data, where_clause, where_params, max_retries=3):
    """安全的记录更新（带重试机制）"""
    for attempt in range(max_retries):
        try:
            with db_utils.get_db_connection() as conn:
                # 开始事务
                db_utils.begin_transaction(conn)

                # 检查记录是否存在
                existing = db_utils.fetch_one(conn, f"SELECT * FROM {table} WHERE {where_clause}", where_params)
                if not existing:
                    raise ValueError("记录不存在")

                # 更新记录
                affected = db_utils.update_record(conn, table, data, where_clause, where_params)

                # 提交事务
                db_utils.commit_transaction(conn)
                return affected

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                # 等待后重试
                import time
                time.sleep(0.1 * (attempt + 1))
                continue
            else:
                raise e

    raise Exception(f"更新失败，超过最大重试次数 {max_retries}")

# 使用安全更新
affected = safe_update_record(
    'users',
    {'age': 26},
    'id = ?', (1,)
)
```

#### Q: 如何处理外键约束错误？

**A:** 外键约束错误处理方法：

```python
def safe_delete_record(table, where_clause, where_params):
    """安全的记录删除（处理外键约束）"""
    try:
        with db_utils.get_db_connection() as conn:
            # 检查是否有相关记录
            if table == 'users':
                # 检查用户是否有订单
                user_id = where_params[0] if 'id = ?' in where_clause else None
                if user_id:
                    order_count = db_utils.fetch_value(
                        conn,
                        "SELECT COUNT(*) FROM orders WHERE user_id = ?",
                        (user_id,)
                    )
                    if order_count > 0:
                        raise ValueError(f"无法删除用户，该用户有 {order_count} 个订单")

            # 执行删除
            return db_utils.delete_record(conn, table, where_clause, where_params)

    except sqlite3.IntegrityError as e:
        if "FOREIGN KEY constraint failed" in str(e):
            raise ValueError("无法删除记录，存在相关的外键约束")
        else:
            raise

# 使用安全删除
try:
    affected = safe_delete_record('users', 'id = ?', (1,))
    print(f"删除了 {affected} 条记录")
except ValueError as e:
    print(f"删除失败: {e}")
```

### 内存和磁盘问题

#### Q: 数据库文件过大，如何清理？

**A:** 数据库清理方法：

```python
def cleanup_database():
    """清理数据库"""
    with db_utils.get_db_connection() as conn:
        try:
            # 开始事务
            db_utils.begin_transaction(conn)

            # 删除过期数据（示例：删除30天前的日志）
            db_utils.execute_query(conn, """
                DELETE FROM logs
                WHERE created_at < datetime('now', '-30 days')
            """)

            # 清理孤立记录
            db_utils.execute_query(conn, """
                DELETE FROM order_items
                WHERE order_id NOT IN (SELECT id FROM orders)
            """)

            # 提交事务
            db_utils.commit_transaction(conn)

            # 执行VACUUM清理数据库文件
            db_utils.execute_query(conn, "VACUUM")

            print("数据库清理完成")

        except Exception as e:
            db_utils.rollback_transaction(conn)
            print(f"数据库清理失败: {e}")
            raise

# 执行清理
cleanup_database()
```

#### Q: 如何处理内存不足问题？

**A:** 内存优化方法：

```python
def memory_efficient_query(query, params=None, batch_size=1000):
    """内存高效的查询（分批处理）"""
    with db_utils.get_db_connection() as conn:
        offset = 0
        while True:
            # 分批查询
            batch_query = f"{query} LIMIT ? OFFSET ?"
            batch_params = (batch_size, offset) + (params or ())

            results = db_utils.fetch_all(conn, batch_query, batch_params)

            if not results:
                break

            # 处理当前批次
            for result in results:
                yield result

            offset += batch_size

# 使用内存高效查询
for user in memory_efficient_query("SELECT * FROM users"):
    # 处理每个用户
    process_user(user)
```

### 调试和日志问题

#### Q: 如何启用详细的 SQL 日志？

**A:** 启用 SQL 日志的方法：

```python
# 在db_config.py中设置
LOG_QUERIES = True
LOG_FILE = 'data/detailed_db.log'

# 或者自定义日志配置
def setup_detailed_logging():
    import logging

    # 创建详细日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # 配置根日志记录器
    logger = logging.getLogger('db_utils')
    logger.setLevel(logging.DEBUG)

    # 文件处理器
    file_handler = logging.FileHandler('data/detailed_db.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# 启用详细日志
setup_detailed_logging()
```

#### Q: 如何调试复杂的 SQL 查询？

**A:** SQL 查询调试方法：

```python
def debug_query(query, params=None):
    """调试SQL查询"""
    print(f"调试查询: {query}")
    if params:
        print(f"参数: {params}")

    try:
        with db_utils.get_db_connection() as conn:
            # 获取查询计划
            plan = db_utils.fetch_all(conn, f"EXPLAIN QUERY PLAN {query}", params)
            print("查询计划:")
            for row in plan:
                print(f"  {row}")

            # 执行查询
            results = db_utils.fetch_all(conn, query, params)
            print(f"查询结果: {len(results)} 行")

            return results

    except Exception as e:
        print(f"查询失败: {e}")
        raise

# 使用调试查询
results = debug_query("""
    SELECT u.name, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.age > ?
    GROUP BY u.id
    HAVING order_count > 0
""", (25,))
```

---

## 💻 示例代码

### 完整的用户管理系统

```python
"""
完整的用户管理系统示例
展示SQLite框架的实际应用
"""

import db_utils
import db_config
from typing import List, Dict, Optional, Tuple
import sqlite3
from datetime import datetime

class UserManager:
    """用户管理器"""

    def __init__(self):
        """初始化用户管理器"""
        self.ensure_database()

    def ensure_database(self):
        """确保数据库和表存在"""
        with db_utils.get_db_connection() as conn:
            if not db_utils.table_exists(conn, 'users'):
                self.create_users_table(conn)

    def create_users_table(self, conn: sqlite3.Connection):
        """创建用户表"""
        db_utils.execute_query(conn, """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                age INTEGER CHECK (age >= 0 AND age <= 150),
                phone TEXT,
                address TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,

                -- 约束条件
                CONSTRAINT email_format CHECK (email LIKE '%@%.%'),
                CONSTRAINT phone_format CHECK (phone IS NULL OR length(phone) >= 10)
            )
        """)

        # 创建索引
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)")

    def create_user(self, user_data: Dict) -> Tuple[Optional[int], Optional[str]]:
        """
        创建用户
        Args:
            user_data: 用户数据字典
        Returns:
            (user_id, error_message)
        """
        try:
            # 验证必填字段
            required_fields = ['username', 'email', 'password_hash', 'full_name']
            for field in required_fields:
                if field not in user_data:
                    return None, f"缺少必填字段: {field}"

            # 验证邮箱格式
            if '@' not in user_data['email']:
                return None, "邮箱格式不正确"

            # 验证年龄
            if 'age' in user_data and (user_data['age'] < 0 or user_data['age'] > 150):
                return None, "年龄必须在0-150之间"

            with db_utils.get_db_connection() as conn:
                user_id = db_utils.insert_record(conn, 'users', user_data)
                return user_id, None

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: users.username" in str(e):
                return None, "用户名已存在"
            elif "UNIQUE constraint failed: users.email" in str(e):
                return None, "邮箱已存在"
            else:
                return None, f"数据完整性错误: {e}"
        except Exception as e:
            return None, f"创建用户失败: {e}"

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """根据ID获取用户"""
        with db_utils.get_db_connection() as conn:
            return db_utils.fetch_one(conn, "SELECT * FROM users WHERE id = ?", (user_id,))

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """根据用户名获取用户"""
        with db_utils.get_db_connection() as conn:
            return db_utils.fetch_one(conn, "SELECT * FROM users WHERE username = ?", (username,))

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """根据邮箱获取用户"""
        with db_utils.get_db_connection() as conn:
            return db_utils.fetch_one(conn, "SELECT * FROM users WHERE email = ?", (email,))

    def update_user(self, user_id: int, update_data: Dict) -> Tuple[bool, Optional[str]]:
        """
        更新用户信息
        Args:
            user_id: 用户ID
            update_data: 更新数据
        Returns:
            (success, error_message)
        """
        try:
            # 检查用户是否存在
            user = self.get_user_by_id(user_id)
            if not user:
                return False, "用户不存在"

            # 验证数据
            if 'email' in update_data and '@' not in update_data['email']:
                return False, "邮箱格式不正确"

            if 'age' in update_data and (update_data['age'] < 0 or update_data['age'] > 150):
                return False, "年龄必须在0-150之间"

            # 移除不允许更新的字段
            protected_fields = ['id', 'created_at', 'password_hash']
            for field in protected_fields:
                update_data.pop(field, None)

            if not update_data:
                return False, "没有要更新的数据"

            with db_utils.get_db_connection() as conn:
                affected = db_utils.update_record(
                    conn, 'users', update_data, 'id = ?', (user_id,)
                )

                if affected > 0:
                    return True, None
                else:
                    return False, "更新失败"

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: users.email" in str(e):
                return False, "邮箱已存在"
            else:
                return False, f"数据完整性错误: {e}"
        except Exception as e:
            return False, f"更新用户失败: {e}"

    def delete_user(self, user_id: int) -> Tuple[bool, Optional[str]]:
        """
        删除用户
        Args:
            user_id: 用户ID
        Returns:
            (success, error_message)
        """
        try:
            # 检查用户是否存在
            user = self.get_user_by_id(user_id)
            if not user:
                return False, "用户不存在"

            with db_utils.get_db_connection() as conn:
                affected = db_utils.delete_record(conn, 'users', 'id = ?', (user_id,))

                if affected > 0:
                    return True, None
                else:
                    return False, "删除失败"

        except Exception as e:
            return False, f"删除用户失败: {e}"

    def list_users(self, page: int = 1, per_page: int = 10,
                   active_only: bool = True,
                   search_term: str = None) -> Dict:
        """
        列出用户
        Args:
            page: 页码
            per_page: 每页数量
            active_only: 是否只显示活跃用户
            search_term: 搜索关键词
        Returns:
            分页结果字典
        """
        offset = (page - 1) * per_page

        # 构建查询条件
        conditions = []
        params = []

        if active_only:
            conditions.append("is_active = ?")
            params.append(True)

        if search_term:
            conditions.append("(username LIKE ? OR email LIKE ? OR full_name LIKE ?)")
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        with db_utils.get_db_connection() as conn:
            # 获取总数
            count_query = f"SELECT COUNT(*) FROM users WHERE {where_clause}"
            total_count = db_utils.fetch_value(conn, count_query, tuple(params))

            # 获取分页数据
            data_query = f"""
                SELECT id, username, email, full_name, age, phone, is_active, created_at, last_login
                FROM users
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """
            data_params = tuple(params) + (per_page, offset)
            users = db_utils.fetch_all(conn, data_query, data_params)

            return {
                'data': users,
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }

    def update_last_login(self, user_id: int) -> bool:
        """更新用户最后登录时间"""
        try:
            with db_utils.get_db_connection() as conn:
                affected = db_utils.update_record(
                    conn, 'users',
                    {'last_login': datetime.now().isoformat()},
                    'id = ?', (user_id,)
                )
                return affected > 0
        except Exception:
            return False

    def change_password(self, user_id: int, new_password_hash: str) -> Tuple[bool, Optional[str]]:
        """
        修改用户密码
        Args:
            user_id: 用户ID
            new_password_hash: 新密码哈希
        Returns:
            (success, error_message)
        """
        try:
            with db_utils.get_db_connection() as conn:
                affected = db_utils.update_record(
                    conn, 'users',
                    {'password_hash': new_password_hash},
                    'id = ?', (user_id,)
                )

                if affected > 0:
                    return True, None
                else:
                    return False, "密码修改失败"

        except Exception as e:
            return False, f"密码修改失败: {e}"

    def get_user_statistics(self) -> Dict:
        """获取用户统计信息"""
        with db_utils.get_db_connection() as conn:
            stats = {}

            # 总用户数
            stats['total_users'] = db_utils.fetch_value(conn, "SELECT COUNT(*) FROM users")

            # 活跃用户数
            stats['active_users'] = db_utils.fetch_value(conn, "SELECT COUNT(*) FROM users WHERE is_active = TRUE")

            # 今日注册用户数
            stats['today_registrations'] = db_utils.fetch_value(
                conn,
                "SELECT COUNT(*) FROM users WHERE DATE(created_at) = DATE('now')"
            )

            # 本月注册用户数
            stats['month_registrations'] = db_utils.fetch_value(
                conn,
                "SELECT COUNT(*) FROM users WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')"
            )

            # 年龄分布
            age_distribution = db_utils.fetch_all(conn, """
                SELECT
                    CASE
                        WHEN age < 18 THEN 'Under 18'
                        WHEN age BETWEEN 18 AND 25 THEN '18-25'
                        WHEN age BETWEEN 26 AND 35 THEN '26-35'
                        WHEN age BETWEEN 36 AND 50 THEN '36-50'
                        ELSE 'Over 50'
                    END as age_group,
                    COUNT(*) as count
                FROM users
                WHERE age IS NOT NULL
                GROUP BY age_group
                ORDER BY
                    CASE age_group
                        WHEN 'Under 18' THEN 1
                        WHEN '18-25' THEN 2
                        WHEN '26-35' THEN 3
                        WHEN '36-50' THEN 4
                        ELSE 5
                    END
            """)
            stats['age_distribution'] = age_distribution

            return stats


# 使用示例
def main():
    """用户管理系统使用示例"""

    # 创建用户管理器
    user_manager = UserManager()

    print("=== 用户管理系统示例 ===")

    # 1. 创建用户
    print("\n1. 创建用户")
    user_data = {
        'username': 'john_doe',
        'email': 'john@example.com',
        'password_hash': 'hashed_password_123',
        'full_name': 'John Doe',
        'age': 30,
        'phone': '13800138000',
        'address': '北京市朝阳区'
    }

    user_id, error = user_manager.create_user(user_data)
    if error:
        print(f"创建用户失败: {error}")
    else:
        print(f"创建用户成功，ID: {user_id}")

    # 2. 查询用户
    print("\n2. 查询用户")
    user = user_manager.get_user_by_id(user_id)
    if user:
        print(f"用户信息: {user['full_name']} ({user['email']})")

    # 3. 更新用户
    print("\n3. 更新用户")
    success, error = user_manager.update_user(user_id, {
        'age': 31,
        'address': '北京市海淀区'
    })
    if error:
        print(f"更新用户失败: {error}")
    else:
        print("更新用户成功")

    # 4. 列出用户
    print("\n4. 列出用户")
    users = user_manager.list_users(page=1, per_page=5)
    print(f"第 {users['page']} 页 / 共 {users['total_pages']} 页")
    for user in users['data']:
        print(f"  {user['full_name']} ({user['email']}) - {'活跃' if user['is_active'] else '非活跃'}")

    # 5. 搜索用户
    print("\n5. 搜索用户")
    search_results = user_manager.list_users(search_term='john')
    print(f"找到 {len(search_results['data'])} 个匹配的用户")

    # 6. 获取统计信息
    print("\n6. 用户统计")
    stats = user_manager.get_user_statistics()
    print(f"总用户数: {stats['total_users']}")
    print(f"活跃用户数: {stats['active_users']}")
    print(f"今日注册: {stats['today_registrations']}")
    print(f"本月注册: {stats['month_registrations']}")
    print("年龄分布:")
    for age_group in stats['age_distribution']:
        print(f"  {age_group['age_group']}: {age_group['count']} 人")

    # 7. 更新最后登录时间
    print("\n7. 更新最后登录时间")
    success = user_manager.update_last_login(user_id)
    print(f"更新最后登录时间: {'成功' if success else '失败'}")

    # 8. 修改密码
    print("\n8. 修改密码")
    success, error = user_manager.change_password(user_id, 'new_hashed_password_456')
    if error:
        print(f"修改密码失败: {error}")
    else:
        print("修改密码成功")

    # 9. 删除用户
    print("\n9. 删除用户")
    success, error = user_manager.delete_user(user_id)
    if error:
        print(f"删除用户失败: {error}")
    else:
        print("删除用户成功")


if __name__ == '__main__':
    main()
```

### 数据迁移工具

```python
"""
数据迁移工具示例
展示如何使用SQLite框架进行数据迁移
"""

import db_utils
import db_config
import json
import csv
from typing import List, Dict, Any
import sqlite3
from datetime import datetime

class DataMigrator:
    """数据迁移器"""

    def __init__(self, source_config: Dict, target_config: Dict):
        """
        初始化数据迁移器
        Args:
            source_config: 源数据库配置
            target_config: 目标数据库配置
        """
        self.source_config = source_config
        self.target_config = target_config

    def migrate_table(self, table_name: str, transform_func=None) -> bool:
        """
        迁移单个表
        Args:
            table_name: 表名
            transform_func: 数据转换函数
        Returns:
            迁移是否成功
        """
        try:
            print(f"开始迁移表: {table_name}")

            # 连接源数据库
            source_conn = sqlite3.connect(**self.source_config)
            source_conn.row_factory = sqlite3.Row

            # 连接目标数据库
            target_conn = sqlite3.connect(**self.target_config)

            # 获取源数据
            source_data = db_utils.fetch_all(source_conn, f"SELECT * FROM {table_name}")
            print(f"  源数据记录数: {len(source_data)}")

            if not source_data:
                print("  无数据需要迁移")
                return True

            # 应用数据转换
            if transform_func:
                source_data = [transform_func(record) for record in source_data]

            # 批量插入目标数据库
            with db_utils.transaction(target_conn):
                for record in source_data:
                    db_utils.insert_record(target_conn, table_name, record)

            print(f"  迁移完成: {len(source_data)} 条记录")
            return True

        except Exception as e:
            print(f"  迁移失败: {e}")
            return False
        finally:
            source_conn.close()
            target_conn.close()

    def migrate_all_tables(self, table_mappings: Dict[str, str]) -> Dict[str, bool]:
        """
        迁移所有表
        Args:
            table_mappings: 表映射 {源表名: 目标表名}
        Returns:
            迁移结果字典
        """
        results = {}

        for source_table, target_table in table_mappings.items():
            try:
                print(f"\n迁移表: {source_table} -> {target_table}")

                # 连接源数据库
                source_conn = sqlite3.connect(**self.source_config)
                source_conn.row_factory = sqlite3.Row

                # 连接目标数据库
                target_conn = sqlite3.connect(**self.target_config)

                # 获取源数据
                source_data = db_utils.fetch_all(source_conn, f"SELECT * FROM {source_table}")
                print(f"  源数据记录数: {len(source_data)}")

                if not source_data:
                    print("  无数据需要迁移")
                    results[target_table] = True
                    continue

                # 批量插入目标数据库
                with db_utils.transaction(target_conn):
                    for record in source_data:
                        # 转换为字典
                        record_dict = dict(record)
                        db_utils.insert_record(target_conn, target_table, record_dict)

                print(f"  迁移完成: {len(source_data)} 条记录")
                results[target_table] = True

            except Exception as e:
                print(f"  迁移失败: {e}")
                results[target_table] = False
            finally:
                source_conn.close()
                target_conn.close()

        return results

    def backup_and_migrate(self, backup_path: str) -> bool:
        """
        备份并迁移数据库
        Args:
            backup_path: 备份文件路径
        Returns:
            是否成功
        """
        try:
            print(f"开始备份和迁移")
            print(f"备份路径: {backup_path}")

            # 备份源数据库
            source_path = self.source_config['database']
            db_utils.backup_database(source_path, backup_path)
            print("备份完成")

            # 获取所有表名
            source_conn = sqlite3.connect(**self.source_config)
            tables = db_utils.fetch_all(source_conn, "SELECT name FROM sqlite_master WHERE type='table'")
            source_conn.close()

            # 构建表映射
            table_mappings = {table['name']: table['name'] for table in tables}

            # 迁移所有表
            results = self.migrate_all_tables(table_mappings)

            # 输出结果
            success_count = sum(1 for result in results.values() if result)
            total_count = len(results)

            print(f"\n迁移完成: {success_count}/{total_count} 个表成功")

            return success_count == total_count

        except Exception as e:
            print(f"备份和迁移失败: {e}")
            return False


# 数据转换函数示例
def transform_user_data(user_data: Dict) -> Dict:
    """转换用户数据"""
    # 创建转换后的数据副本
    transformed = user_data.copy()

    # 重命名字段
    if 'user_name' in transformed:
        transformed['username'] = transformed.pop('user_name')

    # 添加默认值
    if 'is_active' not in transformed:
        transformed['is_active'] = True

    # 格式化日期
    if 'created_at' in transformed and transformed['created_at']:
        try:
            # 假设原始日期格式为 'YYYY-MM-DD'
            dt = datetime.strptime(transformed['created_at'], '%Y-%m-%d')
            transformed['created_at'] = dt.isoformat()
        except ValueError:
            transformed['created_at'] = datetime.now().isoformat()

    return transformed


# CSV导入导出工具
class CSVDataHandler:
    """CSV数据处理工具"""

    @staticmethod
    def export_to_csv(conn: sqlite3.Connection, table_name: str, csv_path: str) -> bool:
        """
        导出表数据到CSV
        Args:
            conn: 数据库连接
            table_name: 表名
            csv_path: CSV文件路径
        Returns:
            是否成功
        """
        try:
            print(f"导出表 {table_name} 到 {csv_path}")

            # 获取表结构
            table_info = db_utils.get_table_info(conn, table_name)
            columns = [col['name'] for col in table_info]

            # 获取数据
            data = db_utils.fetch_all(conn, f"SELECT * FROM {table_name}")

            # 写入CSV
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                writer.writerows(data)

            print(f"导出完成: {len(data)} 条记录")
            return True

        except Exception as e:
            print(f"导出失败: {e}")
            return False

    @staticmethod
    def import_from_csv(conn: sqlite3.Connection, table_name: str, csv_path: str) -> bool:
        """
        从CSV导入数据
        Args:
            conn: 数据库连接
            table_name: 表名
            csv_path: CSV文件路径
        Returns:
            是否成功
        """
        try:
            print(f"从 {csv_path} 导入数据到表 {table_name}")

            # 读取CSV
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

            if not data:
                print("CSV文件为空")
                return True

            # 批量插入
            with db_utils.transaction(conn):
                for record in data:
                    # 移除空值
                    record = {k: v for k, v in record.items() if v and v.strip()}
                    db_utils.insert_record(conn, table_name, record)

            print(f"导入完成: {len(data)} 条记录")
            return True

        except Exception as e:
            print(f"导入失败: {e}")
            return False


# JSON导入导出工具
class JSONDataHandler:
    """JSON数据处理工具"""

    @staticmethod
    def export_to_json(conn: sqlite3.Connection, table_name: str, json_path: str) -> bool:
        """
        导出表数据到JSON
        Args:
            conn: 数据库连接
            table_name: 表名
            json_path: JSON文件路径
        Returns:
            是否成功
        """
        try:
            print(f"导出表 {table_name} 到 {json_path}")

            # 获取数据
            data = db_utils.fetch_all(conn, f"SELECT * FROM {table_name}")

            # 写入JSON
            with open(json_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=2, default=str)

            print(f"导出完成: {len(data)} 条记录")
            return True

        except Exception as e:
            print(f"导出失败: {e}")
            return False

    @staticmethod
    def import_from_json(conn: sqlite3.Connection, table_name: str, json_path: str) -> bool:
        """
        从JSON导入数据
        Args:
            conn: 数据库连接
            table_name: 表名
            json_path: JSON文件路径
        Returns:
            是否成功
        """
        try:
            print(f"从 {json_path} 导入数据到表 {table_name}")

            # 读取JSON
            with open(json_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

            if not data:
                print("JSON文件为空")
                return True

            # 批量插入
            with db_utils.transaction(conn):
                for record in data:
                    db_utils.insert_record(conn, table_name, record)

            print(f"导入完成: {len(data)} 条记录")
            return True

        except Exception as e:
            print(f"导入失败: {e}")
            return False


# 使用示例
def main():
    """数据迁移工具使用示例"""

    print("=== 数据迁移工具示例 ===")

    # 1. 配置源数据库和目标数据库
    source_config = {
        'database': 'data/source.db',
        'timeout': 30.0,
        'check_same_thread': False
    }

    target_config = {
        'database': 'data/target.db',
        'timeout': 30.0,
        'check_same_thread': False
    }

    # 2. 创建数据迁移器
    migrator = DataMigrator(source_config, target_config)

    # 3. 备份并迁移数据库
    backup_path = 'data/backup_before_migration.db'
    success = migrator.backup_and_migrate(backup_path)

    if success:
        print("\n✅ 数据库迁移成功！")
    else:
        print("\n❌ 数据库迁移失败！")

    # 4. CSV导入导出示例
    print("\n=== CSV导入导出示例 ===")

    with db_utils.get_db_connection() as conn:
        # 导出用户表到CSV
        csv_path = 'data/users_export.csv'
        CSVDataHandler.export_to_csv(conn, 'users', csv_path)

        # 从CSV导入数据
        # CSVDataHandler.import_from_csv(conn, 'users', csv_path)

    # 5. JSON导入导出示例
    print("\n=== JSON导入导出示例 ===")

    with db_utils.get_db_connection() as conn:
        # 导出用户表到JSON
        json_path = 'data/users_export.json'
        JSONDataHandler.export_to_json(conn, 'users', json_path)

        # 从JSON导入数据
        # JSONDataHandler.import_from_json(conn, 'users', json_path)

    # 6. 带数据转换的迁移示例
    print("\n=== 带数据转换的迁移示例 ===")

    # 假设我们有一个旧的用户表结构需要迁移
    old_config = {
        'database': 'data/old_users.db',
        'timeout': 30.0,
        'check_same_thread': False
    }

    new_config = {
        'database': 'data/new_users.db',
        'timeout': 30.0,
        'check_same_thread': False
    }

    # 创建迁移器
    old_to_new_migrator = DataMigrator(old_config, new_config)

    # 迁移用户表（带数据转换）
    success = old_to_new_migrator.migrate_table('users', transform_user_data)

    if success:
        print("✅ 带数据转换的迁移成功！")
    else:
        print("❌ 带数据转换的迁移失败！")


if __name__ == '__main__':
    main()
```

---

## 🗄️ SQLite 单文件架构详解

### 核心概念

在 SQLite 中，**一个文件就是一个完整的数据库**。这是 SQLite 的一个核心特性，也是它与 MySQL、PostgreSQL 等客户端-服务器数据库的主要区别之一。

### 单文件架构图示

```
my_database.db  ← 一个完整的数据库文件
├── 表（Tables）
│   ├── users
│   ├── products
│   ├── orders
│   └── ...
├── 索引（Indexes）
│   ├── idx_users_email
│   ├── idx_products_name
│   └── ...
├── 视图（Views）
│   ├── user_order_summary
│   └── product_inventory
├── 触发器（Triggers）
│   ├── update_timestamp
│   └── check_stock
├── 存储过程（在SQLite中是用户自定义函数）
└── 系统表
    ├── sqlite_master
    └── sqlite_sequence
```

### 验证单文件特性

```python
import db_utils
import os
from pathlib import Path

def demonstrate_single_file_database():
    """演示SQLite单文件数据库特性"""

    # 创建数据库文件
    db_path = "data/demo_database.db"

    # 确保目录存在
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    print("=== SQLite单文件数据库演示 ===")
    print(f"数据库文件路径: {db_path}")

    # 检查文件初始状态
    if os.path.exists(db_path):
        initial_size = os.path.getsize(db_path)
        print(f"初始文件大小: {initial_size} 字节")
    else:
        print("文件不存在，将创建新文件")

    # 创建数据库连接（会自动创建文件）
    with db_utils.get_db_connection() as conn:

        # 创建表
        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db_utils.execute_query(conn, """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        """)

        # 创建索引
        db_utils.execute_query(conn, "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")

        # 创建视图
        db_utils.execute_query(conn, """
            CREATE VIEW IF NOT EXISTS user_summary AS
            SELECT name, email, created_at FROM users
        """)

        # 插入数据
        db_utils.insert_record(conn, 'users', {
            'name': '张三',
            'email': 'zhangsan@example.com'
        })

        db_utils.insert_record(conn, 'products', {
            'name': 'iPhone',
            'price': 5999.00,
            'stock': 100
        })

    # 检查文件大小
    if os.path.exists(db_path):
        final_size = os.path.getsize(db_path)
        print(f"最终文件大小: {final_size} 字节")

        # 列出文件内容（SQLite数据库文件）
        print(f"\n数据库文件包含:")
        with db_utils.get_db_connection() as conn:

            # 查看所有表
            tables = db_utils.fetch_all(conn, """
                SELECT name, type FROM sqlite_master
                WHERE type IN ('table', 'view', 'index')
                ORDER BY type, name
            """)

            for item in tables:
                print(f"  {item['type'].upper()}: {item['name']}")

            # 查看数据
            users = db_utils.fetch_all(conn, "SELECT * FROM users")
            products = db_utils.fetch_all(conn, "SELECT * FROM products")

            print(f"\n数据记录:")
            print(f"  用户表: {len(users)} 条记录")
            print(f"  产品表: {len(products)} 条记录")

# 运行演示
demonstrate_single_file_database()
```

### SQLite 文件内部结构

```python
def inspect_sqlite_file_structure():
    """检查SQLite文件内部结构"""

    db_path = "data/demo_database.db"

    if not os.path.exists(db_path):
        print("数据库文件不存在")
        return

    print("\n=== SQLite文件内部结构 ===")

    with db_utils.get_db_connection() as conn:

        # 查看系统表sqlite_master
        print("1. sqlite_master表内容（数据库元数据）:")
        master_data = db_utils.fetch_all(conn, "SELECT * FROM sqlite_master")

        for item in master_data:
            print(f"  {item['type']:8} | {item['name']:20} | {item['tbl_name']:20} | {item['sql'][:50]}...")

        # 查看sqlite_sequence表（自增序列）
        print("\n2. sqlite_sequence表内容（自增序列）:")
        sequence_data = db_utils.fetch_all(conn, "SELECT * FROM sqlite_sequence")
        for seq in sequence_data:
            print(f"  表: {seq['name']}, 序列值: {seq['seq']}")

        # 查看数据库页面信息
        print("\n3. 数据库页面信息:")
        page_size = db_utils.fetch_value(conn, "PRAGMA page_size")
        page_count = db_utils.fetch_value(conn, "PRAGMA page_count")
        freelist_count = db_utils.fetch_value(conn, "PRAGMA freelist_count")

        print(f"  页面大小: {page_size} 字节")
        print(f"  总页面数: {page_count}")
        print(f"  空闲页面数: {freelist_count}")
        print(f"  数据库大小: {page_size * page_count} 字节")

# 运行检查
inspect_sqlite_file_structure()
```

### 多数据库连接（ATTACH DATABASE）

虽然一个文件是一个数据库，但 SQLite 可以同时连接多个数据库文件：

```python
def demonstrate_multiple_databases():
    """演示多数据库连接"""

    # 创建两个数据库文件
    db1_path = "data/company_db.db"
    db2_path = "data/employee_db.db"

    print("=== 多数据库连接演示 ===")

    # 创建第一个数据库
    with db_utils.get_connection() as conn1:
        conn1.execute(f"ATTACH DATABASE '{db2_path}' AS employee_db")

        # 在主数据库中创建公司表
        conn1.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT
            )
        """)

        # 在附加数据库中创建员工表
        conn1.execute("""
            CREATE TABLE IF NOT EXISTS employee_db.employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company_id INTEGER,
                position TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        """)

        # 插入数据
        conn1.execute("""
            INSERT INTO companies (name, address)
            VALUES ('腾讯科技', '深圳市南山区')
        """)

        conn1.execute("""
            INSERT INTO employee_db.employees (name, company_id, position)
            VALUES ('张三', 1, '软件工程师')
        """)

        # 跨数据库查询
        result = conn1.execute("""
            SELECT c.name as company, e.name as employee, e.position
            FROM companies c
            JOIN employee_db.employees e ON c.id = e.company_id
        """).fetchall()

        print("跨数据库查询结果:")
        for row in result:
            print(f"  公司: {row[0]}, 员工: {row[1]}, 职位: {row[2]}")

        conn1.execute("DETACH DATABASE employee_db")

# 运行多数据库演示
demonstrate_multiple_databases()
```

### 数据库文件管理

```python
def database_file_management():
    """数据库文件管理演示"""

    db_path = "data/managed_db.db"

    print("=== 数据库文件管理演示 ===")

    # 1. 创建数据库
    print("1. 创建数据库并添加数据")
    with db_utils.get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 添加大量数据
        for i in range(1000):
            conn.execute("""
                INSERT INTO logs (message, level)
                VALUES (?, ?)
            """, (f"日志消息 {i}", 'INFO'))

    # 2. 检查文件大小
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"2. 数据库文件大小: {size} 字节")

    # 3. 压缩数据库（VACUUM）
    print("3. 压缩数据库")
    with db_utils.get_db_connection() as conn:
        conn.execute("VACUUM")

    if os.path.exists(db_path):
        new_size = os.path.getsize(db_path)
        print(f"   压缩后大小: {new_size} 字节")

    # 4. 备份数据库
    print("4. 备份数据库")
    backup_path = "data/managed_db_backup.db"
    db_utils.backup_database(db_path, backup_path)
    print(f"   备份到: {backup_path}")

    # 5. 验证备份
    print("5. 验证备份")
    with db_utils.get_connection() as conn:
        conn.execute(f"ATTACH DATABASE '{backup_path}' AS backup_db")

        original_count = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
        backup_count = conn.execute("SELECT COUNT(*) FROM backup_db.logs").fetchone()[0]

        print(f"   原数据库记录数: {original_count}")
        print(f"   备份数据库记录数: {backup_count}")
        print(f"   备份验证: {'成功' if original_count == backup_count else '失败'}")

        conn.execute("DETACH DATABASE backup_db")

# 运行文件管理演示
database_file_management()
```

### 内存数据库 vs 文件数据库

```python
def compare_memory_vs_file_database():
    """比较内存数据库和文件数据库"""

    print("=== 内存数据库 vs 文件数据库比较 ===")

    # 1. 文件数据库
    print("1. 文件数据库演示")
    file_db = "data/file_comparison.db"

    with db_utils.get_connection() as conn:
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)")
        conn.execute("INSERT INTO test (data) VALUES ('文件数据库数据')")

        # 数据会持久化
        result = conn.execute("SELECT * FROM test").fetchone()
        print(f"   插入的数据: {result[1]}")

    # 重新连接，数据仍然存在
    with db_utils.get_connection() as conn:
        result = conn.execute("SELECT * FROM test").fetchone()
        print(f"   重新连接后的数据: {result[1]}")

    # 2. 内存数据库
    print("\n2. 内存数据库演示")

    # 创建内存数据库连接
    import sqlite3
    mem_conn = sqlite3.connect(":memory:")

    mem_conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)")
    mem_conn.execute("INSERT INTO test (data) VALUES ('内存数据库数据')")

    result = mem_conn.execute("SELECT * FROM test").fetchone()
    print(f"   插入的数据: {result[1]}")

    mem_conn.close()

    # 重新连接内存数据库，数据不存在
    mem_conn2 = sqlite3.connect(":memory:")
    try:
        result = mem_conn2.execute("SELECT * FROM test").fetchone()
        print(f"   重新连接后的数据: {result[1]}")
    except sqlite3.OperationalError as e:
        print(f"   重新连接后: 表不存在 - {e}")

    mem_conn2.close()

    # 3. 命名内存数据库
    print("\n3. 命名内存数据库演示")

    # 创建命名内存数据库
    named_mem_conn1 = sqlite3.connect("file:memdb?mode=memory&cache=shared", uri=True)
    named_mem_conn1.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)")
    named_mem_conn1.execute("INSERT INTO test (data) VALUES ('命名内存数据库数据')")

    # 另一个连接可以访问同一个内存数据库
    named_mem_conn2 = sqlite3.connect("file:memdb?mode=memory&cache=shared", uri=True)
    result = named_mem_conn2.execute("SELECT * FROM test").fetchone()
    print(f"   另一个连接访问的数据: {result[1]}")

    named_mem_conn1.close()
    named_mem_conn2.close()

# 运行比较演示
compare_memory_vs_file_database()
```

### 完整的数据库文件操作示例

```python
def complete_database_file_operations():
    """完整的数据库文件操作示例"""

    print("=== 完整的数据库文件操作示例 ===")

    # 数据库文件路径
    db_path = "data/complete_example.db"

    # 1. 检查数据库是否存在
    if os.path.exists(db_path):
        print(f"1. 数据库文件已存在: {db_path}")
        print(f"   文件大小: {os.path.getsize(db_path)} 字节")
    else:
        print(f"1. 数据库文件不存在，将创建: {db_path}")

    # 2. 创建完整的数据库结构
    print("\n2. 创建完整的数据库结构")
    with db_utils.get_db_connection() as conn:

        # 用户表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 产品表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL CHECK (price >= 0),
                stock_quantity INTEGER DEFAULT 0,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 订单表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_number TEXT UNIQUE NOT NULL,
                total_amount REAL NOT NULL CHECK (total_amount >= 0),
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # 订单详情表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                unit_price REAL NOT NULL CHECK (unit_price >= 0),
                subtotal REAL NOT NULL CHECK (subtotal >= 0),

                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # 创建索引
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")

        # 创建视图
        conn.execute("""
            CREATE VIEW IF NOT EXISTS user_order_summary AS
            SELECT
                u.id,
                u.username,
                u.full_name,
                COUNT(o.id) as order_count,
                COALESCE(SUM(o.total_amount), 0) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.username, u.full_name
        """)

        # 创建触发器
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS update_users_timestamp
            AFTER UPDATE ON users
            FOR EACH ROW
            BEGIN
                UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)

        print("   数据库结构创建完成")

    # 3. 插入示例数据
    print("\n3. 插入示例数据")
    with db_utils.get_db_connection() as conn:

        # 插入用户
        users_data = [
            ('john_doe', 'john@example.com', 'hash1', 'John Doe'),
            ('jane_smith', 'jane@example.com', 'hash2', 'Jane Smith'),
            ('bob_wilson', 'bob@example.com', 'hash3', 'Bob Wilson')
        ]

        for username, email, password_hash, full_name in users_data:
            conn.execute("""
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))

        # 插入产品
        products_data = [
            ('iPhone 14', '苹果最新款智能手机', 5999.00, 100, '电子产品'),
            ('MacBook Pro', '苹果专业笔记本', 12999.00, 50, '电子产品'),
            ('iPad Air', '苹果平板电脑', 3999.00, 80, '电子产品')
        ]

        for name, description, price, stock, category in products_data:
            conn.execute("""
                INSERT INTO products (name, description, price, stock_quantity, category)
                VALUES (?, ?, ?, ?, ?)
            """, (name, description, price, stock, category))

        # 插入订单
        conn.execute("""
            INSERT INTO orders (user_id, order_number, total_amount, status)
            VALUES (1, 'ORD-2024-001', 5999.00, 'completed')
        """)

        conn.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (1, 1, 1, 5999.00, 5999.00)
        """)

        print("   示例数据插入完成")

    # 4. 验证数据库内容
    print("\n4. 验证数据库内容")
    with db_utils.get_db_connection() as conn:

        # 检查表
        tables = conn.execute("""
            SELECT name, type FROM sqlite_master
            WHERE type IN ('table', 'view', 'index')
            ORDER BY type, name
        """).fetchall()

        print(f"   数据库对象数量: {len(tables)}")
        for table in tables:
            print(f"     {table[1].upper()}: {table[0]}")

        # 检查数据
        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        product_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        order_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

        print(f"   用户数量: {user_count}")
        print(f"   产品数量: {product_count}")
        print(f"   订单数量: {order_count}")

    # 5. 检查文件信息
    print("\n5. 数据库文件信息")
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"   文件路径: {db_path}")
        print(f"   文件大小: {size} 字节")
        print(f"   文件大小: {size / 1024:.2f} KB")

        # 获取数据库统计信息
        with db_utils.get_db_connection() as conn:
            page_size = conn.execute("PRAGMA page_size").fetchone()[0]
            page_count = conn.execute("PRAGMA page_count").fetchone()[0]

            print(f"   页面大小: {page_size} 字节")
            print(f"   页面数量: {page_count}")
            print(f"   计算大小: {page_size * page_count} 字节")

    # 6. 数据库备份
    print("\n6. 数据库备份")
    backup_path = "data/complete_example_backup.db"
    db_utils.backup_database(db_path, backup_path)

    if os.path.exists(backup_path):
        backup_size = os.path.getsize(backup_path)
        print(f"   备份文件: {backup_path}")
        print(f"   备份大小: {backup_size} 字节")
        print(f"   备份验证: {'成功' if backup_size > 0 else '失败'}")

    print("\n=== 数据库文件操作完成 ===")

# 运行完整示例
complete_database_file_operations()
```

### SQLite 单文件数据库的核心特性总结

#### 1. 单文件架构

- **一个文件 = 一个完整数据库**
- 包含所有表、索引、视图、触发器
- 包含所有数据和元数据
- 自包含，无需外部依赖

#### 2. 文件格式标准化

- 使用 SQLite 特定的文件格式
- 跨平台兼容
- 支持加密（使用 SQLite 扩展）

#### 3. 易于管理和部署

- 复制文件 = 备份数据库
- 移动文件 = 移动数据库
- 删除文件 = 删除数据库

#### 4. 性能优势

- 无网络开销
- 本地文件访问
- 适合中小型应用

#### 5. 适用场景对比

| 场景         | 适用性 | 原因                     |
| ------------ | ------ | ------------------------ |
| 移动应用     | ✅     | 单文件、轻量级、无服务器 |
| 桌面应用     | ✅     | 本地存储、易于部署       |
| 小型网站     | ✅     | 简单配置、快速开发       |
| 嵌入式系统   | ✅     | 资源占用少、稳定性高     |
| 数据分析     | ✅     | 便于数据传输和处理       |
| 高并发写入   | ❌     | 写入性能有限             |
| 企业级应用   | ❌     | 缺乏高级特性             |
| 分布式系统   | ❌     | 单文件架构限制           |
| 高可用性需求 | ❌     | 单点故障风险             |

#### 6. 文件操作最佳实践

##### ✅ 推荐做法

```python
# 定期备份
def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"data/backup_{timestamp}.db"
    db_utils.backup_database(db_config.get_db_path(), backup_path)

# 定期清理
def cleanup_database():
    with db_utils.get_db_connection() as conn:
        # 删除过期数据
        conn.execute("DELETE FROM logs WHERE created_at < datetime('now', '-30 days')")
        # 压缩数据库
        conn.execute("VACUUM")

# 文件权限管理
def set_database_permissions():
    import os
    import stat
    db_path = db_config.get_db_path()
    # 设置文件权限为仅所有者可读写
    os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)
```

##### ❌ 避免做法

```python
# 避免直接操作数据库文件
# 不要用文本编辑器打开.db文件
# 不要在数据库正在使用时复制文件
# 不要在多个进程中同时写入同一个数据库文件
```

#### 7. 多数据库策略

虽然 SQLite 是单文件架构，但可以通过以下方式实现多数据库管理：

```python
def multi_database_strategy():
    """多数据库策略示例"""

    # 按业务模块分离数据库
    databases = {
        'user_db': 'data/users.db',
        'product_db': 'data/products.db',
        'order_db': 'data/orders.db'
    }

    # 使用ATTACH DATABASE进行跨库查询
    with db_utils.get_connection() as conn:
        # 附加其他数据库
        for db_name, db_path in databases.items():
            if db_name != 'user_db':  # 主数据库不需要附加
                conn.execute(f"ATTACH DATABASE '{db_path}' AS {db_name}")

        # 执行跨库查询
        results = conn.execute("""
            SELECT u.username, p.name as product_name, o.total_amount
            FROM users u
            JOIN order_db.orders o ON u.id = o.user_id
            JOIN order_db.order_items oi ON o.id = oi.order_id
            JOIN product_db.products p ON oi.product_id = p.id
        """).fetchall()

        # 分离数据库
        for db_name in databases.keys():
            if db_name != 'user_db':
                conn.execute(f"DETACH DATABASE {db_name}")

    return results
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！如果您想为这个项目做出贡献，请遵循以下步骤：

### 开发环境设置

1. **Fork 项目**

   ```bash
   # 克隆您的fork
   git clone https://github.com/your-username/sqlite-framework.git
   cd sqlite-framework
   ```

2. **设置开发环境**

   ```bash
   # 创建虚拟环境
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows

   # 安装依赖
   pip install -r requirements.txt
   ```

3. **运行测试**

   ```bash
   # 运行所有测试
   python db_tests.py

   # 运行特定测试
   python -m unittest db_tests.TestSQLiteFramework.test_connection
   ```

### 代码规范

- **Python 代码风格**: 遵循 PEP 8 规范
- **文档字符串**: 使用 Google 风格的 docstrings
- **类型注解**: 为所有函数添加类型注解
- **错误处理**: 使用具体的异常类型
- **日志记录**: 使用适当的日志级别

### 提交规范

- **提交信息格式**: `类型(范围): 描述`

  - 类型: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - 范围: 影响的模块或功能
  - 描述: 简洁的变更描述

- **示例**:
  ```bash
  feat(utils): 添加批量插入功能
  fix(connection): 修复连接泄漏问题
  docs(readme): 更新API文档
  test(utils): 添加事务测试用例
  ```

### Pull Request 流程

1. **创建功能分支**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **开发并测试**

   ```bash
   # 编写代码
   # 运行测试
   python db_tests.py

   # 代码格式化
   black .
   flake8 .
   ```

3. **提交更改**

   ```bash
   git add .
   git commit -m "feat(utils): 添加新功能"
   ```

4. **推送并创建 PR**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **创建 Pull Request**
   - 清晰的标题和描述
   - 关联相关的 Issue
   - 详细说明变更内容
   - 包含测试结果

---

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

### MIT 许可证摘要

- ✅ **商业使用**: 可以用于商业项目
- ✅ **修改**: 可以自由修改代码
- ✅ **分发**: 可以分发您的修改版本
- ✅ **私有使用**: 可以用于私有项目
- ❌ **责任**: 作者不承担任何责任
- ❌ **保证**: 不提供任何保证

### 第三方许可证

本项目可能使用以下第三方库：

- **SQLite3**: 公共领域
- **Python 标准库**: Python 软件基金会许可证

---

## 📞 联系方式

如果您有任何问题、建议或需要帮助，请通过以下方式联系我们：

- **GitHub Issues**: [提交问题](https://github.com/your-username/sqlite-framework/issues)
- **邮件**: your-email@example.com
- **文档**: [完整文档](https://your-username.github.io/sqlite-framework)

---

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和社区成员！

### 特别感谢

- SQLite 开发团队 - 提供了优秀的嵌入式数据库
- Python 社区 - 提供了强大的生态系统
- 所有贡献者 - 项目的改进和完善

### 贡献者名单

<!-- 请在发布时使用 contributors 命令自动生成 -->

- [@your-username](https://github.com/your-username) - 项目创建者
- [@contributor1](https://github.com/contributor1) - 功能开发
- [@contributor2](https://github.com/contributor2) - 文档改进

---

## 📈 更新日志

### [v1.0.0] - 2024-01-01

#### 新增

- 🎉 初始版本发布
- ✅ 完整的 CRUD 操作支持
- 🔧 事务管理功能
- 📊 数据库统计功能
- 🧪 完整的测试套件
- 📚 详细的文档

#### 修复

- 🔧 修复批量插入的 ID 获取问题
- 🐛 修复连接泄漏问题

#### 改进

- 📝 改进错误处理机制
- ⚡ 优化查询性能
- 🎨 改进代码结构

---

## 🏷️ 项目标签

```
#sqlite #python #database #orm #framework #lightweight
#easy-to-use #well-documented #tested #production-ready
```

---

_最后更新: 2024-01-01_
