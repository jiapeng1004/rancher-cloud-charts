[KubeMQ](https://kubemq.io/) 为面向 Kubernetes 的消息与事件总线。本 Chart 为 **单副本占位**，便于国内镜像前缀试跑；**集群高可用、TLS、Store** 请参考官方文档与 Operator。

默认暴露 **REST(9090)** 与 **gRPC(50000)**；其中 gRPC 往往需 **NodePort / 内网访问**。
