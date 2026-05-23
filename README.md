# rancher-cloud-charts

个人 / 团队可用的 **Helm Chart** 合集，侧重：

- **国内部署**：默认值里大量使用华为云 **SWR 第三方镜像前缀**（`swr.<region>.myhuaweicloud.com/ddn-k8s/docker.io/...`），前缀以控制台说明为准。
- **新旧 Kubernetes**：Ingress 模板在 **`networking.k8s.io/v1` / `v1beta1` / `extensions/v1beta1`** 之间按版本分支，老旧集群避免出现非法 `pathType` 或错误的 `backend` 结构。
- **单体 + 聚合**：每种中间件可有 **独立 chart**，另提供 **`middleware-bundle`** 聚合 MySQL / Redis / PostgreSQL / MinIO。
- **直播 / WebRTC**：SRS、MediaMTX、OvenMediaEngine、Janus 等见 `charts/srs-live`、`charts/mediamtx-live`、`charts/ome-live`、`charts/janus-webrtc`（说明见 [`docs/HUAWEI_AND_INGRESS_zh.md`](./docs/HUAWEI_AND_INGRESS_zh.md) 中「直播协议与 Ingress」）。
- **观测与压测**：`charts/grafana-dash`（可视化）、`charts/k6-cronjobs`（k6 / RPS 与阈值）、`charts/locust-live`（Locust Web UI + Worker），可与既有 `charts/prometheus` 组合使用。
- **消息与 ELK**：`charts/kafka`、`charts/rabbitmq`（已有单体）、新增 **`rocketmq-k8s`、`kubemq-standalone`**；**ELK** 参见 **`charts/elk-bundle`**（子 chart 已嵌入 `charts/elk-bundle/charts/`）与 **`logstash-oss`**。
- **Ingress / NAT 穿透**：**`charts/frp-tunnel`**（首开环境 FRP：`frps` TCP / 可选 HTTP + 可选 `frpc`，见 chart 内 README）
- **平台类**：Harbor **`harbor-registry`（占位+官方 Helm 说明）**、Traefik **`traefik-gateway`（文件 Provider）**、**`supabase`**（**外链 Postgres** 的极简 API 栈：`charts/supabase/README.zh-CN.md`，与上游全量 chart 区分开）、WordPress **`wordpress-site`**、ONLYOFFICE **`onlyoffice-docs`**、OpenClaw **`openclaw-runner`**、Dify / CozeLoop **`dify-lite` / `cozeloop-platform`（Compose/源码说明占位）**、Hadoop **`hadoop-dev`（说明占位）**。

## Chart 图标

各 Chart 的 `icon` **优先使用 Devicon 彩色矢量**（`*-original.svg`，经 jsDelivr：`https://cdn.jsdelivr.net/gh/devicons/devicon@v2.17.0/icons/...`）；少数 Devicon 未收录的品牌（如 Milvus）退回 **Simple Icons** 单色官方标识；MinIO / Gitea 等使用对应开源仓库内经 jsDelivr 镜像的 **官方彩色 SVG**。映射表见 [`scripts/apply_chart_icons.py`](./scripts/apply_chart_icons.py)；修改后在仓库根执行 `py -3 scripts/apply_chart_icons.py` 写回全部 `Chart.yaml`。

## 文档

| 文档 | 说明 |
|------|------|
| [docs/HUAWEI_AND_INGRESS_zh.md](./docs/HUAWEI_AND_INGRESS_zh.md) | 镜像前缀与 Ingress 兼容策略 |
| [docs/TEMPLATING_zh.md](./docs/TEMPLATING_zh.md) | Helm 模板约定（少用 tpl / 少套娃） |
| [docs/CHART_CATALOG_zh.md](./docs/CHART_CATALOG_zh.md) | 当前 Chart 目录一览（节选） |
| `charts/supabase/README.zh-CN.md` | Supabase（社区 Helm 内嵌说明） |
| `charts/middleware-bundle/README.md` | 聚合中间件；子 chart 已内置，见该 README |

## 快速聚合安装

```bash
cd charts/middleware-bundle
helm upgrade --install my-mw . -n default --create-namespace
```

按需覆盖子 chart 的配置，例如在父级 `values.yaml` 中使用 `postgresql.*`、`redis.*`。

## Helm Library（可选）

参见 `charts/rancher-lib/README.md`，用于在新 chart 内复用 `Ingress apiVersion` 推导。

---

历史模板中若仍存在硬编码 `networking.k8s.io/v1` 或未分支的 Ingress，可按 `postgresql-new` / `nginx-web` 中的写法逐步对齐。
