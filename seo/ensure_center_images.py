#!/usr/bin/env python3
"""Check center imagery without adding unrelated stock photography."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
def overview_block(text):
    # The overview contains a nested copy div, so its first closing </div> is
    # not the end of the overview. The facts block is its stable boundary.
    m = re.search(r'<div class="center-overview(?: has-image)?"[^>]*>.*?(?=<div class="center-facts">)', text, re.S)
    return m


def main():
    centers = sorted((SITE / "centers").glob("*/index.html"))
    if not centers:
        raise RuntimeError("No generated center pages found")
    with_images = []
    for page in centers:
        text = page.read_text(encoding="utf-8", errors="replace")
        if 'noindex,follow' in text and 'http-equiv="refresh"' in text:
            continue
        block = overview_block(text)
        if not block:
            raise RuntimeError(f"Missing center overview: {page}")
        if "<img " in block.group(0):
            with_images.append(page)
        if 'center-fallback.jpg' in text:
            raise RuntimeError(f"Generic fallback image survived: {page}")
    print(f"CENTER_IMAGES_OK pages={len(centers)} verified_images={len(with_images)} redirects_skipped={len(centers)-len([p for p in centers if 'noindex,follow' not in p.read_text(encoding='utf-8',errors='replace')])} no_stock_fallbacks=1")


if __name__ == "__main__":
    main()
