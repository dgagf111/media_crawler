---

name: skill-writer  
description: 引导用户为 Claude Code 创建 Agent Skills。当用户希望创建、编写、设计新的 Skill，或需要帮助编写 SKILL.md 文件、前置信息（frontmatter）、或技能结构时使用。

# 技能编写助手（Skill Writer）

该技能帮助你创建符合最佳实践与验证要求的 Claude Code Agent 技能。

## 何时使用此技能

在以下情况下使用本技能：

- 创建新的 Agent Skill
    
- 编写或更新 SKILL.md 文件
    
- 设计技能结构与 frontmatter
    
- 排查技能识别问题
    
- 将现有提示词或工作流转换为 Skill
    

## 使用说明

### 第 1 步：确定 Skill 的作用范围

首先，明确该 Skill 应完成的功能：

1. **提出澄清性问题**：
    
    - 该 Skill 应提供哪些具体能力？
        
    - Claude 何时应使用该 Skill？
        
    - 它需要哪些工具或资源？
        
    - 是供个人使用还是团队共享？
        
2. **保持专注：一个 Skill = 一个能力**
    
    - ✅ 好例子：“PDF 表单填写”、“Excel 数据分析”
        
    - ❌ 太宽泛：“文档处理”、“数据工具”
        

### 第 2 步：选择 Skill 存放位置

确定 Skill 的创建位置：

**个人技能**（`~/.claude/skills/`）：

- 个人工作流与偏好
    
- 实验性技能
    
- 个人效率工具
    

**项目技能**（`.claude/skills/`）：

- 团队工作流与约定
    
- 项目特定能力
    
- 共享工具（可提交至 git）
    

### 第 3 步：创建技能结构

创建目录与文件：

```bash
# 个人技能
mkdir -p ~/.claude/skills/skill-name

# 项目技能
mkdir -p .claude/skills/skill-name
```

多文件技能结构：

```
skill-name/
├── SKILL.md（必需）
├── reference.md（可选）
├── examples.md（可选）
├── scripts/
│   └── helper.py（可选）
└── templates/
    └── template.txt（可选）
```

### 第 4 步：编写 SKILL.md frontmatter

创建带必填字段的 YAML frontmatter：

```yaml
---

name: skill-name
description: 简要描述功能及使用场景

---

````

**字段要求**：

- **name**：

	- 仅限小写字母、数字、连字符

	- 最长 64 个字符

	- 必须与目录名一致

	- ✅ 示例：`pdf-processor`, `git-commit-helper`

	- ❌ 示例：`PDF_Processor`, `Git Commits!`

- **description**：

	- 最长 1024 个字符

	- 必须同时包含「功能」与「使用场景」

	- 使用用户可能说出的触发词

	- 指明文件类型、操作与上下文

**可选字段**：

- **allowed-tools**：限制可用工具（逗号分隔）

	```yaml
    allowed-tools: Read, Grep, Glob
    ```

	适用于：

	- 只读技能

	- 安全敏感场景

	- 功能范围受限的操作

### 第 5 步：撰写高效描述

描述是 Claude 能否发现技能的关键。

**公式**：`[做什么] + [何时用] + [触发词]`

**示例**：

✅ **好例子**：

```yaml
description: 提取 PDF 文件中的文本和表格、填写表单、合并文档。当处理 PDF、表单或文档提取任务时使用。
````

✅ **好例子**：

```yaml
description: 分析 Excel 表格、创建数据透视表并生成图表。适用于处理 Excel 文件、电子表格或 .xlsx 格式的表格数据分析。
```

❌ **模糊例子**：

```yaml
description: 帮助处理文档
description: 用于数据分析
```

**技巧**：

- 指明文件扩展名（.pdf,.xlsx,.json）
- 包含常见动作词（" 分析 "、" 提取 "、" 生成 "）
- 使用具体操作而非泛化动词
- 添加上下文提示（" 当……时使用 "、" 用于……"）

### 第 6 步：组织技能内容结构

采用清晰的 Markdown 章节：

````markdown
# 技能名称

简要说明该技能的功能。

## 快速开始

提供立即可用的示例。

## 使用说明

为 Claude 提供分步指导：

1. 明确的第一步操作

2. 第二步及预期结果

3. 处理边界情况

## 示例

展示具体使用案例（代码或命令）。

## 最佳实践

- 应遵循的关键约定
- 常见陷阱
- 适用与不适用场景

## 依赖项

列出所需依赖：

```bash
pip install package-name
```
````

## 高级用法

更多复杂示例见 [reference.md](https://chatgpt.com/c/reference.md)

````

### 第 7 步：添加辅助文件（可选）

用于渐进式展示的附加文件：

**reference.md**：API 详情、高级选项
**examples.md**：扩展示例与用例
**scripts/**：辅助脚本与工具
**templates/**：模板或样板文件

在 SKILL.md 中引用：
```markdown
详细用法见 [reference.md](reference.md)。

运行辅助脚本：
\`\`\`bash
python scripts/helper.py input.txt
\`\`\`
````

### 第 8 步：验证 Skill

检查以下内容：

✅ **文件结构**：

- SKILL.md 位于正确位置
- 目录名与 frontmatter 的 `name` 匹配

✅ **YAML frontmatter**：

- 第 1 行 `---`
- 内容前后均有分隔符
- 合法 YAML（无 Tab、缩进正确）
- `name` 命名规则正确
- `description` 具体且少于 1024 字符

✅ **内容质量**：

- 对 Claude 指令清晰
- 提供实际示例
- 处理边界情况
- 列出依赖项（如有）

✅ **测试**：

- 描述与用户问题匹配
- 能触发相关查询
- 指令明确可执行

### 第 9 步：测试 Skill

1. **重启 Claude Code** 以加载新技能

2. **提出匹配描述的问题**

   ```
   你能帮我从这个 PDF 中提取文本吗？
   ```

3. **验证触发**：Claude 应自动使用该 Skill

4. **检查行为**：确认执行逻辑正确

### 第 10 步：调试 Skill

若 Claude 未触发技能：

1. **优化描述**：

   - 增加触发词
   - 指明文件类型
   - 添加常见表达

2. **检查文件位置**：

   ```bash
   ls ~/.claude/skills/skill-name/SKILL.md
   ls .claude/skills/skill-name/SKILL.md
   ```

3. **验证 YAML**：

   ```bash
   cat SKILL.md | head -n 10
   ```

4. **运行调试模式**：

   ```bash
   claude --debug
   ```

## 常见模式

### 只读技能

```yaml
---
name: code-reader
description: 读取并分析代码而不修改。用于代码审查、理解代码库或生成文档。
allowed-tools: Read, Grep, Glob
---
```

### 基于脚本的技能

```yaml
---
name: data-processor
description: 使用 Python 脚本处理 CSV 和 JSON 数据文件。适用于数据分析或数据转换。
---
# 数据处理器

## 使用说明

1. 运行处理脚本：
\`\`\`bash
python scripts/process.py input.csv --output results.json
\`\`\`

2. 验证输出：
\`\`\`bash
python scripts/validate.py results.json
\`\`\`
```

### 多文件渐进技能

```yaml
---
name: api-designer
description: 设计遵循最佳实践的 REST API。用于创建接口、规划路由或设计 API 架构。
---

# API 设计器

快速入门：见 [examples.md](examples.md)
详细参考：见 [reference.md](reference.md)

## 使用说明

1. 收集需求


2. 设计接口（见 examples.md）


3. 编写 OpenAPI 规范


4. 对照最佳实践检查（见 reference.md）
```

## 技能作者最佳实践

1. **单一职责**：一个 Skill 只做一件事

2. **具体描述**：包含用户会说的触发词

3. **清晰指令**：为 Claude 而写，不为人类

4. **具体示例**：展示真实代码

5. **列出依赖**：在描述中说明必要包

6. **团队验证**：测试触发效果与清晰度

7. **版本管理**：记录内容变更

8. **渐进展示**：高级内容放入附加文件

## 验证清单

提交前确认：

- 名称为小写连字符，≤64 字符
- 描述具体且 ≤1024 字符
- 描述包含 " 做什么 " 和 " 何时用 "
- YAML 格式正确
- 指令分步明确
- 示例具体可执行
- 依赖完整列出
- 路径使用正斜杠
- 技能能被正确触发
- Claude 执行行为正确

## 故障排查

**技能未触发**：

- 增加触发词
- 包含文件类型与操作
- 使用 " 当……时使用 " 描述句

**多个技能冲突**：

- 区分描述
- 使用不同触发词
- 收窄范围

**技能出错**：

- 检查 YAML 缩进与语法
- 验证路径正确
- 脚本需具执行权限
- 列出所有依赖

## 示例

参见完整案例：

- 单文件技能（commit-helper）
- 带工具权限的技能（code-reviewer）
- 多文件技能（pdf-processing）

## 输出格式

创建技能时，我将：

1. 提出范围与需求问题

2. 建议技能名称与位置

3. 创建带正确 frontmatter 的 SKILL.md

4. 编写清晰指令与示例

5. 添加必要辅助文件

6. 提供测试指导

7. 校验所有规则

结果将是一份完整、可用、符合最佳实践与验证标准的 Skill。
