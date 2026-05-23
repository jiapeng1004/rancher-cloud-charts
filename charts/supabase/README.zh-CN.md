## `charts/supabase`（外链优先 · 可选内建）

与本仓库一致：**优先、完整支持外链**（PostgreSQL / Kong / nginx 等可由现网或托管提供）；**内建为辅**（`bundled`、`gateway.mode=nginx/kong` 仅兜底或联调）。外链库的 `postgres://` 在 **`templates/secret.yaml`** 内联拼装（**无独立 `*.tpl`**）；Rancher 表单只让用户填域名+端口。

> 说明：上游完整 Supabase chart 的子目录模板中可能仍带有官方提供的 `_helpers.tpl`；与本 README 强调的「极简链路」/`secret.yaml`、`deployment-realtime.yaml` **不是一回事**，若你希望整包零 `.tpl` 需另行剥离官方模板。

### 选型原则

| 能力 | **推荐（外链）** | **可选（内建）** |
|------|------------------|------------------|
| **数据库** | `bundled.postgres=false`，填 **`externalDatabase.host`/`port`/账号**（不写 `postgres://`） | `bundled.postgres=true`，子 chart **`charts/postgresql`**（拷贝自 `postgresql-new/16`） |
| **网关** | `gateway.mode=external`，自备 Kong/nginx/SLB，上游指本集群 `*-auth/rest/realtime` | `nginx`（轻量反向代理）或 `kong`（本 chart 内嵌 declarative Kong） |

> 内建 PG 自动生成 **单一 postgres URL**（开发向）；上线请完成 Supabase 官方迁移后再用外链多角色写法。

部署内容恒定：**gotrue + PostgREST + realtime**。网关三选一：

| `gateway.mode` | 典型用途 |
|----------------|----------|
| **`external`（外链优先场景）** | 不部署内置网关 Pod；必填 **`gateway.externalPublicUrl`**（给 GOTRUE 的对外根）；你在集群外公网入口把 **`/auth|/rest|/realtime`** 指到后端 Service |
| **`nginx`**（内建备选） | 集群内 nginx + 可选 Ingress |
| **`kong`**（内建备选） | 集群内 Kong DB-less，`Ingress` 默认指 `*-kong-proxy` |

### 对外 URL

- **`gateway.mode != external`**：填 **`api.publicUrl`**（或兼容 **`api.externalUrl`**）。
- **`gateway.mode == external`**：填 **`gateway.externalPublicUrl`**。

### Postgres

| `bundled.postgres` | 说明 |
|--------------------|------|
| **`false`（外链默认）** | 必填 **主机名（域名或 Kubernetes DNS）**、端口、用户名、数据库名与密码（Rancher 表单层不展示整条 URL）；GoTrue / PostgREST 在 Secret 中由模板自动拼 **`postgres://...`** |
| **`true`（可选内建）** | Helm dependency `postgresql`，并设置 **`postgresql.postgresql.password`** |

### 安装示例（外链 RDS + 外链网关）

```yaml
bundled:
  postgres: false
gateway:
  mode: external
  externalPublicUrl: https://api.example.com
externalDatabase:
  host: my-pg.region.rds.amazonaws.com   # 仅域名或服务名，不写协议前缀
  port: "5432"
  dbName: postgres
  user: supabase_admin
  password: "替换为强口令"
```

### 安装示例（全内建兜底）

参见仓库内此前示例：**`bundled.postgres=true` + `gateway.mode=kong`** + Ingress。

### 进阶（Realtime 与 GoTrue/PGRST 使用不同 PG）

- **`externalDatabase.realtime.*`**（`host`、`port`、`dbName`、`user`、`password` 任一）：仅 Realtime Deployment 使用该覆盖；仍为「字段拆分」，不需要在表单里手写 `postgres://`。
- **`externalDatabase.gotrueDbUrl` / `externalDatabase.restDbUri`**：若密码自动 URI 编码后仍不适用等极少数情况，可在 **YAML** 中为 GoTrue / PostgREST 单独提供完整 **`postgres://...`**；REST 为空时会复用 GOTRUE。

### 与独立 chart

- 独立网关仍可用 [`kong-gateway`](../kong-gateway/README.zh-CN.md)。
- 独立 PG 仍可用 **`postgresql-new`**；本 umbrella 仅在 `bundled.postgres=false` 时与之组合。
