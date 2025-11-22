# Spider_XHS 模块

## 模块目标
- 将原 `Spider_XHS` 工具嵌入 FastAPI 主服务，统一依赖、配置与日志。
- 对外暴露 API，支持笔记批量采集、用户笔记抓取与搜索下载。
- 共享项目的任务调度、监控以及配置体系，便于后续扩展。

## 目录结构
```
src/media_crawler/modules/spider_xhs/
├── assets/              # js 算法、作者素材等静态资源
├── clients/             # 小红书 PC/创作者 HTTP 客户端
├── services/            # 业务服务封装
├── schemas.py           # Pydantic 数据模型
├── dependencies.py      # FastAPI 依赖提供者
└── module.py            # BaseModule 接入
```

## 配置项
位于 `config/settings.py -> SpiderXHSSettings`，可在 `config/env.yaml`（基础）与 `config/dev.yaml`/`config/prod.yaml` 覆盖：

| 配置项 | 说明 |
| --- | --- |
| `enabled` | 是否启用 Spider_XHS 模块 |
| `default_cookies` | 默认 cookies，未传入请求参数时使用 |
| `storage.base_directory` | 媒体与 Excel 输出的根目录 |
| `storage.media_subdir` | 媒体文件子目录名 |
| `storage.excel_subdir` | Excel 子目录名 |

新增变量已同步到 `docs/guides/configuration.md`。

## 使用方式
1. **配置 cookies**：在 `.env` 中设置 `PPT_SPIDER_XHS__DEFAULT_COOKIES` 或在请求体传入。
2. **运行服务**：`uvicorn main:app --reload`，模块会在应用启动时自动注册并注入 `app.state.spider_xhs_service`。
3. **调用 API**：
   - `POST /api/v1/spider-xhs/notes:batch` 批量获取笔记详情，可选 `save_choice`（`none|media|media-image|media-video|excel|all`）
   - `POST /api/v1/spider-xhs/user-notes` 拉取用户全部笔记
   - `POST /api/v1/spider-xhs/search` 搜索关键字并导出

所有接口返回统一的 `ResultVO`，`data` 字段包含笔记列表与导出路径。

## TODO
- 与调度中心联动，支持后台批量任务。
- 将创作者接口对接到 API，提供自动化发布能力。
