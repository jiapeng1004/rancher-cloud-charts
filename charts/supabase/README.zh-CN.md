# Supabase Helm（本仓库 fork）

- 基于 **GitHub [supabase-community/supabase-kubernetes](https://github.com/supabase-community/supabase-kubernetes)** 结构与官方 **docker-compose** 思路；具体以本目录 `templates/`、`values.yaml` 为准。
- **国内镜像**：见 `values.yaml` 顶部注释与根目录 **`questions.yaml`** —— 默认华为云 **SWR「ddn-k8s/docker.io/…」** 前缀；**MinIO / MC** 已改为 **`docker.io/minio/minio` + `docker.io/minio/mc`**。
- **Rancher**：表单见 **`questions.yaml`**；Ingress Host、TLS、外链库等仍可「编辑 YAML」。
- **英文说明**：[**README.md**](./README.md)。
