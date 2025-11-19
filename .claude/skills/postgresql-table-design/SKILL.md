---
name: postgresql-table-design
description: 设计 PostgreSQL 专用的数据库模式。涵盖最佳实践、数据类型、索引、约束、性能模式与高级特性。
---

# PostgreSQL 表设计

## 核心规则

- 为引用型表（如 users、orders 等）定义 **PRIMARY KEY（主键）**。时间序列 / 事件 / 日志类数据不一定需要主键。若使用，推荐 `BIGINT GENERATED ALWAYS AS IDENTITY`；只有在需要全局唯一性或不透明 ID 时才使用 `UUID`。
- **优先进行规范化（至少至 3NF）** 以消除数据冗余与更新异常；仅在确证连接查询性能成为瓶颈时，为提高读性能进行有度的反规范化。过早反规范化会导致维护负担。
- 对语义上必须存在值的列添加 **NOT NULL**；对常见默认值使用 **DEFAULT**。
- 为**实际会查询的访问路径创建索引**：PK/UNIQUE（自动）、**外键列（需手动！）**、频繁过滤/排序的列以及连接键。
- 优先使用：事件时间用 **TIMESTAMPTZ**，金额用 **NUMERIC**，字符串用 **TEXT**，整数用 **BIGINT**，浮点数用 **DOUBLE PRECISION**（或 `NUMERIC` 用于精确小数计算）。

## PostgreSQL “陷阱点”

- **标识符（Identifiers）**：未加引号的会自动转为小写。避免使用带引号或混合大小写的名称。推荐表名/列名使用 `snake_case`。
- **UNIQUE + NULL**：UNIQUE 允许多个 NULL。若需仅允许一个 NULL，使用 `UNIQUE (...) NULLS NOT DISTINCT`（PG15+）。
- **外键索引（FK indexes）**：PostgreSQL **不会自动**为外键列建立索引，需手动添加。
- **无隐式类型转换**：长度/精度溢出会报错（不会截断）。如：向 `NUMERIC(2,0)` 插入 999 会报错，而其他数据库可能会自动截断或四舍五入。
- **序列/标识列存在间隙**（正常现象，不必修复）。回滚、崩溃与并发事务都会导致 ID 序列出现跳号（如 1,2,5,6…）。这是预期行为，不要试图让 ID 连续。
- **堆存储（Heap storage）**：默认不按主键聚簇（不同于 SQL Server/MySQL InnoDB）；`CLUSTER` 仅为一次性重组，之后插入不会维持顺序。磁盘行顺序即插入顺序，除非显式聚簇。
- **MVCC**：更新/删除会留下“死元组”，由 vacuum 处理——设计时应避免频繁更新宽行。

## 数据类型

- **ID**：推荐使用 `BIGINT GENERATED ALWAYS AS IDENTITY`（或 `BY DEFAULT`）。`UUID` 用于分布式系统、跨库合并或需不透明 ID 时。生成方式：PG18+ 用 `uuidv7()`，旧版本用 `gen_random_uuid()`。
- **整数**：除非极度节省空间，否则推荐使用 `BIGINT`；小范围可用 `INTEGER`；除非必要避免 `SMALLINT`。
- **浮点**：推荐 `DOUBLE PRECISION`；仅在空间受限时用 `REAL`。需精确小数计算时用 `NUMERIC`。
- **字符串**：推荐 `TEXT`；如需长度限制，用 `CHECK (LENGTH(col) <= n)` 替代 `VARCHAR(n)`；避免 `CHAR(n)`。二进制用 `BYTEA`。大于 2KB 的字符串或二进制数据会自动存入 TOAST（带压缩）。TOAST 存储策略：`PLAIN`（不 TOAST）、`EXTENDED`（压缩+外部存储）、`EXTERNAL`（外部存储不压缩）、`MAIN`（压缩且尽量内联）。默认 `EXTENDED` 最优。可通过 `ALTER TABLE tbl ALTER COLUMN col SET STORAGE strategy` 控制策略，并用 `ALTER TABLE tbl SET (toast_tuple_target = 4096)` 调整阈值。大小写不敏感：如需区域化/重音处理用非确定性排序；纯 ASCII 可使用 `LOWER(col)` 表达式索引（优先）或 `CITEXT`。
- **货币**：使用 `NUMERIC(p,s)`（切勿用浮点）。
- **时间**：时间戳用 `TIMESTAMPTZ`；仅日期用 `DATE`；持续时间用 `INTERVAL`。避免使用无时区的 `TIMESTAMP`。事务开始时间用 `now()`，当前系统时间用 `clock_timestamp()`。
- **布尔值**：使用 `BOOLEAN` 并加 `NOT NULL`，除非确需三态。
- **枚举（Enums）**：小且稳定的集合用 `CREATE TYPE ... AS ENUM`（如州名、星期几）；业务逻辑驱动且可能变化的值（如订单状态）应使用 TEXT（或 INT）+ CHECK 或查找表。
- **数组（Arrays）**：`TEXT[]`、`INTEGER[]` 等，用于有序列表。可用 **GIN** 索引支持包含（`@>`、`<@`）与重叠（`&&`）查询。访问方式：`arr[1]`（1 起始）、`arr[1:3]`（切片）。适用于标签、分类等；若是关系数据，应使用中间表。字面量语法：`'{val1,val2}'` 或 `ARRAY[val1,val2]`。
- **区间类型（Range types）**：`daterange`、`numrange`、`tstzrange` 用于时间或数值区间。支持重叠（`&&`）、包含（`@>`）操作。索引用 **GiST**。常用于排班、版本控制、数值范围。推荐使用 `[)`（左闭右开）。
- **网络类型**：`INET` 表示 IP 地址，`CIDR` 表示网段，`MACADDR` 表示 MAC 地址。支持网络运算符（`<<`, `>>`, `&&`）。
- **几何类型**：`POINT`、`LINE`、`POLYGON`、`CIRCLE` 等二维空间数据。索引用 **GiST**。复杂地理空间应用推荐 **PostGIS**。
- **全文搜索（Text search）**：`TSVECTOR` 表示文档，`TSQUERY` 表示查询。索引用 **GIN**。始终指定语言：`to_tsvector('english', col)`、`to_tsquery('english', 'query')`。切勿使用单参数版本。
- **域类型（Domain types）**：如 `CREATE DOMAIN email AS TEXT CHECK (VALUE ~ '^[^@]+@[^@]+$')`，可在多表复用。
- **复合类型（Composite types）**：如 `CREATE TYPE address AS (street TEXT, city TEXT, zip TEXT)`。访问语法 `(col).field`。
- **JSONB**：优于 JSON，索引用 **GIN**。仅用于可选/半结构化属性。若必须保留原始顺序，则使用 JSON。
- **向量类型**：使用 `pgvector` 扩展的 `vector` 类型，用于嵌入向量相似度搜索。

### 禁用数据类型

- 禁用 `timestamp`（无时区）；请使用 `timestamptz`
- 禁用 `char(n)` 或 `varchar(n)`；请使用 `text`
- 禁用 `money`；请使用 `numeric`
- 禁用 `timetz`；请使用 `timestamptz`
- 禁用 `timestamptz(0)` 等精度形式；请使用 `timestamptz`
- 禁用 `serial`；请使用 `generated always as identity`

## 表类型

- **Regular**：默认类型，完全持久化且记录 WAL。
- **TEMPORARY**：会话级临时表，自动删除，不记录日志，适合临时数据。
- **UNLOGGED**：持久但不具备崩溃安全性。写入更快，适合缓存/中间数据。

## 行级安全（Row-Level Security）

使用 `ALTER TABLE tbl ENABLE ROW LEVEL SECURITY` 启用。示例策略：  
`CREATE POLICY user_access ON orders FOR SELECT TO app_users USING (user_id = current_user_id());`  
实现内置基于用户的行级访问控制。

## 约束（Constraints）

- **PK**：隐含 UNIQUE + NOT NULL，自动创建 B-tree 索引。
- **FK**：需指定 `ON DELETE/UPDATE` 动作（`CASCADE`、`RESTRICT`、`SET NULL`、`SET DEFAULT`）。为引用列显式创建索引以加速连接并避免父表更新/删除锁。循环外键可用 `DEFERRABLE INITIALLY DEFERRED`。
- **UNIQUE**：创建 B-tree 索引；默认允许多个 NULL，PG15+ 可用 `NULLS NOT DISTINCT` 限制为一个 NULL。推荐启用 `NULLS NOT DISTINCT`。
- **CHECK**：行级约束；NULL 自动通过。例：`CHECK (price > 0)` 允许 NULL。需强制时应加 `NOT NULL`。
- **EXCLUDE**：使用操作符防止值重叠。例：`EXCLUDE USING gist (room_id WITH =, booking_period WITH &&)` 防止重复预订。需相应索引类型（常为 GiST）。

## 索引（Indexing）

- **B-tree**：默认；适用于等值/范围查询（`=`, `<`, `>`, `BETWEEN`, `ORDER BY`）
- **复合索引**：顺序重要；仅当左前缀匹配时使用。将选择性最高或最常过滤的列放前。
- **覆盖索引**：`CREATE INDEX ON tbl (id) INCLUDE (name, email)`，索引仅扫描即可获取字段。
- **部分索引**：用于热门子集，如 `CREATE INDEX ON tbl (user_id) WHERE status = 'active'`
- **表达式索引**：基于计算列，如 `CREATE INDEX ON tbl (LOWER(email))`，WHERE 必须完全匹配。
- **GIN**：JSONB、数组、全文搜索。
- **GiST**：区间、几何、排他约束。
- **BRIN**：适用于大规模顺序数据（时间序列），存储占用极低。

## 分区（Partitioning）

- 用于超大表（>1 亿行）且查询始终过滤分区键（如时间）。
- 也适用于定期裁剪或批量替换的数据。
- **RANGE**：最常见（如 `created_at`）。示例：  
  `CREATE TABLE logs_2024_01 PARTITION OF logs FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');`  
  **TimescaleDB** 可自动进行基于时间或 ID 的分区与压缩。
- **LIST**：离散值，如地区。
- **HASH**：无自然键时的均匀分布。
- 自动分区（PG10+）支持基于约束的查询裁剪。
- 推荐声明式分区或 hypertables，不要使用继承。
- **限制**：无全局 UNIQUE 约束，主键/唯一键需含分区键；分区表不支持外键引用。

## 特殊场景

### 更新频繁表

- **冷热分离**：将频繁更新列放入独立表以减小膨胀。
- 设置 `fillfactor=90` 留出 HOT 更新空间。
- **避免更新带索引列**。
- **按更新模式分区**：将活跃数据与稳定数据分开。

### 插入密集表

- **减少索引**：每个索引都会拖慢插入。
- 使用 `COPY` 或多行 `INSERT`。
- 可用 **UNLOGGED** 表暂存数据以提高速度。
- **先删索引再导入再建索引**。
- 按时间或哈希分区以分散负载。
- 若需全局唯一，可使用 `(timestamp, device_id)` 复合键；多数插入密集表无需主键。
- 若需代理键，推荐 `BIGINT GENERATED ALWAYS AS IDENTITY` 而非 `UUID`。

### Upsert 设计

- 必须对冲突列建立 **UNIQUE 索引**。
- 使用 `EXCLUDED.column` 引用插入值，仅更新实际变化的字段。
- 若不需更新，`DO NOTHING` 更快。

### 安全的模式演进

- **事务性 DDL**：多数 DDL 可在事务中执行并回滚。
- **并发索引创建**：`CREATE INDEX CONCURRENTLY` 不阻塞写入但不可放入事务。
- **易变默认值会触发全表重写**：添加 `NOT NULL` 且默认值为易变函数（如 `now()`、`gen_random_uuid()`）会导致全表重写。非易变默认更快。
- **删除列前应先删除约束**。
- **函数签名变更**：`CREATE OR REPLACE` 参数不同会生成重载而非替换；如不需重载应先 DROP。

## 生成列（Generated Columns）

`... GENERATED ALWAYS AS (<expr>) STORED` 创建可索引的计算列。PG18+ 支持 `VIRTUAL`（仅读时计算，不存储）。

## 扩展（Extensions）

- **pgcrypto**：`crypt()` 密码哈希。
- **uuid-ossp**：替代 UUID 生成函数（新项目推荐 pgcrypto）。
- **pg_trgm**：模糊搜索（`%`、`similarity()`），配合 GIN 加速 `LIKE '%pattern%'`。
- **citext**：不区分大小写文本类型。除非需大小写无关约束，否则推荐用 `LOWER()` 索引。
- **btree_gin / btree_gist**：支持混合类型索引。
- **hstore**：键值存储，已基本被 JSONB 取代。
- **timescaledb**：时间序列必备，支持自动分区、保留策略、压缩、连续聚合。
- **postgis**：全面地理空间支持。
- **pgvector**：向量相似度搜索。
- **pgaudit**：数据库活动审计。

## JSONB 指南

- 推荐使用 `JSONB` + **GIN** 索引。  
  默认：  
  `CREATE INDEX ON tbl USING GIN (jsonb_col);`  
  可加速：
  - **包含查询** `jsonb_col @> '{"k":"v"}'`
  - **键存在** `jsonb_col ? 'k'`，或 `?|`, `?&`
  - **路径包含**
  - **多条件或查询** `jsonb_col @> ANY(ARRAY['{"status":"active"}', '{"status":"pending"}'])`
- 重度 `@>` 查询可使用 `jsonb_path_ops` 提升性能：  
  `CREATE INDEX ON tbl USING GIN (jsonb_col jsonb_path_ops);`  
  但会失去键存在查询支持，仅支持包含。
- 针对特定字段的等值/范围查询：提取并存储为生成列并建 B-tree 索引：
  ```sql
  ALTER TABLE tbl ADD COLUMN price INT GENERATED ALWAYS AS ((jsonb_col->>'price')::INT) STORED;
  CREATE INDEX ON tbl (price);
  ```
  推荐 `WHERE price BETWEEN 100 AND 500` 而非直接在 JSON 表达式上比较。
- JSONB 内部数组可用 GIN + `@>`。
- 核心关系数据应建表，JSONB 仅存放可选/变结构属性。
- 可通过约束限制 JSONB 值类型：  
  `config JSONB NOT NULL CHECK(jsonb_typeof(config) = 'object')`

## 示例

### Users

```sql
CREATE TABLE users (
  user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX ON users (LOWER(email));
CREATE INDEX ON users (created_at);
```

### Orders

```sql
CREATE TABLE orders (
  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id),
  status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','PAID','CANCELED')),
  total NUMERIC(10,2) NOT NULL CHECK (total > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON orders (user_id);
CREATE INDEX ON orders (created_at);
```

### JSONB

```sql
CREATE TABLE profiles (
  user_id BIGINT PRIMARY KEY REFERENCES users(user_id),
  attrs JSONB NOT NULL DEFAULT '{}',
  theme TEXT GENERATED ALWAYS AS (attrs->>'theme') STORED
);
CREATE INDEX profiles_attrs_gin ON profiles USING GIN (attrs);
```
