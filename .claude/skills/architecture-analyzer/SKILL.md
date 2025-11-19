---
name: architecture-analyzer
description: 分析代码仓库的整体架构，识别项目结构、模块依赖、设计模式和服务架构。适用于理解新代码库、审查架构设计或持续分析项目架构。
allowed-tools: Read, Glob, Grep, Task, Bash, Write, Edit, mcp__mcp-deepwiki
---

# 整体架构分析器

分析代码仓库的整体架构，识别项目结构、模块依赖、设计模式和服务架构，生成架构文档、架构图和改进建议。

## 使用说明

当用户要求分析代码库架构时，按以下步骤执行：

### 步骤 1: 项目基础分析

1. 扫描项目根目录，识别语言和框架：
   - Python: 查找 requirements.txt, pyproject.toml, setup.py
   - JavaScript/TypeScript: 查找 package.json
   - Go: 查找 go.mod, go.sum
   - Java: 查找 pom.xml, build.gradle
   - Rust: 查找 Cargo.toml
   - 其他语言特征文件

2. 分析项目结构：
   - 识别主要目录（src/, app/, lib/, modules/, etc）
   - 查看 README.md 和文档文件
   - 检查配置文件（.env*, config/, settings/）

3. 识别技术栈：
   - Web 框架（FastAPI, Flask, Django, Express, Spring Boot 等）
   - 数据库（SQLAlchemy, Prisma, TypeORM, GORM 等）
   - 消息队列、缓存、外部服务

### 步骤 2: 语言特定深度分析

根据识别的语言，进行深入分析：

#### Python 项目
1. 使用 Task 工具（subagent_type=Explore, thoroughness=very thorough）分析：
   - 模块导入关系和依赖
   - ORM 模型和数据库表结构
   - API 路由和端点
   - 中间件和装饰器
   - 异步模式和并发处理

2. 关键文件模式：
   - `src/**/models.py` - 数据模型
   - `src/**/services.py` - 业务逻辑
   - `src/**/repositories.py` - 数据访问
   - `src/api/routes/**/*.py` - API 路由
   - `src/**/config/**/*.py` - 配置管理

3. 识别设计模式：
   - 仓储模式（Repository）
   - 服务层模式（Service Layer）
   - 工厂模式（Factory）
   - 依赖注入（Dependency Injection）
   - 工作单元（Unit of Work）

#### JavaScript/TypeScript 项目
1. 分析：
   - 模块导入导出关系
   - React/Vue/Angular 组件结构
   - API 服务和数据流
   - 状态管理（Redux, Vuex, Zustand 等）
   - 路由配置

2. 关键文件模式：
   - `src/components/**/*` - UI 组件
   - `src/services/**/*` - API 服务
   - `src/store/**/*` - 状态管理
   - `src/routes/**/*` - 路由配置

### 步骤 3: 模块依赖分析

1. 分析模块/组件之间的依赖关系：
   - 使用依赖分析脚本生成模块依赖图
   - 识别循环依赖
   - 评估模块耦合度
   - 识别核心模块和边缘模块

2. 分析方法：
   ```bash
   # 对于 Python
   python .claude/skills/architecture-analyzer/scripts/analyze_dependencies.py python

   # 对于 JavaScript/TypeScript
   python .claude/skills/architecture-analyzer/scripts/analyze_dependencies.py js
   ```

### 步骤 4: 设计模式识别

1. 识别应用的设计模式：
   - 创建型模式：单例、工厂、建造者
   - 结构型模式：适配器、装饰器、代理、外观
   - 行为型模式：观察者、策略、命令、中介者

2. 分析架构模式：
   - 分层架构（Layered Architecture）
   - 六边形架构（Hexagonal Architecture）
   - 洋葱架构（Onion Architecture）
   - 微服务架构（Microservices）
   - 事件驱动架构（Event-Driven）

### 步骤 5: 数据流分析

1. 识别数据流动路径：
   - 用户请求 → API → 服务 → 仓库 → 数据库
   - 外部 API 调用和集成
   - 消息队列和异步任务
   - 缓存策略和数据一致性

2. 绘制数据流图：
   ```mermaid
   graph TD
       User[用户] --> API[HTTP API]
       API --> Service[业务服务]
       Service --> Cache[Redis Cache]
       Service --> Repository[数据仓库]
       Repository --> Database[(数据库)]
       Service --> Queue[消息队列]
       Queue --> Worker[异步任务]
   ```

### 步骤 6: 架构评估与改进建议

1. 评估架构质量：
   - 可维护性：模块化程度、耦合度、内聚性
   - 可扩展性：水平扩展能力、性能瓶颈
   - 可测试性：单元测试覆盖率、测试便利性
   - 可靠性：错误处理、容错机制、监控

2. 识别架构问题：
   - 过度耦合的模块
   - 职责不清晰的类/函数
   - 违反单一职责原则（SRP）
   - 循环依赖
   - 过大的文件或函数
   - 不一致的命名和结构

3. 提供改进建议：
   - 重构方向（提取服务、拆分模块）
   - 性能优化建议
   - 可扩展性改进
   - 测试策略建议
   - 监控和日志改进

### 步骤 7: 生成架构文档

创建包含以下内容的 markdown 文档：

1. 项目概览
   - 技术栈
   - 架构风格
   - 主要功能

2. 项目结构
   ```
   project/
   ├── src/
   │   ├── api/          # API 层
   │   ├── modules/      # 业务模块
   │   ├── core/         # 核心组件
   │   └── config/       # 配置
   ├── tests/
   └── docs/
   ```

3. 模块依赖图（mermaid）
4. 关键组件说明
5. 数据流图
6. 设计模式识别
7. 架构优点
8. 改进建议

## 示例输出

### 示例 1: 请求分析架构

**用户输入**: "分析这个项目的整体架构"

**执行流程**: 按照上述 7 个步骤完整分析，生成架构文档。

### 示例 2: 识别架构问题

**用户输入**: "审查这个代码库的架构设计问题"

**执行流程**:
- 重点执行步骤 6（架构评估）
- 识别具体问题
- 提供优先级排序的改进建议
- 生成架构问题报告

### 示例 3: 生成架构文档

**用户输入**: "为这个仓库生成架构文档"

**执行流程**:
- 执行完整分析
- 生成详细的 markdown 文档
- 包含 mermaid 图表
- 保存到 docs/architecture.md

## 最佳实践

- **多语言支持**: 自动识别代码库使用的语言，按照语言特性调整分析策略
- **渐进式分析**: 对于大型项目，先分析高层结构，再深入具体模块
- **可视化输出**: 尽可能生成 mermaid 图表，直观展示架构
- **提供可操作建议**: 不仅指出问题，还要给出具体的改进步骤
- **考虑上下文**: 结合项目的 README、文档和配置文件获取完整上下文

## 依赖项

```bash
# 脚本依赖（如需导出依赖图）
pip install ast-decompiler networkx matplotlib
```
