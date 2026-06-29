# Docker Compose 本地栈

| 目录 | 说明 |
|------|------|
| [**middleware/**](./middleware/) | 常用中间件 MVP + `include` 聚合（Java / 多库 / 数据平台） |
| [kong/](./kong/) | Kong + PostgreSQL + Konga |
| [snowy/](./snowy/) | Snowy Cloud 全家桶 |
| [openclaw/](./openclaw/) | OpenClaw Gateway + DeepSeek |

中间件聚合示例：

```bash
cd middleware
docker compose -f stacks/java-full.compose.yaml up -d
```

需 **Docker Compose v2.20+**（`include`）。
