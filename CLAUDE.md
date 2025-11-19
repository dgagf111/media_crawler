# CLAUDE.md

本文档为 Claude Code（claude.ai/code）在本仓库中处理代码时提供指导。

## 项目概述

这是一个使用 FastAPI 构建的现代化 Python 企业级应用模板，具有标准化的架构，涵盖缓存、监控、任务调度和完善的测试基础设施。

**技术栈：**

- **框架**：FastAPI 0.112.0+，支持异步
- **数据库**：SQLAlchemy 2.0 + MySQL，支持 Alembic 迁移
- **缓存**：Redis + 内存缓存，支持平滑回退
- **测试**：pytest + 自定义测试运行器
- **代码质量**：black、isort、mypy、flake8、bandit、safety
- **部署**：Docker + Docker Compose

## 基本开发命令

### 环境配置

```bash
# 安装依赖（使用智能脚本）
./dependencies/install_dependencies.sh dev    # 开发环境
./dependencies/install_dependencies.sh prod   # 生产环境
./dependencies/install_dependencies.sh check  # 检查依赖状态

# 配置环境变量
cp .env.example .env
# 需编辑：PPT_DATABASE__USERNAME, PPT_DATABASE__PASSWORD, PPT_SECURITY__TOKEN__SECRET_KEY
```

### 开发服务器

```bash
# 启动开发服务器（热重载）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或使用项目入口文件
python main.py

# 使用 Docker 启动
docker-compose up -d
docker-compose down
```

### 测试

```bash
# 使用项目测试运行器运行所有测试
python tests/run_tests.py all        # 全部测试
python tests/run_tests.py framework  # 框架层测试
python tests/run_tests.py business   # 业务逻辑测试

# 带覆盖率运行测试
pytest --cov=src tests/
pytest --cov=src --cov-report=html tests/
```

### 代码质量

```bash
# 格式化代码（提交前执行）
black src/ tests/
isort src/ tests/

# 类型检查
mypy src/

# 安全扫描
bandit -r src/
safety check
```

### 数据库迁移

```bash
# 生成迁移（模型修改后）
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head
alembic downgrade -1
```

## 架构概览

### 项目结构

```
src/pythonprojecttemplate/
├── api/           # API 层——路由与请求/响应模型
├── cache/         # 缓存系统——Redis 与内存缓存
├── config/        # 配置管理——基于 YAML 的配置系统
├── core/          # 核心基础设施——常量、异常、工具
├── db/            # 数据库层——SQLAlchemy 模型与会话
├── modules/       # 业务模块——领域逻辑
├── repositories/  # 数据访问层——仓储模式
├── scheduler/     # 任务调度——APScheduler 集成
├── monitoring/    # 监控——Prometheus 指标
├── plugins/       # 插件系统——可扩展性支持
└── utils/         # 工具函数
```

### 关键架构模式

**配置驱动架构：**

- 多环境配置基于 YAML 文件
- 支持 `${VAR:-default}` 环境变量插值语法
- 使用 Pydantic 模型实现类型安全配置
- 配置源文件：`src/config/settings.py`

**异步优先设计：**

- 所有数据库操作使用 SQLAlchemy 2.0 异步模式
- 缓存操作支持 async/await
- API 端点应尽可能为异步函数

**依赖注入机制：**

- 数据库会话自动管理
- JWT 鉴权通过依赖注入
- 服务依赖通过 FastAPI DI 系统解析

**异常处理机制：**

- 分层异常系统位于 `core/exceptions.py`
- 全局异常处理器：`api/middleware/exception_handler.py`
- 标准化错误响应，包含错误码

**缓存策略：**

- 使用工厂模式选择缓存类型（Redis/内存）
- 当 Redis 不可用时自动回退至内存缓存
- 缓存键由 `cache_key_builder.py` 管理

### API 开发指南

**创建新端点：**

1. 在 `api/routes/` 下相应模块定义路由
2. 使用 Pydantic 模型进行请求/响应验证
3. 实现合理的错误处理与自定义异常
4. 在 `tests/` 中编写对应测试

**认证机制：**

- JWT 双令牌机制（访问令牌/刷新令牌）
- 受保护端点使用 `Depends(get_current_user)`
- 基于角色的访问控制通过 `requires_role` 依赖实现

**数据库操作：**

- 使用 `repositories/` 下的仓储模式
- 实现异步会话管理
- 事务遵循“工作单元”（Unit of Work）模式

### 测试策略

**测试组织结构：**

- 框架测试：核心功能
- 模块测试：独立业务模块
- 业务测试：端到端场景

**编写测试：**

- 使用 pytest fixtures 进行通用初始化
- 合理 mock 外部依赖
- 测试成功与错误两种情况
- 保持测试间独立性

### 常见开发任务

**添加新业务模块：**

1. 在 `modules/` 下创建模块目录
2. 在模块的 `models.py` 中定义模型
3. 在 `repositories/` 下创建对应仓储
4. 实现服务逻辑
5. 在 `api/routes/` 中添加 API 路由
6. 编写完善的测试

**数据库结构变更：**

1. 修改对应 `models.py` 文件
2. 生成迁移：`alembic revision --autogenerate -m "description"`
3. 审查迁移脚本
4. 应用迁移：`alembic upgrade head`
5. 更新相关测试

**添加新配置项：**

1. 在 `config/settings.py` 中添加字段
2. 更新对应 YAML 配置文件
3. 如需环境变量映射，补充映射逻辑
4. 在 `.env.example` 中添加新变量

### 注意事项

- 提交前务必执行 `black` 与 `isort` 格式化
- 所有测试必须通过后才能合并
- 所有新代码必须包含类型注解
- 保持代码风格一致
- 生产部署前必须通过安全扫描
- 通过 Prometheus 端点监控应用指标
