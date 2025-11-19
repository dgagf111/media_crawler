# 功能文档生成器参考文档

## 核心实现逻辑

### 上下文分析算法

```python
def analyze_context():
    """分析当前开发上下文"""
    # 1. 检查 git 状态
    git_status = get_git_status()
    modified_files = git_status.get('modified', [])

    # 2. 识别功能类型
    function_type = identify_function_type(modified_files)

    # 3. 提取关键信息
    context_info = {
        'files': modified_files,
        'function_type': function_type,
        'recent_commits': get_recent_commits(),
        'current_branch': get_current_branch()
    }

    return context_info
```

### 信息提取策略

#### API 接口提取
- 从 `api/routes/` 目录提取路由定义
- 解析 FastAPI 装饰器 `@app.post()`, `@app.get()` 等
- 提取请求/响应模型 (Pydantic schemas)
- 识别依赖注入和中间件

#### 数据模型提取
- 从 `modules/*/models.py` 提取 SQLAlchemy 模型
- 解析表结构、字段类型、约束关系
- 识别索引和外键关系
- 提取数据库迁移信息

#### 配置信息提取
- 从 `config/` 目录提取配置项
- 解析 YAML 配置文件
- 识别环境变量映射
- 提取默认值和说明

#### 测试用例提取
- 从 `tests/` 目录提取相关测试
- 识别测试场景和边界条件
- 提取 Mock 数据和预期结果
- 分析测试覆盖率

### 模板适配规则

#### 必需章节
- 文档信息
- 功能概述
- 目标与范围
- 错误码处理

#### 条件章节判断逻辑

```python
def should_include_interface_section():
    """判断是否需要界面说明章节"""
    return has_frontend_files() or has_ui_components()

def should_include_api_section():
    """判断是否需要接口定义章节"""
    return has_api_routes() or has_endpoint_definitions()

def should_include_database_section():
    """判断是否需要数据库设计章节"""
    return has_database_models() or has_migration_files()

def should_include_deployment_section():
    """判断是否需要部署运维章节"""
    return has_docker_files() or has_deployment_scripts()
```

### 智能内容生成

#### 功能概述生成
```python
def generate_function_overview(context):
    """生成功能概述"""
    function_type = context.get('function_type')

    templates = {
        'auth': '本功能用于实现用户身份验证与权限管理，确保系统访问安全与用户操作可控。',
        'api': '本功能提供RESTful API接口，支持数据的增删改查操作和业务逻辑处理。',
        'crud': '本功能实现基础的数据管理功能，支持完整的数据生命周期管理。'
    }

    return templates.get(function_type, '本功能实现系统的核心业务逻辑。')
```

#### API 文档生成
```python
def generate_api_docs(route_files):
    """生成 API 接口文档"""
    api_docs = []

    for file in route_files:
        routes = parse_fastapi_routes(file)
        for route in routes:
            doc = {
                'method': route.method,
                'path': route.path,
                'summary': route.summary,
                'parameters': route.parameters,
                'responses': route.responses
            }
            api_docs.append(doc)

    return format_api_table(api_docs)
```

## 扩展功能

### 自定义模板支持
支持用户定义自己的文档模板：
- 模板使用 Mustache 语法
- 支持条件渲染和循环
- 可插入自定义处理逻辑

### 多格式输出
- Markdown（默认）
- HTML
- PDF（通过 pandoc）
- Word 文档

### 国际化支持
- 中文（默认）
- 英文
- 可扩展其他语言

## 配置选项

### 默认配置
```yaml
functional_doc_generator:
  output_dir: "docs/functional-docs/"
  template: "standard"
  auto_detect: true
  include_tests: true
  include_performance: true
  version_format: "v{major}.{minor}"
```

### 项目级配置
在项目根目录创建 `.functional-doc.yaml`：
```yaml
project_name: "Python项目模板"
default_module: "系统管理"
api_base_path: "/api/v1"
test_coverage_threshold: 80
performance_requirements:
  response_time: "100ms"
  throughput: "500 QPS"
```

## 错误处理

### 常见错误及解决方案

1. **无法识别功能类型**
   - 检查文件命名规范
   - 确认目录结构符合标准
   - 手动指定功能类型

2. **模板变量未替换**
   - 检查模板语法是否正确
   - 确认数据提取是否成功
   - 验证变量名是否匹配

3. **输出路径创建失败**
   - 检查目录权限
   - 确认父目录存在
   - 使用绝对路径

## 性能优化

### 大型项目处理
- 增量分析：只分析变更的文件
- 并行处理：同时分析多个模块
- 缓存机制：缓存分析结果

### 内存优化
- 流式读取：避免大文件一次性加载
- 垃圾回收：及时释放不需要的对象
- 分批处理：大文件分批分析

## 扩展接口

### 自定义分析器
```python
class CustomAnalyzer:
    def analyze(self, files):
        """自定义分析逻辑"""
        pass

    def extract_info(self, file_path):
        """提取文件信息"""
        pass
```

### 自定义生成器
```python
class CustomGenerator:
    def generate(self, context, template):
        """自定义文档生成逻辑"""
        pass

    def format_output(self, content, format_type):
        """格式化输出"""
        pass
```