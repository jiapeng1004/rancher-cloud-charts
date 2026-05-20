`type: library` 的 Helm 库，不向集群渲染资源，仅供其他 chart 依赖后 `include`。

### 在其他 Chart 中引用

```yaml
# Chart.yaml dependencies
dependencies:
  - name: rancher-lib
    version: 0.1.0
    repository: file://../rancher-lib
```

随后在 Ingress 模板里写一行即可：`{{ include "rancher-lib.ingress.apiVersion" . }}`（实现见 `templates/_ingress.tpl`，已压缩为**单个 define**，避免多层模板嵌套）。

单体 chart **也可不依赖本库**：直接复制本项目 `mysql-new/8.0/templates/ingress.yaml` 里顶部几行 `semverCompare` + `$kv` 的写法即可；详见仓库 [`docs/TEMPLATING_zh.md`](../../docs/TEMPLATING_zh.md)。
