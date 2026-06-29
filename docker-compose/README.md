# Docker Compose 本地栈

| 目录 | 说明 |
|------|------|
| [**middleware/**](./middleware/) | 常用中间件 MVP + `include` 聚合（Java / 多库 / 数据平台） |
| [**k3s/**](./k3s/) | K3s 单节点（Docker 内，导出 kubeconfig） |
| [kong/](./kong/) | Kong + PostgreSQL + Konga |
| [snowy/](./snowy/) | Snowy Cloud 全家桶 |
| [openclaw/](./openclaw/) | OpenClaw Gateway + DeepSeek |

中间件聚合示例：

```bash
cd middleware
docker compose -f stacks/java-full.compose.yaml up -d
```

需 **Docker Compose v2.20+**（`include`）。

## 镜像加速

**不必改宿主机 `daemon.json`**。在 compose 里两种写法即可：

1. **服务镜像**：`image: docker.1ms.run/命名空间/镜像:tag`（或 `.env` 里 `DOCKER_MIRROR` 变量前缀）
2. **K3s Pod 镜像**：`configs` 内联 `mirrors.docker.io.endpoint`（见 [`k3s/compose.yaml`](./k3s/compose.yaml)）

默认 mirror：`https://docker.1ms.run`
