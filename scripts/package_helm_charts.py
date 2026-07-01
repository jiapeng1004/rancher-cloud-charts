#!/usr/bin/env python3
"""Pack publishable charts under charts/ — 备用脚本，CI / make 不使用；日常请 make helm-package。"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalize_index_utf8 import normalize_index_utf8  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
CHARTS_ROOT = REPO_ROOT / "charts"
DEFAULT_REPO_URL = "https://jiapeng1004.github.io/rancher-cloud-charts"
DEFAULT_OUTPUT = REPO_ROOT / ".helm-packages"


def discover_publishable_charts() -> list[Path]:
    """Return chart directories to publish (exclude embedded dependency subcharts)."""
    found: list[Path] = []
    for chart_yaml in sorted(CHARTS_ROOT.rglob("Chart.yaml")):
        chart_dir = chart_yaml.parent
        rel = chart_dir.relative_to(CHARTS_ROOT)
        # e.g. middleware-bundle/charts/mysql — skip nested dependency charts
        if len(rel.parts) > 1 and "charts" in rel.parts[1:]:
            continue
        found.append(chart_dir)
    return found


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd or REPO_ROOT, check=True)


def package_chart(chart_dir: Path, output_dir: Path) -> Path | None:
    rel = chart_dir.relative_to(REPO_ROOT)
    chart_yaml = (chart_dir / "Chart.yaml").read_text(encoding="utf-8")
    if "dependencies:" in chart_yaml:
        try:
            run(["helm", "dependency", "build", str(rel)])
        except subprocess.CalledProcessError as exc:
            print(
                f"[warn] {rel}: dependency build failed ({exc.returncode}), trying package anyway",
                file=sys.stderr,
            )

    try:
        run(["helm", "package", str(rel), "-d", str(output_dir)])
    except subprocess.CalledProcessError as exc:
        print(f"[fail] {rel}: helm package failed ({exc.returncode})", file=sys.stderr)
        return None

    tgz = sorted(output_dir.glob("*.tgz"), key=lambda p: p.stat().st_mtime)[-1]
    print(f"[ok] {tgz.name}")
    return tgz


def build_index(output_dir: Path, repo_url: str, merge: bool) -> None:
    index = output_dir / "index.yaml"
    cmd = ["helm", "repo", "index", str(output_dir), "--url", repo_url.rstrip("/")]
    if merge and index.exists():
        cmd.extend(["--merge", str(index)])
    run(cmd)
    normalize_index_utf8(index)
    (output_dir / ".nojekyll").touch(exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output directory (default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--repo-url",
        default=DEFAULT_REPO_URL,
        help=f"Helm repo base URL for index.yaml (default: {DEFAULT_REPO_URL})",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="merge with existing index.yaml in output dir",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove output directory before packaging",
    )
    args = parser.parse_args()

    output_dir: Path = args.output.resolve()
    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    charts = discover_publishable_charts()
    print(f"Found {len(charts)} publishable chart(s)")

    ok = 0
    failed: list[str] = []
    for chart_dir in charts:
        rel = chart_dir.relative_to(REPO_ROOT)
        result = package_chart(chart_dir, output_dir)
        if result is None:
            failed.append(str(rel))
        else:
            ok += 1

    if ok == 0:
        print("No charts packaged.", file=sys.stderr)
        return 1

    build_index(output_dir, args.repo_url, args.merge)
    print(f"\nDone: {ok} packaged, {len(failed)} failed")
    print(f"Index: {output_dir / 'index.yaml'}")
    print(f"Repo:  helm repo add rancher-cloud-charts {args.repo_url.rstrip('/')}")
    if failed:
        print("\nFailed charts:", file=sys.stderr)
        for name in failed:
            print(f"  - {name}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
