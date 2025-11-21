# XHS-Downloader 模块

## 模块目标
- 将社区项目 `XHS-Downloader` 原始能力整合到 FastAPI 主服务，统一配置、日志与依赖管理。
- 复用 `XHS` 核心 SDK，实现作品数据提取与可选的无水印下载。
- 对外暴露 REST API，方便与调度、鉴权等子系统协同。

## 目录结构
```
src/media_crawler/modules/xhs_downloader/
├── core/           # 原 project 的 source 目录，包含 XHS、TUI、CLI 等实现
├── locale/         # 翻译文件 (.mo)
├── static/         # TUI/脚本资源
├── schemas.py      # FastAPI 层请求/响应模型
├── services/       # XHSDownloaderService 封装
├── dependencies.py # FastAPI 依赖注入
└── module.py       # BaseModule 生命周期
```

## 配置项
位于 `config/settings.py -> XHSDownloaderSettings`，可通过 `.env` 或 `env.yaml`/`dev.yaml` 覆盖：

| 配置项 | 说明 |
| --- | --- |
| `enabled` | 是否启用模块，关闭时不会注册路由 |
| `storage.work_directory` | 媒体数据根目录，默认 `~/data/xhs_downloader` |
| `storage.folder_name` | 媒体文件夹名，默认 `Download` |
| `storage.name_format` | 文件命名规则，需由空格分隔的占位符 |
| `default_cookie` | 全局 Cookie，接口未传时使用 |
| `proxy` | 默认代理（可被请求体覆盖） |
| `timeout_seconds` | 请求超时时间（秒） |
| `chunk_size` | 下载块大小（字节） |
| `max_retry` | 请求失败重试次数 |
| `record_data`/`download_record` | 是否持久化作品信息/下载记录 |
| `image_format`/`image_download`/`video_download`/`live_download` | 下载策略 |
| `author_archive`/`folder_mode`/`write_mtime` | 文件存储策略配置 |
| `language` | 内置多语言，默认 `zh_CN` |
| `read_cookie` | 自动读取浏览器 Cookie 时的序号/名称 |
| `print_logs` | 是否输出底层终端日志 |
| `mapping_file`/`mapping_data` | 作者备注映射（文件优先，格式为 JSON 字典） |

## API 使用方式
1. **启用模块**：在 `.env` 中设置 `PPT_XHS_DOWNLOADER__ENABLED=true`，并保证 `module_config.modules` 中包含 `media_crawler.modules.xhs_downloader`. 
2. **启动服务**：`uvicorn main:app --reload`。
3. **调用接口**：
   - `POST /api/v1/xhs-downloader/detail`
   - 请求体字段：
     | 字段 | 类型 | 说明 |
     | --- | --- | --- |
     | `url` | `str` | 必填，小红书作品链接或含分享码文本 |
     | `download` | `bool` | 是否下载文件，默认 `false` |
     | `index` | `list[int]` | 针对图文作品下载的图片序号列表 |
     | `cookie` | `str` | 单次请求覆盖默认 Cookie |
     | `proxy` | `str` | 单次请求使用的代理地址 |
     | `skip_downloaded` | `bool` | 已存在下载记录时是否跳过 |
   - 返回值：统一 `ResultVO`，`data` 字段包含 `url`、`message` 及原始 `XHS-Downloader` 作品数据。

## 注意事项
- 初次运行会在 `storage.work_directory` 下自动创建 `Volume/Download` 等子目录。
- 下载逻辑依赖 `aiofiles` 与 `aiosqlite`，运行前请执行 `pip install -r dependencies/requirements.txt`。
- 若需使用浏览器 Cookie 自动读取功能，需在服务器具备图形桌面环境并安装对应浏览器。
- MCP / TUI / CLI 仍保留在 `core/` 中，如需使用可手动引用原模块。
