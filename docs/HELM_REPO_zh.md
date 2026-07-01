# Helm 仓库（GitHub Pages）

本仓库 `charts/` 下的可安装 Chart 会打包发布到 GitHub Pages，作为标准 Helm HTTP 仓库使用。

## 添加仓库

```bash
helm repo add rancher-cloud-charts https://jiapeng1004.github.io/rancher-cloud-charts
helm repo update
```

## 安装示例

```bash
# 聚合中间件
helm upgrade --install my-mw rancher-cloud-charts/middleware-bundle -n default --create-namespace

# 单体 MySQL 8.0（版本化 chart 名含路径，以 search 结果为准）
helm search repo rancher-cloud-charts/mysql

# Supabase 栈
helm upgrade --install supabase rancher-cloud-charts/supabase -n supabase --create-namespace
```

## 本地打包

需 **Helm 3 + make**（MinGW / Linux）：

```bash
make helm-package
```

等价于：`find` 扫描 chart → `helm dependency build` → `helm package` → `helm repo index`，index 用 shell 加 UTF-8 BOM（浏览器中文不乱码）。**不依赖 Python。**

产物在 `.helm-packages/`（`*.tgz` + `index.yaml` + `.nojekyll`），已 gitignore。

## CI 发布

推送到 `main` / `develop` 且 `charts/**` 有变更时，CI 执行 **`make helm-package`**，然后推送到 **`gh-pages`**。

工作流：[`.github/workflows/helm-publish.yml`](../.github/workflows/helm-publish.yml)

### 首次启用 GitHub Pages

在 GitHub 仓库 **Settings → Pages**：

- **Source**：Deploy from a branch
- **Branch**：`gh-pages` / `/ (root)`

保存后数分钟内 `https://jiapeng1004.github.io/rancher-cloud-charts/index.yaml` 可访问。

## 发布范围

`make helm-package` 会发布：

- 顶层 chart（如 `charts/kafka`）
- 版本化子目录 chart（如 `charts/mysql-new/8.0`、`charts/redis-new/7.2`）

**不会**单独发布仅作为依赖嵌入的 chart（如 `middleware-bundle/charts/mysql`、`supabase/charts/auth`）。

备用脚本 [`scripts/package_helm_charts.py`](../scripts/package_helm_charts.py) 仍保留（本地调试、失败汇总），**CI 与 make 均不使用**。
