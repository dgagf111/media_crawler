# Git 提交助手示例

## 实际使用场景

### 场景 1: 功能开发
```bash
# 开发新功能后
git add src/api/user.py tests/test_user.py
./scripts/commit-helper.sh

# 建议的提交信息：
feat(auth): 添加用户认证功能

实现基于 JWT 的用户认证系统：
- 添加登录/注册端点
- 实现令牌生成和验证
- 添加相关单元测试
```

### 场景 2: Bug 修复
```bash
# 修复 bug 后
git add src/utils/validation.py
git commit -m "fix(validation): 修复邮箱格式验证正则表达式

之前的正则表达式无法正确验证包含子域名的邮箱地址。
现在支持 user@sub.domain.com 格式。"
```

### 场景 3: 文档更新
```bash
# 更新文档后
git add README.md docs/api.md
./scripts/commit-helper.sh

# 建议的提交信息：
docs(readme): 更新安装和快速开始指南

- 添加 Python 版本要求
- 完善依赖安装说明
- 添加故障排查章节
```

### 场景 4: 代码重构
```bash
# 重构代码后
git add src/core/database.py src/repositories/base.py
git commit -m "refactor(db): 重构数据库连接池管理

将连接池逻辑从 Database 类中提取为独立的
ConnectionPool 类，提高代码可维护性和测试性。"
```

### 场景 5: 测试相关
```bash
# 添加测试后
git add tests/test_integration.py tests/fixtures/user_data.json
./scripts/commit-helper.sh

# 建议的提交信息：
test(integration): 添加用户注册流程集成测试

覆盖从注册到验证的完整用户流程，
包括边界条件和错误处理场景。
```

## 批量提交示例

### 大型功能拆分提交
```bash
# 第1次：基础结构
git add src/models/user.py src/database/migrations/
git commit -m "feat(models): 定义用户数据模型

创建 User 模型和相关数据库迁移脚本。"

# 第2次：API 端点
git add src/api/routes/users.py src/schemas/user.py
git commit -m "feat(api): 添加用户管理端点

实现用户的 CRUD 操作：
- POST /users - 创建用户
- GET /users/{id} - 获取用户信息
- PUT /users/{id} - 更新用户
- DELETE /users/{id} - 删除用户"

# 第3次：业务逻辑
git add src/services/user_service.py
git commit -m "feat(services): 实现用户业务逻辑

添加用户注册、验证和权限检查等核心业务逻辑。"

# 第4次：测试
git add tests/test_user_service.py tests/test_api_users.py
git commit -m "test(user): 添加用户功能完整测试套件

包含单元测试、集成测试和边界条件测试。"
```

## 高级用法

### 使用 Issue 编号
```bash
# 关联 GitHub Issue
git add src/feature.py
git commit -m "feat(payment): 集成 Stripe 支付网关 (#123)

实现信用卡支付功能，支持：
- 一次性支付
- 订阅计费
- 退款处理

Closes #123"
```

### 重大变更标记
```bash
# 破坏性变更
git add src/api/v2/
git commit -m "feat(api)!: 重构 API 响应格式 v2

BREAKING CHANGE: 所有 API 响应现在遵循 JSON:API 规范

之前格式：
{ "data": {...}, "status": "ok" }

新的格式：
{ "data": {...}, "meta": {...}, "links": {...} }

迁移指南：更新客户端代码以处理新的响应结构"
```

### 自动化提交脚本
```bash
# 创建自动化提交别名
echo 'alias gcommit="./scripts/commit-helper.sh"' >> ~/.bashrc
echo 'alias gst="git status"' >> ~/.bashrc
echo 'alias gadd="git add ."' >> ~/.bashrc

# 现在可以快速使用：
gadd   # 暂存所有更改
gcommit  # 运行提交助手
```

## 最佳实践示例

### 好的提交信息
```
✅ feat(auth): 实现 JWT 双令牌认证机制

添加访问令牌和刷新令牌支持：
- 访问令牌有效期 15 分钟
- 刷新令牌有效期 7 天
- 自动令牌轮换机制

提升安全性同时保持用户体验。
```

### 需要改进的提交信息
```
❌ 修复登录问题

❌ update code

❌ feat: 添加用户

❌ 修复了认证的bug并添加了测试
```

### 原子提交示例
```bash
# 每个提交只做一件事
git add src/utils/logger.py
git commit -m "feat(utils): 添加结构化日志记录"

git add src/middleware/logging.py
git commit -m "feat(middleware): 添加请求日志中间件"

git add config/logging.yaml
git commit -m "chore(config): 配置日志输出格式"
```

## 常见问题处理

### 忘记暂存文件
```bash
# 提交后发现问题
git add forgotten_file.py
git commit --amend --no-edit  # 添加到上一次提交
```

### 错误的提交信息
```bash
# 修改最后一次提交信息
git commit --amend

# 或者修改更早的提交（需要 rebase）
git rebase -i HEAD~3
```

### 撤销提交
```bash
# 保留更改，撤销提交
git reset --soft HEAD~1

# 完全撤销（包括更改）
git reset --hard HEAD~1
```