# KubePi（飞致云）

[KubePi](https://gitee.com/fit2cloud-feizhiyun/KubePi) 是飞致云 / 1Panel 出品的 **K8s 多集群管理面板**，支持导入 kubeconfig、权限与多集群管理。

## 启动

```bash
cd docker-compose/kubepi
cp .env.example .env   # 可选
docker compose up -d
```

浏览器：<http://127.0.0.1:8091/>  
默认账号：**`admin` / `kubepi`**

## 与 K3s 联合套件

```bash
cd docker-compose/stacks
cp k3s-kubepi.env.example .env
docker compose -f k3s-kubepi.compose.yaml up -d
```

见 [stacks/README.md](../stacks/README.md)。套件启动后会自动导入 K3s 集群（`kubepi-import-init`），默认集群名 **`k3s-local`**。

## 说明

- 镜像默认华为云 SWR：`1panel/kubepi:v1.9.0`（SWR 无 `latest` 标签）
- 数据卷 `kubepi-data` → `/var/lib/kubepi`
- 需 `privileged: true`（官方推荐）
- 与 Kuboard 套件 **不要同时 up**（共用 `k3s-server` 容器名）
