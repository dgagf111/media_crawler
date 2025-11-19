# 依赖管理指南

## 📋 概述

本项目采用标准的 Python 依赖管理方式，支持传统的 pip + requirements.txt 以及现代化的 Poetry/pipenv 管理方式。本指南将帮助您理解项目依赖结构，并提供详细的安装和维护说明。

## 🏗️ 依赖架构

### 依赖分层
```
项目依赖架构
├── 统一依赖文件 (requirements.txt)       # 所有依赖的统一管理
│   ├── 生产依赖部分                    # 运行必需
│   └── 开发依赖部分（注释）            # 开发时需要
└── 开发专用文件 (requirements-dev-only.txt) # 开发工具独立管理
```

### 依赖类别说明

| 分类 | 文件 | 用途 | 环境 |
|------|------|------|------|
| **核心依赖** | `requirements.txt` | 应用运行必需 | 生产+开发 |
| **开发依赖** | `requirements-dev.txt` | 开发工具和测试 | 仅开发 |
| **系统依赖** | 系统包管理器 | 底层库支持 | 所有环境 |

## 📦 核心依赖详解

### Web 框架栈
```bash
# 高性能异步 Web 框架
fastapi==0.112.2          # 核心 Web 框架
uvicorn==0.30.6            # ASGI 服务器
python-multipart==0.0.9   # 文件上传支持
```

### 数据库栈
```bash
# ORM 和数据库连接
sqlalchemy==2.0.32         # 现代 ORM 框架
mysql-connector-python==9.0.0  # 官方 MySQL 驱动
pymysql==1.1.1             # 纯 Python MySQL 驱动
alembic==1.13.2            # 数据库迁移工具
```

### 缓存和存储栈
```bash
# 缓存解决方案
redis==5.0.8               # Redis 客户端
cachetools==5.5.0          # 内存缓存工具
```

### 任务调度栈
```bash
# 定时任务和后台作业
apscheduler==3.10.4        # 高级任务调度器
```

### 监控和日志栈
```bash
# 系统监控
prometheus_client==0.20.0  # Prometheus 指标客户端
psutil==6.0.0              # 系统信息获取
```

### 配置和工具栈
```bash
# 配置管理
pyyaml==6.0.2              # YAML 配置解析
python-dotenv==1.0.1       # 环境变量管理

# 安全和加密
cryptography==43.0.0       # 加密库
passlib==1.7.4             # 密码哈希
bcrypt==4.2.0              # bcrypt 哈希算法
python-jose==3.3.0         # JWT 令牌处理

# HTTP 和网络
requests==2.32.3           # HTTP 客户端
httpx==0.27.2              # 异步 HTTP 客户端

# 文档和数据处理
openpyxl==3.1.5            # Excel 文件处理
```

### 测试框架
```bash
# 基础测试
pytest==8.3.2             # 测试框架核心
```

### 开发工具
```bash
# 依赖分析
pipreqs==0.5.0            # 依赖需求分析
setuptools==74.0.0        # 包构建工具
```

## 🛠️ 开发依赖详解

### 测试工具套件
```bash
# 核心测试框架
pytest==8.3.2             # 测试框架
pytest-cov==5.0.0         # 覆盖率测试
pytest-mock==3.12.0       # Mock 测试
pytest-asyncio==0.23.2    # 异步测试支持
```

### 代码质量工具
```bash
# 代码格式化
black==24.8.0             # 代码格式化工具
isort==5.13.2             # 导入排序工具

# 代码检查
flake8==7.1.1             # 代码风格检查
mypy==1.11.2              # 类型检查

# 安全检查
bandit==1.7.9             # 安全漏洞扫描
safety==3.2.7             # 依赖安全检查
```

### 开发辅助工具
```bash
# Git 工具
pre-commit==3.8.0         # Git hooks 管理

# 调试工具
ipython==8.27.0           # 增强交互式 Python
ipdb==0.13.13             # 调试器
rich==13.8.0              # 美化终端输出

# 性能分析
memory-profiler==0.61.0   # 内存使用分析
line-profiler==4.1.3      # 代码行级性能分析
```

### 文档工具
```bash
# 文档生成
mkdocs==1.6.1             # 文档生成器
mkdocs-material==9.5.34   # Material 主题
mkdocs-mermaid2-plugin==1.1.1  # Mermaid 图表支持
```

## 🚀 安装方式

### 方式一：传统 pip 安装 (推荐新手)

#### 生产环境
```bash
# 1. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows

# 2. 升级 pip
pip install --upgrade pip

# 3. 安装生产依赖
pip install -r requirements.txt

# 4. 验证安装
python -c "import fastapi, uvicorn; print('✓ 核心依赖安装成功')"
```

#### 开发环境
```bash
# 基于生产环境，额外安装开发工具
pip install -r requirements-dev.txt

# 验证开发工具
python -c "import pytest, black, mypy; print('✓ 开发工具安装成功')"
```

### 方式二：Poetry 管理 (推荐进阶用户)

#### 初始设置
```bash
# 1. 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. 配置 Poetry (可选)
poetry config virtualenvs.in-project true

# 3. 初始化项目 (如果没有 pyproject.toml)
poetry init
```

#### 创建 pyproject.toml 配置
```toml
[tool.poetry]
name = "pythonprojecttemplate"
version = "2.1.0"
description = "企业级 Python 应用程序模板"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.8"
fastapi = "^0.112.2"
uvicorn = "^0.30.6"
sqlalchemy = "^2.0.32"
mysql-connector-python = "^9.0.0"
pymysql = "^1.1.1"
redis = "^5.0.8"
apscheduler = "^3.10.4"
prometheus-client = "^0.20.0"
psutil = "^6.0.0"
pyyaml = "^6.0.2"
python-dotenv = "^1.0.1"
cryptography = "^43.0.0"
passlib = "^1.7.4"
bcrypt = "^4.2.0"
python-jose = "^3.3.0"
requests = "^2.32.3"
httpx = "^0.27.2"
cachetools = "^5.5.0"
alembic = "^1.13.2"
openpyxl = "^3.1.5"
pytest = "^8.3.2"
pipreqs = "^0.5.0"
setuptools = "^74.0.0"
python-multipart = "^0.0.9"

[tool.poetry.group.dev.dependencies]
pytest-cov = "^5.0.0"
pytest-mock = "^3.12.0"
pytest-asyncio = "^0.23.2"
black = "^24.8.0"
isort = "^5.13.2"
flake8 = "^7.1.1"
mypy = "^1.11.2"
bandit = "^1.7.9"
safety = "^3.2.7"
pre-commit = "^3.8.0"
ipython = "^8.27.0"
ipdb = "^0.13.13"
rich = "^13.8.0"
memory-profiler = "^0.61.0"
line-profiler = "^4.1.3"
mkdocs = "^1.6.1"
mkdocs-material = "^9.5.34"
mkdocs-mermaid2-plugin = "^1.1.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

#### Poetry 使用命令
```bash
# 安装所有依赖
poetry install

# 仅安装生产依赖
poetry install --without dev

# 激活虚拟环境
poetry shell

# 添加新依赖
poetry add requests
poetry add --group dev pytest-xdist

# 更新依赖
poetry update

# 导出 requirements.txt
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --output requirements-dev.txt --with dev
```

### 方式三：pipenv 管理

```bash
# 1. 安装 pipenv
pip install pipenv

# 2. 从 requirements.txt 安装
pipenv install -r requirements.txt

# 3. 安装开发依赖
pipenv install -r requirements-dev.txt --dev

# 4. 激活环境
pipenv shell

# 5. 添加新依赖
pipenv install requests
pipenv install pytest --dev
```

## 🔄 依赖维护

### 定期更新流程

#### 1. 检查过期依赖
```bash
# 使用 pip
pip list --outdated

# 使用 Poetry
poetry show --outdated

# 使用 pipenv
pipenv update --outdated
```

#### 2. 安全漏洞扫描
```bash
# 使用 safety
pip install safety
safety check

# 使用 bandit (代码安全)
bandit -r src/

# 使用 Poetry 审计
poetry audit
```

#### 3. 依赖兼容性检查
```bash
# 检查依赖冲突
pip check

# 查看依赖树
pip install pipdeptree
pipdeptree

# 显示具体包信息
pip show <package_name>
```

#### 4. 批量更新流程
```bash
# 1. 备份当前环境
pip freeze > requirements_backup.txt

# 2. 更新到最新版本
pip install --upgrade -r requirements.txt

# 3. 运行测试验证
python tests/run_tests.py all

# 4. 如果有问题，回滚
pip install -r requirements_backup.txt
```

### 版本管理策略

#### 语义化版本控制
```bash
# 主版本.次版本.修订版本
fastapi==0.112.2    # 精确版本 (生产推荐)
fastapi>=0.112.0    # 最低版本
fastapi~=0.112.0    # 兼容版本 (0.112.x)
fastapi^0.112.0     # 主版本兼容 (Poetry)
```

#### 依赖锁定建议
- **生产环境**: 使用精确版本 (`==`)
- **开发环境**: 使用兼容版本 (`~=` 或 `^`)
- **CI/CD**: 使用锁定文件 (`poetry.lock` 或 `Pipfile.lock`)

## 🚨 故障排除

### 常见问题解决

#### 1. 依赖冲突
```bash
# 问题：Multiple versions of package
# 解决：
pip uninstall <conflicting_package>
pip install <package_name>==<specific_version>

# 或强制重新安装
pip install --force-reinstall <package_name>
```

#### 2. 编译错误
```bash
# 问题：Failed building wheel for <package>
# 解决：安装系统依赖

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential libmysqlclient-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel mysql-devel

# macOS
xcode-select --install
brew install mysql-client
```

#### 3. 网络问题
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 配置永久镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 4. 权限问题
```bash
# 避免使用 sudo pip
# 使用虚拟环境或用户安装
pip install --user <package_name>
```

### 性能优化

#### 并行安装
```bash
# 使用并行下载
pip install --upgrade pip
pip install -r requirements.txt --use-feature=fast-deps

# Poetry 并行安装
poetry config installer.parallel true
```

#### 缓存优化
```bash
# 启用 pip 缓存
pip config set global.cache-dir ~/.cache/pip

# 清理缓存
pip cache purge
```

## 📊 依赖监控

### 自动化工具

#### GitHub Dependabot
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    reviewers:
      - "your-username"
```

#### 安全扫描集成
```bash
# CI/CD 流水线中添加
safety check
bandit -r src/
```

### 监控指标
- **依赖数量**: 控制在合理范围内
- **版本新鲜度**: 定期更新到稳定版本
- **安全漏洞**: 零容忍原则
- **许可证合规**: 确保许可证兼容

## 🎯 最佳实践

### 开发流程
1. **新功能开发**: 先添加到开发依赖测试
2. **稳定后提升**: 移至生产依赖
3. **定期审查**: 移除不再使用的依赖
4. **安全优先**: 及时更新安全补丁
5. **文档同步**: 更新依赖说明文档

### 团队协作
- **锁定文件**: 提交到版本控制
- **环境一致**: 使用相同的依赖管理工具
- **更新协调**: 统一的更新时间和流程
- **问题共享**: 建立依赖问题知识库

## 🔗 相关资源

- [Python 包管理指南](https://packaging.python.org/)
- [Poetry 官方文档](https://python-poetry.org/docs/)
- [pipenv 用户指南](https://pipenv.pypa.io/en/latest/)
- [安全最佳实践](https://pypi.org/project/safety/)

---

**文档版本**: v2.1.0  
**最后更新**: 2025-09-01  
**维护团队**: pythonProjectTemplate团队