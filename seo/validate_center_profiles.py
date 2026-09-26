#!/usr/bin/env python3
"""Enforce text-only clinic profiles and substantive sourced introductions."""
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
        if 'noindex' in text and 'http-equiv="refresh"' in text:
            continue
        block = overview_block(text)
        if not block:
            if 'noindex' in text or 'http-equiv="refresh"' in text:
                continue
            raise RuntimeError(f"Missing center overview: {page}")
        section = block.group(0)
        if "<img " in section or "<figure" in section:
            raise RuntimeError(f"Clinic image must not be published: {page}")
        paragraphs = re.findall(r'<div class="center-overview-copy">(.*?)</div>', section, re.S)
        copies = re.findall(r'<p>(.*?)</p>', paragraphs[0], re.S) if paragraphs else []
        if not copies or len(re.sub(r'<[^>]+>', '', copies[0]).strip()) < 70:
            raise RuntimeError(f"Missing substantive center introduction: {page}")
        if 'This page brings together current cancer studies' in section or 'This page groups the current cancer studies' in section:
            raise RuntimeError(f"Generic center introduction survived: {page}")
        banned = ('represented in the current treatment catalog', 'is listed as a participating hospital')
        if any(phrase in section for phrase in banned):
            raise RuntimeError(f"Template center introduction survived: {page}")
        if section.count('<div class="center-overview-copy">') != 1:
            raise RuntimeError(f"Center introduction wrapper duplicated: {page}")
        if not re.search(r'<a href="https?://', section):
            raise RuntimeError(f"Missing official center or study link: {page}")
        checked.append(page)
    print(f"CENTER_PROFILES_OK pages={len(centers)} verified_profiles={len(checked)} redirects_skipped={len(centers)-len(checked)}")


if __name__ == "__main__":
    main()
