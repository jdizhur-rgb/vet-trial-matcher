#!/usr/bin/env python3
"""Submit changed, indexable production pages to IndexNow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


HOST = "vettrialfinder.com"
ORIGIN = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"
KEY = "ca36635c41120f89495c9cd121d884744872420f261fc4e44272c6f5555d3b62"
KEY_LOCATION = f"{ORIGIN}/{KEY}.txt"
NOINDEX_RE = re.compile(
    r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I
)
REDIRECT_RE = re.compile(r'<meta\s+[^>]*http-equiv=["\']refresh["\']', re.I)


def public_pages(site: Path) -> dict[str, str]:
    """Return sitemap URLs and content hashes after enforcing indexing rules."""
    sitemap = site / "sitemap.xml"
    root = ET.parse(sitemap).getroot()
    pages: dict[str, str] = {}
    for node in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        location = node.findtext("{http://www.sitemaps.org/schemas/sitemap/0.9}loc", "")
        parsed = urllib.parse.urlsplit(location)
        if parsed.scheme != "https" or parsed.netloc != HOST or parsed.query or parsed.fragment:
            raise ValueError(f"Non-production URL in sitemap: {location}")
        relative = urllib.parse.unquote(parsed.path).lstrip("/")
        page = site / relative / "index.html" if relative else site / "index.html"
        if not page.is_file() or not page.resolve().is_relative_to(site.resolve()):
            raise ValueError(f"Sitemap URL has no generated page: {location}")
        html = page.read_text(encoding="utf-8")
        if NOINDEX_RE.search(html) or REDIRECT_RE.search(html):
            raise ValueError(f"Sitemap contains noindex or redirected page: {location}")
        canonical = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', html, re.I)
        if not canonical or canonical.group(1) != location:
            raise ValueError(f"Generated page has a mismatched canonical URL: {location}")
        pages[location] = hashlib.sha256(page.read_bytes()).hexdigest()
    return pages


def load_manifest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise ValueError(f"Invalid IndexNow manifest: {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("seo/site"))
    parser.add_argument("--manifest", type=Path, default=Path(".indexnow-manifest.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    current = public_pages(args.site)
    previous = load_manifest(args.manifest)
    changed = sorted(url for url, digest in current.items() if previous.get(url) != digest)
    print(f"INDEXNOW_ELIGIBLE={len(current)} INDEXNOW_CHANGED={len(changed)}")
    if args.dry_run:
        print("\n".join(changed))
        return 0
    if not changed:
        args.manifest.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return 0

    payload = json.dumps(
        {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": changed}
    ).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status not in (200, 202):
                raise urllib.error.HTTPError(ENDPOINT, response.status, "Unexpected response", response.headers, None)
    except (OSError, urllib.error.URLError, urllib.error.HTTPError) as error:
        # IndexNow is an optional post-deployment notification. Retain the old
        # manifest so these URLs are retried after a future successful deploy.
        print(f"::warning::IndexNow submission unavailable; deployment remains successful: {error}")
        if not args.manifest.exists():
            args.manifest.write_text("{}\n", encoding="utf-8")
        return 0

    args.manifest.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"INDEXNOW_SUBMITTED={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
