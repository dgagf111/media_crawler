在使用SQLAlchemy时，如果需要修改表结构而表中已经有数据，可以采用数据库迁移工具来管理数据库模式的更改。Alembic是SQLAlchemy官方推荐的数据库迁移工具，支持在保持数据的情况下进行数据库模式的更改。

以下是一个使用Alembic进行数据库迁移的基本步骤：

### 1. 安装Alembic

首先，确保安装了Alembic：

```sh
pip install alembic
```

### 2. 初始化Alembic

在项目根目录下运行以下命令来初始化Alembic：

```sh
alembic init alembic
```

这将创建一个名为`alembic`的目录，其中包含Alembic配置文件和示例脚本。

### 3. 配置Alembic

编辑`alembic.ini`文件，配置数据库连接字符串：

```ini
# 在 alembic.ini 文件中
sqlalchemy.url = sqlite:///example.db  # 修改为你的数据库连接字符串
```

编辑`alembic/env.py`文件，配置目标元数据：

```python
from myapp import mymodel  # 导入你的模型
from sqlalchemy import create_engine
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

# 读取配置文件中的数据库URL
config = context.config

# 设置日志配置
fileConfig(config.config_file_name)

# 导入目标元数据
target_metadata = mymodel.Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 4. 创建迁移脚本

使用Alembic自动生成迁移脚本。首先，确保你的模型定义已经更新，然后运行以下命令：

```sh
alembic revision --autogenerate -m "描述性消息"
```

这将根据现有模型和数据库状态生成迁移脚本。生成的脚本位于`alembic/versions`目录下。

### 5. 编辑迁移脚本

检查并编辑生成的迁移脚本以确保其正确性。Alembic会自动生成`upgrade`和`downgrade`函数，你可以在其中添加任何需要的表结构更改。

### 6. 应用迁移

运行以下命令应用迁移：

```sh
alembic upgrade head
```

这将执行迁移脚本并更新数据库结构，同时保留现有数据。

### 示例

假设有一个简单的模型，初始定义如下：

```python
# myapp/mymodel.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

然后需要向`users`表添加一个新的列`email`：

1. 更新模型定义：

```python
# myapp/mymodel.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)  # 新增列
```

2. 生成迁移脚本：

```sh
alembic revision --autogenerate -m "add email column to users table"
```

3. 检查生成的迁移脚本（`alembic/versions/<revision_id>_add_email_column_to_users_table.py`），确保它正确地反映了更改：

```python
# 示例迁移脚本内容
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abcdef123456'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))

def downgrade():
    op.drop_column('users', 'email')
```

4. 应用迁移：

```sh
alembic upgrade head
```

这将更新数据库结构，同时保留现有数据。

通过使用Alembic，您可以方便地管理数据库模式的更改，而无需手动修改数据库结构。