Oracle **Free / XE** 容器镜像通常为 **gvenzl/oracle-free**（社区维护），首次启动较慢，请调高 `startupProbe`。生产环境建议使用官方云数据库或 StatefulSet + 持久化卷。

镜像经华为云 SWR 同步示例：`swr.<region>.myhuaweicloud.com/ddn-k8s/docker.io/gvenzl/oracle-free`
