# Docker Compose 本地栈

| 目录 | 说明 |
|------|------|
| [**middleware/**](./middleware/) | 常用中间件 MVP + `include` 聚合（Java / 多库 / 数据平台） |
| [**k3s/**](./k3s/) | K3s 单节点（Docker 内，导出 kubeconfig） |
| [**kuboard/**](./kuboard/) | Kuboard v3 集群管理 UI |
| [**kubepi/**](./kubepi/) | KubePi（飞致云）K8s 管理面板 |
| [**stacks/**](./stacks/) | 聚合栈（**K3s + Kuboard** / **K3s + KubePi**） |
| [kong/](./kong/) | Kong + PostgreSQL + Konga |
| [snowy/](./snowy/) | Snowy Cloud 全家桶 |
| [openclaw/](./openclaw/) | OpenClaw Gateway + DeepSeek |

中间件聚合示例：

```bash
cd middleware
docker compose -f stacks/java-full.compose.yaml up -d
```

K3s + Kuboard：

```bash
cd stacks
cp k3s-kuboard.env.example .env
docker compose -f k3s-kuboard.compose.yaml up -d
```

K3s + KubePi（飞致云）：

```bash
cd stacks
cp k3s-kubepi.env.example .env
docker compose -f k3s-kubepi.compose.yaml up -d
```

需 **Docker Compose v2.20+**（`include`）。

## 镜像

默认使用华为云 SWR 第三方库前缀（与 Helm Chart 一致）：

```text
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/…
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/…
```

K3s 集群内 Pod 另在 `k3s/compose.yaml` 的 `configs.k3s-registries` 内联 mirror 指向同一 SWR 路径。
