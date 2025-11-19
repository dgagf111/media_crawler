# 2025-11-19 Spider_XHS 集成

- 将根目录下的 `Spider_XHS` 抽象为 `media_crawler.modules.spider_xhs`，统一依赖、日志与配置。
- 新增 `SpiderXHSService`、FastAPI 路由与模块生命周期，提供批量笔记、用户笔记与搜索接口。
- 新增配置项 `SpiderXHSSettings`、静态资源打包、docs 说明及最小化测试用例。
