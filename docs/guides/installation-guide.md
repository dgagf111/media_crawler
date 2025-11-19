# 安装和配置指南

> 💡 **已有项目想推送到GitHub？** 查看我们的 [GitHub推送指南集合](github/index.md)

## 系统要求

### 基础要求
- **Python**: 3.8 或更高版本
- **操作系统**: Linux, macOS, Windows
- **内存**: 至少 2GB RAM
- **存储**: 至少 500MB 可用空间

### 可选组件
- **MySQL**: 5.7+ 或 8.0+ (用于持久化存储)
- **Redis**: 6.0+ (用于缓存，可选)
- **Docker**: 20.10+ (用于容器化部署)

## 安装步骤

### 1. 获取项目代码

```bash
# 从Git仓库克隆
git clone <repository-url>
cd pythonProjectTemplate

# 或下载并解压源码包
wget <download-url>
unzip pythonProjectTemplate.zip
cd pythonProjectTemplate
```

### 2. Python环境设置

#### 方法一：使用venv (推荐)

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 验证虚拟环境
which python  # 应该显示 .venv/bin/python
```

#### 方法二：使用conda

```bash
# 创建conda环境
conda create -n pytemplate python=3.8
conda activate pytemplate
```

#### 方法三：使用pyenv (Linux/macOS)

```bash
# 安装特定Python版本
pyenv install 3.8.10
pyenv local 3.8.10

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate
```

### 3. 依赖管理和安装

#### 📦 依赖概览

项目包含以下核心依赖：

| 类别 | 依赖包 | 版本 | 说明 |
|------|--------|------|------|
| **Web框架** | FastAPI | 0.112.2 | 高性能异步Web框架 |
| **ASGI服务器** | Uvicorn | 0.30.6 | 异步服务器 |
| **数据库ORM** | SQLAlchemy | 2.0.32 | 现代化ORM框架 |
| **数据库驱动** | PyMySQL | 1.1.1 | MySQL连接器 |
| **缓存** | Redis | 5.0.8 | 内存数据库 |
| **任务调度** | APScheduler | 3.10.4 | 定时任务调度器 |
| **监控** | Prometheus Client | 0.20.0 | 监控指标收集 |
| **配置管理** | PyYAML | 6.0.2 | YAML配置解析 |
| **环境管理** | python-dotenv | 1.0.1 | 环境变量管理 |
| **测试框架** | pytest | 8.3.2 | 单元测试框架 |

#### 🚀 生产环境安装 (推荐)

```bash
# 升级pip到最新版本
pip install --upgrade pip

# 安装所有依赖（推荐）
pip install -r dependencies/requirements.txt

# 验证关键依赖安装
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|redis)"
```

#### 🛠️ 开发环境安装 (开发者推荐)

```bash
# 安装完整开发环境
pip install -r dependencies/requirements.txt
pip install -r dependencies/requirements-dev-only.txt

# 验证开发工具安装
pip list | grep -E "(pytest|black|mypy|pre-commit)"
```

#### 📋 依赖分类说明

**统一依赖文件 (dependencies/requirements.txt)**:
- 运行应用程序必需的核心依赖
- 包含所有运行时需要的包
- 生产环境和开发环境都需要

**开发专用依赖 (dependencies/requirements-dev-only.txt)**:
- 代码质量工具：black, isort, flake8, mypy
- 测试工具：pytest, pytest-cov, pytest-mock
- 调试工具：ipython, ipdb, rich
- 文档工具：mkdocs, mkdocs-material
- 安全工具：bandit, safety
- Git hooks：pre-commit

#### 🔧 现代化依赖管理 (可选)

##### 使用 Poetry (推荐)

```bash
# 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 初始化Poetry项目
poetry init

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell

# 添加新依赖
poetry add fastapi
poetry add --group dev pytest
```

##### 使用 pipenv

```bash
# 安装pipenv
pip install pipenv

# 从统一依赖文件安装
pipenv install -r dependencies/requirements.txt

# 额外安装开发依赖
pipenv install -r dependencies/requirements-dev-only.txt --dev

# 激活虚拟环境
pipenv shell
```

#### ⚠️ 常见依赖问题解决

**问题1: 依赖冲突**
```bash
# 查看依赖树
pip install pipdeptree
pipdeptree

# 解决冲突
pip install --force-reinstall <package_name>
```

**问题2: 版本不兼容**
```bash
# 检查依赖兼容性
pip check

# 升级依赖
pip install --upgrade -r requirements.txt
```

**问题3: 缺少系统依赖**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libmysqlclient-dev

# CentOS/RHEL
sudo yum install python3-devel mysql-devel

# macOS
brew install mysql-client
```

## 配置指南

### 1. 环境变量配置

#### 创建 `.env` 文件

```bash
# 复制示例文件
cp .env.example .env

# 编辑配置
vim .env  # 或使用其他编辑器
```

#### 必需的环境变量

```bash
# === 数据库配置 ===
PPT_DATABASE__USERNAME=your_username
PPT_DATABASE__PASSWORD=your_password
PPT_DATABASE__HOST=localhost
PPT_DATABASE__PORT=3306
PPT_DATABASE__DATABASE=your_database

# === 安全配置 ===
PPT_SECURITY__TOKEN__SECRET_KEY=your-super-secret-key-here
PPT_SECURITY__TOKEN__ALGORITHM=HS256
PPT_SECURITY__TOKEN__ACCESS_TOKEN_EXPIRE_MINUTES=180
PPT_SECURITY__TOKEN__REFRESH_TOKEN_EXPIRE_DAYS=7

# === 可选配置 ===
# Redis缓存 (如果不配置将使用内存缓存)
PPT_CACHE__REDIS__HOST=localhost
PPT_CACHE__REDIS__PORT=6379
PPT_CACHE__REDIS__DB=0

# Token撤销（可选）
PPT_SECURITY__REVOCATION__BACKEND=memory
PPT_SECURITY__REVOCATION__REDIS__HOST=localhost
PPT_SECURITY__REVOCATION__REDIS__PORT=6379

# 环境标识
ENV=dev  # dev, test, prod
```

#### 生成令牌密钥

```bash
# 方法一：使用Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 方法二：使用OpenSSL
openssl rand -base64 32

# 方法三：使用在线工具
# 访问 https://passwordsgenerator.net/
```

### 2. 数据库配置

#### MySQL 设置

```bash
# 1. 安装MySQL (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install mysql-server

# 2. 启动MySQL服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 3. 安全配置
sudo mysql_secure_installation

# 4. 创建数据库和用户
mysql -u root -p
```

```sql
-- 创建数据库
CREATE DATABASE pythonprojecttemplate CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'secure_password';

-- 授权
GRANT ALL PRIVILEGES ON pythonprojecttemplate.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;

-- 退出
EXIT;
```

#### 数据库迁移

```bash
# 初始化迁移
alembic init alembic

# 生成迁移文件
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 3. Redis配置 (可选)

#### 安装Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# macOS
brew install redis

# 启动Redis
sudo systemctl start redis
# 或
redis-server
```

#### 验证Redis连接

```bash
# 连接测试
redis-cli ping
# 应该返回 PONG

# 查看Redis配置
redis-cli info server
```

### 4. 配置文件说明

#### `env.yaml` - 环境配置

```yaml
# 当前环境 (dev, test, prod)
env: dev

# 日志配置
logging:
  project_name: "pythonprojecttemplate"
  base_log_directory: "./logs"
  log_level: "DEBUG"

# 模块配置
module_config:
  base_path: "modules"
  modules:
    - "user_management"
    - "product_management"

# 调度器配置
scheduler:
  enabled: true
  timezone: "Asia/Shanghai"

# 时区配置
TIME_ZONE: "Asia/Shanghai"
```

#### `config/dev.yaml` - 开发环境配置

```yaml
# API服务配置
api:
  host: "0.0.0.0"
  port: 8000
  docs_url: "/docs"
  cors_origins: ["*"]
  max_concurrency: 100
  request_timeout: 30
  api_version: ${PPT_COMMON__API_VERSION:-v1}

security:
  token:
    secret_key: ${PPT_SECURITY__TOKEN__SECRET_KEY}
    algorithm: HS256
    access_token_expire_minutes: 180
    refresh_token_expire_days: 7
  revocation:
    backend: memory
    redis:
      host: ${PPT_SECURITY__REVOCATION__REDIS__HOST:-localhost}
      port: ${PPT_SECURITY__REVOCATION__REDIS__PORT:-6379}
      db: 2

# 缓存配置
cache:
  type: redis  # redis 或 memory
  ttl: 3600
  max_size: 1000
  redis:
    host: ${PPT_CACHE__REDIS__HOST:-localhost}
    port: ${PPT_CACHE__REDIS__PORT:-6379}
    db: 0

# 监控配置
monitoring:
  prometheus_port: 9966
  cpu_threshold: 80
  memory_threshold: 80

# 任务配置
tasks:
  task1:
    trigger: interval
    args:
      seconds: 10
    max_attempts: 3
    retry_delay: 2
```

## 启动和运行

### 1. 开发模式启动

```bash
# 方法一：直接运行
python main.py

# 方法二：使用uvicorn (推荐开发环境)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 方法三：使用gunicorn (生产环境)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 2. 后台运行

```bash
# 使用nohup
nohup python main.py > app.log 2>&1 &

# 使用screen
screen -S app
python main.py
# Ctrl+A, D 离开screen

# 使用systemd服务
sudo systemctl start pythonapp
```

### 3. 验证运行状态

```bash
# 检查进程
ps aux | grep python

# 检查端口
netstat -tlnp | grep 8000

# 测试API
curl http://localhost:8000/health

# 访问API文档
# 浏览器打开: http://localhost:8000/docs
```

## 服务验证

### 1. 健康检查

```bash
# API健康检查
curl -X GET http://localhost:8000/health

# 预期响应
{
  "status": "ok",
  "timestamp": "2023-12-01T10:00:00Z",
  "services": {
    "database": "connected",
    "cache": "connected",
    "scheduler": "running"
  }
}
```

### 2. 功能测试

```bash
# 运行测试套件
python tests/run_tests.py all

# 预期输出
Running all tests...
✓ Framework tests passed
✓ Business tests passed
✓ Integration tests passed
All tests completed successfully!
```

### 3. 监控指标

```bash
# 查看Prometheus指标
curl http://localhost:9966/metrics

# 查看应用日志
tail -f logs/pythonprojecttemplate/$(date +%Y/%Y-%m)/$(date +%Y-%m-%d).log
```

## 故障排除

### 常见问题

#### 1. 模块导入错误

```bash
# 问题：ModuleNotFoundError
# 解决：检查PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 或在代码中添加路径
import sys
sys.path.append('/path/to/project/src')
```

#### 2. 数据库连接失败

```bash
# 问题：Database connection failed
# 解决步骤：
1. 检查MySQL服务状态
sudo systemctl status mysql

2. 验证连接参数
mysql -h localhost -u username -p database_name

3. 检查防火墙设置
sudo ufw status
```

#### 3. Redis连接问题

```bash
# 问题：Redis connection refused
# 解决步骤：
1. 检查Redis服务
sudo systemctl status redis

2. 测试连接
redis-cli ping

3. 检查配置文件
cat /etc/redis/redis.conf | grep bind
```

#### 4. 端口占用

```bash
# 问题：Port 8000 already in use
# 解决：
1. 查找占用进程
lsof -i :8000

2. 杀死进程
kill -9 <PID>

3. 或使用不同端口
uvicorn main:app --port 8001
```

### 日志分析

```bash
# 查看错误日志
grep ERROR logs/pythonprojecttemplate/*/$(date +%Y-%m-%d).log

# 查看最近的日志
tail -f logs/pythonprojecttemplate/*/$(date +%Y-%m-%d).log

# 按级别过滤
grep -E "(ERROR|CRITICAL)" logs/pythonprojecttemplate/*/$(date +%Y-%m-%d).log
```

### 性能调优

#### 数据库优化

```sql
-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- 开启慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

#### 应用优化

```bash
# 使用多进程
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# 调整数据库连接池
# 在config.py中修改数据库配置
pool_size=10,
max_overflow=20,
pool_timeout=30
```

## 安全配置

### 1. 环境变量保护

```bash
# 设置文件权限
chmod 600 .env

# 添加到.gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
```

### 2. 数据库安全

```sql
-- 删除默认用户
DROP USER ''@'localhost';
DROP USER ''@'hostname';

-- 限制root用户访问
UPDATE mysql.user SET Host='localhost' WHERE User='root';
FLUSH PRIVILEGES;
```

### 3. 应用安全

```bash
# 使用HTTPS
# 在nginx配置中添加SSL证书

# 限制文件权限
chmod 644 config/*.yaml
chmod 600 .env

# 使用防火墙
sudo ufw allow 8000/tcp
sudo ufw enable
```

## 下一步

安装完成后，建议阅读：

1. **[运行指南](running-guide.md)** - 详细的运行和部署说明
2. **[开发指南](development-guide.md)** - 开发环境配置和最佳实践
3. **[API文档](../modules/api.md)** - API接口详细说明
4. **[故障排除指南](troubleshooting-guide.md)** - 常见问题和解决方案

如果遇到任何问题，请查看日志文件或提交Issue。
