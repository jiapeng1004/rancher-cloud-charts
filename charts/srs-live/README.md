# srs-live — SRS 开源流媒体服务端

[SRS（Simple Realtime Server）](https://github.com/ossrs/srs) 支持 RTMP、HLS、HTTP-FLV/S、WebRTC 等能力，是国内常用的直播/WebRTC 服务端之一。

## 镜像与华为云

默认 `values.yaml` 使用华为云 SWR 「第三方镜像库」前缀，请按控制台显示的 `swr.<region>.myhuaweicloud.com/ddn-k8s/docker.io/ossrs/srs:<tag>` 核对 tag（如 `5` / `v5.0.213`）。

## Kubernetes 注意事项

| 场景 | 建议 |
|------|------|
| 仅 RTMP 推 → HLS / HTTP-FLV 播放 | 一般 `Deployment + ClusterIP/NodePort` 即可，`ingress.enabled` 可开 HTTP 路径 |
| WebRTC（浏览器） | UDP、ICE `candidate` 常需设置为**公网或对端可达 IP**；生产常见 **hostNetwork**/固定节点 DaemonSet/Ingress udp 注解等，需结合集群 CNI |

本 Chart 的 `ingress` **仅涵盖 HTTP**(如 HLS/控制台)；**RTMP/WebRTC RTP 无法用七层 Ingress 终结**。

在 `values.srsConfig` 中将 `rtcEnabled: true` 并填写合理的 `rtcCandidate`（常为节点 EIP 或由 Sidecar 注入）。

## 安装

```bash
helm upgrade --install my-srs charts/srs-live -n streaming --create-namespace
```

## 相关开源栈（未全部打包成 Chart）

常与 SRS 组合的组件包括：**`coturn`（TURN/STUN）**、边转码 **`ffmpeg`**（通常用 CronJob/Job）、以及 **`ZLMediaKit`**（国产流媒体框架，可自行仿照 `mediamtx-live` 挂载配置文件打包 Helm）。
