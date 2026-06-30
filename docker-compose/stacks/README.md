# Compose 聚合栈

| 文件 | 包含 |
|------|------|
| [`k3s-kuboard.compose.yaml`](./k3s-kuboard.compose.yaml) | K3s + Kuboard + kubeconfig 改写 + **自动导入集群** |
| [`k3s-kubepi.compose.yaml`](./k3s-kubepi.compose.yaml) | K3s + KubePi + kubeconfig 改写 + **自动导入集群** |

> **Kuboard / KubePi 套件二选一**（共用 `k3s-server` 固定容器名，不可同时 up）。

## K3s + Kuboard

```bash
cd docker-compose/stacks
mkdir -p ../k3s/output
cp k3s-kuboard.env.example .env
docker compose -f k3s-kuboard.compose.yaml up -d
```

| 服务 | 地址 |
|------|------|
| Kuboard | http://127.0.0.1:8090（`admin` / `Kuboard123`） |
| K3s API | https://127.0.0.1:6443 |

启动后 `kuboard-import-init` 会自动将 K3s 以集群名 **`k3s-local`** 导入 Kuboard（无需手动粘贴 kubeconfig）。确认：

```bash
docker logs kuboard-import-init
# 期望：cluster 'k3s-local' imported 或 already exists, skip
```

## K3s + KubePi

```bash
cd docker-compose/stacks
mkdir -p ../k3s/output
cp k3s-kubepi.env.example .env
docker compose -f k3s-kubepi.compose.yaml up -d
```

| 服务 | 地址 |
|------|------|
| KubePi | http://127.0.0.1:8091（`admin` / `kubepi`） |
| K3s API | https://127.0.0.1:6443 |

启动后 `kubepi-import-init` 会自动导入集群 **`k3s-local`**。确认：

```bash
docker logs kubepi-import-init
```

### 可选环境变量（`.env`）

| 变量 | 默认 | 说明 |
|------|------|------|
| `KUBOARD_CLUSTER_NAME` / `KUBEPI_CLUSTER_NAME` | `k3s-local` | 导入后的集群显示名 |
| `KUBOARD_USER` / `KUBEPI_USER` | 见各面板默认账号 | 管理 UI 登录用户 |
| `KUBOARD_PASS` / `KUBEPI_PASS` | 见各面板默认密码 | 管理 UI 登录密码 |

### 停止

```bash
docker compose -f k3s-kubepi.compose.yaml down
# 或
docker compose -f k3s-kuboard.compose.yaml down
```

需 **Docker Compose v2.20+**（`include`）。
