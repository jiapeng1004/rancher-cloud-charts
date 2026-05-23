## middleware-bundle

聚合安装 MySQL / Redis / PostgreSQL / MinIO。各组件「权威」源码仍在 **`charts/mysql-new`、`charts/redis-new` 等**；本聚合包内 **`charts/`** 为副本，便于 **Rancher / helm-git 直接 `helm template`**，无需在安装机执行 `helm dependency update`。更新单体后可从对应目录手工同步并重打 Umbrella **version**。

### 安装示例（无需前置 dependency）

```bash
cd charts/middleware-bundle
helm upgrade --install data-stack . -n default --create-namespace \
  --set mysql.enabled=true,redis.enabled=true,postgresql.enabled=true,minio.enabled=true
```

镜像仓库默认建议在子 Chart 的 `values.yaml` 中使用华为云 SWR「第三方库」加速前缀：`swr.<region>.myhuaweicloud.com/ddn-k8s/docker.io/...`。
