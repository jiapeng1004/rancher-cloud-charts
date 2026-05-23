Elastic **Logstash** 许可证与镜像说明以 Elastic 文档为准。

本 Chart 假定已有 **Elasticsearch**（本仓库 ES 子 Chart 创建的 Service 名常为 `elasticsearch`，端口 9200）。输入为 **TCP 5044 JSON** —— 可自行改为 `beats`/`kafka`/`http` pipeline。
