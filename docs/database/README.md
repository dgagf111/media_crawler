# 数据库文档 (Database Documentation)

## 📋 目录说明

这个目录包含了项目数据库相关的专门文档，涵盖数据库设计、迁移、维护等方面。

## 📁 文件列表

### 数据库表结构管理
- **[Table_structure_modification.md](Table_structure_modification.md)** - 数据库表结构修改指南
  - Alembic迁移工具使用方法
  - 数据库表结构变更流程
  - 迁移脚本编写规范
  - 版本控制和回滚策略

## 🗄️ 数据库架构概览

项目采用现代化的数据库架构设计：

### 技术栈
- **ORM框架**: SQLAlchemy 2.0
- **数据库**: MySQL 8.0+
- **迁移工具**: Alembic
- **连接驱动**: PyMySQL + MySQL Connector

### 核心特性
- ✅ **现代ORM**: 支持异步操作和类型提示
- ✅ **自动迁移**: 版本化的数据库架构管理
- ✅ **事务管理**: 完整的事务支持和回滚机制
- ✅ **连接池**: 高性能的数据库连接池
- ✅ **模型抽象**: 标准化的数据模型基类

## 📖 详细文档参考

### 核心模块文档
- **[数据库系统文档](../modules/database.md)** - 完整的数据库系统说明
  - 架构设计和组件说明
  - 数据模型定义规范
  - 事务管理器使用指南
  - 性能优化策略

### 配置和部署
- **[安装指南](../guides/installation-guide.md)** - 数据库环境搭建
- **[部署指南](../guides/deployment-guide.md)** - 生产环境数据库配置

## 🔧 快速参考

### 常用迁移命令

```bash
# 初始化迁移环境
alembic init alembic

# 生成迁移脚本
alembic revision --autogenerate -m "描述信息"

# 执行迁移
alembic upgrade head

# 查看迁移历史
alembic history

# 回滚到指定版本
alembic downgrade <revision_id>
```

### 数据库连接配置

```yaml
# config/dev.yaml
mysql:
  username: ${MYSQL_USERNAME}
  password: ${MYSQL_PASSWORD}
  host: ${MYSQL_HOST:-localhost}
  port: ${MYSQL_PORT:-3306}
  database: ${MYSQL_DATABASE}
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
```

### 模型定义示例

```python
from sqlalchemy import Column, String, Boolean
from db.mysql.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
```

## 🚨 重要注意事项

### 数据库迁移最佳实践
1. **备份数据**: 生产环境迁移前务必备份
2. **测试验证**: 在测试环境充分验证迁移脚本
3. **版本控制**: 迁移文件必须纳入版本控制
4. **文档记录**: 重要变更要有详细的文档说明

### 安全考虑
- 数据库连接密码使用环境变量
- 限制数据库用户权限
- 定期备份重要数据
- 监控数据库访问日志

## 🔗 相关资源

### 技术文档
- [SQLAlchemy官方文档](https://docs.sqlalchemy.org/)
- [Alembic迁移指南](https://alembic.sqlalchemy.org/)
- [MySQL官方文档](https://dev.mysql.com/doc/)

### 项目文档
- [项目架构文档](../PROJECT_ARCHITECTURE.md)
- [配置管理文档](../modules/config.md)
- [测试文档](../modules/testing.md)

---

**目录版本**: v2.1.0  
**最后更新**: 2025-09-01  
**维护团队**: pythonProjectTemplate团队