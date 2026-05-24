# Supabase Helm（本仓库 fork）

- 基于 **GitHub [supabase-community/supabase-kubernetes](https://github.com/supabase-community/supabase-kubernetes)** 结构与官方 **docker-compose** 思路；具体以本目录 `templates/`、`values.yaml` 为准。
- **国内镜像**：见 `values.yaml` 顶部注释与根目录 **`questions.yaml`** —— 默认华为云 **SWR「ddn-k8s/docker.io/…」** 前缀；**MinIO / MC** 已改为 **`docker.io/minio/minio` + `docker.io/minio/mc`**。
- **Rancher**：表单见 **`questions.yaml`**。**Kong** 只对 API，`ingress.tls`（多域名 + `secretName`）需在 values /「编辑 YAML」中配置。**Studio** 另有独立 Ingress（`ingress.studio.*`），表单可填 **逗号分隔域名 + tlsAuto.secretName**，或手写 `ingress.studio.tls`，结构同官方 `Ingress.spec.tls`。
- **Studio 外链**：Ingress 发布后，请将 **`environment.studio.SUPABASE_PUBLIC_URL`** 等指向浏览器访问 Studio 的根 URL（与 TLS 域名一致），否则控制台可能仍以默认值请求。
- **英文说明**：[**README.md**](./README.md)。
