# Helm 模板编写约定（尽量少用「模板魔法」）

本仓库 Chart 面向运维可读、易改。**默认写法是普通 YAML + 最少的 Helm 插值**，不要为了抽象而抽象。

## 避免的写法

1. **不要使用 `tpl` / `mustTpl`**  
   把整段 YAML 做成字符串再二次渲染，报错信息难定位，也难做静态检查。若有动态片段，优先拆成多个小的显式字段或单独的模板文件。

2. **`templates/_helpers.tpl` 已不再使用**  
   命名与常用标签已**内联在各 `templates/*.yaml` 文件顶部**（`$name`、`$fullname`，以及少数 Chart 的 `$chartLabel`、`$masterHostname`、`$feFullname` 等），不在单独 `_helpers.tpl` 里维护 `define` / `include`。若你用 `helm create` 生成带 `_helpers.tpl` 的 chart，可参考本仓库写法删掉该文件并把变量段落拷到每个业务模板顶端；或对接到维护脚本 [`scripts/strip_helpers_tpl.py`](../scripts/strip_helpers_tpl.py)（会按惯例替换常见 `include` 并移除 `_helpers.tpl`，改完务必本地 `helm template` 自检）。

3. **避免大面积 `{{- if eq ... }}` 嵌套五六层**，以及零碎的多层 `{{- define }}` / `include` 库式拼装  
   条件多时优先考虑：拆资源（多个 yaml）、或用 values 开关分成两段可读结构。

## 推荐写法

1. **Ingress API 版本分支**  
   - **单体 chart**：在 `ingress.yaml` 顶部用几行 `semverCompare` + 本地变量 `$kv`（与本仓库已有 mysql/redis 等 chart 一致），一目了然。  
   - **希望单行引用**：可依赖 [`charts/rancher-lib`](../charts/rancher-lib/README.md)，使用 `{{ include "rancher-lib.ingress.apiVersion" . }}`（库内模板已刻意保持短小）。

2. **`range` / `index`**  
   仅在确有动态列表（如多 host、按名称取端口）时使用；能用固定字段表达的就不要用 `index .Values.map $key`。

3. **新增 Chart**  
   先写出「不加模板也能看懂」的静态 YAML，再把名字、镜像、端口等替换为 `{{ .Values... }}`。

## 与本仓库脚本的关系

图标批量维护见根目录 `scripts/apply_chart_icons.py`。**若从「helm create」迁入并带 `_helpers.tpl`**，可试运行 `scripts/strip_helpers_tpl.py` 做机械内联（仍须 `helm template` 验证）。请勿为图标维护引入模板字符串拼接。
