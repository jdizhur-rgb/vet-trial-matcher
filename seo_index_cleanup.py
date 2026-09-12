#!/usr/bin/env python3
"""Apply the production indexing policy after the static site is generated.

The public pages remain available to owners.  This pass only controls which
pages we ask search engines to index and keeps all SEO signals on the custom
domain.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse


SITE = "https://vettrialfinder.com"
LANGUAGE_PREFIXES = {"de", "fr", "es", "it", "nl"}
LASTMOD = "2026-09-12"


def add_robots_noindex(text: str) -> str:
    if re.search(r'<meta\s+name=["\']robots["\']', text, re.I):
        return re.sub(
            r'<meta\s+name=["\']robots["\'][^>]*>',
            '<meta name="robots" content="noindex, follow">',
            text,
            count=1,
            flags=re.I,
        )
    return text.replace("</head>", '<meta name="robots" content="noindex, follow"></head>', 1)


def remove_unready_hreflang(text: str) -> str:
    return re.sub(
        r'<link\s+rel="alternate"\s+hreflang="(?:de|fr|es|it|nl)"[^>]*>',
        "",
        text,
        flags=re.I,
    )


def opportunity_count(text: str) -> int | None:
    match = re.search(r'class="opportunity-count"[^>]*>\s*(\d+)\s+current', text, re.I)
    if not match:
        match = re.search(r'>\s*(\d+)\s+current treatment opportunities', text, re.I)
    return int(match.group(1)) if match else None


def canonical_url(text: str) -> str | None:
    match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', text, re.I)
    return html.unescape(match.group(1)) if match else None


def page_title(text: str) -> str:
    match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    if not match:
        match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    value = re.sub(r'<[^>]+>', '', match.group(1) if match else "Vet Trial Finder")
    return html.unescape(value).strip()


def breadcrumbs(path: str, title: str) -> list[dict[str, str]]:
    parts = [part for part in path.strip('/').split('/') if part]
    crumbs = [{"name": "Vet Trial Finder", "item": f"{SITE}/"}]
    if not parts:
        return crumbs
    if len(parts) >= 3 and parts[0] in {"north-america", "uk-europe"} and parts[1] in {"dogs", "cats"}:
        crumbs.append({"name": "Cancer Types", "item": f"{SITE}/cancer-types/"})
    elif parts[0] == "centers" and len(parts) > 1:
        crumbs.append({"name": "Oncology Centers", "item": f"{SITE}/centers/"})
    crumbs.append({"name": title, "item": f"{SITE}/{path.strip('/')}/"})
    return crumbs


def add_structured_data(text: str, path: str) -> str:
    # The cancer-page renderer already emits a richer WebPage/Breadcrumb graph.
    # Never stack a second graph on pages which own their structured data.
    if 'type="application/ld+json"' in text:
        return text
    if not path:
        data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": f"{SITE}/#website",
                    "url": f"{SITE}/",
                    "name": "Vet Trial Finder",
                    "description": "Free finder for cancer clinical trials and treatment options for dogs and cats.",
                },
                {
                    "@type": "Organization",
                    "@id": f"{SITE}/#organization",
                    "name": "Vet Trial Finder",
                    "url": f"{SITE}/",
                    "founder": {"@type": "Person", "name": "Yuliia Dizhur"},
                },
            ],
        }
    else:
        items = [
            {"@type": "ListItem", "position": i, "name": crumb["name"], "item": crumb["item"]}
            for i, crumb in enumerate(breadcrumbs(path, page_title(text)), 1)
        ]
        data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    script = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    return text.replace("</head>", script + "</head>", 1)


def should_noindex(relative: Path, text: str) -> bool:
    parts = relative.parts
    if parts and parts[0] in LANGUAGE_PREFIXES:
        return True
    if len(parts) >= 4 and parts[0] in {"north-america", "uk-europe"} and parts[1] in {"dogs", "cats"}:
        count = opportunity_count(text)
        # The owner-guide renderer intentionally removes the old numeric summary,
        # so the absence of study cards is the durable zero-opportunity signal.
        return count == 0 or '<article class="card">' not in text
    if len(parts) >= 3 and parts[0] == "centers":
        count = opportunity_count(text)
        return count == 0
    return False


def write_sitemap(root: Path, indexable: list[str]) -> None:
    entries = "".join(
        f"  <url><loc>{html.escape(url)}</loc><lastmod>{LASTMOD}</lastmod></url>\n"
        for url in sorted(indexable, key=lambda value: (value != f"{SITE}/", value))
    )
    (root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + entries
        + '</urlset>\n',
        encoding="utf-8",
    )


def write_404(root: Path) -> None:
    (root / "404.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex, follow"><title>Page Not Found | Vet Trial Finder</title>'
        '<style>body{margin:0;background:#f6f8fb;color:#17324d;font:16px/1.55 system-ui,sans-serif}'
        'main{max-width:680px;margin:12vh auto;padding:24px}a{color:#175b8c}</style></head><body><main>'
        '<h1>We could not find that page</h1><p>The page may have moved or the listing may have changed.</p>'
        f'<p><a href="{SITE}/">Go to Vet Trial Finder</a> · '
        f'<a href="{SITE}/cancer-types/">Browse cancer types</a></p></main></body></html>',
        encoding="utf-8",
    )


def main() -> None:
    root = Path(__file__).resolve().parent / "seo" / "site"
    if not root.exists():
        raise SystemExit(f"generated site not found: {root}")

    indexable: list[str] = []
    noindexed = 0
    for page in sorted(root.rglob("index.html")):
        relative = page.relative_to(root)
        path = "" if relative == Path("index.html") else relative.parent.as_posix()
        text = page.read_text(encoding="utf-8")
        text = remove_unready_hreflang(text)
        canonical = canonical_url(text)
        if not canonical or urlparse(canonical).netloc != "vettrialfinder.com":
            raise AssertionError(f"invalid production canonical in {relative}: {canonical}")
        if should_noindex(relative, text):
            text = add_robots_noindex(text)
            noindexed += 1
        else:
            indexable.append(canonical)
        text = add_structured_data(text, path)
        page.write_text(text, encoding="utf-8")

    write_sitemap(root, indexable)
    (root / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    write_404(root)

    sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
    assert "jdizhur-rgb.github.io" not in sitemap
    assert not any(f"{SITE}/{lang}/" in sitemap for lang in LANGUAGE_PREFIXES)
    assert len(indexable) == len(set(indexable))
    print(f"SEO_INDEX_POLICY_OK indexable={len(indexable)} noindex={noindexed}")


if __name__ == "__main__":
    main()
