#!/usr/bin/env python3
"""TEST BRANCH ONLY: preview reviewed cancer-guide indexing policy.

This file must be folded into seo_index_cleanup.py before any merge to main.
"""
from pathlib import Path
import re

SITE = "https://vettrialfinder.com"
LASTMOD = "2026-09-13"


def main() -> None:
    root = Path(__file__).resolve().parent / "seo" / "site"
    sitemap_path = root / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8")
    closing = "</urlset>"
    assert closing in sitemap

    pages = []
    for species in ("dogs", "cats"):
        pages.extend(sorted((root / "north-america" / species).glob("*/index.html")))
    assert len(pages) == 44, len(pages)

    added = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        required = (
            'class="disease owner-guide"',
            "How it is usually treated",
            "What can affect treatment choices",
            "Tests that may matter",
        )
        assert all(marker in text for marker in required), page
        text = re.sub(
            r'<meta\s+name=["\']robots["\'][^>]*noindex[^>]*>',
            "",
            text,
            flags=re.I,
        )
        page.write_text(text, encoding="utf-8")
        rel = page.parent.relative_to(root).as_posix()
        url = f"{SITE}/{rel}/"
        if f"<loc>{url}</loc>" not in sitemap:
            entry = f"  <url><loc>{url}</loc><lastmod>{LASTMOD}</lastmod></url>\n"
            sitemap = sitemap.replace(closing, entry + closing, 1)
            added += 1

    sitemap_path.write_text(sitemap, encoding="utf-8")
    assert all("noindex" not in p.read_text(encoding="utf-8").lower() for p in pages)
    assert all(f"<loc>{SITE}/{p.parent.relative_to(root).as_posix()}/</loc>" in sitemap for p in pages)
    assert "/uk-europe/" not in sitemap
    print(f"REVIEWED_CANCER_GUIDES_PREVIEW_OK pages={len(pages)} newly_added={added}")


if __name__ == "__main__":
    main()
