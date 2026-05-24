# nfs-subdir-external-provisioner（本仓库发行版）

本目录自 [kubernetes-sigs/nfs-subdir-external-provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner) 官方 Helm Chart **.vendor** 入内，并与 Rancher **`questions.yaml`** 对齐：

- **`nfs.server` / `nfs.path`**：在图形界面或 `values.yaml` 中必填；指向你**已就绪**的 NFS 导出。
- **镜像**：默认使用华为云 SWR 公开的 **registry.k8s.io** 三方同步前缀（可按 Region / 加速器改写 `image.repository`）。

上游 Helm Repo 索引：<https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/>

若仅使用官方远程仓库（不从本 Git 仓安装），可执行：

```bash
helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm repo update
```

安装前请确认 NFS 导出权限、防火墙与挂载路径与实际业务一致。
