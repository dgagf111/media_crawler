# 认证系统文档

## 概述

认证系统提供了基于JWT (JSON Web Token) 的用户认证和授权功能，包括用户注册、登录、令牌刷新、权限验证等完整的认证流程。系统采用现代化的安全设计，支持访问令牌和刷新令牌分离机制。

## 架构设计

### 核心组件

```
认证系统组件分布：
├── src/pythonprojecttemplate/
│   ├── core/
│   │   ├── constants.py      # JWT相关常量
│   │   ├── utils.py          # JWT和密码工具类
│   │   └── exceptions.py     # 认证异常定义
│   ├── services/
│   │   └── auth_service.py   # 认证服务主逻辑
│   └── models/
│       └── user.py          # 用户模型
└── api/auth/                # API接口层
    ├── login.py             # 登录接口
    └── deps.py              # 依赖注入
```

### 安全特性

1. **JWT令牌机制**: 使用RS256/HS256算法签名
2. **双令牌设计**: 访问令牌(短期) + 刷新令牌(长期)
3. **密码安全**: bcrypt哈希加密，自适应成本
4. **依赖注入**: 基于FastAPI的依赖系统
5. **异常处理**: 统一的认证异常管理

## 功能模块

### 1. 用户模型 (User Model)

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }
```

### 2. JWT工具类 (JWTUtils)

```python
from src.pythonprojecttemplate.core.utils import JWTUtils
from src.pythonprojecttemplate.core.constants import Constants

class JWTUtils:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """创建访问令牌"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=Constants.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire, "type": "access"})
        
        return jwt.encode(
            to_encode, 
            Constants.SECRET_KEY, 
            algorithm=Constants.ALGORITHM
        )
    
    @staticmethod
    def create_refresh_token(data: dict):
        """创建刷新令牌"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            days=Constants.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire, "type": "refresh"})
        
        return jwt.encode(
            to_encode,
            Constants.SECRET_KEY,
            algorithm=Constants.ALGORITHM
        )
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """解码令牌"""
        try:
            payload = jwt.decode(
                token,
                Constants.SECRET_KEY,
                algorithms=[Constants.ALGORITHM]
            )
            return payload
        except JWTError:
            raise AuthenticationError("无效的令牌")
```

### 3. 密码工具类 (PasswordUtils)

```python
from src.pythonprojecttemplate.core.utils import PasswordUtils

class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """哈希密码"""
        return bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def generate_password(length: int = 12) -> str:
        """生成随机密码"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
```

### 4. 认证服务 (AuthService)

```python
from src.pythonprojecttemplate.services.auth_service import AuthService

class AuthService:
    def __init__(self, db_session):
        self.db = db_session
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = self.db.query(User).filter(
            User.username == username
        ).first()
        
        if not user or not PasswordUtils.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            raise AuthenticationError("账户已被禁用")
        
        return user
    
    def create_user(self, user_data: dict) -> User:
        """创建用户"""
        # 检查用户名和邮箱唯一性
        existing_user = self.db.query(User).filter(
            (User.username == user_data['username']) |
            (User.email == user_data['email'])
        ).first()
        
        if existing_user:
            raise ValidationError("用户名或邮箱已存在")
        
        # 创建新用户
        hashed_password = PasswordUtils.hash_password(user_data['password'])
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            hashed_password=hashed_password
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def login(self, username: str, password: str) -> dict:
        """用户登录"""
        user = self.authenticate_user(username, password)
        if not user:
            raise AuthenticationError("用户名或密码错误")
        
        # 生成令牌
        access_token = JWTUtils.create_access_token(
            data={"sub": str(user.id)}
        )
        refresh_token = JWTUtils.create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        """刷新访问令牌"""
        try:
            payload = JWTUtils.decode_token(refresh_token)
            
            # 验证令牌类型
            if payload.get("type") != "refresh":
                raise AuthenticationError("无效的刷新令牌")
            
            user_id = payload.get("sub")
            user = self.db.query(User).filter(User.id == int(user_id)).first()
            
            if not user or not user.is_active:
                raise AuthenticationError("用户不存在或已被禁用")
            
            # 生成新的访问令牌
            new_access_token = JWTUtils.create_access_token(
                data={"sub": str(user.id)}
            )
            
            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }
            
        except JWTError:
            raise AuthenticationError("无效的刷新令牌")
```

## API接口

### 1. 登录接口

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录"""
    try:
        auth_service = AuthService(db)
        result = auth_service.login(form_data.username, form_data.password)
        
        return ResultVO.success(data=result)
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/refresh")
async def refresh_token(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db)
):
    """刷新访问令牌"""
    try:
        auth_service = AuthService(db)
        result = auth_service.refresh_access_token(refresh_token)
        
        return ResultVO.success(data=result)
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/register")
async def register(
    user_data: UserCreateSchema,
    db: Session = Depends(get_db)
):
    """用户注册"""
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data.dict())
        
        return ResultVO.success(
            data=user.to_dict(),
            message="注册成功"
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### 2. 依赖注入

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    try:
        payload = JWTUtils.decode_token(token)
        
        # 验证令牌类型
        if payload.get("type") != "access":
            raise AuthenticationError("无效的访问令牌")
        
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("无效的令牌")
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None or not user.is_active:
            raise AuthenticationError("用户不存在或已被禁用")
        
        return user
        
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取超级用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

## 使用示例

### 1. 用户注册和登录

```python
from httpx import AsyncClient

# 用户注册
async def register_user():
    async with AsyncClient() as client:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
        
        response = await client.post(
            "http://localhost:8000/api/v1/auth/register",
            json=user_data
        )
        
        return response.json()

# 用户登录
async def login_user():
    async with AsyncClient() as client:
        login_data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        
        response = await client.post(
            "http://localhost:8000/api/v1/auth/login",
            data=login_data
        )
        
        return response.json()
```

### 2. 受保护的API端点

```python
@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """获取用户资料"""
    return ResultVO.success(data=current_user.to_dict())

@router.put("/profile")
async def update_profile(
    profile_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户资料"""
    # 更新用户信息
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return ResultVO.success(
        data=current_user.to_dict(),
        message="资料更新成功"
    )
```

### 3. 前端集成示例

```javascript
// JavaScript/TypeScript 示例
class AuthService {
    private baseURL = 'http://localhost:8000/api/v1/auth';
    
    async login(username: string, password: string) {
        const response = await fetch(`${this.baseURL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username,
                password
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 存储令牌
            localStorage.setItem('access_token', result.data.access_token);
            localStorage.setItem('refresh_token', result.data.refresh_token);
            return result.data.user;
        } else {
            throw new Error(result.message);
        }
    }
    
    async makeAuthenticatedRequest(url: string, options: RequestInit = {}) {
        const token = localStorage.getItem('access_token');
        
        const response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            }
        });
        
        // 如果令牌过期，尝试刷新
        if (response.status === 401) {
            await this.refreshToken();
            return this.makeAuthenticatedRequest(url, options);
        }
        
        return response;
    }
    
    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        
        const response = await fetch(`${this.baseURL}/refresh`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh_token: refreshToken
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            localStorage.setItem('access_token', result.data.access_token);
        } else {
            // 刷新失败，跳转到登录页
            this.logout();
            window.location.href = '/login';
        }
    }
    
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
}
```

## 安全最佳实践

### 1. 密码策略

```python
import re

class PasswordPolicy:
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        if len(password) < 8:
            raise ValidationError("密码长度至少8位")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("密码必须包含至少一个大写字母")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("密码必须包含至少一个小写字母")
        
        if not re.search(r'\d', password):
            raise ValidationError("密码必须包含至少一个数字")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("密码必须包含至少一个特殊字符")
        
        return True
```

### 2. 速率限制

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")  # 每分钟最多5次登录尝试
async def login(request: Request, ...):
    # 登录逻辑
    pass
```

### 3. 令牌黑名单

```python
class TokenBlacklist:
    def __init__(self, cache):
        self.cache = cache
    
    def add_token(self, token: str, exp_time: datetime):
        """将令牌添加到黑名单"""
        ttl = int((exp_time - datetime.utcnow()).total_seconds())
        if ttl > 0:
            self.cache.set(f"blacklist:{token}", True, ttl=ttl)
    
    def is_blacklisted(self, token: str) -> bool:
        """检查令牌是否在黑名单中"""
        return self.cache.exists(f"blacklist:{token}")
    
    def revoke_token(self, token: str):
        """撤销令牌"""
        try:
            payload = JWTUtils.decode_token(token)
            exp_time = datetime.fromtimestamp(payload.get('exp', 0))
            self.add_token(token, exp_time)
        except JWTError:
            pass
```

### 4. 多因素认证 (2FA)

```python
import pyotp
import qrcode
from io import BytesIO

class TwoFactorAuth:
    @staticmethod
    def generate_secret() -> str:
        """生成2FA密钥"""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(user_email: str, secret: str) -> bytes:
        """生成QR码"""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name="Your App Name"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """验证TOTP令牌"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
```

## 监控和日志

### 1. 认证事件日志

```python
from log.logHelper import get_logger

logger = get_logger()

class AuthLogger:
    @staticmethod
    def log_login_success(user_id: int, ip_address: str):
        logger.info(f"用户登录成功 - 用户ID: {user_id}, IP: {ip_address}")
    
    @staticmethod
    def log_login_failure(username: str, ip_address: str, reason: str):
        logger.warning(f"登录失败 - 用户名: {username}, IP: {ip_address}, 原因: {reason}")
    
    @staticmethod
    def log_token_refresh(user_id: int):
        logger.info(f"令牌刷新 - 用户ID: {user_id}")
    
    @staticmethod
    def log_logout(user_id: int):
        logger.info(f"用户登出 - 用户ID: {user_id}")
```

### 2. 安全指标监控

```python
from prometheus_client import Counter, Histogram

# 认证相关指标
auth_attempts = Counter('auth_attempts_total', 
                       'Total authentication attempts',
                       ['status', 'method'])

auth_duration = Histogram('auth_duration_seconds',
                         'Authentication duration')

active_sessions = Gauge('active_sessions_total',
                       'Number of active user sessions')
```

## 故障排除

### 常见问题

1. **令牌解码失败**
   ```python
   # 检查SECRET_KEY配置
   # 确保算法一致
   # 验证令牌格式
   ```

2. **密码验证失败**
   ```python
   # 检查密码哈希过程
   # 确保bcrypt版本一致
   # 验证字符编码
   ```

3. **依赖注入错误**
   ```python
   # 检查FastAPI依赖配置
   # 确保数据库会话正确传递
   # 验证OAuth2配置
   ```

通过合理配置和使用认证系统，可以为应用程序提供强大而安全的用户认证功能。关键是要根据安全需求选择合适的策略和配置。