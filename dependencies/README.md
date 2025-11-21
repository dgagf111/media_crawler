# 依赖管理 (Dependencies)

## 📋 目录说明

这个目录包含了项目的所有依赖管理相关文件，方便项目移植和环境搭建。

## 📁 文件结构

```
dependencies/
├── README.md                    # 本说明文件
├── requirements.txt             # 统一依赖列表（生产+开发）
├── requirements-dev-only.txt    # 开发环境专用依赖
├── install_dependencies.sh      # 智能依赖安装脚本
├── update_requirements.py       # 依赖更新脚本
└── DEPENDENCY_MANAGEMENT.md     # 完整依赖管理指南
```

## 🚀 快速开始

### 方式一：使用智能安装脚本 (推荐)

```bash
# 进入项目根目录
cd /path/to/pythonProjectTemplate

# 生产环境安装
./dependencies/install_dependencies.sh

# 开发环境安装
./dependencies/install_dependencies.sh dev

# 检查依赖状态
./dependencies/install_dependencies.sh check

# 显示帮助
./dependencies/install_dependencies.sh help
```

### 方式二：传统pip安装

```bash
# 安装所有依赖（推荐）
pip install -r dependencies/requirements.txt

# 额外安装开发工具（可选）
pip install -r dependencies/requirements-dev-only.txt
```

## 📦 依赖说明

### 统一依赖文件 (requirements.txt)
包含所有依赖，分为生产依赖和开发依赖两部分：

**生产依赖部分**（必需，共24个）:

**核心框架**:
- `fastapi==0.112.2` - 高性能异步Web框架
- `uvicorn==0.31.1` - ASGI服务器
- `sqlalchemy==2.0.32` - 现代ORM框架

**数据库驱动**:
- `mysql-connector-python==9.0.0` - MySQL官方驱动
- `pymysql==1.1.1` - 纯Python MySQL驱动

**缓存和任务调度**:
- `redis==5.0.8` - Redis客户端
- `apscheduler==3.10.4` - 任务调度器

**监控和工具**:
- `prometheus_client==0.20.0` - 监控指标
- `pytest==8.3.2` - 测试框架

### 开发专用依赖 (requirements-dev-only.txt)
额外包含开发、测试、调试工具，共21个额外包：

**代码质量工具**:
- `black==24.8.0` - 代码格式化
- `mypy==1.11.2` - 类型检查
- `flake8==7.1.1` - 代码风格检查

**测试工具**:
- `pytest-cov==5.0.0` - 覆盖率测试
- `pytest-mock==3.12.0` - Mock测试

**开发调试**:
- `ipython==8.27.0` - 增强交互式Python
- `rich==13.8.0` - 美化终端输出

## 🔧 工具脚本

### install_dependencies.sh
智能依赖安装脚本，特性：
- ✅ 自动检查Python版本和虚拟环境
- ✅ 支持多种安装模式 (prod/dev/check/clean)
- ✅ 依赖验证和健康检查
- ✅ 彩色输出和详细日志
- ✅ 跨平台兼容 (Linux/macOS/Windows)

### update_requirements.py
依赖更新脚本，用于：
- 从pip install命令自动生成requirements.txt
- 获取已安装包的精确版本
- 批量处理依赖包列表

## 📖 完整文档

查看 [DEPENDENCY_MANAGEMENT.md](DEPENDENCY_MANAGEMENT.md) 获取：
- 详细的依赖架构说明
- 现代化依赖管理方法 (Poetry/pipenv)
- 依赖维护和故障排除
- 团队协作最佳实践

## ⚙️ 环境要求

### pip版本要求
本项目需要使用 **pip 25.2** 或更高版本以确保依赖管理的兼容性和稳定性。

**检查当前pip版本**:
```bash
pip --version
```

**升级到指定版本**:
```bash
# 升级到最新版本
pip install --upgrade pip

# 安装指定版本 (如果需要)
pip install pip==25.2
```

**版本验证**:
```bash
# 应该显示: pip 25.2 from ... (python 3.12)
pip --version
```

> 💡 **提示**: 智能安装脚本 `install_dependencies.sh` 会自动检查并升级pip到最新版本

### Python版本
- **Python 3.12** 或更高版本
- 推荐使用虚拟环境 (venv)

## 🚨 注意事项

### 文件路径变更
> ⚠️ **重要**: 依赖文件已从项目根目录移动到 `dependencies/` 目录
> 
> 如果您的脚本、CI/CD或其他工具引用了以下文件，请更新路径：
> - `requirements.txt` → `dependencies/requirements.txt`
> - `requirements-dev.txt` → `dependencies/requirements-dev-only.txt`
> - `install_dependencies.sh` → `dependencies/install_dependencies.sh`

### Docker构建
如果使用Docker，需要更新Dockerfile中的路径：

```dockerfile
# 旧版本
COPY requirements.txt .
RUN pip install -r requirements.txt

# 新版本
COPY dependencies/requirements.txt .
RUN pip install -r requirements.txt
```

### CI/CD管道
更新CI/CD配置文件中的依赖安装命令：

```yaml
# 旧版本
- run: pip install -r requirements.txt

# 新版本  
- run: pip install -r dependencies/requirements.txt
```

## 🔗 相关文档

- [项目架构文档](../docs/PROJECT_ARCHITECTURE.md)
- [安装指南](../docs/guides/installation-guide.md)
- [开发指南](../docs/guides/development-guide.md)
- [Docker部署指南](../docs/guides/deployment-guide.md)

---

**目录版本**: v2.1.0  
**最后更新**: 2025-09-01  
**维护团队**: pythonProjectTemplate团队
