# rancher-cloud-charts

个人 / 团队可用的 **Helm Chart** 合集，侧重：

- **国内部署**：默认值里大量使用华为云 **SWR 第三方镜像前缀**（`swr.<region>.myhuaweicloud.com/ddn-k8s/docker.io/...`），前缀以控制台说明为准。
- **新旧 Kubernetes**：Ingress 模板在 **`networking.k8s.io/v1` / `v1beta1` / `extensions/v1beta1`** 之间按版本分支，老旧集群避免出现非法 `pathType` 或错误的 `backend` 结构。
- **单体 + 聚合**：每种中间件可有 **独立 chart**，另提供 **`middleware-bundle`** 聚合 MySQL / Redis / PostgreSQL / MinIO。
- **动态存储**：**`charts/nfs-subdir-external-provisioner`**（[kubernetes-sigs](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner) vendor + 国内 registry.k8s.io 镜像默认值 + Rancher `questions`：`nfs.server` / `nfs.path`）。
- **直播 / WebRTC**：SRS、MediaMTX、OvenMediaEngine、Janus 等见 `charts/srs-live`、`charts/mediamtx-live`、`charts/ome-live`、`charts/janus-webrtc`（说明见 [`docs/HUAWEI_AND_INGRESS_zh.md`](./docs/HUAWEI_AND_INGRESS_zh.md) 中「直播协议与 Ingress」）。
- **观测与压测**：`charts/grafana-dash`（可视化）、`charts/k6-cronjobs`（k6 / RPS 与阈值）、`charts/locust-live`（Locust Web UI + Worker），可与既有 `charts/prometheus` 组合使用。
- **消息与 ELK**：`charts/kafka`、`charts/rabbitmq`（已有单体）、新增 **`rocketmq-k8s`、`kubemq-standalone`**；**ELK** 参见 **`charts/elk-bundle`**（子 chart 已嵌入 `charts/elk-bundle/charts/`）与 **`logstash-oss`**。
- **Ingress / NAT 穿透**：**`charts/frp-tunnel`**（首开环境 FRP：`frps` TCP / 可选 HTTP + 可选 `frpc`，见 chart 内 README）；另有 **Kong 声明式网关** **`charts/kong-gateway`**（`README.zh-CN.md`）。
- **平台类**：Harbor **`harbor-registry`（占位+官方 Helm 说明）**、Traefik **`traefik-gateway`（文件 Provider）**、**`supabase`**（上游 Helm/K8s 栈 + 国内镜像 + `questions.yaml`：`charts/supabase/README.zh-CN.md`）、WordPress **`wordpress-site`**、ONLYOFFICE **`onlyoffice-docs`**、OpenClaw **`openclaw-runner`**、Dify / CozeLoop **`dify-lite` / `cozeloop-platform`（Compose/源码说明占位）**、Hadoop **`hadoop-dev`（说明占位）**。

## Chart 图标

各 Chart 的 `icon` **优先使用 Devicon 彩色矢量**（`*-original.svg`，经 jsDelivr：`https://cdn.jsdelivr.net/gh/devicons/devicon@v2.17.0/icons/...`）；少数 Devicon 未收录的品牌（如 Milvus）退回 **Simple Icons** 单色官方标识；MinIO / Gitea 等使用对应开源仓库内经 jsDelivr 镜像的 **官方彩色 SVG**。映射表见 [`scripts/apply_chart_icons.py`](./scripts/apply_chart_icons.py)；修改后在仓库根执行 `py -3 scripts/apply_chart_icons.py` 写回全部 `Chart.yaml`。

## 文档

| 文档 | 说明 |
|------|------|
| [docs/HUAWEI_AND_INGRESS_zh.md](./docs/HUAWEI_AND_INGRESS_zh.md) | 镜像前缀与 Ingress 兼容策略 |
| [docs/TEMPLATING_zh.md](./docs/TEMPLATING_zh.md) | Helm 模板约定（少用 tpl / 少套娃） |
| [docs/HELM_REPO_zh.md](./docs/HELM_REPO_zh.md) | Helm 仓库发布与 `helm repo add` |
| `charts/supabase/README.zh-CN.md` | Supabase（upstream Helm/K8s 栈 · 默认 SWR · Rancher questions） |
| `charts/kong-gateway/README.zh-CN.md` | Kong（DB-less 声明式网关） |
| `charts/middleware-bundle/README.md` | 聚合中间件；子 chart 已内置，见该 README |

## Rancher 自定义答案（questions.yaml）

- **`type: library`** 的子 chart **不生成表单**（本仓库一般不单独再放仅含模板片段的 library chart；Ingress / 兼容性逻辑写在对应资源的 `ingress.yaml` 等处）。
- **其余 application Chart**：每个 Chart 目录下均有非空 `questions.yaml`（或由子 chart / 手写维护）；表单字段与常用 `values` 对齐，**复杂段落仍建议在 Rancher「编辑 YAML」中维护**。
- **批量同步**：仓库根目录执行 **`py -3 scripts/sync_rancher_questions.py`**，可按 `values.yaml` 自动生成/补齐常见项（**跳过已有人工维护的非空文件**）。
- **历史 `questions.yml`**：脚本会在缺少 `questions.yaml` 时用同名 `.yml` 复制补齐（便于 Rancher 读取）。

## Helm 仓库（GitHub Pages）

Chart 已打包发布为标准 HTTP Helm 仓库，详见 [`docs/HELM_REPO_zh.md`](./docs/HELM_REPO_zh.md)。

```bash
helm repo add rancher-cloud-charts https://jiapeng1004.github.io/rancher-cloud-charts
helm repo update
helm search repo rancher-cloud-charts
```

本地打包（需 Helm 3）：

```bash
py -3 scripts/package_helm_charts.py --clean
```

## 快速聚合安装

```bash
cd charts/middleware-bundle
helm upgrade --install my-mw . -n default --create-namespace
```

按需覆盖子 chart 的配置，例如在父级 `values.yaml` 中使用 `postgresql.*`、`redis.*`。

历史模板中若仍存在硬编码 `networking.k8s.io/v1` 或未分支的 Ingress，可复制 **`postgresql-new`**、**`nginx-web`**、**`middleware-bundle/charts/mysql`** 等 chart 里 **`ingress.yaml` 顶部**的 **`$kv` + `semverCompare`** 写法（[`docs/TEMPLATING_zh.md`](./docs/TEMPLATING_zh.md)）。
