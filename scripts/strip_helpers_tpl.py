#!/usr/bin/env python3
"""
将各 Chart 对 templates/_helpers.tpl 的依赖内联到同目录 *.yaml，
然后删除 _helpers.tpl。约定：仅用 $name / $fullname / $chartLabel 等与 dict|toYaml|nindent，
避免跨文件 define。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHARTS = REPO_ROOT / "charts"


def discover_prefix(text: str) -> str:
    m = re.search(r"define\s+\"([^\"]+)\.name\"", text)
    if not m:
        raise ValueError("no *.name define in _helpers.tpl")
    return m.group(1)


def classify_kind(text: str) -> str:
    if "doris.fe.fullname" in text:
        return "doris"
    if "locust-live.masterHostname" in text or "selectorMaster" in text:
        return "locust"
    if re.search(r'define\s+"[^\"]+\.serviceAccountName"', text):
        return "full"
    m = re.search(r'define\s+"([^\"]+)\.labels"', text)
    if m:
        start = text.find(m.group(0))
        chunk = text[start : start + 800]
        if "helm.sh/chart" in chunk:
            return "full"
        return "slim"
    return "minimal"


def build_header(kind: str) -> str:
    lines = [
        '{{- $name := default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}',
        "{{- $fullname := .Values.fullnameOverride | default (printf \"%s-%s\" .Release.Name $name) | trunc 63 | trimSuffix \"-\" }}",
    ]
    if kind in ("full", "doris"):
        lines.append(
            '{{- $chartLabel := printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}'
        )
    if kind == "doris":
        lines.append('{{- $feFullname := printf "%s-fe" $fullname | trunc 63 | trimSuffix "-" }}')
        lines.append('{{- $beFullname := printf "%s-be" $fullname | trunc 63 | trimSuffix "-" }}')
    if kind == "locust":
        lines.append('{{- $masterHostname := printf "%s-master" $fullname | trunc 63 | trimSuffix "-" }}')
    return "\n".join(lines) + "\n"


def already_has_header(content: str) -> bool:
    return "{{- $fullname :=" in content or "{{ $fullname :=" in content


def prepend_header(content: str, header: str) -> str:
    if already_has_header(content):
        return content
    return header + content.lstrip("\ufeff")


def expand_full_labels(n: str) -> str:
    return (
        '{{- $baseLbl := dict "helm.sh/chart" $chartLabel "app.kubernetes.io/name" $name '
        '"app.kubernetes.io/instance" .Release.Name "app.kubernetes.io/managed-by" .Release.Service }}'
        "{{- if .Chart.AppVersion }}"
        "{{ mustMergeOverwrite $baseLbl (dict \"app.kubernetes.io/version\" .Chart.AppVersion) "
        "| toYaml | nindent "
        + n
        + " }}"
        "{{- else }}"
        "{{ $baseLbl | toYaml | nindent "
        + n
        + " }}"
        "{{- end }}"
    )


def expand_slim_labels(n: str) -> str:
    return (
        '{{- dict "app.kubernetes.io/name" $name "app.kubernetes.io/instance" .Release.Name | toYaml | nindent '
        + n
        + " }}"
    )


def expand_selector(n: str) -> str:
    return (
        '{{- dict "app.kubernetes.io/name" $name "app.kubernetes.io/instance" .Release.Name | toYaml | nindent '
        + n
        + " }}"
    )


def expand_svc_account() -> str:
    return "{{ if .Values.serviceAccount.create }}{{ default $fullname .Values.serviceAccount.name }}{{ else }}{{ default \"default\" .Values.serviceAccount.name }}{{ end }}"


def replace_includes(body: str, prefix: str, kind: str) -> str:
    pe = re.escape(prefix)

    body = re.sub(
        rf"\{{\{{\s*-?\s*\$fullName\s*:=\s*include\s+\"{pe}\.fullname\"\s+\.\s*-?\s*\}}\}}\s*\n?",
        "",
        body,
    )
    body = re.sub(rf'\{{\{{\s*-?\s*include\s+"{pe}\.fullname"\s+\.\s*-?\s*\}}\}}', "{{ $fullname }}", body)

    # printf(..., include "PREFIX.fullname" .) の括弧を $fullname に置換
    body = re.sub(rf"\(\s*include\s+\"{pe}\.fullname\"\s+\.\s*\)", "$fullname", body)

    body = re.sub(
        rf'\{{\{{\s*-?\s*include\s+"{pe}\.serviceAccountName"\s+\.\s*-?\s*\}}\}}',
        expand_svc_account(),
        body,
    )

    body = re.sub(rf'\{{\{{\s*-?\s*include\s+"{pe}\.selectorLabels"\s+\.\s*\|\s*nindent\s+(\d+)\s*\}}\}}',
                  lambda m: expand_selector(m.group(1)), body)

    body = re.sub(rf'\{{\{{\s*-?\s*include\s+"{pe}\.name"\s+\.\s*-?\s*\}}\}}', "{{ $name }}", body)

    if kind == "doris":
        body = re.sub(
            rf'\{{\{{\s*-?\s*include\s+"{pe}\.fe\.fullname"\s+\.\s*-?\s*\}}\}}', "{{ $feFullname }}", body
        )
        body = re.sub(
            rf'\{{\{{\s*-?\s*include\s+"{pe}\.be\.fullname"\s+\.\s*-?\s*\}}\}}', "{{ $beFullname }}", body
        )
        body = re.sub(
            rf'\{{\{{\s*-?\s*include\s+"{pe}\.fe\.selectorLabels"\s+\.\s*\|\s*nindent\s+(\d+)\s*\}}\}}',
            lambda m: (
                '{{- dict "app.kubernetes.io/name" $name "app.kubernetes.io/instance" .Release.Name '
                '"component" "fe" | toYaml | nindent '
                + m.group(1)
                + " }}"
            ),
            body,
        )
        body = re.sub(
            rf'\{{\{{\s*-?\s*include\s+"{pe}\.be\.selectorLabels"\s+\.\s*\|\s*nindent\s+(\d+)\s*\}}\}}',
            lambda m: (
                '{{- dict "app.kubernetes.io/name" $name "app.kubernetes.io/instance" .Release.Name '
                '"component" "be" | toYaml | nindent '
                + m.group(1)
                + " }}"
            ),
            body,
        )

    if kind == "locust":
        body = re.sub(
            rf"\{{\{{\s*-?\s*\$(\w+)\s*:=\s*include\s+\"{pe}\.masterHostname\"\s+\.\s*-?\s*\}}\}}\s*",
            lambda m: "{{- $" + m.group(1) + " := $masterHostname }}",
            body,
        )
        body = re.sub(rf'\{{\{{\s*-?\s*include\s+"{pe}\.masterHostname"\s+\.\s*-?\s*\}}\}}',
                      "{{ $masterHostname }}", body)
        body = re.sub(rf'\{{\{{\s*-?\s*include\s+"{pe}\.fullname"\s+\.\s*-?\s*\}}\}}',
                      "{{ $fullname }}", body)

        body = re.sub(
            rf'\{{\{{\s*printf\s+"%s-worker"\s*\(\s*include\s+"{pe}\.fullname"\s+\.\s*\)\s*\}}\}}',
            "{{ printf \"%s-worker\" $fullname }}",
            body,
        )
        body = re.sub(
            rf'\{{\{{\s*printf\s+"%s\.%s\.svc\.cluster\.local"\s*\(\s*include\s+"{pe}\.masterHostname"\s+\.\s*\)\s*\.Release\.Namespace\s*\|\s*quote\s*\}}\}}',
            "{{ printf \"%s.%s.svc.cluster.local\" $masterHostname .Release.Namespace | quote }}",
            body,
        )

        body = re.sub(
            rf'\{{\{{\s*-?\s*include\s+"{pe}\.selectorMaster"\s+\.\s*\|\s*nindent\s+(\d+)\s*\}}\}}',
            lambda m: (
                '{{- dict "app.kubernetes.io/name" $name "app.kubernetes.io/instance" .Release.Name '
                '"app.kubernetes.io/component" "master" | toYaml | nindent '
                + m.group(1)
                + " }}"
            ),
            body,
        )
        body = re.sub(
            rf'\{{\{{\s*-?\s*include\s+"{pe}\.selectorWorker"\s+\.\s*\|\s*nindent\s+(\d+)\s*\}}\}}',
            lambda m: (
                '{{- dict "app.kubernetes.io/name" $name "app.kubernetes.io/instance" .Release.Name '
                '"app.kubernetes.io/component" "worker" | toYaml | nindent '
                + m.group(1)
                + " }}"
            ),
            body,
        )
        body = re.sub(labels_sub, lambda m: expand_slim_labels(m.group(1)), body)

    labels_sub = rf'\{{\{{\s*-?\s*include\s+"{pe}\.labels"\s+\.\s*\|\s*nindent\s+(\d+)\s*\}}\}}'

    if kind == "full":
        body = re.sub(labels_sub, lambda m: expand_full_labels(m.group(1)), body)
    elif kind == "slim":
        body = re.sub(labels_sub, lambda m: expand_slim_labels(m.group(1)), body)

    leftover = list(re.finditer(rf'include\s+"{pe}[^\"\s]*"', body))
    if leftover and kind not in ("doris", "locust"):
        snippet = leftover[0].group(0)
        raise RuntimeError(f"unhandled include remaining: {snippet}")

    leftover_doris = list(re.finditer(rf'include\s+"{pe}\.', body)) if kind == "doris" else []
    if leftover_doris:
        raise RuntimeError(f"unhandled doris include: {leftover_doris[0].group(0)}")

    return body


def process_helpers_file(helpers: Path) -> None:
    templates_dir = helpers.parent
    text = helpers.read_text(encoding="utf-8")
    prefix = discover_prefix(text)
    kind = classify_kind(text)
    header = build_header(kind)

    for ypath in sorted(templates_dir.rglob("*.yaml")):
        raw = ypath.read_text(encoding="utf-8")
        if not raw.strip():
            continue
        new = replace_includes(raw, prefix, kind)
        new = prepend_header(new, header)
        if new != raw:
            ypath.write_text(new, encoding="utf-8")

    helpers.unlink()


def main() -> int:
    paths = sorted(CHARTS.rglob("_helpers.tpl"))
    if not paths:
        print("no _helpers.tpl under charts/", file=sys.stderr)
        return 1
    for p in paths:
        process_helpers_file(p)
        print("stripped", p.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
