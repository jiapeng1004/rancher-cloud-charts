在 `charts/elk-bundle` 目录执行：`helm dependency update`

然后：`helm upgrade --install my-elk . -n logging --create-namespace`

- Elasticsearch / Kibana 行为由子 chart `charts/elasticsearch/8.17.3` 控制；
- Logstash TCP *5044* 接收简易 JSON，`logstash-oss.elasticsearch.hosts` 需能与 ES Service 对齐（默认 `http://elasticsearch:9200`）。

生产请补充：**Filebeat/Vector、存储类、PVC、Ingress、安全与 RBAC**，并复核 Elastic 订阅与许可证边界。
