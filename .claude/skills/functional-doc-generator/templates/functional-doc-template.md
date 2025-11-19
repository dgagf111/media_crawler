# 功能说明文档 - {{FUNCTION_NAME}}

## 一、文档信息
| 项目 | 内容 |
|------|------|
| 文档版本 | v{{VERSION}} |
| 作者 | {{AI_MODEL}} |
| 所属模块 | {{MODULE_NAME}} |
| 编写日期 | {{CREATE_DATE}} |
| 最近更新 | {{UPDATE_DATE}} |

---

## 二、功能概述
{{FUNCTION_OVERVIEW}}

---

## 三、功能目标与范围
- **目标**：{{FUNCTION_GOALS}}
- **范围**：{{FUNCTION_SCOPE}}
- **不在范围内**：{{OUT_OF_SCOPE}}

---

## 四、功能逻辑与流程说明
### 4.1 总体逻辑
{{OVERALL_LOGIC}}

### 4.2 异常与分支逻辑
- 输入不合法时的处理：{{INPUT_VALIDATION}}
- 异常状态返回：{{EXCEPTION_HANDLING}}
- 边界条件说明：{{BOUNDARY_CONDITIONS}}

---

{{#HAS_INTERFACE}}
## 五、界面与交互说明
| 元素 | 类型 | 操作说明 | 响应行为 |
|------|------|-----------|-----------|
{{INTERFACE_TABLE}}
---

{{#HAS_API}}
## 六、接口与数据结构说明
### 6.1 接口定义
{{API_DEFINITIONS}}

---

{{#HAS_DATABASE}}
## 七、数据库设计与数据流
| 表名 | 说明 |
|------|------|
{{DATABASE_TABLES}}

**主要字段说明：**
{{FIELD_DESCRIPTIONS}}
---

{{#HAS_SECURITY}}
## 八、权限与安全控制
- 访问权限：{{ACCESS_PERMISSIONS}}
- 鉴权方式：{{AUTH_METHOD}}
- 防护措施：{{SECURITY_MEASURES}}

---

## 九、错误码与异常处理
| 错误码 | 含义 | 解决方式 |
|--------|------|-----------|
{{ERROR_CODES}}

---

## 十、配置项与依赖说明
| 配置项 | 默认值 | 说明 |
|--------|--------|------|
{{CONFIG_ITEMS}}

---

## 十一、测试与验证
- 单元测试覆盖率：{{TEST_COVERAGE}}
- 测试用例示例：
{{TEST_CASES}}

---

## 十二、性能与限制
- 平均响应时间：{{RESPONSE_TIME}}
- 支持并发：{{CONCURRENT_SUPPORT}}
- 限制条件：{{LIMITATIONS}}

---

{{#HAS_DEPLOYMENT}}
## 十三、部署与运维
**部署步骤：**
{{DEPLOYMENT_STEPS}}

**监控指标：**
{{MONITORING_METRICS}}

**回滚方案：**
{{ROLLBACK_PLAN}}

---

## 十四、版本记录与变更日志
| 版本 | 日期 | 作者 | 变更内容 |
|------|------|------|----------|
{{CHANGE_LOG}}