Meetecho **[Janus](https://janus.conf.meetecho.com/)** 是常见的 **WebRTC 服务器**（SFU/MCU）。本 Chart 占位暴露 **REST(7088)** 与常用 **WS(8188)**。**UDP RTP 范围、STUN/TURN** 须在集群外层单独规划（常为 `hostNetwork`、`NodePort UDP`、`coturn`、裸机网络等）。

- `ingress.enabled=true` 时会自动合并注解 `nginx.ingress.kubernetes.io/websocket-services`，便于 Ingress-Nginx 转发 WebSocket。
- `instrumentisto/janus-gateway` 仅为社区镜像示例；生产环境请校对 **许可证**，或替换为你自建、且已在华为云 SWR 同步的镜像。
