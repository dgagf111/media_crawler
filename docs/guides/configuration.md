# 配置指南

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
