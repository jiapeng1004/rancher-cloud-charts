# Supabase Helm（本仓库 fork）

- 基于 **GitHub [supabase-community/supabase-kubernetes](https://github.com/supabase-community/supabase-kubernetes)** 结构与官方 **docker-compose** 思路；具体以本目录 `templates/`、`values.yaml` 为准。
- **国内镜像**：见 `values.yaml` 顶部注释与根目录 **`questions.yaml`** —— 默认华为云 **SWR「ddn-k8s/docker.io/…」** 前缀；**MinIO / MC** 已改为 **`docker.io/minio/minio` + `docker.io/minio/mc`**。
- **Rancher**：表单见 **`questions.yaml`**。Ingress 只做扁平字段：**`ingress.kongHostname`**（Kong/API 对外域名）、**`ingress.tlsSecretName`**（HTTPS 时用集群 TLS Secret），**Studio** 另开 Ingress：**`ingress.studio.hostname`**、可选 **`ingress.studio.tlsSecretName`**（不填则沿用全局 `tlsSecretName`）。不设多 host / 不写 `Ingress.spec.tls` 结构副本。
- **外链与环境变量**：**`environment.auth.API_EXTERNAL_URL`**、**`GOTRUE_SITE_URL`**、**`environment.studio.SUPABASE_PUBLIC_URL`** 等必须与你对外访问的根 URL **自行对齐**，Chart 不从 Ingress 反推。
- **英文说明**：[**README.md**](./README.md)。
