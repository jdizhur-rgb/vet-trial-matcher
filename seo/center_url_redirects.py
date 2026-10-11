"""Preserve published center URLs when canonical slugs are shortened.

GitHub Pages serves static HTML: instant meta refresh is the permanent redirect
available here, not an HTTP 301. Only redirect to an existing same-center page.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from generate_seo import slugify
from site_config import SITE


# Published historical spelling not recoverable from the current center name.
LEGACY_CENTER_SLUGS = {
    "bridge-animal-referral-center-barc": "bridge-animal-referral-center",
}


def preserve_center_urls(root: Path) -> dict[str, str]:
    centers = root / "centers"
    pages = {}
    for page in sorted(centers.glob("*/index.html")):
        text = page.read_text(encoding="utf-8")
        if re.search(r'<meta\s+http-equiv=["\']refresh["\']', text, re.I):
            continue
        heading = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.I | re.S)
        if heading:
            pages[page.parent.name] = html.unescape(re.sub(r"<[^>]+>", "", heading[1])).strip()

    aliases = dict(LEGACY_CENTER_SLUGS)
    for current, name in pages.items():
        former = slugify(name)
        if former and former != current:
            if former in aliases and aliases[former] != current:
                raise ValueError(f"Conflicting center redirect: {former}")
            aliases[former] = current

    written = {}
    for former, current in sorted(aliases.items()):
        if current not in pages:
            continue  # No matching replacement: never guess another institution.
        if former in pages:
            raise ValueError(f"Center redirect would overwrite a live page: {former}")
        target = f"{SITE}/centers/{current}/"
        escaped = html.escape(target, quote=True)
        title = html.escape(pages[current])
        output = centers / former / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex, follow">'
            f'<link rel="canonical" href="{escaped}">'
            f'<meta http-equiv="refresh" content="0; url={escaped}">'
            f'<title>{title}</title></head><body>'
            f'<p><a href="{escaped}">{title}</a></p></body></html>',
            encoding="utf-8",
        )
        written[former] = current
    print(f"CENTER_URL_REDIRECTS_OK redirects={len(written)}")
    return written
