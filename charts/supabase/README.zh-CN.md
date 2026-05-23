## `charts/supabase`（极简，符合本仓库模板约定）

已**替换**原先的 community 大而全 Helm 树（大量 `_helpers.tpl`）。当前 chart：

- **不引入** standalone `templates/_helpers.tpl`；在每个模板文件顶部仅用 `$name`、`$fullname`。
- **不部署 Postgres / Redis**；默认假设你已有 **完成 Supabase 初始化迁移** 的数据库实例（云上 RDS、`postgresql-new` 等均可，但库里必须有官方自助主机要求的角色与 schema）。
- **不部署** Kong、Studio、Storage、Functions、Analytics，仅保留常用 API 切面：**nginx 网关 → gotrue + PostgREST + realtime**。
- Realtime **不依赖 Redis**：与上游 `docker-compose.yml` 一致，仅用 Postgres + JWT。

### 必填 values

| 字段 | 说明 |
|------|------|
| `externalDatabase.gotrueDbUrl` | 官方示例形态：`postgres://supabase_auth_admin:...@host:5432/postgres` |
| `externalDatabase.restDbUri` | `postgres://authenticator:...@host:5432/postgres` |
| `externalDatabase.realtime.host` / `password` | Realtime 用 `supabase_admin`（默认 user）登录 |
| `api.externalUrl` | 浏览器/SDK 访问的 API 根，如 `https://api.example.com`（**不要**尾随 `/` 歧义时注意与 Ingress 对齐） |
| `jwt.secret` | `GOTRUE` / PostgREST / Realtime 共用（≥32 字符） |
| `realtimeSecretKeyBase` | Realtime `SECRET_KEY_BASE` |

客户端（`supabase-js` 等）还需 **anon / service_role API key JWT**，须与 `jwt.secret` 配套生成（Supabase CLI 或官方脚本）；本 chart **不写进** Kubernetes，请自行安全管理。

### Redis

本栈镜像环境变量沿用官方 Compose，**无 Redis**。若你以后接其它增值服务，可自行在集群里单独建 Redis chart，与本目录无关。

### 安装示例

```bash
helm upgrade --install sb charts/supabase -n supabase --create-namespace \
  -f my-secret-values.yaml
```

### 与「全量 Supabase」的关系

若要 **Studio / Storage / Kong 全套**，请直接使用上游发行版：`helm repo add supabase-community https://supabase-community.github.io/supabase-kubernetes`；本仓库刻意保持可读、无外网依赖子 chart。
