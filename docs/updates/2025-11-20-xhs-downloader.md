# 2025-11-20 XHS-Downloader 集成

- 将根目录 `XHS-Downloader` 的源码迁入 `media_crawler.modules.xhs_downloader.core`，归档 locale/static 资源。
- 新增 `XHSDownloaderService`、FastAPI 路由与模块生命周期钩子，暴露 `/api/v1/xhs-downloader/detail` 接口。
- 扩展 `config/settings.py`，提供 `SpiderXHSSettings` 与 `XHSDownloaderSettings`，统一配置出口。
- 添加必要依赖（`aiofiles`、`aiosqlite`、`fastmcp` 等）以及最小化单元测试，保证模块在禁用/启用场景下行为可控。
