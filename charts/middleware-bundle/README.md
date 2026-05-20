## middleware-bundle

聚合安装 MySQL / Redis / PostgreSQL / MinIO。各组件完整模板分别在 `charts/mysql-new`、`charts/redis-new` 等目录，可同时维护「单体」与「组合」两套入口。

### 准备依赖

```bash
cd charts/middleware-bundle
helm dependency update
```

### 安装示例

```bash
helm upgrade --install data-stack . -n default --create-namespace \
  --set mysql.enabled=true,redis.enabled=true,postgresql.enabled=true,minio.enabled=true
```

镜像仓库默认建议在子 Chart 的 `values.yaml` 中使用华为云 SWR「第三方库」加速前缀：`swr.<region>.myhuaweicloud.com/ddn-k8s/docker.io/...`。
