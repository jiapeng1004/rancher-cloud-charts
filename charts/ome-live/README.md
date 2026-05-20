[OvenMediaEngine](https://github.com/AirenSoft/OvenMediaEngine) 是一套常见的 **超低延迟直播**开源引擎（LLHLS/WebRTC）。其 **XML 配置与环境变量**分支较多，本仓库仅提供可调 **镜像/`args`/端口**的占位 Deployment，生产使用请挂载 **Secret/ConfigMap** 中的官方 `Origin.xml`、`Edge.xml` 等或由 CI 下发。

常与 **Ingress-NGINX 的 udp-controller**、`hostNetwork`、`NodePool` RTP 放行等方案配合使用。

镜像建议经华为云 SWR 预先同步：`docker.io/airensoft/ovenmediaengine`（tag 请以官方 release 为准）。
