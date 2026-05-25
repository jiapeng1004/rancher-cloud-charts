# OpenClaw（Docker Compose）

约定优于配置：只暴露 **端口**、**网关密码**、**DeepSeek API Key**，其余走 `openclaw.json` 默认。

## 快速启动

```bash
cd docker-compose/openclaw
cp env.example .env          # 按需改端口
cp env.example agent.env     # 填写 OPENCLAW_GATEWAY_PASSWORD、DEEPSEEK_API_KEY
docker compose up -d
```

控制台：<http://127.0.0.1:18789/>，使用 `agent.env` 里的 `OPENCLAW_GATEWAY_PASSWORD` 登录。

健康检查：`curl -fsS http://127.0.0.1:18789/healthz`

## 说明

- 镜像：`ghcr.io/openclaw/openclaw:latest`
- 状态目录：`./_data`（持久化，已 gitignore）
- 默认模型：`deepseek/deepseek-chat`
- Telegram 等通道默认关闭，需要时在 `openclaw.json` 中启用并配置 token
