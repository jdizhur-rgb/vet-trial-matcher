#!/usr/bin/env python3
"""Harden generated HTML against stale browser copies.

GitHub Pages controls the HTTP Cache-Control header, so the static site cannot
set CDN response headers itself. These HTML directives tell browsers to
revalidate HTML once a fresh document reaches them, without changing canonical
URLs, sitemap URLs, or trial data.
"""
from __future__ import annotations

from pathlib import Path

META = (
    '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">'
    '<meta http-equiv="Pragma" content="no-cache">'
    '<meta http-equiv="Expires" content="0">'
)


def apply_cache_policy(root: Path) -> int:
    root = Path(root)
    changed = 0
    for path in root.rglob('*.html'):
        text = path.read_text(encoding='utf-8', errors='replace')
        if 'http-equiv="Cache-Control"' in text:
            continue
        if '<head>' not in text:
            continue
        text = text.replace('<head>', '<head>' + META, 1)
        path.write_text(text, encoding='utf-8')
        changed += 1
    if not changed:
        raise AssertionError('Cache policy matched no generated HTML pages')
    print('CACHE_POLICY_APPLIED', changed)
    return changed
