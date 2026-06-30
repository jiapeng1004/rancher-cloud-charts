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

一键 K3s + Kuboard + 生成 Kuboard 专用 kubeconfig，并**自动导入**集群：

```bash
cd docker-compose/stacks
cp k3s-kuboard.env.example .env
docker compose -f k3s-kuboard.compose.yaml up -d
```

启动后 `kuboard-import-init` 会将 K3s 以 **`k3s-local`** 导入 Kuboard，详见 [stacks/README.md](../stacks/README.md)。

## 端口

| 映射 | 用途 |
|------|------|
| `8090` → 80 | Kuboard Web |
| `10081` | kuboard-agent TCP（导入集群时 agent 通信用） |

## 镜像

默认 `swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/eipwork/kuboard:v3`，与 [k3s](../k3s/compose.yaml)、[middleware](../middleware/) 同一套 SWR 前缀。

## 绑定外部集群

套件模式已自动导入；单独使用 Kuboard 时可在 UI **添加集群 → KubeConfig 导入**，`server` 须为容器网络内可达地址（如 `https://k3s-server:6443`）。

## 停止

```bash
docker compose down        # 保留 kuboard-data 卷
docker compose down -v     # 删 Kuboard 数据（慎用）
```
