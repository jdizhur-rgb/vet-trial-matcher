#!/usr/bin/env python3
"""Guarantee every generated center page has a visible image.

Existing center images are left untouched. Pages without one get one neutral
veterinary-care fallback, cached locally into the generated site.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import re

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
STATIC = ROOT / "static" / "images" / "centers"
FALLBACK = STATIC / "center-fallback.jpg"
FALLBACK_URL = "https://images.pexels.com/photos/6235650/pexels-photo-6235650.jpeg?cs=srgb&fm=jpg"
PUBLIC_SRC = "/images/centers/center-fallback.jpg"


def ensure_fallback_file():
    STATIC.mkdir(parents=True, exist_ok=True)
    if FALLBACK.exists() and FALLBACK.stat().st_size > 5000:
        return
    req = Request(FALLBACK_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as r:
        data = r.read(8_000_000)
        content_type = (r.headers.get_content_type() or "").lower()
    if len(data) <= 5000 or not content_type.startswith("image/"):
        raise RuntimeError("Fallback veterinary image download failed validation")
    FALLBACK.write_bytes(data)


def overview_block(text):
    m = re.search(r'<div class="center-overview"[^>]*>.*?</div>', text, re.S)
    return m


def main():
    centers = sorted((SITE / "centers").glob("*/index.html"))
    if not centers:
        raise RuntimeError("No generated center pages found")
    missing = []
    for page in centers:
        text = page.read_text(encoding="utf-8", errors="replace")
        block = overview_block(text)
        if not block:
            raise RuntimeError(f"Missing center overview: {page}")
        if "<img " in block.group(0):
            continue
        missing.append(page)
    if missing:
        ensure_fallback_file()
        figure = (
            '<figure style="margin:16px 0 22px;text-align:left">'
            f'<img src="{PUBLIC_SRC}" alt="Dog receiving veterinary care" loading="lazy" '
            'style="width:100%;max-height:430px;object-fit:cover;border-radius:14px;display:block">'
            '<figcaption style="font-size:.86rem;color:#607086;margin-top:7px">'
            'Veterinary care photo: Tima Miroshnichenko / Pexels.</figcaption></figure>'
        )
        for page in missing:
            text = page.read_text(encoding="utf-8", errors="replace")
            block = overview_block(text)
            updated = re.sub(r'(</h2>)', r'\1' + figure, block.group(0), count=1)
            text = text[:block.start()] + updated + text[block.end():]
            page.write_text(text, encoding="utf-8")
    # Hard guarantee: no center page may leave this step without an image.
    for page in centers:
        text = page.read_text(encoding="utf-8", errors="replace")
        block = overview_block(text)
        if not block or "<img " not in block.group(0):
            raise RuntimeError(f"Center page still has no image: {page}")
    print(f"CENTER_IMAGES_OK pages={len(centers)} fallback_pages={len(missing)}")


if __name__ == "__main__":
    main()
