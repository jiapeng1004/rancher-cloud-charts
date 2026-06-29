# 中间件 Compose（MVP）

约定优于配置：**单服务 compose + `include` 聚合 stack**，统一网络 **`app`**、命名数据卷、健康检查、华为云 SWR 镜像默认值。

与 Helm `middleware-bundle` 思路一致，面向 **本机 / CI 联调**，非生产高可用。

## 目录

```
middleware/
  services/          # 单中间件，可独立 up
    mysql/
    redis/
    postgresql/
    mongodb/
    elasticsearch/
    kafka/
    rabbitmq/
    minio/
  stacks/            # include 聚合
    java-core.compose.yaml
    java-messaging.compose.yaml
    java-streaming.compose.yaml
    java-search.compose.yaml
    java-full.compose.yaml      # MySQL + Redis + ES + Kafka + RabbitMQ
    polyglot-db.compose.yaml    # MySQL + PG + Mongo + Redis
    object-storage.compose.yaml
    data-platform.compose.yaml
    all-dev.compose.yaml
  .env.example
```

## 快速开始

```bash
cd docker-compose/middleware
cp .env.example .env   # 可选，改密码/端口

# 单服务
docker compose -f services/mysql/compose.yaml up -d

# Java 常用组合
docker compose -f stacks/java-core.compose.yaml up -d
docker compose -f stacks/java-full.compose.yaml up -d
```

停止并保留数据卷：

```bash
docker compose -f stacks/java-full.compose.yaml down
```

连卷一起删（慎用）：

```bash
docker compose -f stacks/java-full.compose.yaml down -v
```

## 网络 `app`

所有服务 compose 里写死：

```yaml
networks:
  middleware:
    name: app
    driver: bridge
```

**没有**单独的环境变量；全仓库 middleware 栈共用这一个 Docker 网络名。

### `app` 已存在时会怎样？

**复用，不报错**（当前写法，未设 `external: true`）：

- 不存在 → Compose **创建**名为 `app` 的 bridge 网络
- 已存在（手动 `docker network create app`，或其它 compose / stack 建的）→ Compose **直接挂上去**，跳过创建

因此 middleware 与将来接入同一 `app` 网络的其它 compose（业务应用等）可以互通，只要都声明 `name: app`。

若希望 **必须由你预先创建、Compose 绝不创建**，改为：

```yaml
networks:
  middleware:
    name: app
    external: true
```

此时 `app` 不存在会 **启动失败**；存在则只复用。

## 默认连接（容器内用 **服务名**，均在 `app` 网络）

| 组件 | 地址 | 默认账号 |
|------|------|----------|
| MySQL | `mysql:3306` | root / 123456，库 `app` |
| Redis | `redis:6379` | 无密码 |
| PostgreSQL | `postgresql:5432` | postgres / 123456，库 `app` |
| MongoDB | `mongodb:27017` | root / 123456 |
| Elasticsearch | `http://elasticsearch:9200` | 无认证（dev） |
| Kafka | `kafka:9092` | Apache **kafka-native**（KRaft，PLAINTEXT） |
| RabbitMQ | `rabbitmq:5672`，控制台 `:15672` | admin / 123456 |
| MinIO | API `:9000`，控制台 `:9001` | minioadmin / minioadmin |

宿主机访问用 `127.0.0.1` + 映射端口（见 `.env.example`）。

Kafka 容器内 bootstrap 用 `kafka:9092`；若 Java 跑在宿主机且 metadata 异常，可在 `.env` 设 `KAFKA_ADVERTISED_HOST=127.0.0.1` 后重启。

## Stack 选型

| Stack | 包含 |
|-------|------|
| `java-core` | MySQL + Redis |
| `java-messaging` | + RabbitMQ |
| `java-streaming` | + Kafka |
| `java-search` | + Elasticsearch |
| `java-full` | MySQL + Redis + ES + Kafka + RabbitMQ |
| `polyglot-db` | MySQL + PostgreSQL + MongoDB + Redis |
| `object-storage` | MinIO + Redis |
| `data-platform` | MySQL + Redis + ES + Kafka + MinIO |
| `all-dev` | 上述全部 8 种 |

## 说明

- 需要 **Docker Compose v2.20+**（支持 `include`）。
- 各 stack 使用固定 `container_name`（如 `mw-mysql`），**同一时刻只能跑一套**；换 stack 前先 `down`。
- 数据卷名 `mw-*-data` 跨 stack 复用，换 stack 不会丢库。
- 默认密码仅供开发；生产请改 `.env` 且勿提交 Git。
