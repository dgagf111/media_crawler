# 仓库指南（所有说明必须始终使用中文）

## 项目结构与模块组织
- 核心应用代码位于 `src/pythonprojecttemplate/`，其中 `api/`、`services/`、`models/` 与 `core/` 模块构成 FastAPI 技术栈；新增业务逻辑请与现有同类放在一起，保持可预测的导入路径。
- 支撑系统（如 `config/`、`cache/`、`db/`、`scheduler/`、`monitoring/`、`modules/`）承载基础设施适配器；优先扩展这些包而不是创建临时目录。
- 测试代码在 `tests/` 中与包结构一一对应；文档、RFC 与 runbook 放在 `docs/`。
- 自动化脚本位于 `scripts/`，依赖清单在 `dependencies/`；引入新工具前先复用这些产物。

## 构建、测试与开发命令
- 通过 `python -m venv .venv && source .venv/bin/activate` 创建运行时，然后执行 `pip install -r dependencies/requirements.txt`（或运行 `./dependencies/install_dependencies.sh dev` 安装开发依赖）。
- 本地运行应用可使用 `python main.py` 或 `uvicorn main:app --reload --port 8000`；Prometheus 指标暴露在 `:9966/metrics`。
- 使用 `black src tests`、`isort src tests` 与 `mypy src tests` 维护格式和类型健康。
- 运行自定义测试套件用 `python tests/run_tests.py all`；若需直接使用 Pytest，运行 `pytest tests -v --strict-markers`；覆盖率通过 `pytest --cov=src tests/` 获取。

## 编码风格与命名约定
- 遵循 Black 默认（88 字符行宽、双引号）与 isort 的 Black 配置；导入按标准库/三方/本地分组。
- 模块、包及文件命名全部小写加下划线；FastAPI 路由文件通常以 `_router.py` 结尾。
- 全面添加类型注解——`mypy` 以严格模式运行；契约优先使用 `Protocol`/`TypedDict` 而非 `Any`。
- 使用四空格缩进、为公共接口编写 docstring，并复用 `core/logging` 中的结构化日志工具。

## 测试规范
- 按功能组织测试：例如 `tests/api/test_users.py` 覆盖 `src/pythonprojecttemplate/api/users.py`。
- 测试命名为 `test_<行为>`，并置于以 `Test` 开头的类中，符合 `pyproject.toml` 的发现规则。
- 集成测试以 `@pytest.mark.integration` 或 `slow` 标记，方便 CI 通过 `pytest -m "not slow"` 过滤。
- 只要覆盖率不下降就可接受改动；触碰关键服务时在本地运行 `coverage html`。

## 提交与 PR 指南
- 使用 Conventional Commits（如 `feat(auth): ...`、`refactor(monitoring): ...`），作用域按包或子系统划分。
- 每个 PR 需说明动机、概述架构决策、关联相关 issue，并记录配置或迁移变化；UI/指标变更时附上 API 文档或仪表盘截图。
- 当行为发生变化时，务必在 `docs/updates/` 或相关模块文档中更新记录，并在请求评审前确认所有必需的检查全部通过。

## 安全与配置提示
- 将 `.env.example` 复制为 `.env`，确保密钥不入库，新增变量记得写入 `docs/guides/configuration.md`。
- 在合并前通过 `docker-compose up -d` 在预发环境验证数据库/缓存的变更，保护共享的基础设施。
