## frp-tunnel — 首开 / Demo 向内穿 HTTP · TCP（FRP）

基于 [FRP（fatedier/frp）](https://github.com/fatedier/frp)。本 Chart 在同一 Release 可选部署：

| 组件 | 角色 | 说明 |
|------|------|------|
| **frps** | 中继端 | `bindPort` 收 frpc、`vhostHTTPPort`（可选）收 HTTP Host；自带可选 Web Dashboard |
| **frpc** | 出站端 | 连到现有 frps（可在集群内外），把 **TCP / HTTP** 代理到集群内 `Service`/`Pod` |

默认值：镜像走华为云 SWR → `docker.io/fatedier/frp`。

### 快速安装（仅集群内 frps）

```bash
helm upgrade --install myfrp charts/frp-tunnel -n ingress-basic --create-namespace
```

首开若需集群外打进 frps，将 `values.yaml` 中 `frps.service.type` 设为 `LoadBalancer` 或 `NodePort`，并按需填 `peer.nodePort`。

### Dashboard + Ingress（可选）

`frps.ingress.enabled: true`，并填入 `hosts`；对外仍须保证 frps-bind 端口从客户端可达。

### 开启 HTTP（经 FRP vhost）

1. `frps.vhostHTTPPort` 设为如 `8080`（并保持与 Service 端口一致）。
2. 在同一 release 启用 `frpc`，`serverAddr` 指向可达的 **frps 监听地址**，并配置：

```yaml
frps:
  authToken: "changeme-shared"
  vhostHTTPPort: 8080

frpc:
  enabled: true
  serverAddr: <frps-ip-or-dns>
  serverPort: 7000
  auth:
    token: "changeme-shared"
  httpProxies:
    - name: demo-web
      localIP: my-nginx.my-ns.svc.cluster.local
      localPort: 80
      customDomains:
        - demo.example.local
```

客户端需在 DNS/hosts 将 `demo.example.local` 解析到可达 frps HTTP 监听（NodePort/LB）。

### TCP 映射

```yaml
frpc:
  tcpProxies:
    - name: redis-hit
      localIP: redis-master.redis.svc.cluster.local
      localPort: 6379
      remotePort: 36379   # frps 侧对外端口示意
```

**安全：** 请务必修改 Dashboard 口令与 token，限制安全组与白名单。
