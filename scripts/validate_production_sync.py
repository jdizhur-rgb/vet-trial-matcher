#!/usr/bin/env python3
"""Fail the build if catalog IDs, counters, or public matcher routes drift."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo.catalog_selection import current_access, current_public, current_treatments  # noqa: E402


SITE = ROOT / "seo" / "site"
MATCHER = SITE / "matcher"


def read(path: Path) -> str:
    assert path.exists(), f"Missing production file: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def first_stat(page: str) -> int:
    match = re.search(r'class="(?:home-stat|registry-stat)"><strong>(\d+)</strong>', page)
    assert match, "Could not find the primary catalog counter"
    return int(match.group(1))


def validate_internal_links() -> int:
    missing: set[tuple[str, str]] = set()
    checked = 0
    for page in SITE.rglob("*.html"):
        for target in re.findall(r'(?:href|src)="([^"]+)"', read(page)):
            parsed = urlparse(target)
            if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
                continue
            if parsed.netloc and parsed.netloc != "vettrialfinder.com":
                continue
            path = parsed.path
            if not path:
                continue
            if path == "/":
                candidate = SITE / "index.html"
            elif path.startswith("/") and path.endswith("/"):
                candidate = SITE / path.lstrip("/") / "index.html"
            elif path.startswith("/"):
                candidate = SITE / path.lstrip("/")
            else:
                candidate = (page.parent / path).resolve()
                if path.endswith("/"):
                    candidate /= "index.html"
            checked += 1
            if not candidate.exists():
                missing.add((str(page.relative_to(SITE)), path))
    assert not missing, "Broken internal links: " + json.dumps(sorted(missing), ensure_ascii=False)
    return checked


def main() -> None:
    public = current_public()
    treatments = current_treatments()
    access = current_access()
    expected_ids = {row["id"] for row in public}
    assert len(expected_ids) == len(public), "Duplicate IDs in current public catalog"

    matcher_rows = json.loads(read(MATCHER / "trials.json"))
    matcher_ids = {row["id"] for row in matcher_rows}
    assert len(matcher_ids) == len(matcher_rows), "Duplicate IDs in matcher catalog"
    assert matcher_ids == expected_ids, {
        "missing_from_matcher": sorted(expected_ids - matcher_ids),
        "extra_in_matcher": sorted(matcher_ids - expected_ids),
    }

    mapping = json.loads(read(SITE / "mapping-audit.json"))
    assert mapping["effective_treatment_records"] == len(treatments)
    assert first_stat(read(SITE / "index.html")) == len(treatments)
    assert first_stat(read(SITE / "veterinary-cancer-clinical-trials" / "index.html")) == len(treatments)

    matcher_routes = ("", "centers", "ect", "advanced", "expanded-access")
    for route in matcher_routes:
        page = MATCHER / route / "index.html" if route else MATCHER / "index.html"
        html = read(page)
        assert "matcher-preview" not in html, f"Preview URL leaked into {page}"
        assert not re.search(r'<meta name="robots" content="noindex', html, re.I), f"Production matcher is noindex: {page}"

    generated_html = "\n".join(read(path) for path in SITE.rglob("*.html"))
    assert "c-trials.streamlit.app" not in generated_html
    assert "vet-cancer-trial-finder.streamlit.app" not in generated_html

    sitemap = read(SITE / "sitemap.xml")
    for route in matcher_routes:
        url = "https://vettrialfinder.com/matcher/" + (f"{route}/" if route else "")
        assert url in sitemap, f"Matcher route missing from sitemap: {url}"

    checked_links = validate_internal_links()
    print(
        "PRODUCTION_SYNC_OK",
        f"total={len(public)}",
        f"treatment={len(treatments)}",
        f"access={len(access)}",
        f"matcher_ids={len(matcher_ids)}",
        f"internal_links={checked_links}",
    )


if __name__ == "__main__":
    main()
