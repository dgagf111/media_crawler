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
