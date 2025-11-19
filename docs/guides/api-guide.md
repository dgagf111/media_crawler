# API接口文档

## 概述

本项目基于FastAPI构建，提供RESTful API接口，支持自动生成OpenAPI文档、请求验证、响应序列化等现代Web API特性。API采用版本化设计，当前版本为v1。

## API架构

### 接口规范

- **基础URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token (JWT)
- **数据格式**: JSON
- **字符编码**: UTF-8
- **API版本**: v1

### 响应格式

所有API接口都使用统一的响应格式：

```json
{
    "success": true,
    "code": 200,
    "message": "操作成功",
    "data": {},
    "timestamp": "2023-12-01T10:00:00Z"
}
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 操作是否成功 |
| `code` | integer | HTTP状态码 |
| `message` | string | 操作结果消息 |
| `data` | object/array | 返回的数据 |
| `timestamp` | string | 响应时间戳 |

### 错误处理

#### 错误响应格式

```json
{
    "success": false,
    "code": 400,
    "message": "请求参数有误",
    "errors": [
        {
            "field": "email",
            "message": "邮箱格式不正确"
        }
    ],
    "timestamp": "2023-12-01T10:00:00Z"
}
```

#### HTTP状态码

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证或token无效 |
| 403 | Forbidden | 权限不足 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 请求格式正确但语义错误 |
| 500 | Internal Server Error | 服务器内部错误 |

## 认证接口

### 用户登录

**接口地址**: `POST /api/v1/auth/login`

**请求参数**:
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "message": "登录成功",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 10800,
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "is_active": true,
            "created_at": "2023-12-01T10:00:00Z"
        }
    }
}
```

### 用户注册

**接口地址**: `POST /api/v1/auth/register`

**请求参数**:
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
}
```

**响应示例**:
```json
{
    "success": true,
    "code": 201,
    "message": "注册成功",
    "data": {
        "id": 2,
        "username": "newuser",
        "email": "newuser@example.com",
        "is_active": true,
        "created_at": "2023-12-01T10:05:00Z"
    }
}
```

### 刷新令牌

**接口地址**: `POST /api/v1/auth/refresh`

**请求头**:
```
Authorization: Bearer <refresh_token>
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "message": "令牌刷新成功",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 10800
    }
}
```

### 用户登出

**接口地址**: `POST /api/v1/auth/logout`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "message": "登出成功"
}
```

## 用户管理接口

### 获取当前用户信息

**接口地址**: `GET /api/v1/users/me`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "message": "获取成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "is_active": true,
        "is_verified": false,
        "created_at": "2023-12-01T10:00:00Z",
        "updated_at": "2023-12-01T10:00:00Z"
    }
}
```

### 更新用户信息

**接口地址**: `PUT /api/v1/users/me`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求参数**:
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "This is my updated bio"
}
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Updated",
        "last_name": "Name",
        "bio": "This is my updated bio",
        "updated_at": "2023-12-01T11:00:00Z"
    }
}
```

### 修改密码

**接口地址**: `POST /api/v1/users/change-password`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求参数**:
```json
{
    "current_password": "oldpassword123",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "message": "密码修改成功"
}
```

## 系统接口

### 健康检查

**接口地址**: `GET /health`

**响应示例**:
```json
{
    "status": "ok",
    "timestamp": "2023-12-01T10:00:00Z",
    "version": "1.0.0",
    "services": {
        "database": "connected",
        "cache": "connected",
        "scheduler": "running"
    }
}
```

### 系统信息

**接口地址**: `GET /api/v1/system/info`

**请求头**:
```
Authorization: Bearer <admin_token>
```

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "data": {
        "version": "1.0.0",
        "environment": "development",
        "uptime": "2 days, 3 hours, 45 minutes",
        "memory_usage": "156.7MB",
        "cpu_usage": "12.3%",
        "active_users": 42
    }
}
```

## 请求和响应示例

### 分页查询

大多数列表接口支持分页查询：

**接口地址**: `GET /api/v1/users?page=1&size=10&sort=created_at&order=desc`

**查询参数**:

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `page` | integer | 1 | 页码 |
| `size` | integer | 20 | 每页数量 |
| `sort` | string | id | 排序字段 |
| `order` | string | asc | 排序方向 (asc/desc) |

**响应示例**:
```json
{
    "success": true,
    "code": 200,
    "data": {
        "items": [
            {
                "id": 1,
                "username": "user1",
                "email": "user1@example.com"
            }
        ],
        "pagination": {
            "page": 1,
            "size": 10,
            "total": 100,
            "pages": 10,
            "has_prev": false,
            "has_next": true
        }
    }
}
```

### 搜索和过滤

**接口地址**: `GET /api/v1/users/search?q=john&status=active&created_after=2023-01-01`

**查询参数**:

| 参数 | 类型 | 说明 |
|------|------|------|
| `q` | string | 搜索关键词 |
| `status` | string | 用户状态过滤 |
| `created_after` | string | 创建时间过滤 |

## 开发工具

### API文档

项目集成了Swagger UI和ReDoc，提供交互式API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Postman集合

我们提供了Postman集合文件，包含所有API接口的示例请求：

```bash
# 导入Postman集合
docs/postman/PythonProjectTemplate.postman_collection.json

# 导入环境变量
docs/postman/PythonProjectTemplate.postman_environment.json
```

### 接口测试

#### 使用curl

```bash
# 用户登录
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "password123"
     }'

# 获取用户信息
curl -X GET "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer <access_token>"
```

#### 使用httpx (Python)

```python
import httpx
import asyncio

async def test_login():
    async with httpx.AsyncClient() as client:
        # 用户登录
        login_response = await client.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["data"]["access_token"]
            
            # 获取用户信息
            profile_response = await client.get(
                "http://localhost:8000/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            return profile_response.json()

# 运行测试
result = asyncio.run(test_login())
print(result)
```

#### 使用JavaScript/TypeScript

```javascript
// 使用fetch API
class ApiClient {
    constructor(baseURL = 'http://localhost:8000/api/v1') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('access_token');
    }
    
    async login(username, password) {
        const response = await fetch(`${this.baseURL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const result = await response.json();
        
        if (result.success) {
            this.token = result.data.access_token;
            localStorage.setItem('access_token', this.token);
        }
        
        return result;
    }
    
    async getProfile() {
        const response = await fetch(`${this.baseURL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        });
        
        return response.json();
    }
}

// 使用示例
const api = new ApiClient();

api.login('testuser', 'password123')
   .then(() => api.getProfile())
   .then(profile => console.log(profile));
```

## 错误处理指南

### 常见错误及解决方案

#### 1. 认证错误 (401)

```json
{
    "success": false,
    "code": 401,
    "message": "未认证或token无效"
}
```

**解决方案**:
- 检查请求头中是否包含正确的Authorization字段
- 验证token是否过期，如果过期使用refresh token获取新的access token
- 确保token格式正确: `Bearer <token>`

#### 2. 权限不足 (403)

```json
{
    "success": false,
    "code": 403,
    "message": "权限不足，无法访问该资源"
}
```

**解决方案**:
- 检查当前用户是否有相应的权限
- 联系管理员分配相应权限

#### 3. 参数验证错误 (422)

```json
{
    "success": false,
    "code": 422,
    "message": "请求参数验证失败",
    "errors": [
        {
            "field": "email",
            "message": "邮箱格式不正确"
        },
        {
            "field": "password",
            "message": "密码长度至少8位"
        }
    ]
}
```

**解决方案**:
- 根据errors字段中的提示修正请求参数
- 确保所有必填字段都已提供
- 验证字段格式和长度限制

#### 4. 资源不存在 (404)

```json
{
    "success": false,
    "code": 404,
    "message": "请求的资源不存在"
}
```

**解决方案**:
- 检查请求的URL是否正确
- 验证资源ID是否存在
- 确认API版本号是否正确

## 性能和限制

### 速率限制

为了保护API免受滥用，我们实施了速率限制：

| 接口类型 | 限制 |
|----------|------|
| 登录接口 | 每分钟5次 |
| 注册接口 | 每小时10次 |
| 一般接口 | 每分钟100次 |
| 搜索接口 | 每分钟30次 |

当超过限制时，API会返回429状态码：

```json
{
    "success": false,
    "code": 429,
    "message": "请求过于频繁，请稍后再试",
    "retry_after": 60
}
```

### 数据大小限制

- 请求体大小：最大10MB
- 单次查询返回记录：最大1000条
- 文件上传大小：最大50MB

### 性能建议

1. **使用分页**: 对于大量数据，使用分页查询避免一次性获取过多数据
2. **字段选择**: 使用fields参数只获取需要的字段
3. **缓存策略**: 对于不经常变化的数据，客户端可以实施适当的缓存策略
4. **并发控制**: 避免对同一接口发起过多并发请求

## 版本管理

### 版本策略

API采用语义化版本管理，版本号格式为：`vMAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的API变更
- **MINOR**: 新增功能，向后兼容
- **PATCH**: 问题修复，向后兼容

### 版本指定

可以通过以下方式指定API版本：

1. **URL路径** (推荐): `/api/v1/users`
2. **请求头**: `API-Version: 1.0`
3. **查询参数**: `/api/users?version=1.0`

### 版本弃用

当API版本需要弃用时：

1. 提前3个月发布弃用通知
2. 在响应头中添加弃用警告：`Deprecation: true`
3. 提供迁移指南
4. 设置明确的停用日期

## SDK和工具

### Python SDK

```python
from pythonprojecttemplate_sdk import ApiClient

# 初始化客户端
client = ApiClient(
    base_url="http://localhost:8000/api/v1",
    api_key="your_api_key"
)

# 用户登录
result = await client.auth.login("username", "password")

# 获取用户信息
user = await client.users.get_profile()
```

### JavaScript SDK

```javascript
import { ApiClient } from 'pythonprojecttemplate-js-sdk';

const client = new ApiClient({
    baseURL: 'http://localhost:8000/api/v1',
    apiKey: 'your_api_key'
});

// 用户登录
const loginResult = await client.auth.login('username', 'password');

// 获取用户信息
const user = await client.users.getProfile();
```

## 监控和分析

### API指标

系统提供以下API指标监控：

- 请求总数
- 响应时间分布
- 错误率统计
- 活跃用户数
- 接口使用频率

可以通过 `/metrics` 端点获取Prometheus格式的指标数据。

### 日志记录

所有API请求都会记录详细日志，包括：

- 请求时间
- 用户信息
- 请求参数
- 响应状态
- 处理时间

这些信息有助于问题排查和性能优化。

## 安全考虑

### HTTPS

生产环境必须使用HTTPS确保数据传输安全。

### 输入验证

所有输入数据都会进行严格验证，防止SQL注入、XSS等攻击。

### 访问控制

实施基于角色的访问控制（RBAC），确保用户只能访问授权的资源。

### 审计日志

记录所有重要操作的审计日志，便于安全审查。

通过遵循这些API设计和使用指南，开发者可以高效、安全地集成和使用本项目的API服务。