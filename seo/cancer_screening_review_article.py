#!/usr/bin/env python3
"""Publish the owner-approved comparative review of canine cancer tests."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

SLUG = "cancer-screening-tests-for-dogs"
TITLE = "Cancer screening tests for dogs: what they look for and what results mean"
DESCRIPTION = "A practical review of canine cancer blood and urine tests: how they work, which cancers they look for, sensitivity, specificity, follow-up and insurance questions."
IMAGE_NAME = "canine-cancer-screening-review.jpg"


def generate_cancer_screening_review_article(root: Path) -> None:
    url = f"{SITE}/articles/{SLUG}/"
    image = f"{SITE}/assets/social/{IMAGE_NAME}"
    source = Path(__file__).resolve().parent
    assets = root / "assets" / "social"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / "assets" / "social" / IMAGE_NAME, assets / IMAGE_NAME)
    content = (source / "content" / "cancer-screening-tests-for-dogs.html").read_text(encoding="utf-8")
    body = f'''<article class="article-page">
<p class="eyebrow">Cancer testing · November 19, 2026</p>
<h1>{TITLE}</h1>
<figure class="article-hero"><img src="{image}" alt="Illustration of a senior dog beside blood and urine sample containers in a veterinary setting" width="1536" height="1024" style="display:block;width:100%;height:auto;border-radius:12px"><figcaption>Illustrative image generated with AI; not a study patient.</figcaption></figure>
{content}
<div class="article-byline"><p><strong>By:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, founder of Vet Cancer Care Finder.</p><p><strong>Published and sources checked:</strong> November 19, 2026.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the linked research and manufacturer information. This owner-focused review has not been independently reviewed by a veterinarian and does not replace veterinary advice. Availability varies by country and clinic.</p></div>
</article>'''
    rendered = g.page(TITLE, DESCRIPTION, body, url)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Cancer Care Finder"><meta property="og:title" content="{g.esc(TITLE)}"><meta property="og:description" content="{g.esc(DESCRIPTION)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{image}"><meta property="og:image:secure_url" content="{image}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:alt" content="Illustration of a dog beside blood and urine sample containers"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{g.esc(TITLE)}"><meta name="twitter:description" content="{g.esc(DESCRIPTION)}"><meta name="twitter:image" content="{image}">'''
    schema = {
        "@context": "https://schema.org", "@type": "Article", "headline": TITLE,
        "description": DESCRIPTION, "image": [image],
        "datePublished": "2026-11-19", "dateModified": "2026-11-19",
        "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"},
        "publisher": {"@type": "Organization", "name": "Vet Cancer Care Finder", "url": f"{SITE}/"},
        "mainEntityOfPage": url,
    }
    rendered = rendered.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    destination = root / "articles" / SLUG
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(wrap_html(rendered), encoding="utf-8")

    index = root / "articles" / "index.html"
    index_text = index.read_text(encoding="utf-8")
    if url not in index_text:
        card = f'<a class="directory-card" href="{url}"><strong>{TITLE}</strong><span>Blood and urine tests, the cancers they look for, false results and what happens after a positive signal.</span></a>'
        marker = '<div class="directory-grid">'
        if marker not in index_text:
            raise AssertionError("Article index must be generated before the screening review")
        index.write_text(index_text.replace(marker, marker + card, 1), encoding="utf-8")
    sitemap = root / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    if url not in text:
        sitemap.write_text(text.replace("</urlset>", f"<url><loc>{url}</loc></url>\n</urlset>"), encoding="utf-8")


if __name__ == "__main__":
    generate_cancer_screening_review_article(Path(__file__).resolve().parent / "site")
