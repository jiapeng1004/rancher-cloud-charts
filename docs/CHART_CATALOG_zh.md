# Chart 一览（节选）

以下为仓库内可直接 `helm install` 的目录（与子目录中带 `Chart.yaml` 的发行版）。

| 类目 | Chart 路径 | 说明 |
|------|-------------|------|
| 聚合一键装 | `charts/middleware-bundle` | MySQL / Redis / PostgreSQL / MinIO，子 chart 已嵌入 **`charts/`**，Rancher 可直接安装 |
| 组合（历史） | `charts/server-new` | 嵌入式子 chart；**单体权威**仍为 `charts/mysql-new/5.7`、`redis-new/7.0`、`minio-new/2024-01` |
| 数据库 | `charts/mysql-new/5.7`、`8.0` | MySQL |
| | `charts/postgresql-new/16` | PostgreSQL 16 |
| | `charts/mongodb` | MongoDB |
| | `charts/oracle-free-db` | gvenzl Oracle Free（占位/测试） |
| **BaaS** | **`charts/supabase`** | **默认内嵌 Postgres + Kong**（与上游 compose）；可关 `bundled` / `gateway.external` 接 RDS · `README.zh-CN.md` |
| 缓存/消息 | `charts/redis-new/6.2`、`7.0`、`7.2` | Redis |
| | `charts/kafka`、`charts/rabbitmq`（已有单体） | 消息队列（Kafka / AMQP） |
| | **`charts/rocketmq-k8s`** | RocketMQ Namesrv + Broker（试跑占位） |
| | **`charts/kubemq-standalone`** | KubeMQ 单机占位 |
| OLAP / 向量 / 检索 | `charts/server-new/charts/doris`（随 **server-new**） | Doris 分析库当前仅内嵌于此 |
| | `charts/elasticsearch/7.17.6`、`8.17.3` | ES |
| | **`charts/elk-bundle`** | **ELK**：ES chart + **`logstash-oss`**（子 chart 已嵌入 **`charts/elk-bundle/charts/`**） |
| | **`charts/logstash-oss`**（亦被 elk-bundle 引用） | Logstash → Elasticsearch |
| | `charts/milvus` | Milvus |
| 镜像/注册中心 | **`charts/harbor-registry`** | Harbor：**官方 Helm 指引占位** |
| Ingress / 网关 | `charts/nginx-web`、`charts/openresty-web`、`charts/pingora-proxy`、`charts/nginx-ingress` | 常见网关/入口 |
| | **`charts/traefik-gateway`** | Traefik：**文件 Provider 起步**，生产请看官方 Helm |
| | **`charts/kong-gateway`** | **Kong**：DB-less **声明式**（`declarative.config`），可选 Ingress；详见 `README.zh-CN.md` |
| | **`charts/frp-tunnel`** | **FRP**：首开/Demo：`frps`（TCP / 可选 HTTP vhost）+ 可选 `frpc` 暴露集群内服务 |
| **直播/WebRTC** | `charts/srs-live` | OSSRS SRS（RTMP/HLS/HTTP-FLV，可选极简 WebRTC 块） |
| | `charts/mediamtx-live` | MediaMTX（RTSP/RTMP/HLS/WebRTC 网关） |
| | `charts/ome-live` | OvenMediaEngine 占位 |
| | `charts/janus-webrtc` | Janus WebRTC 占位（WS + REST） |
| **观测 · 可视化 · 压测** | `charts/grafana-dash` | Grafana OSS 控制台（PVC SQLite 起步形态） |
| | `charts/k6-cronjobs` | **k6 CronJob**：RPS/阈值/p95，`scriptBody` + `TARGET_URL` |
| | `charts/locust-live` | Locust：**Web UI + 分布式 Worker** |
| | `charts/prometheus` | Prometheus 采集（可按需再接 Grafana DS） |
| | `charts/spring-boot-admin` | Spring Boot 应用运行时面板（若在用 Spring） |
| **AI / CMS / 文档 / 占位** | **`charts/openclaw-runner`** | OpenClaw：**生产推荐 Operator**，本目录为占位 Deployment |
| | **`charts/dify-lite`**、**`charts/cozeloop-platform`** | Dify / CozeLoop：**Compose / 源码部署指引占位** |
| | **`charts/wordpress-site`** | WordPress + 外置 MySQL |
| | **`charts/onlyoffice-docs`** | ONLYOFFICE Docs |
| 大数据占位 | **`charts/hadoop-dev`** | Hadoop：**说明占位**（建议云上 MRS/EMR） |
| 应用模板 | `charts/ruoyi-vue`、`charts/halo`、… | 其它业务模板按需替换镜像 |

新增组件时优先：**单体 chart 可被 umbrella 引用**（`middleware-bundle` 模式）；模板避免再引入 `templates/_helpers.tpl`。
