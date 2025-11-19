# 开发指南

## 开发环境配置

### IDE推荐配置

#### Visual Studio Code

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.associations": {
        "*.yaml": "yaml",
        "*.yml": "yaml"
    }
}
```

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "redhat.vscode-yaml",
        "ms-vscode.test-adapter-converter"
    ]
}
```

#### PyCharm配置

1. **解释器设置**: File → Settings → Python Interpreter → 选择虚拟环境
2. **代码风格**: File → Settings → Code Style → Python → 设置Line length为88
3. **导入优化**: Tools → Optimize Imports → 配置自动导入排序
4. **测试配置**: Run/Debug Configurations → 添加pytest配置

### Git配置

#### `.gitignore` 文件

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Environment Variables
.env
.env.local
.env.*.local

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Database
*.sqlite3
*.db

# Cache
.cache/
.pytest_cache/
.mypy_cache/

# OS
.DS_Store
Thumbs.db

# Project specific
temp/
tmp/
uploads/
```

#### Git Hooks

```bash
# 创建pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running pre-commit checks..."

# 运行代码格式化
black --check src/ tests/
if [ $? -ne 0 ]; then
    echo "Code formatting issues found. Run 'black src/ tests/' to fix."
    exit 1
fi

# 运行类型检查
mypy src/
if [ $? -ne 0 ]; then
    echo "Type checking failed."
    exit 1
fi

# 运行测试
python -m pytest tests/ -x
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

echo "All checks passed!"
EOF

chmod +x .git/hooks/pre-commit
```

## 代码规范

### Python代码风格

#### 1. PEP 8 规范

```python
# 好的例子
def calculate_user_score(user_id: int, base_score: float) -> float:
    """计算用户得分
    
    Args:
        user_id: 用户ID
        base_score: 基础分数
        
    Returns:
        计算后的用户得分
    """
    if user_id <= 0:
        raise ValueError("用户ID必须为正数")
    
    # 获取用户数据
    user_data = get_user_data(user_id)
    
    # 计算得分
    final_score = base_score * user_data.multiplier
    
    return round(final_score, 2)

# 避免的例子
def calc(uid,bs):
    if uid<=0:raise ValueError("Invalid ID")
    ud=get_user_data(uid)
    fs=bs*ud.multiplier
    return round(fs,2)
```

#### 2. 类型提示

```python
from typing import Optional, Dict, List, Union
from datetime import datetime

class UserService:
    def __init__(self, db: Database) -> None:
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user_data: Dict[str, Union[str, int]]) -> User:
        """创建新用户"""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        return user
    
    def get_user_list(self, limit: int = 10) -> List[User]:
        """获取用户列表"""
        return self.db.query(User).limit(limit).all()
```

#### 3. 文档字符串

```python
def process_payment(
    amount: float, 
    payment_method: str, 
    user_id: int,
    metadata: Optional[Dict[str, str]] = None
) -> PaymentResult:
    """处理支付请求
    
    这个函数处理用户的支付请求，支持多种支付方式，
    并返回支付结果。
    
    Args:
        amount: 支付金额，必须大于0
        payment_method: 支付方式 ('credit_card', 'alipay', 'wechat_pay')
        user_id: 用户ID
        metadata: 可选的元数据字典
        
    Returns:
        PaymentResult对象，包含支付状态和交易信息
        
    Raises:
        ValueError: 当金额小于等于0时
        PaymentError: 当支付处理失败时
        
    Example:
        >>> result = process_payment(100.0, 'credit_card', 12345)
        >>> print(result.status)
        'success'
    """
    if amount <= 0:
        raise ValueError("支付金额必须大于0")
    
    # 实现支付逻辑...
    pass
```

### 项目结构规范

#### 1. 模块组织

```python
# src/pythonprojecttemplate/services/user_service.py
from typing import Optional
from ..core.exceptions import UserNotFoundError
from ..core.utils import ValidationUtils
from ..models.user import User

class UserService:
    """用户服务类"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundError(f"用户 {user_id} 不存在")
        return user
```

#### 2. 导入规范

```python
# 标准库导入
import os
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, List

# 第三方库导入
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import redis

# 本地导入
from .core.config import settings
from .core.exceptions import BaseCustomException
from .core.utils import JWTUtils, PasswordUtils
from .models.user import User
from .services.auth_service import AuthService
```

## 开发工作流

### 1. 功能开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/user-authentication

# 2. 开发功能
# 编写代码...

# 3. 运行测试
python -m pytest tests/ -v

# 4. 代码格式化
black src/ tests/
isort src/ tests/

# 5. 类型检查
mypy src/

# 6. 提交代码
git add .
git commit -m "feat: 添加用户认证功能"

# 7. 推送并创建PR
git push origin feature/user-authentication
```

### 2. 测试驱动开发 (TDD)

```python
# 1. 先写测试 (tests/test_user_service.py)
import pytest
from src.pythonprojecttemplate.services.user_service import UserService
from src.pythonprojecttemplate.core.exceptions import UserNotFoundError

def test_get_user_by_id_success():
    """测试成功获取用户"""
    service = UserService(mock_db_session)
    user = service.get_user_by_id(1)
    assert user.id == 1
    assert user.email == "test@example.com"

def test_get_user_by_id_not_found():
    """测试用户不存在的情况"""
    service = UserService(mock_db_session)
    with pytest.raises(UserNotFoundError):
        service.get_user_by_id(999)

# 2. 运行测试 (应该失败)
pytest tests/test_user_service.py -v

# 3. 实现功能代码
# src/pythonprojecttemplate/services/user_service.py
class UserService:
    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundError(f"用户 {user_id} 不存在")
        return user

# 4. 再次运行测试 (应该通过)
pytest tests/test_user_service.py -v
```

### 3. 代码审查清单

#### 功能性
- [ ] 功能是否按需求正确实现？
- [ ] 边界条件是否正确处理？
- [ ] 错误处理是否完善？
- [ ] 性能是否满足要求？

#### 代码质量
- [ ] 代码是否遵循PEP 8规范？
- [ ] 变量和函数命名是否清晰？
- [ ] 是否有适当的注释和文档？
- [ ] 是否有重复代码？

#### 测试覆盖
- [ ] 是否有充分的单元测试？
- [ ] 测试用例是否覆盖主要场景？
- [ ] 是否测试了异常情况？

#### 安全性
- [ ] 是否有SQL注入风险？
- [ ] 用户输入是否经过验证？
- [ ] 敏感信息是否正确处理？

## 调试技巧

### 1. 日志调试

```python
from log.logHelper import get_logger

logger = get_logger()

def process_order(order_data: dict):
    logger.debug(f"开始处理订单: {order_data}")
    
    try:
        # 验证订单数据
        validated_data = validate_order(order_data)
        logger.info(f"订单验证成功: {validated_data['order_id']}")
        
        # 处理支付
        payment_result = process_payment(validated_data)
        logger.info(f"支付处理完成: {payment_result}")
        
        return payment_result
        
    except ValidationError as e:
        logger.error(f"订单验证失败: {e}", exc_info=True)
        raise
    except PaymentError as e:
        logger.error(f"支付处理失败: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f"订单处理异常: {e}", exc_info=True)
        raise
```

### 2. 断点调试

```python
# 使用pdb调试器
import pdb

def complex_calculation(data):
    result = 0
    for item in data:
        pdb.set_trace()  # 设置断点
        result += item * 2
    return result

# 使用IPython调试器 (推荐)
from IPython import embed

def debug_function(params):
    # 一些复杂逻辑
    processed_data = process_data(params)
    
    embed()  # 进入交互式调试环境
    
    return processed_data
```

### 3. 性能分析

```python
import cProfile
import pstats
from functools import wraps

def profile(func):
    """性能分析装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats()
        
        return result
    return wrapper

@profile
def slow_function():
    # 需要分析的慢函数
    pass
```

## 部署准备

### 1. 环境配置

```bash
# 创建部署配置文件
# config/prod.yaml
api:
  host: "0.0.0.0"
  port: 8000
  debug: false
  cors_origins: 
    - "https://yourdomain.com"
  
cache:
  type: redis
  redis:
    host: ${REDIS_HOST}
    port: 6379
    db: 0

monitoring:
  prometheus_port: 9966
  enable_metrics: true
```

### 2. 依赖管理

```bash
# 生成生产环境依赖
pip-compile requirements.in --output-file requirements.txt

# 创建开发依赖文件
# requirements-dev.in
-r requirements.in
pytest
pytest-cov
black
flake8
mypy
pre-commit

# 编译开发依赖
pip-compile requirements-dev.in --output-file requirements-dev.txt
```

### 3. 构建脚本

```bash
#!/bin/bash
# scripts/build.sh

set -e

echo "开始构建应用..."

# 清理旧文件
rm -rf dist/
rm -rf build/

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/ -v

# 构建包
python -m build

# 生成Docker镜像
docker build -t pythonprojecttemplate:latest .

echo "构建完成!"
```

## 最佳实践

### 1. 错误处理

```python
# 好的错误处理
def divide_numbers(a: float, b: float) -> float:
    """安全的除法运算"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("参数必须为数字类型")
    
    if b == 0:
        raise ValueError("除数不能为零")
    
    try:
        result = a / b
        return result
    except Exception as e:
        logger.error(f"除法运算失败: a={a}, b={b}", exc_info=True)
        raise RuntimeError(f"计算错误: {e}") from e
```

### 2. 配置管理

```python
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    """应用配置"""
    database_url: str
    secret_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """获取配置实例 (缓存)"""
    return Settings()
```

### 3. 依赖注入

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    # 验证token并返回用户
    pass

# 在API中使用
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 4. 缓存策略

```python
from functools import wraps
import json
import hashlib

def cache_result(ttl: int = 3600):
    """结果缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{hash_args(args, kwargs)}"
            
            # 尝试从缓存获取
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            await redis_client.setex(
                cache_key, 
                ttl, 
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator

def hash_args(args, kwargs):
    """生成参数哈希"""
    content = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(content.encode()).hexdigest()
```

这个开发指南为团队提供了统一的开发标准和最佳实践，确保代码质量和开发效率。