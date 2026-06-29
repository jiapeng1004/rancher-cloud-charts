# K3s on Docker（MVP）

在 Docker 里跑 **单节点 K3s**，用于本地试 Helm Chart、验证 Rancher 应用模板等。Pod 由 K3s 内置 **containerd** 调度（不挂载 `docker.sock`）。

## 要求

- Docker Desktop / Docker Engine + Compose v2
- **Linux 容器模式**（WSL2 后端可用）
- 需 `privileged: true`

## 启动

```bash
cd docker-compose/k3s
mkdir -p output
cp .env.example .env   # 可选
docker compose up -d
```

就绪后 kubeconfig 在 **`output/kubeconfig.yaml`**（`server` 已改写为 `https://127.0.0.1:6443`）。

```bash
kubectl --kubeconfig output/kubeconfig.yaml get node
kubectl --kubeconfig output/kubeconfig.yaml get pods -A
```

或：

```bash
export KUBECONFIG=$PWD/output/kubeconfig.yaml
kubectl get node
```

## 端口

| 映射 | 用途 |
|------|------|
| `6443` | Kubernetes API |
| `8088` → 容器 `80` | ServiceLB / Ingress 类 HTTP（避免占宿主机 80） |
| `8443` → 容器 `443` | HTTPS |

## 网络 `app`

与 [middleware](../middleware/) 共用 **`app`** 网络名：middleware 先起或后起均可，Compose 会复用已有 `app` 网络。

K3s Pod 默认在 K3s 内部 CNI，**不会**自动与 `app` 上的 MySQL 等同网；业务 Pod 需通过宿主机端口或 K8s Service 访问 middleware。

## 默认选项

- 关闭内置 **Traefik**（`--disable=traefik`），可自装 `charts/traefik-gateway` 等
- 保留 **ServiceLB**（LoadBalancer → 节点 80/443，经端口映射到 8088/8443）

## 试装本仓库 Chart

```bash
export KUBECONFIG=$PWD/output/kubeconfig.yaml
helm upgrade --install demo ../../charts/nginx-web -n default --create-namespace
```

## 停止

```bash
docker compose down          # 保留 k3s-server-data 卷
docker compose down -v       # 删集群数据（慎用）
```

## 说明

- 镜像默认华为云 SWR：`rancher/k3s:v1.31.5-k3s1`
- 非生产高可用；多节点请用 k3d / 真机 k3s
- 若需 Pod 与宿主机 Docker 同级（`--docker` + `docker.sock`），见 [k3s 文档](https://docs.k3s.io/)，本 MVP 未默认开启
