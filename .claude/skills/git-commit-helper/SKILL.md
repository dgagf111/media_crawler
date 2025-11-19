---
name: git-commit-helper

description: 分析 git diff 生成 Conventional Commits 格式的中文提交信息。当需要编写提交信息、审查暂存更改或自动化 commit 时使用。支持 Git 操作、提交信息生成和代码提交。

allowed-tools: Bash, Read, Write, Edit, Grep

initial-prompt: |
  你是一个专业的 Git 提交助手，专门帮助用户生成符合 Conventional Commits 规范的中文提交信息。

  **核心要求：**
  1. 所有提交信息必须使用中文
  2. 遵循 Conventional Commits 格式：type(scope): description
  3. 使用祈使语气的中文描述
  4. 智能分析代码更改并建议合适的提交类型

  **工作流程：**
  1. 分析当前 Git 状态和暂存的更改
  2. 智能识别更改类型（feat/fix/refactor/test/docs 等）
  3. 确定合适的作用域（api/db/auth 等）
  4. 生成中文提交信息建议
  5. 协助用户完成提交

  **中文提交信息示例：**
  - feat(auth): 添加用户认证功能
  - fix(api): 修复空指针异常
  - refactor(db): 重构数据库连接逻辑
  - docs(readme): 更新安装说明

  始终优先使用中文进行所有交互和信息生成。

## 中文提交信息生成规则

### 智能分析流程
1. **文件类型识别**：根据文件扩展名和路径判断更改类型
2. **内容分析**：分析代码更改的具体内容和意图
3. **类型推断**：自动推断最适合的提交类型
4. **中文生成**：使用中文生成符合规范的信息

### 中文提交类型映射
- **feat** → 新功能、新增、添加、实现
- **fix** → 修复、解决、处理、修正
- **refactor** → 重构、优化、改进、简化
- **test** → 测试、用例、验证、覆盖
- **docs** → 文档、说明、注释、指南
- **style** → 格式、风格、样式、美化
- **chore** → 维护、配置、依赖、更新

### 作用域中文化建议
- **api** → 接口、API、路由
- **db** → 数据库、模型、存储
- **auth** → 认证、权限、用户
- **ui** → 界面、组件、样式
- **config** → 配置、设置、环境
- **utils** → 工具、函数、辅助

### 中文描述模板
- 新功能：`添加 {功能名称} 功能`、`实现 {功能描述} 支持`
- Bug 修复：`修复 {问题} 错误`、`解决 {异常} 问题`
- 重构：`重构 {模块} 代码`、`优化 {功能} 实现`
- 文档：`更新 {文档} 说明`、`完善 {指南} 内容`

---

# Git 提交助手

智能分析 Git 更改并生成符合 Conventional Commits 规范的中文提交信息。

## 快速开始

### 方式 1: 交互式提交助手
```bash
# 运行自动化提交脚本
./scripts/commit-helper.sh
```

### 方式 2: 手动分析提交
```bash
# 查看已暂存的更改
git diff --staged

# Claude 将根据 diff 内容建议合适的提交信息
```

### 方式 3: 一键提交
```bash
# 暂存所有更改并提交
git add .
git commit -m "feat(scope): 描述性提交信息"
```

## 提交信息格式

遵循 Conventional Commits 格式：

```
<type>(<scope>): <description>

[可选正文]

[可选页脚]
```

### 类型

- **feat**: 新功能
- **fix**: Bug 修复
- **docs**: 文档修改
- **style**: 代码样式修改（格式化、缺少分号等）
- **refactor**: 代码重构
- **test**: 添加或更新测试
- **chore**: 维护性任务

### 示例

**新功能提交：**

```
feat(auth): 添加 JWT 认证

实现基于 JWT 的认证系统，包括：
- 带令牌生成的登录端点
- 令牌验证中间件
- 刷新令牌支持
```

**Bug 修复：**

```
fix(api): 处理用户资料中的 null 值

防止当用户资料字段为 null 时出现崩溃。
在访问嵌套属性前增加 null 检查。
```

**代码重构：**

```
refactor(database): 简化查询构建器

将常见的查询模式提取为可重用函数。
减少数据库层的代码重复。
```

## 分析更改

查看将要提交的内容：

```bash
# 显示已修改文件
git status

# 显示详细更改
git diff --staged

# 显示统计信息
git diff --staged --stat

# 显示指定文件的更改
git diff --staged path/to/file
```

## 提交信息编写指南

**应当：**

- 使用祈使语气（“add feature”，而不是“added feature”）
- 保持首行少于 50 个字符
- 首字母大写
- 不在摘要末尾加句号
- 在正文中解释“为什么”，而不仅仅是“做了什么”

**不应：**

- 使用模糊的信息，如 “update” 或 “fix stuff”
- 在摘要中包含技术实现细节
- 在摘要行写成段落
- 使用过去时态

## 多文件提交

当提交多个相关更改时：

```
refactor(core): 重构认证模块

- 将认证逻辑从控制器移动到服务层
- 将验证逻辑提取为独立验证器
- 更新测试以适配新结构
- 添加认证流程的集成测试

重大变更：认证服务现在需要配置对象
```

## 作用域示例

**前端：**

- `feat(ui): 为仪表板添加加载动画`
- `fix(form): 验证邮箱格式`

**后端：**

- `feat(api): 添加用户资料接口`
- `fix(db): 解决连接池泄漏问题`

**基础设施：**

- `chore(ci): 更新 Node 版本至 20`
- `feat(docker): 添加多阶段构建`

## 重大变更（Breaking Changes）

明确标示重大变更：

```
feat(api)!: 重构 API 响应格式

BREAKING CHANGE: 所有 API 响应现在遵循 JSON:API 规范

之前格式：
{ "data": {…}, "status": "ok" }

新的格式：
{ "data": {…}, "meta": {…} }

迁移指南：更新客户端代码以处理新的响应结构
```

## 模板化工作流程

1. **审查更改**：`git diff --staged`

2. **确定类型**：是 feat、fix、refactor 等？

3. **确定作用域**：修改的是代码的哪个部分？

4. **编写摘要**：简短且使用祈使语气

5. **补充正文**：解释原因和影响

6. **标注重大变更**：如适用

## 交互式提交助手

使用 `git add -p` 选择性暂存：

```bash
# 交互式暂存更改
git add -p

# 查看已暂存的内容
git diff --staged

# 提交并写入信息
git commit -m "type(scope): description"
```

## 修改提交

修正上一次提交信息：

```bash
# 仅修改提交信息
git commit --amend

# 修改并添加更多更改
git add forgotten-file.js
git commit --amend --no-edit
```

## 最佳实践

1. **原子提交** —— 每次提交仅包含一个逻辑更改

2. **提交前测试** —— 确保代码可运行

3. **引用问题** —— 如果适用，包含 issue 编号

4. **保持聚焦** —— 不要混合无关更改

5. **为人类编写** —— 未来的你会阅读这些信息

## 提交信息检查清单

- [ ] 类型合适（feat/fix/docs 等）
- [ ] 作用域具体且明确
- [ ] 摘要不超过 50 个字符
- [ ] 摘要使用祈使语气
- [ ] 正文解释"为什么"而不仅是"做了什么"
- [ ] 明确标注重大变更
- [ ] 包含相关 issue 编号

## 辅助工具

### 交互式提交脚本
使用 [`scripts/commit-helper.sh`](scripts/commit-helper.sh) 进行智能提交：

```bash
# 给脚本执行权限（首次使用）
chmod +x scripts/commit-helper.sh

# 运行交互式提交助手
./scripts/commit-helper.sh
```

**脚本功能：**
- 自动检测暂存的更改
- 分析文件类型和更改统计
- 建议合适的提交类型
- 交互式生成符合规范的提交信息
- 支持详细描述和多行提交信息

### 更多示例
查看 [`examples.md`](examples.md) 获取：
- 实际项目提交示例
- 批量提交策略
- 高级用法技巧
- 常见问题处理

### 快速别名设置
在 `.bashrc` 或 `.zshrc` 中添加：
```bash
# Git 提交助手别名
alias gcommit="./scripts/commit-helper.sh"
alias gst="git status"
alias gadd="git add ."

# 使用方式：
# gadd    # 暂存所有更改
# gst     # 查看状态
# gcommit # 运行提交助手
```
