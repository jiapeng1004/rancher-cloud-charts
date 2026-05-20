[MediaMTX（原 rtsp-simple-server）](https://github.com/bluenviron/mediamtx) 常用于 **RTSP/RTMP 接入 + HLS / WebRTC** 的简单汇聚，是比「纯 SRS」更易起步的一类方案（两者可并行存在，选型由业务而定）。

镜像经华为云 SWR 前缀拉取时注意 **tag**：`latest` 仅示意，请在生产锁定 digest 或 semver tag。

Ingress 仅能暴露 **TCP 上的 HTTP/HLS**，WebRTC RTP/RTC 往往需要 **UDP、NodePort 或 hostNetwork**，与 SRS 一节说明类似。
