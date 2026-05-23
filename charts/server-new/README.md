聚合 chart **`server-new`** 将 **`mysql`、`redis`、`minio`、`doris`** 子 chart 放在 **`charts/server-new/charts/`**，与外层 `middleware-bundle`（MySQL / Redis / PG / MinIO）相比多 **Doris** 一条线，仍为 **嵌入式副本**：

- **`mysql` / `redis` / `minio`**：`robocopy` 与 **`charts/mysql-new/5.7`、`charts/redis-new/7.0`、`charts/minio-new/2024-01`** 对齐（维护时请改单体再同步）。
- **`doris`**：仅见于本嵌入目录，暂无仓库级独立 `doris-new` 目录时以这里为准。

**推荐做法：**

1. **只要中间件四件套**：用 **`charts/middleware-bundle`**（子 chart 已内置 `charts/`）。
2. **要 Doris + 上述栈**：继续用本目录，或拆成 **middleware-bundle + 独立 Doris chart**（若后续提供）。

若希望完全消除嵌套拷贝，可把与 `middleware-bundle` 重叠的三项改为仅从单体目录拷贝的自动化脚本 / CI，本仓库当前以 ** Rancher helm-git 可装**为先。
