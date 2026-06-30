# Compose 聚合栈

| 文件 | 包含 |
|------|------|
| [`k3s-kuboard.compose.yaml`](./k3s-kuboard.compose.yaml) | K3s + Kuboard + 生成 `kuboard-kubeconfig.yaml` |

## K3s + Kuboard

```bash
cd docker-compose/stacks
mkdir -p ../k3s/output
cp k3s-kuboard.env.example .env
docker compose -f k3s-kuboard.compose.yaml up -d
```

### 访问

| 服务 | 地址 |
|------|------|
| Kuboard | http://127.0.0.1:8090（`admin` / `Kuboard123`） |
| K3s API | https://127.0.0.1:6443（宿主机 kubectl 用 `../k3s/output/kubeconfig.yaml`） |

### 导入 K3s 到 Kuboard

1. 等待 `kuboard-kubeconfig-init` 完成（一次性任务，退出码 0）
2. 打开 Kuboard → **添加集群** → **KubeConfig 导入**
3. 粘贴 **`docker-compose/k3s/output/kuboard-kubeconfig.yaml`** 全文  
   （`server` 已为 `https://k3s-server:6443`，供 Kuboard 容器访问）

```bash
# 查看生成的配置
cat ../k3s/output/kuboard-kubeconfig.yaml
```

若 init 容器已退出，可手动改写：

```bash
sed 's|https://127.0.0.1:6443|https://k3s-server:6443|g' ../k3s/output/kubeconfig.yaml > ../k3s/output/kuboard-kubeconfig.yaml
```

### 停止

```bash
docker compose -f k3s-kuboard.compose.yaml down
```

需 **Docker Compose v2.20+**（`include`）。
