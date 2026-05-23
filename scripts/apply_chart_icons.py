#!/usr/bin/env python3
"""统一 Chart.yaml icon：优先 Devicon 彩色矢量（*-original.svg），经 jsDelivr Git/npm CDN。"""

from __future__ import annotations

import re
from pathlib import Path

DEVICON_VER = "v2.17.0"
DEVICON_BASE = f"https://cdn.jsdelivr.net/gh/devicons/devicon@{DEVICON_VER}/icons"
# Simple Icons 仍为单色品牌矢量；仅 Devicon 未收录时使用（如 Milvus）
SI_BASE = "https://cdn.jsdelivr.net/npm/simple-icons@11/icons"

# 官方彩色 logo（仓库内静态资源），走 jsDelivr
MINIO_LOGO = "https://cdn.jsdelivr.net/gh/minio/minio@master/.github/logo.svg"
GITEA_LOGO = "https://cdn.jsdelivr.net/gh/go-gitea/gitea@main/public/assets/img/logo.svg"


def dv(icon_dir: str, filename: str | None = None) -> str:
    """Devicon 图标路径；默认使用彩色 original。"""
    if filename is None:
        filename = f"{icon_dir}-original.svg"
    return f"{DEVICON_BASE}/{icon_dir}/{filename}"


def si(slug: str) -> str:
    """Simple Icons（单色）；兜底用。"""
    return f"{SI_BASE}/{slug}.svg"


BY_PATH_SUFFIX: dict[str, str] = {
    "postgresql-new/16/Chart.yaml": dv("postgresql"),
    "rancher-lib/Chart.yaml": dv("rancher"),
    "middleware-bundle/Chart.yaml": dv("helm"),
    "elk-bundle/Chart.yaml": dv("elasticsearch"),
    "logstash-oss/Chart.yaml": dv("elasticsearch"),
    "wordpress-site/Chart.yaml": dv("wordpress"),
    "onlyoffice-docs/Chart.yaml": dv("vscode"),
    "traefik-gateway/Chart.yaml": dv("traefikproxy"),
    "openresty-web/Chart.yaml": dv("nginx"),
    "rocketmq-k8s/Chart.yaml": dv("apachekafka"),
    "kubemq-standalone/Chart.yaml": dv("kubernetes"),
    "locust-live/Chart.yaml": dv("python"),
    "k6-cronjobs/Chart.yaml": dv("k6"),
    "oracle-free-db/Chart.yaml": dv("oracle"),
    # Devicon 无 Milvus：Simple Icons 为官方单色标识
    "milvus/Chart.yaml": si("milvus"),
    "nginx-web/Chart.yaml": dv("nginx"),
    "pingora-proxy/Chart.yaml": dv("cloudflare"),
    "spring-boot-admin/Chart.yaml": dv("spring"),
    "janus-webrtc/Chart.yaml": dv("firefox"),
    "mediamtx-live/Chart.yaml": dv("firefox"),
    "srs-live/Chart.yaml": dv("firefox"),
    "ome-live/Chart.yaml": dv("premierepro"),
    "rustfs/Chart.yaml": dv("rust"),
    "openclaw-runner/Chart.yaml": dv("graphql", "graphql-plain.svg"),
    "hadoop-dev/Chart.yaml": dv("hadoop"),
    "harbor-registry/Chart.yaml": dv("harbor"),
    "dify-lite/Chart.yaml": dv("pytorch"),
    "cozeloop-platform/Chart.yaml": dv("slack"),
    "halo/Chart.yaml": dv("markdown"),
    "shopxo/Chart.yaml": dv("woocommerce"),
    "mall4j/Chart.yaml": dv("woocommerce"),
    "ruoyi-vue/Chart.yaml": dv("vuejs"),
    "gitea/Chart.yaml": GITEA_LOGO,
    "prometheus/Chart.yaml": dv("prometheus"),
    "grafana-dash/Chart.yaml": dv("grafana"),
    "frp-tunnel/Chart.yaml": dv("nginx"),
    "supabase/Chart.yaml": "https://avatars.githubusercontent.com/u/54469796?s=280&v=4",
}

BY_DIR: dict[str, str] = {
    "redis": dv("redis"),
    "redis-new": dv("redis"),
    "mysql": dv("mysql"),
    "mysql-new": dv("mysql"),
    "mongodb": dv("mongodb"),
    "kafka": dv("apachekafka"),
    "rabbitmq": dv("rabbitmq"),
    # Nacos：Devicon 无专用图标，用 Java 官方彩色标识表示 JVM 中间件生态
    "nacos": dv("java"),
    "minio-new": MINIO_LOGO,
    "elasticsearch": dv("elasticsearch"),
    "doris-new": dv("apache"),
    "nginx-ingress": dv("nginx"),
    "jenkins": dv("jenkins"),
    "snowy": dv("spring"),
    "server-new": dv("docker"),
    "server": dv("kubernetes"),
}

NESTED_SUB: dict[str, str] = {
    "charts/server-new/charts/mysql/Chart.yaml": dv("mysql"),
    "charts/server-new/charts/redis/Chart.yaml": dv("redis"),
    "charts/server-new/charts/minio/Chart.yaml": MINIO_LOGO,
    "charts/server-new/charts/doris/Chart.yaml": dv("apache"),
}

ICON_LINE = re.compile(r"^icon:\s*.*$")


def icon_insert_index(lines: list[str]) -> int:
    """在顶层 name/version（若出现在 description 之前）之后插入 icon，勿插在 description:| 字面量块内侧。"""
    desc_i = next(
        (i for i, ln in enumerate(lines) if ln.startswith("description:")),
        len(lines),
    )
    name_i = next((i for i, ln in enumerate(lines) if ln.startswith("name:")), -1)
    ver_i = next((i for i, ln in enumerate(lines) if ln.startswith("version:")), -1)
    if 0 <= ver_i < desc_i:
        return ver_i + 1
    if name_i >= 0:
        return min(name_i + 1, desc_i)
    return 0


def pick_icon(path: Path, repo_root: Path) -> str:
    rel = path.relative_to(repo_root).as_posix()
    if rel in NESTED_SUB:
        return NESTED_SUB[rel]
    for suffix, url in BY_PATH_SUFFIX.items():
        if rel.endswith(suffix):
            return url
    parts = path.parts
    idx = parts.index("charts") if "charts" in parts else -1
    if idx >= 0 and idx + 1 < len(parts):
        d = parts[idx + 1]
        if d in BY_DIR:
            return BY_DIR[d]
    return dv("helm")


def ensure_icon(text: str, icon_url: str) -> str:
    ending_newline = text.endswith("\n")
    raw = text.splitlines(keepends=False)
    stripped = [ln for ln in raw if not ICON_LINE.match(ln)]
    idx = icon_insert_index(stripped)
    stripped.insert(idx, f"icon: {icon_url}")
    body = "\n".join(stripped)
    if ending_newline:
        body += "\n"
    return body


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    for f in sorted((repo / "charts").rglob("Chart.yaml")):
        url = pick_icon(f, repo)
        old = f.read_text(encoding="utf-8")
        new = ensure_icon(old, url)
        if new != old:
            f.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
