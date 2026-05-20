Pingora（Cloudflare 开源代理框架）**通常需要自建 Worker 镜像**；此 Chart 仅提供可调命令/端口的占位 Deployment，可与 **nginx-web** / **openresty-web** 相同方式覆盖镜像与启动参数。
默认镜像仍使用 nginx 占位，请将 `values.yaml` 中 `image`、`command`、`args` 替换为你的 Pingora 运行时。

参考：[Pingora GitHub](https://github.com/cloudflare/pingora)
