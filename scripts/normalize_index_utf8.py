#!/usr/bin/env python3
"""Write index.yaml as UTF-8 with BOM (GitHub Pages / Windows browser friendly)."""

from __future__ import annotations

import sys
from pathlib import Path


def normalize_index_utf8(index_path: Path) -> None:
    raw = index_path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    for encoding in ("utf-8", "gbk", "cp936"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.endswith("\n"):
        text += "\n"
    index_path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <index.yaml>", file=sys.stderr)
        sys.exit(2)
    normalize_index_utf8(Path(sys.argv[1]))
    print(f"normalized: {sys.argv[1]}")
