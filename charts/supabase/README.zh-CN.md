## `charts/supabase`（外链优先 · 可选内建）

与本仓库一致：**优先、完整支持外链**（PostgreSQL / Kong / nginx 等可由现网或托管提供）；**内建为辅**（`bundled`、`gateway.mode=nginx/kong` 仅兜底或联调）。模板 **无 `_helpers.tpl`**。

### 选型原则

| 能力 | **推荐（外链）** | **可选（内建）** |
|------|------------------|------------------|
| **数据库** | `bundled.postgres=false`，填 RDS 等 **`externalDatabase.*`** URL | `bundled.postgres=true`，子 chart **`charts/postgresql`**（拷贝自 `postgresql-new/16`） |
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
| **`false`（外链默认）** | 必填 `externalDatabase.*` |
| **`true`（可选内建）** | Helm dependency `postgresql`，并设置 **`postgresql.postgresql.password`** |

### 安装示例（外链 RDS + 外链网关）

```yaml
bundled:
  postgres: false
gateway:
  mode: external
  externalPublicUrl: https://api.example.com
externalDatabase:
  gotrueDbUrl: "postgres://..."
  restDbUri: "postgres://..."
  realtime:
    host: "..."

```

### 安装示例（全内建兜底）

参见仓库内此前示例：**`bundled.postgres=true` + `gateway.mode=kong`** + Ingress。

### 与独立 chart

- 独立网关仍可用 [`kong-gateway`](../kong-gateway/README.zh-CN.md)。
- 独立 PG 仍可用 **`postgresql-new`**；本 umbrella 仅在 `bundled.postgres=false` 时与之组合。
