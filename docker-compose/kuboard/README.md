# Kuboard v3（Docker Compose MVP）

[Kuboard](https://kuboard.cn/) 是 Kubernetes 多集群 Web 管理界面。本 compose **独立于集群**运行，可管理本仓库 [k3s](../k3s/) 或任意已有集群。

## 启动

```bash
cd docker-compose/kuboard
cp .env.example .env   # 按需改端口
docker compose up -d
```

浏览器：<http://127.0.0.1:8090/>（默认账号 **`admin` / `Kuboard123`**）

## 与 K3s 联合套件

一键 K3s + Kuboard + 生成 Kuboard 专用 kubeconfig：

```bash
cd docker-compose/stacks
cp k3s-kuboard.env.example .env
docker compose -f k3s-kuboard.compose.yaml up -d
```

导入集群见 [stacks/README.md](../stacks/README.md)。

## 端口

| 映射 | 用途 |
|------|------|
| `8090` → 80 | Kuboard Web |
| `10081` | kuboard-agent TCP（导入集群时 agent 通信用） |

## 镜像

默认 `swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/eipwork/kuboard:v3`，与 [k3s](../k3s/compose.yaml)、[middleware](../middleware/) 同一套 SWR 前缀。

## 绑定外部集群

1. 登录 Kuboard → **添加集群** → **KubeConfig 导入**
2. 粘贴 kubeconfig；`server` 须为 **Kuboard 容器能访问的地址**（同 Docker 网络内用服务名，如 `https://k3s-server:6443`）

## 停止

```bash
docker compose down        # 保留 kuboard-data 卷
docker compose down -v     # 删 Kuboard 数据（慎用）
```
