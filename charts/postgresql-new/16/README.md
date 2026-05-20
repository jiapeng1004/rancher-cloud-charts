PostgreSQL 16 单副本模板，Ingress 与 `charts/mysql-new` 系列对齐：在 1.19+ 使用 `networking.k8s.io/v1` 与带 `pathType` 的规则；更早集群退化为 `v1beta1` / `extensions/v1beta1` 并使用 `serviceName` / `servicePort` backend。
