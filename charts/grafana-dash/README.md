# grafana-dash

[Grafana](https://grafana.com/oss/grafana/) 用于指标/Prometheus/Victorialogs/Loki 等 **可视化**。本 Chart 仅为 **单机 SQLite + PVC** 的起步形态；数据源与仪表盘建议通过 **Provisioning**（`ConfigMap`/Secret）或 UI 导入。

默认镜像可走华为云 SWR 前缀；生产环境请改掉 `admin.password` 并挂载 **数据源 YAML**。

对接本仓库自带的 `charts/prometheus` 或其它 Prometheus 兼容端点时：在 Grafana 添加 DataSource HTTP URL（常为 `http://prometheus-server:9090` 或自建 Service）。
