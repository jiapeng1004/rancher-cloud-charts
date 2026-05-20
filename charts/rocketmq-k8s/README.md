RocketMQ Namesrv **9876** + Broker **10909/10911/10912** 的最小拓扑。命令与 JVM 占位，请参阅 [RocketMQ](https://rocketmq.apache.org/) 官方部署指南。

Broker 默认同命名空间直连 Namesrv 的 Kubernetes DNS（`*.svc.cluster.local`）。
