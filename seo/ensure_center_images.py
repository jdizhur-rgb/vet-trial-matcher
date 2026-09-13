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
    checked = []
    for page in centers:
        text = page.read_text(encoding="utf-8", errors="replace")
        if 'noindex,follow' in text and 'http-equiv="refresh"' in text:
            continue
        block = overview_block(text)
        if not block:
            raise RuntimeError(f"Missing center overview: {page}")
        section = block.group(0)
        if "<img " not in section:
            raise RuntimeError(f"Missing center image: {page}")
        if not re.search(r'<figcaption>[^<]{4,}</figcaption>', section):
            raise RuntimeError(f"Missing image credit: {page}")
        copy = re.search(r'<div class="center-overview-copy"><p>(.*?)</p>', section, re.S)
        if not copy or len(re.sub(r'<[^>]+>', '', copy.group(1)).strip()) < 70:
            raise RuntimeError(f"Missing substantive center introduction: {page}")
        if 'This page brings together current cancer studies' in section or 'This page groups the current cancer studies' in section:
            raise RuntimeError(f"Generic center introduction survived: {page}")
        if not re.search(r'<a href="https?://', section):
            raise RuntimeError(f"Missing official center or study link: {page}")
        checked.append(page)
        if 'center-fallback.jpg' in text:
            raise RuntimeError(f"Generic fallback image survived: {page}")
    print(f"CENTER_PROFILES_OK pages={len(centers)} verified_profiles={len(checked)} redirects_skipped={len(centers)-len(checked)}")


if __name__ == "__main__":
    main()
