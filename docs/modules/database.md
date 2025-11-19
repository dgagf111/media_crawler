# 数据库系统文档

## 概述

数据库系统基于SQLAlchemy 2.0构建，提供了现代化的ORM功能，支持异步操作、事务管理、连接池、数据库迁移等企业级特性。系统采用Repository模式和Unit of Work模式，确保数据操作的一致性和可维护性。

## 架构设计

### 核心组件

```
db/
├── mysql/
│   ├── mysql.py              # 数据库连接管理
│   ├── base.py               # 基础模型类
│   ├── models/               # 数据模型定义
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   └── base.py          # 模型基类
│   └── transaction/
│       └── transaction_manager.py  # 事务管理器
├── alembic/                  # 数据库迁移
│   ├── versions/            # 迁移脚本
│   ├── env.py              # Alembic环境配置
│   └── script.py.mako      # 迁移模板
└── database.py              # 数据库工厂类
```

### 设计模式

1. **Repository模式**: 封装数据访问逻辑
2. **Unit of Work模式**: 管理事务边界
3. **Factory模式**: 数据库连接工厂
4. **Active Record模式**: 模型自带数据操作方法

## 核心功能

### 1. 数据库连接管理

#### 连接配置

```python
# config/dev.yaml
mysql:
  username: ${MYSQL_USERNAME}
  password: ${MYSQL_PASSWORD}
  host: ${MYSQL_HOST:-localhost}
  port: ${MYSQL_PORT:-3306}
  database: ${MYSQL_DATABASE}
  
  # 连接池配置
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
  pool_recycle: 3600
  
  # 连接参数
  connect_args:
    charset: "utf8mb4"
    autocommit: False
    
  # 引擎配置
  echo: False  # 是否打印SQL日志
  echo_pool: False  # 是否打印连接池日志
```

#### 数据库工厂类

```python
from db.mysql.mysql import MySQL_Database

class DatabaseFactory:
    _instances = {}
    
    @classmethod
    def get_database(cls, db_type: str = "mysql") -> MySQL_Database:
        """获取数据库实例 (单例模式)"""
        if db_type not in cls._instances:
            if db_type == "mysql":
                cls._instances[db_type] = MySQL_Database()
            else:
                raise ValueError(f"不支持的数据库类型: {db_type}")
        
        return cls._instances[db_type]

# 使用示例
db = DatabaseFactory.get_database("mysql")
session = db.get_session()
```

### 2. 模型定义

#### 基础模型类

```python
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

Base = declarative_base()

class BaseModel(Base):
    """基础模型类"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @declared_attr
    def __tablename__(cls):
        """自动生成表名"""
        return cls.__name__.lower() + 's'
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data: dict):
        """从字典更新模型"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
```

#### 用户模型示例

```python
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    """用户模型"""
    __tablename__ = 'users'
    
    # 基础信息
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 状态字段
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # 个人信息
    first_name = Column(String(50))
    last_name = Column(String(50))
    avatar_url = Column(String(255))
    bio = Column(Text)
    
    # 关联关系
    profiles = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    @property
    def full_name(self):
        """完整姓名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

class UserProfile(BaseModel):
    """用户资料扩展"""
    __tablename__ = 'user_profiles'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    birth_date = Column(DateTime)
    
    # 关联关系
    user = relationship("User", back_populates="profiles")
```

### 3. 事务管理

#### 事务管理器

```python
from db.mysql.transaction.transaction_manager import TransactionManager

class TransactionManager:
    """事务管理器 - 实现Unit of Work模式"""
    
    def __init__(self, session):
        self.session = session
        self._is_active = False
    
    def __enter__(self):
        """进入上下文管理器"""
        self._is_active = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.close()
            self._is_active = False
    
    def add(self, instance):
        """添加实例"""
        self.session.add(instance)
    
    def add_all(self, instances):
        """批量添加实例"""
        self.session.add_all(instances)
    
    def delete(self, instance):
        """删除实例"""
        self.session.delete(instance)
    
    def commit(self):
        """提交事务"""
        self.session.commit()
    
    def rollback(self):
        """回滚事务"""
        self.session.rollback()
    
    def close(self):
        """关闭会话"""
        self.session.close()
    
    def query(self, *entities):
        """查询"""
        return self.session.query(*entities)
    
    def execute(self, statement):
        """执行SQL语句"""
        return self.session.execute(statement)

# 使用示例
with TransactionManager(session) as tm:
    user = User(username="testuser", email="test@example.com")
    tm.add(user)
    # 自动提交或回滚
```

### 4. Repository模式

#### 基础Repository类

```python
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

class BaseRepository:
    """基础Repository类"""
    
    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class
    
    def create(self, **kwargs) -> Any:
        """创建实例"""
        instance = self.model_class(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def get_by_id(self, id: int) -> Optional[Any]:
        """根据ID获取实例"""
        return self.session.query(self.model_class).filter(
            self.model_class.id == id
        ).first()
    
    def get_by_field(self, field_name: str, value: Any) -> Optional[Any]:
        """根据字段获取实例"""
        return self.session.query(self.model_class).filter(
            getattr(self.model_class, field_name) == value
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        """获取所有实例"""
        return self.session.query(self.model_class).offset(skip).limit(limit).all()
    
    def update(self, id: int, **kwargs) -> Optional[Any]:
        """更新实例"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
        return instance
    
    def delete(self, id: int) -> bool:
        """删除实例"""
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
    
    def count(self) -> int:
        """统计总数"""
        return self.session.query(self.model_class).count()
```

#### 用户Repository

```python
class UserRepository(BaseRepository):
    """用户Repository"""
    
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.session.query(User).filter(
            User.username == username
        ).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.session.query(User).filter(
            User.email == email
        ).first()
    
    def get_active_users(self) -> List[User]:
        """获取活跃用户"""
        return self.session.query(User).filter(
            User.is_active == True
        ).all()
    
    def search_users(self, keyword: str) -> List[User]:
        """搜索用户"""
        return self.session.query(User).filter(
            (User.username.contains(keyword)) |
            (User.email.contains(keyword)) |
            (User.first_name.contains(keyword)) |
            (User.last_name.contains(keyword))
        ).all()
    
    def create_user_with_profile(self, user_data: dict, profile_data: dict) -> User:
        """创建用户并关联资料"""
        user = User(**user_data)
        self.session.add(user)
        self.session.flush()  # 获得用户ID
        
        profile = UserProfile(user_id=user.id, **profile_data)
        self.session.add(profile)
        self.session.commit()
        
        self.session.refresh(user)
        return user
```

### 5. 查询构建器

#### 动态查询构建

```python
class QueryBuilder:
    """查询构建器"""
    
    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class
        self.query = session.query(model_class)
    
    def filter_by(self, **kwargs):
        """按字段过滤"""
        self.query = self.query.filter_by(**kwargs)
        return self
    
    def filter(self, *criterion):
        """条件过滤"""
        self.query = self.query.filter(*criterion)
        return self
    
    def order_by(self, *criterion):
        """排序"""
        self.query = self.query.order_by(*criterion)
        return self
    
    def limit(self, limit):
        """限制数量"""
        self.query = self.query.limit(limit)
        return self
    
    def offset(self, offset):
        """偏移量"""
        self.query = self.query.offset(offset)
        return self
    
    def paginate(self, page: int, per_page: int = 20):
        """分页查询"""
        offset = (page - 1) * per_page
        self.query = self.query.offset(offset).limit(per_page)
        return self
    
    def join(self, *props, **kwargs):
        """连接查询"""
        self.query = self.query.join(*props, **kwargs)
        return self
    
    def first(self):
        """获取第一个结果"""
        return self.query.first()
    
    def all(self):
        """获取所有结果"""
        return self.query.all()
    
    def count(self):
        """统计数量"""
        return self.query.count()

# 使用示例
users = QueryBuilder(session, User)\
    .filter(User.is_active == True)\
    .filter(User.email.contains('@gmail.com'))\
    .order_by(User.created_at.desc())\
    .paginate(page=1, per_page=10)\
    .all()
```

## 数据库迁移

### 1. Alembic配置

#### 环境配置

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from db.mysql.models import Base
from config.config import config as app_config

# Alembic Config对象
config = context.config

# 设置数据库URL
mysql_config = app_config.get_mysql_config()
database_url = f"mysql+pymysql://{mysql_config['username']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"
config.set_main_option("sqlalchemy.url", database_url)

# 目标元数据
target_metadata = Base.metadata

def run_migrations_offline():
    """离线模式运行迁移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """在线模式运行迁移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

#### 迁移命令

```bash
# 初始化迁移环境
alembic init alembic

# 生成迁移文件
alembic revision --autogenerate -m "Add user table"

# 查看迁移历史
alembic history

# 执行迁移
alembic upgrade head

# 回滚到上一版本
alembic downgrade -1

# 回滚到特定版本
alembic downgrade <revision_id>

# 查看当前版本
alembic current

# 查看SQL但不执行
alembic upgrade head --sql
```

### 2. 迁移脚本示例

```python
# alembic/versions/001_add_user_table.py
"""Add user table

Revision ID: 001
Revises: 
Create Date: 2023-12-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """升级操作"""
    # 创建用户表
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

def downgrade():
    """降级操作"""
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
```

## 性能优化

### 1. 查询优化

#### 预加载关联数据

```python
from sqlalchemy.orm import joinedload, selectinload

# 使用joinedload进行连接查询
users_with_profiles = session.query(User)\
    .options(joinedload(User.profiles))\
    .all()

# 使用selectinload进行子查询
users_with_profiles = session.query(User)\
    .options(selectinload(User.profiles))\
    .all()
```

#### 批量操作

```python
# 批量插入
users_data = [
    {'username': f'user{i}', 'email': f'user{i}@example.com'}
    for i in range(1000)
]

# 使用bulk_insert_mappings提高性能
session.bulk_insert_mappings(User, users_data)
session.commit()

# 批量更新
session.bulk_update_mappings(User, [
    {'id': 1, 'username': 'new_username1'},
    {'id': 2, 'username': 'new_username2'},
])
```

### 2. 连接池优化

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=20,        # 连接池大小
    max_overflow=30,     # 最大溢出连接数
    pool_timeout=30,     # 获取连接超时时间
    pool_recycle=3600,   # 连接回收时间
    pool_pre_ping=True,  # 连接预检查
)
```

### 3. 索引策略

```python
from sqlalchemy import Index

class User(BaseModel):
    # 单列索引
    username = Column(String(50), index=True)
    
    # 复合索引
    __table_args__ = (
        Index('idx_user_email_status', 'email', 'is_active'),
        Index('idx_user_created', 'created_at'),
    )
```

## 使用示例

### 1. 基础CRUD操作

```python
from db.database import DatabaseFactory

# 获取数据库连接
db = DatabaseFactory.get_database()
session = db.get_session()

try:
    # 创建用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password_here"
    )
    session.add(user)
    session.commit()
    
    # 查询用户
    user = session.query(User).filter(User.username == "testuser").first()
    
    # 更新用户
    user.email = "newemail@example.com"
    session.commit()
    
    # 删除用户
    session.delete(user)
    session.commit()

finally:
    session.close()
```

### 2. 使用Repository模式

```python
def create_user_service(user_data: dict) -> User:
    """用户创建服务"""
    db = DatabaseFactory.get_database()
    session = db.get_session()
    
    try:
        user_repo = UserRepository(session)
        
        # 检查用户是否已存在
        if user_repo.get_by_username(user_data['username']):
            raise ValueError("用户名已存在")
        
        if user_repo.get_by_email(user_data['email']):
            raise ValueError("邮箱已存在")
        
        # 创建用户
        user = user_repo.create(**user_data)
        return user
        
    finally:
        session.close()
```

### 3. 事务管理

```python
def transfer_operation(from_user_id: int, to_user_id: int, amount: float):
    """转账操作示例"""
    db = DatabaseFactory.get_database()
    session = db.get_session()
    
    with TransactionManager(session) as tm:
        # 获取用户
        from_user = tm.query(User).filter(User.id == from_user_id).first()
        to_user = tm.query(User).filter(User.id == to_user_id).first()
        
        if not from_user or not to_user:
            raise ValueError("用户不存在")
        
        # 检查余额 (假设User模型有balance字段)
        if from_user.balance < amount:
            raise ValueError("余额不足")
        
        # 执行转账
        from_user.balance -= amount
        to_user.balance += amount
        
        # 记录转账日志
        transfer_log = TransferLog(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount
        )
        tm.add(transfer_log)
        
        # 事务会自动提交或回滚
```

## 监控和调试

### 1. SQL日志记录

```python
import logging

# 配置SQLAlchemy日志
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

# 在配置中启用SQL回显
engine = create_engine(database_url, echo=True)
```

### 2. 性能监控

```python
from sqlalchemy import event
from time import time

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time() - context._query_start_time
    logger.debug(f"Query: {statement[:100]}... | Time: {total:.4f}s")
    
    # 记录慢查询
    if total > 1.0:  # 超过1秒的查询
        logger.warning(f"Slow Query: {statement} | Time: {total:.4f}s")
```

### 3. 连接池监控

```python
from prometheus_client import Gauge

# 连接池指标
db_connections_active = Gauge('db_connections_active', 'Active database connections')
db_connections_idle = Gauge('db_connections_idle', 'Idle database connections')

def monitor_connection_pool(engine):
    """监控连接池状态"""
    pool = engine.pool
    db_connections_active.set(pool.checkedout())
    db_connections_idle.set(pool.checkedin())
```

## 故障排除

### 常见问题

1. **连接池耗尽**
   ```python
   # 检查连接是否正确关闭
   # 调整连接池参数
   # 使用连接池监控
   ```

2. **死锁问题**
   ```python
   # 确保事务操作顺序一致
   # 减少事务持有时间
   # 使用适当的隔离级别
   ```

3. **N+1查询问题**
   ```python
   # 使用预加载 (joinedload, selectinload)
   # 批量查询
   # 合理设计数据模型关系
   ```

4. **迁移冲突**
   ```bash
   # 检查迁移历史
   alembic history
   
   # 手动解决冲突
   alembic merge -m "merge heads" <rev1> <rev2>
   ```

通过合理使用数据库系统的各种功能，可以构建高性能、可维护的数据层。关键是要根据业务需求选择合适的设计模式和优化策略。