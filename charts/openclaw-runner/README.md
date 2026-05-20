[OpenClaw](https://openclaw.rocks/) 在 Kubernetes 上的 **推荐方式**是使用 **官方 Operator**（`openclaw-rocks/openclaw-operator`）与 `OpenClawInstance` CRD。

本 Chart 提供一个 **单 Deployment 占位**，便于与华为云镜像前缀快速试跑；镜像、端口、鉴权与密钥管理请严格按官方指引。

- GitHub Operator: `https://github.com/openclaw-rocks/openclaw-operator`
- 典型镜像：`ghcr.io/openclaw/openclaw`（已通过 `values.image.repository` 支持 SWR 前缀拼接）
