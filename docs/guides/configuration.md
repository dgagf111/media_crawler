# 配置指南

## 加载顺序与位置
- 配置文件目录：默认 `src/media_crawler/config/`（可通过 `PPT_CONFIG_DIR` 覆盖）；基础文件 `config/env.yaml`，环境文件如 `config/dev.yaml`、`config/prod.yaml`。
- 优先级（高→低）：显式传参 > 环境变量（前缀 `PPT_`）> `.env` > YAML（`env.yaml` + `<env>.yaml`，可用 `PPT_ENV_FILE` 指定单文件）> 默认值。
- 环境选择：`PPT_ENV` 优先，其次 `env.yaml` 里的 `env` 字段，最终默认为 `dev`。
- 调试：可用 `from pythonprojecttemplate.config.settings import settings; print(settings.dump())` 查看当前配置，敏感字段自动脱敏；`settings.load_trace` 提供加载源与覆盖记录。

## Spider_XHS 模块

| 环境变量 | 说明 | 示例 |
| --- | --- | --- |
| `PPT_SPIDER_XHS__ENABLED` | 是否启用模块 | `true` |
| `PPT_SPIDER_XHS__DEFAULT_COOKIES` | 默认 cookies 字符串 | `a1=xxx; web_session=xxx` |
| `PPT_SPIDER_XHS__STORAGE__BASE_DIRECTORY` | 媒体与 Excel 输出根目录 | `/data/spider_xhs` |
| `PPT_SPIDER_XHS__STORAGE__MEDIA_SUBDIR` | 媒体目录名 | `media` |
| `PPT_SPIDER_XHS__STORAGE__EXCEL_SUBDIR` | Excel 目录名 | `excel` |

> 所有路径均可使用相对路径，最终会在应用启动时自动创建。

## XHS-Downloader 模块

| 环境变量 | 说明 | 示例 |
| --- | --- | --- |
| `PPT_XHS_DOWNLOADER__ENABLED` | 是否启用模块 | `true` |
| `PPT_XHS_DOWNLOADER__DEFAULT_COOKIE` | 默认 Cookie | `a1=xxx; web_session=xxx` |
| `PPT_XHS_DOWNLOADER__STORAGE__WORK_DIRECTORY` | 存储根目录 | `/data/xhs_downloader` |
| `PPT_XHS_DOWNLOADER__STORAGE__FOLDER_NAME` | 媒体文件夹名 | `Download` |
| `PPT_XHS_DOWNLOADER__STORAGE__NAME_FORMAT` | 文件命名格式 | `发布时间 作者昵称 作品标题` |
| `PPT_XHS_DOWNLOADER__PROXY` | 默认代理 | `http://127.0.0.1:7890` |
| `PPT_XHS_DOWNLOADER__TIMEOUT_SECONDS` | 请求超时 | `15` |
| `PPT_XHS_DOWNLOADER__CHUNK_SIZE` | 下载块大小（字节） | `2097152` |
| `PPT_XHS_DOWNLOADER__MAX_RETRY` | 最大重试次数 | `5` |
| `PPT_XHS_DOWNLOADER__LANGUAGE` | 语言 | `zh_CN` |
| `PPT_XHS_DOWNLOADER__MAPPING_FILE` | 映射文件路径 | `/data/xhs_downloader/mapping.json` |
