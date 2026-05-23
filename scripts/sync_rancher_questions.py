#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补齐 Rancher Charts 可用的 questions.yaml：
- 跳过 type:library
- 若已有非空 questions.yaml 则不覆盖（人工维护为准）
- 若仅有 questions.yml 则复制为 questions.yaml（Rancher 原生读 *.yaml）

用法（仓库根目录）:
  py -3 scripts/sync_rancher_questions.py
"""

from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHARTS = ROOT / "charts"

# 若 questions.yaml 内容过短视为占位文件，可被覆盖为非空自动生成内容
_nonempty_threshold = 40


def _rd(p: Path) -> dict | None:
    if not p.is_file():
        return None
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        return None


def _dump(doc: dict) -> str:
    return yaml.safe_dump(
        doc,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )


def _bq(
    variable: str,
    typ: str,
    *,
    label: str,
    description: str,
    group: str,
    default=None,
    required: bool | None = None,
    options: list[str] | None = None,
    show_if: str | None = None,
):
    row: dict = {
        "variable": variable,
        "type": typ,
        "label": label,
        "description": description,
        "group": group,
    }
    if default is not None:
        row["default"] = default
    if required is not None:
        row["required"] = required
    if options:
        row["options"] = options
    if show_if:
        row["show_if"] = show_if
    return row


def _pull_policy_enum(default: str):
    opts = ["IfNotPresent", "Always", "Never"]
    if default not in opts:
        default = "IfNotPresent"
    return default, opts


def _svc_type_enum(vals: dict):
    svc = vals.get("service") or {}
    raw = svc.get("type") or svc.get("Type") or "ClusterIP"
    d = raw if isinstance(raw, str) else "ClusterIP"
    opts = ["ClusterIP", "NodePort", "LoadBalancer"]
    if d not in opts:
        d = "ClusterIP"
    return svc, d, opts


def _image_block(vals: dict, group="镜像"):
    im = vals.get("image") or {}
    qs: list = []
    if "repository" in im:
        qs.append(
            _bq(
                "image.repository",
                "string",
                label="镜像仓库",
                description="容器镜像仓库地址",
                group=group,
                default=str(im["repository"]),
                required=True,
            )
        )
    if "tag" in im:
        qs.append(
            _bq(
                "image.tag",
                "string",
                label="镜像标签",
                description="镜像 tag",
                group=group,
                default=str(im["tag"]),
                required=True,
            )
        )
    if "pullPolicy" in im:
        dflt, opts = _pull_policy_enum(str(im.get("pullPolicy") or "IfNotPresent"))
        qs.append(
            _bq(
                "image.pullPolicy",
                "enum",
                label="镜像拉取策略",
                description="Kubernetes imagePullPolicy",
                group=group,
                default=dflt,
                options=opts,
                required=True,
            )
        )
    return qs


def _ingress_questions(vals: dict):
    ig = vals.get("ingress") or {}
    if not isinstance(ig, dict):
        return []
    qs: list = []
    if "enabled" in ig:
        qs.append(
            _bq(
                "ingress.enabled",
                "boolean",
                label="启用 Ingress",
                description="若为 true，将渲染 Ingress（具体 hosts/tls 可在 YAML 中编辑）",
                group="Ingress",
                default=bool(ig.get("enabled", False)),
                required=False,
            )
        )
    if "className" in ig:
        extra = dict(
            variable="ingress.className",
            type="string",
            label="IngressClass 名称",
            description="Ingress 使用的 ingressClassName",
            group="Ingress",
            default=str(ig.get("className") or ""),
            required=False,
        )
        if "enabled" in ig:
            extra["show_if"] = "ingress.enabled=true"
        qs.append(extra)
    return qs


def _persistence(vals: dict):
    pv = vals.get("persistence") or {}
    if not isinstance(pv, dict) or not pv:
        return []
    qs: list = []
    if "enabled" in pv:
        qs.append(
            _bq(
                "persistence.enabled",
                "boolean",
                label="启用持久卷",
                group="持久化",
                default=bool(pv.get("enabled", True)),
                required=False,
                description="若为 true，使用 PVC 持久化数据",
            )
        )
    if "size" in pv:
        qs.append(
            _bq(
                "persistence.size",
                "string",
                label="PVC 容量",
                group="持久化",
                default=str(pv.get("size") or "10Gi"),
                required=False,
                show_if="persistence.enabled=true",
                description="Kubernetes 请求的存储大小（如 10Gi）",
            )
        )
    return qs


def _service_common(vals: dict):
    svc, d_svc, svc_opts = _svc_type_enum(vals)
    qs: list = []
    if "type" in svc:
        qs.append(
            _bq(
                "service.type",
                "enum",
                label="Service 类型",
                group="服务",
                default=d_svc,
                options=svc_opts,
                required=True,
                description="Kubernetes Service.type",
            )
        )
    for key in ("port", "webPort", "httpPort", "httpsPort"):
        if key in svc:
            qs.append(
                _bq(
                    f"service.{key}",
                    "int",
                    label=f"Service 端口 ({key})",
                    group="服务",
                    default=int(svc[key]) if isinstance(svc[key], (int, float)) else int(str(svc[key])),
                    required=True,
                    description=f"读写 service.{key}",
                )
            )
    return qs


def _generic_document(name: str, values: dict) -> dict:
    """从常见 values 片段生成兜底 questions（不写业务深度字段）"""
    qs: list = []
    if "enabled" in values:
        qs.append(
            _bq(
                "enabled",
                "boolean",
                label="启用本 Chart",
                group="通用",
                default=bool(values["enabled"]),
                required=True,
                description="若为 false，通常不会在集群中创建工作负载（视模板而定）",
            )
        )
    if isinstance(values.get("replicaCount"), (int, float)):
        qs.append(
            _bq(
                "replicaCount",
                "int",
                label="副本数",
                group="通用",
                default=int(values["replicaCount"]),
                required=True,
                description="Deployment 副本数量",
            )
        )

    qs.extend(_image_block(values))
    qs.extend(_service_common(values))
    qs.extend([q for q in _ingress_questions(values) if q])
    qs.extend(_persistence(values))

    pg = values.get("postgresql") or {}
    if isinstance(pg, dict) and any(k in pg for k in ("user", "password", "database", "postgresPassword")):
        qs.append(
            _bq(
                "postgresql.user",
                "string",
                label="PostgreSQL 用户名（POSTGRES_USER）",
                group="PostgreSQL",
                default=str(pg.get("user", "postgres")),
                required=True,
                description="数据库初始化用户名",
            )
        )
        if "password" in pg:
            qs.append(
                _bq(
                    "postgresql.password",
                    "password",
                    label="PostgreSQL 密码（POSTGRES_PASSWORD）",
                    group="PostgreSQL",
                    default=str(pg.get("password", "")),
                    required=True,
                    description="与 POSTGRES_PASSWORD 对应的密码",
                )
            )
        if "postgresPassword" in pg:
            qs.append(
                _bq(
                    "postgresql.postgresPassword",
                    "password",
                    label="超级用户 postgres 密码（可选，POSTGRESQL_POSTGRES_PASSWORD）",
                    group="PostgreSQL",
                    default=str(pg.get("postgresPassword", "") or ""),
                    required=False,
                    description="留空常继承 password；适配 Bitnami 变量名",
                )
            )
        if "database" in pg:
            qs.append(
                _bq(
                    "postgresql.database",
                    "string",
                    label="PostgreSQL 默认库名（POSTGRES_DB）",
                    group="PostgreSQL",
                    default=str(pg.get("database", "postgres")),
                    required=True,
                    description="初始化数据库名称",
                )
            )

    wp = values.get("wordpress")
    if isinstance(wp, dict):
        db = wp.get("db")
        if isinstance(db, dict):
            if "host" in db:
                qs.append(
                    _bq(
                        "wordpress.db.host",
                        "string",
                        label="WordPress DB 主机",
                        group="WordPress（数据库连接）",
                        default=str(db.get("host") or ""),
                        required=True,
                        description="MySQL/PG Hostname 或集群内 DNS",
                    )
                )
            if "name" in db:
                qs.append(
                    _bq(
                        "wordpress.db.name",
                        "string",
                        label="WordPress DB 名称",
                        group="WordPress（数据库连接）",
                        default=str(db.get("name") or "wordpress"),
                        required=True,
                        description="数据库名",
                    )
                )
            if "user" in db:
                qs.append(
                    _bq(
                        "wordpress.db.user",
                        "string",
                        label="WordPress DB 用户名",
                        group="WordPress（数据库连接）",
                        default=str(db.get("user") or ""),
                        required=True,
                        description="数据库用户",
                    )
                )
            if "password" in db:
                qs.append(
                    _bq(
                        "wordpress.db.password",
                        "password",
                        label="WordPress DB 密码",
                        group="WordPress（数据库连接）",
                        default=str(db.get("password") or ""),
                        required=True,
                        description="数据库密码（安装后请及时修改）",
                    )
                )

    if not qs:
        qs.append(
            _bq(
                "rancherUiNote",
                "string",
                label="表单说明（本 Chart 可选 values 很少）",
                group="文档",
                default="请在 Rancher 「编辑 Helm」中用 YAML 直接调整；或通过独立 values.yaml 传入。",
                required=False,
                description="自动生成占位表单项；可随时编辑或忽略。",
            )
        )

    return {"categories": [name.replace("-", " ")], "questions": qs}


def _middleware_bundle_preset() -> dict:
    # 与 umbrella values.yaml 对齐
    return {
        "categories": ["middleware", "umbrella"],
        "questions": [
            _bq(
                "mysql.enabled",
                "boolean",
                label="启用 MySQL",
                description="若为 true，安装嵌入式 MySQL 子 chart（另有独立表单）",
                group="组件开关",
                default=True,
                required=True,
            ),
            _bq(
                "mysql.image.repository",
                "string",
                label="MySQL 镜像仓库（覆盖前缀）",
                description="可按镜像加速前缀调整嵌入式 MySQL 拉取仓库",
                group="组件镜像前缀",
                default="swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/mysql",
                required=False,
                show_if="mysql.enabled=true",
            ),
            _bq(
                "redis.enabled",
                "boolean",
                label="启用 Redis",
                group="组件开关",
                default=True,
                required=True,
                description="若为 true，安装嵌入式 Redis 子 chart",
            ),
            _bq(
                "redis.image.repository",
                "string",
                label="Redis 镜像仓库（覆盖前缀）",
                description="可按镜像加速前缀调整嵌入式 Redis 拉取仓库",
                group="组件镜像前缀",
                default="swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis",
                required=False,
                show_if="redis.enabled=true",
            ),
            _bq(
                "postgresql.enabled",
                "boolean",
                label="启用 PostgreSQL",
                group="组件开关",
                default=True,
                required=True,
                description="若为 true，安装嵌入式 PostgreSQL 子 chart（另有独立表单）",
            ),
            _bq(
                "postgresql.image.repository",
                "string",
                label="PostgreSQL 镜像仓库（覆盖前缀）",
                description="可按镜像加速前缀调整嵌入式 PostgreSQL 拉取仓库",
                group="组件镜像前缀",
                default="swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/postgres",
                required=False,
                show_if="postgresql.enabled=true",
            ),
            _bq(
                "minio.enabled",
                "boolean",
                label="启用 MinIO",
                group="组件开关",
                default=False,
                required=True,
                description="若为 true，安装嵌入式 MinIO 子 chart",
            ),
            _bq(
                "minio.image.repository",
                "string",
                label="MinIO 镜像仓库（覆盖前缀）",
                description="可按镜像加速前缀调整嵌入式 MinIO 拉取仓库",
                group="组件镜像前缀",
                default="swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/minio/minio",
                required=False,
                show_if="minio.enabled=true",
            ),
        ],
    }


def _elk_bundle_preset() -> dict:
    return {
        "categories": ["elk-bundle", "elasticsearch", "logging"],
        "questions": [
            _bq(
                "elasticsearch.enabled",
                "boolean",
                label="启用 Elasticsearch",
                group="Elasticsearch",
                default=True,
                required=True,
                description="若为 true，安装嵌入式 Elasticsearch（见子 chart Elasticsearch 表单）",
            ),
            _bq(
                "elasticsearch.createIngress",
                "boolean",
                label="为 Elasticsearch 创建 Ingress",
                group="Elasticsearch",
                default=False,
                required=False,
                show_if="elasticsearch.enabled=true",
                description="子 chart elasticsearch 的值透传前缀 elasticsearch.*",
            ),
            _bq(
                "elasticsearch.installKibana",
                "boolean",
                label="同时安装 Kibana（子 chart）",
                group="Elasticsearch",
                default=True,
                required=False,
                show_if="elasticsearch.enabled=true",
                description="与 elk-bundle/README 对齐；详情请查子 chart README",
            ),
            _bq(
                "logstash-oss.enabled",
                "boolean",
                label="启用 Logstash OSS",
                group="Logstash",
                default=True,
                required=True,
                description="安装嵌入式 Logstash OSS 子 chart",
            ),
        ],
    }


def _redis_legacy(values: dict) -> dict:
    return {
        "categories": ["redis"],
        "questions": [
            _bq(
                "port",
                "int",
                label="hostPort（与模板一致）",
                group="网络",
                default=int(values.get("port") or 6379),
                required=True,
                description="本 chart 在 Deployment 中使用 hostPort=Values.port；注意安全风险",
            )
        ],
    }


def _server_umbrella(values: dict) -> dict:
    return {
        "categories": ["server"],
        "questions": [
            _bq(
                "redis.port",
                "int",
                label="Redis 端口",
                group="Redis（父级透传）",
                default=int(str(values.get("redis", {}).get("port") or 6379)),
                required=True,
                description="与 server/values.yaml 中 redis.port 对齐",
            ),
            _bq(
                "redis.enable",
                "boolean",
                label="启用 Redis 子 Chart（沿用 values 字段名 enable）",
                group="Redis（父级透传）",
                default=bool(values.get("redis", {}).get("enable", True)),
                required=True,
                description="Chart 依赖条件使用 redis.enabled；若与模板不一致请以 YAML 为准",
            ),
            _bq(
                "mysql.port",
                "int",
                label="MySQL 端口",
                group="MySQL（父级透传）",
                default=int(str(values.get("mysql", {}).get("port") or 3306)),
                required=True,
                description="与 server/values.yaml 中 mysql.port 对齐",
            ),
            _bq(
                "mysql.enable",
                "boolean",
                label="启用 MySQL 子 Chart（沿用 values 字段名 enable）",
                group="MySQL（父级透传）",
                default=bool(values.get("mysql", {}).get("enable", True)),
                required=True,
                description="Chart 依赖条件使用 mysql.enabled",
            ),
            _bq(
                "mysql.password",
                "password",
                label="MySQL root 密码",
                group="MySQL（父级透传）",
                default=str(values.get("mysql", {}).get("password") or ""),
                required=True,
                description="透传给子 mysql chart",
            ),
            _bq(
                "mysql.dataPath",
                "string",
                label="MySQL 数据路径",
                group="MySQL（父级透传）",
                default=str(values.get("mysql", {}).get("dataPath") or "/var/lib/mysql"),
                required=False,
                description="数据目录（若有）",
            ),
        ],
    }


def _preset_document(rel_posix: str, name: str, values: dict) -> dict | None:
    if rel_posix == "middleware-bundle":
        return _middleware_bundle_preset()
    if rel_posix == "elk-bundle":
        return _elk_bundle_preset()
    if rel_posix == "redis" or rel_posix.endswith("/redis"):
        if not (values or {}).get("image"):
            return _redis_legacy(values or {})
    if rel_posix == "server":
        return _server_umbrella(values)
    return None


def nonempty_quest_yaml(path: Path) -> bool:
    if not path.is_file():
        return False
    return len(path.read_text(encoding="utf-8").strip()) >= _nonempty_threshold


def maybe_copy_legacy_yml(chart_dir: Path) -> None:
    yml = chart_dir / "questions.yml"
    yml_yaml = chart_dir / "questions.yaml"
    if yml.exists() and (not yml_yaml.exists() or not nonempty_quest_yaml(yml_yaml)):
        yml_yaml.write_text(yml.read_text(encoding="utf-8"), encoding="utf-8")


def sync_one(chart_yaml: Path) -> str | None:
    chart_dir = chart_yaml.parent
    rel_posix = chart_dir.relative_to(CHARTS).as_posix()
    meta = _rd(chart_yaml) or {}
    if (meta.get("type") or "application").strip() == "library":
        return None

    qpath = chart_dir / "questions.yaml"

    maybe_copy_legacy_yml(chart_dir)

    if nonempty_quest_yaml(qpath):
        return None

    values = _rd(chart_dir / "values.yaml") or {}

    preset = _preset_document(rel_posix, meta.get("name", chart_dir.name), values)

    chart_name = str(meta.get("name") or chart_dir.name)

    doc = preset or _generic_document(chart_name, values)

    qpath.parent.mkdir(parents=True, exist_ok=True)
    txt = _dump(doc)
    header = (
        "## 自动生成 / 或由 sync_rancher_questions.py 维护；"
        "与 values.yaml 常见字段对齐。高级项请直接在 Rancher 「编辑 YAML」中补充。\n"
    )
    qpath.write_text(header + txt, encoding="utf-8")
    return rel_posix


def main():
    touched: list[str] = []
    for chart_yaml in sorted(CHARTS.rglob("Chart.yaml")):
        r = sync_one(chart_yaml)
        if r:
            touched.append(r)

    print(f"sync_rancher_questions: wrote/updated {len(touched)} questions.yaml")
    for line in touched:
        print(f"  - {line}")


if __name__ == "__main__":
    main()
