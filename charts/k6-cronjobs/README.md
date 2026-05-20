[K6](https://k6.io/) 常用于 **RPS / 场景压测** 与 **SLO 阈值**（成功率、p95）。本 Chart 用 **CronJob** 挂载由 `jobs.default.scriptBody` 生成的脚本；需要人工触发时可设 `suspend: true`。

与 Grafana Cloud、k6 OSS 的生态集成请参考官方文档；镜像默认可走华为云 SWR 前缀的 `docker.io/grafana/k6`。
