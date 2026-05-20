[Harbor](https://github.com/goharbor/harbor) 建议使用 **官方 Helm**：

```bash
helm repo add harbor https://helm.goharbor.io
helm upgrade --install harbor harbor/harbor -n harbor-system --create-namespace
```

国内部署请规划 **externalURL、PostgreSQL、Redis、对象存储/PVC**；镜像可经华为云 SWR 中转同步。

对本占位 chart 执行 `helm install` 只会输出 **NOTES**。若希望在命名空间内看到资源，可设 **`stubConfigMap.enabled: true`**。
