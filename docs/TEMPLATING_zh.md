# Helm 模板编写约定（尽量少用「模板魔法」）

本仓库 Chart 面向运维可读、易改。**默认写法是普通 YAML + 最少的 Helm 插值**，不要为了抽象而抽象。

## 避免的写法

1. **不要使用 `tpl` / `mustTpl`**  
   把整段 YAML 做成字符串再二次渲染，报错信息难定位，也难做静态检查。若有动态片段，优先拆成多个小的显式字段或单独的模板文件。

2. **`templates/_helpers.tpl` 已不再使用**  
   命名与常用标签已**内联在各 `templates/*.yaml` 文件顶部**（`$name`、`$fullname`，以及少数 Chart 的 `$chartLabel`、`$masterHostname`、`$feFullname` 等），不在单独 `_helpers.tpl` 里维护 `define` / `include`。若你用 `helm create` 生成带 `_helpers.tpl` 的 chart，可参考本仓库写法删掉该文件并把变量段落拷到每个业务模板顶端；或对接到维护脚本 [`scripts/strip_helpers_tpl.py`](../scripts/strip_helpers_tpl.py)（会按惯例替换常见 `include` 并移除 `_helpers.tpl`，改完务必本地 `helm template` 自检）。

3. **不要用 `.tpl` 后缀**，也**不要为了复用 Ingress 而再建单独的「不占业务资源」YAML**（例如单独的 library chart、或 `templates/` 里只有 `define` 且无具体 Kind 的文件）：**兼容性分支写在当前这份 Ingress 模板顶部**——与 `postgresql-new`、`nginx-web` 等一致。「不要用 `tpl` / `mustTpl`」（Sprig）与「文件名不用 `.tpl`」是两件事。

4. **避免大面积嵌套**，以及多套 `define`/`include` 串起来拼清单  
   条件多时优先考虑：拆资源文件、或用 values 开关。

## 推荐写法

1. **Ingress**：在每个 **`ingress.yaml` 开头**写好 **`$kv := default .Capabilities.KubeVersion.Version .Capabilities.KubeVersion.GitVersion`**，紧跟 **`semverCompare`** 选对 **`networking.k8s.io/v1` / `v1beta1` / `extensions/v1beta1`**，与同路径 **`pathType` / backend** 结构一起放在同一文件里。

2. **seccompProfile**（仅此字段常踩旧集群）：**&lt;1.22 不要写入**——在写 `securityContext` 的那段里 **`if semverCompare ">=1.22.0-0"` 包住**，或对 values **`omit ... "seccompProfile"`**。可照 **`charts/nginx-ingress`** / **`charts/supabase/charts/postgresql`** deployment。

3. **`range` / `index`**：确有动态列表再用。

4. **新增 Chart**：先写能看懂的静态 YAML，再改成 `Values` 插值。

## 与本仓库脚本的关系

图标批量维护见根目录 `scripts/apply_chart_icons.py`。**若从「helm create」迁入并带 `_helpers.tpl`**，可试运行 `scripts/strip_helpers_tpl.py` 做机械内联（仍须 `helm template` 验证）。请勿为图标维护引入模板字符串拼接。
