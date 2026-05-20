[Locust](https://locust.io/) 自带 **Web 控制台**，适合 **HTTP/API 压测**。本 Chart：`Master` ×1 + **`worker.replicas` 个 Worker**；`locustfile` 由 ConfigMap 挂载。

**Ingress** 仅用于 Web UI **8089**；Worker 访问 Master 使用的 **5557** 必须集群内可达。

与 **k6** 选型：脚本/CI/`thresholds` 偏 k6（见 **`charts/k6-cronjobs`**）；需要 **Python DSL + UI** 时偏 Locust。
