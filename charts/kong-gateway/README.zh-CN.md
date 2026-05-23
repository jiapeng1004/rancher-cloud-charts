## `charts/kong-gateway`

- **选型**：**优先外链**——若已使用云上托管 Kong、全局 API 网关或 SLB+Nginx，只要把路由指到集群内 Service 即可，**不必部署**本 chart。需要集群内自持 Kong 时再装（**可选内建**）。
- **模式**：**DB-less**，`KONG_DATABASE=off`，通过 **`declarative.config`**（写入 ConfigMap）声明路由/服务。
- **约定**：**无** `_helpers.tpl**，各模板文件顶部仅用 `$name` / `$fullname`（见 [`docs/TEMPLATING_zh.md`](../../docs/TEMPLATING_zh.md)）。
- **镜像**：默认走华为 **SWR 第三方前缀**下的 `kong/kong:3.9.1`。

### Service

默认 `fullname` 为 `{Release}-{Chart.Name}`（可 `fullnameOverride` 覆盖）。

- **`{fullname}-proxy`**：对外网关（Ingress 绑定此端口，默认映射到 Pod **8000**）。
- **`{fullname}-admin`**（可 `service.admin.enabled` 关掉）：Admin API **8001**，仅建议在集群内需 ACL / RBAC。

### 示例安装

```bash
helm upgrade --install kg charts/kong-gateway -n kong --create-namespace \
  --set declarative.config="$(cat ./my-kong.yml)"
```

生产中建议用 **单独的 values 文件 / GitOps** 管理 `declarative.config`，并保持 `jwt` / `upstream` / `插件` 与团队规范一致。

### 与 upstream 的区别

不包含 Kong 官方的 **PostgreSQL 模式**与本仓库 **`traefik-gateway`**（文件 Provider）；需要传统 Kong + DB / 控制台请使用 [Kong Helm chart](https://github.com/Kong/charts) 或云上托管网关。
