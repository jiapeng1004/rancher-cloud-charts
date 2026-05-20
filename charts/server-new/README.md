聚合 chart `server-new` **将 mysql/redis/minio/doris 子 chart 放在 `charts/server-new/charts/`**，与 Helm 惯例「单体 chart + 外层 umbrella 指向 `file://../mysql-new`」相比维护成本高。

**推荐做法：**

1. **单体**：使用 `charts/mysql-new`、`charts/redis-new`、`charts/minio-new`、`charts/postgresql-new`、独立 `charts/doris-new` 等。
2. **一键**：使用 `charts/middleware-bundle/`（请先执行 `helm dependency update`）。

若继续使用本目录，建议在后续迭代中改为 `file://` 引用上一级单体 chart，删掉嵌套拷贝。
