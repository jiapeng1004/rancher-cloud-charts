## `charts/supabase`（默认内建 Postgres + Kong · 可选外链）

**默认**与上游 **docker/docker-compose.yml** 一致：**内嵌 PostgreSQL**（建议镜像 `supabase/postgres`）、**网关 Kong**（`gateway.mode=kong`）。生产可将 **`bundled.postgres=false`** 接 RDS / 自建 PG，或将 **`gateway.mode=external`** 接现网网关。外链库的 `postgres://` 在 **`templates/secret.yaml`** 内拼装（**无独立 `*.tpl`**）；Rancher 表单让用户填域名+端口等拆分字段。

> 说明：若引入上游完整 Supabase chart 的子目录模板，其中可能仍有官方 `_helpers.tpl`；与本 README 强调的「密钥在 `secret.yaml`、Realtime 特例在 `deployment-realtime.yaml`」不一定是同一套，整包剥离需另行清理。

### 密钥与 Rancher「生成」按钮

- **`jwt.secret`**（写入 `JWT_SECRET` / `PGRST_JWT_SECRET`）：PostgREST **硬性要求不少于 32 字符**。表单已设 **`min_length: 32`**，且 **Helm 在不足 32 时用 sha256 salt（含用户输入、Release Name/Namespace）截取后缀补齐**，同一集群同一 release **可重复**。仍建议直接使用 ≥32 位随机串。
- **`realtimeSecretKeyBase`**：Realtime（Phoenix）常见要求 **不少于 43 字符**；**不足 43 时用同样思路补齐**。表单已设 **`min_length: 43`**。

### 选型原则（与 compose 对齐的默认）

| 能力 | **默认（与 compose）** | **生产 / 拆分部署（外链）** |
|------|------------------------|-----------------------------|
| **数据库** | `bundled.postgres=true`，子 chart **`charts/postgresql`**，镜像宜用 **`supabase/postgres`** | `bundled.postgres=false`，填 **`externalDatabase.host`/`port`/账号**（不写 `postgres://`） |
| **网关** | **`gateway.mode=kong`**（Declarative Kong） | **`gateway.mode=external`**（自备 Kong/SLB，上游指本集群 `*-auth/rest/realtime`），或仍可 `nginx` |

**多数据库角色**：`bundledDb.composeDbRoles=true`（默认）时，`secret.yaml` 为 GoTrue / PostgREST 使用 **`supabase_auth_admin` / `authenticator`**，`deployment-realtime` 使用 **`supabase_admin`**，与 compose 命名一致。**必须**镜像与初始化能提供这些角色；若使用单用户 Postgres，请 **`bundledDb.composeDbRoles: false`** 并统一用 **`postgresql.postgresql.user`**。

部署内容恒定：**gotrue + PostgREST + realtime**。网关三选一：

| `gateway.mode` | 典型用途 |
|----------------|----------|
| **`kong`（默认）** | 集群内 Kong DB-less，`Ingress` 默认可指 `*-kong-proxy` |
| **`nginx`** | 集群内 nginx + 可选 Ingress |
| **`external`** | 不部署内置网关 Pod；必填 **`gateway.externalPublicUrl`**；集群外公网入口把 **`/auth|/rest|/realtime`** 指到后端 Service |

### 对外 URL

- **`gateway.mode != external`**：填 **`api.publicUrl`**（或兼容 **`api.externalUrl`**）。
- **`gateway.mode == external`**：填 **`gateway.externalPublicUrl`**。

### Postgres

**安全上下文**：内嵌 PG 在 **`postgresql.podSecurityContext`** / **`postgresql.securityContext`** 中默认 **`runAsUser: 105`、`runAsGroup: 106`、`fsGroup: 106`**，且 **`podSecurityContext.seccompProfile: RuntimeDefault`**（与你的 `supabase/postgres` 镜像内 **`postgres` 用户 UID/GID 不一致时**会权限失败，务必 **`kubectl exec … id`** 核对）。部署模板会读取 **`Capabilities.KubeVersion`**：版本 **低于 1.22** 时自动从 **`PodSecurityContext` 剔除 `seccompProfile`**（避免 APIServer 校验 `unknown field`）；另有 `runAsNonRoot`、`capabilities.drop` 等。本地 **`helm template` 未带 `--kube-version` 时使用默认 Capability 版本，若需与高版本对齐请显式传参。

| `bundled.postgres` | 说明 |
|--------------------|------|
| **`true`（默认）** | Helm dependency `postgresql`，设置 **`postgresql.postgresql.password`**（及按需持久化）；`composeDbRoles` 时对角色名见上文 |
| **`false`（外链）** | 必填 **主机名**、端口、用户名、数据库名与密码；GoTrue / PostgREST 在 Secret 中由模板拼 **`postgres://...`** |

### 安装示例（默认：内嵌 + Kong，占位 URL）

参见 **`values.yaml`**：`bundled.postgres: true`、`gateway.mode: kong`、`api.publicUrl`、`postgresql.image`（supabase/postgres tag）。

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

### 进阶（Realtime 与 GoTrue/PGRST 使用不同 PG）

- **`externalDatabase.realtime.*`**（`host`、`port`、`dbName`、`user`、`password` 任一）：仅 Realtime Deployment 使用该覆盖；仍为「字段拆分」，不需要在表单里手写 `postgres://`。
- **`externalDatabase.gotrueDbUrl` / `externalDatabase.restDbUri`**：极少数情况可在 **YAML** 中为 GoTrue / PostgREST 单独提供完整 **`postgres://...`**；REST 为空时会复用 GOTRUE。

### 局限（与 compose 的差异）

Compose 常为 **`db` 挂载初始化 SQL/JWT**。本 chart 通过子 chart **`Deployment` 风格** 跑 Postgres，不等价于挂载同一卷；仅用 **`bundled.postgres=true` + compose 对齐角色名**时，请以 **`supabase/postgres`** 镜像并自行确认首次初始化能满足业务（或在外链库走完官方迁移）。

### 与独立 chart

- 独立网关仍可用 [`kong-gateway`](../kong-gateway/README.zh-CN.md)。
- 独立 PG 仍可用 **`postgresql-new`**；本 umbrella 在 `bundled.postgres=false` 时与之组合。
