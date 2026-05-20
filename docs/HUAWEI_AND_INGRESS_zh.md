# 华为云镜像与 Ingress 兼容性说明（简版）

本项目大量 Chart 的 `values.yaml` 默认使用：

`swr.<区域>.myhuaweicloud.com/ddn-k8s/docker.io/<原 Docker Hub 路径>`

该区域与「组织」请以 **华为云云容器镜像服务** 控制台中「镜像拉取」「第三方镜像库」展示的地址为准 (`ddn-k8s`、`swr` 路径可能随产品文档调整)。

## Ingress API 分层

兼容策略（与多数已修正模板一致）：

| Kubernetes              | Ingress `apiVersion`       | `ingressClassName` | `backend` 写法        |
|-------------------------|----------------------------|---------------------|-----------------------|
| ≥ 1.19                  | `networking.k8s.io/v1`      | ✅ (≥ 1.18)         | `service.name` + port |
| 1.14 – 1.21             | `networking.k8s.io/v1beta1` | ✅ (≥ 1.18)         | `serviceName` 形式    |
| 更旧集群                 | `extensions/v1beta1`        | ❌                   | `serviceName` 形式    |

新版本集群请使用 **`networking.k8s.io/v1`**，并务必设置与各路径匹配的 **`pathType`**（`ImplementationSpecific` 常用于正则 + `nginx.ingress-controller`）。

## 直播协议与 Ingress

普通 **HTTP(S) Ingress（七层）** 只能暴露 **HTTPS/HTTP**：例如 **HLS 的 `http-flv`/部分 LL-HLS**。以下能力 **不能单靠 Ingress-NGINX 对外暴露**：

- **RTMP**（常用于推流）：需要 **四层**（NodePort、`hostNetwork`、`LoadBalancer` TCP 监听等）。
- **WebRTC RTP/ICE、SRT UDP**：往往要 **UDP 端口放行**、`hostNetwork`、云厂商 **UDP 监听器**，或 DaemonSet + 注解。

相关 Chart：`charts/srs-live`、`charts/mediamtx-live`、`charts/ome-live`、`charts/janus-webrtc` —— 使用前请优先阅读各自的 `README.md`。

## Helm Library

`charts/rancher-lib` 为 **`type: library`**，可向新 Chart 增加 `dependency` 后通过 `define` 模板复用 Ingress API 推导逻辑（按需逐步迁入现有 Chart）。
