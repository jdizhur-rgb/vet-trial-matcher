#!/usr/bin/env python3
"""Generate the Vet Trial Finder news index and the Cornell Smart-Start item."""

from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html


NEWS_URL = f"{SITE}/news/"
ARTICLE_URL = f"{NEWS_URL}cornell-smart-start-b-cell-lymphoma/"
OFFICIAL_URL = "https://www.vet.cornell.edu/hospitals/clinical-trials/smart-start-therapy-canine-b-cell-lymphoma"
MATCHER_URL = f"{SITE}/matcher/"


def add_to_sitemap(root: Path, urls: tuple[str, ...]) -> None:
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        raise AssertionError("Sitemap is required before generating news")
    text = sitemap.read_text(encoding="utf-8")
    for url in urls:
        if url not in text:
            text = text.replace("</urlset>", f"<url><loc>{g.esc(url)}</loc></url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def generate_news_section(root: Path) -> None:
    index_body = f'''<div class="registry-page news-index">
<h1>Veterinary oncology news</h1>
<p class="lead">Newly opened treatment trials, meaningful recruitment changes and other developments that may matter to owners looking for cancer treatment options.</p>
<div class="directory-grid"><a class="directory-card" href="{ARTICLE_URL}"><strong>Cornell opens Smart-Start trial for dogs with B-cell lymphoma</strong><span>September 17, 2026. A biology-guided pre-treatment is followed by standard CHOP chemotherapy; there is no placebo.</span></a></div>
</div>'''
    index_dir = root / "news"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_page = g.page(
        "Veterinary Oncology News | Vet Trial Finder",
        "New veterinary cancer treatment trials, recruitment changes and other oncology developments for dogs and cats.",
        index_body,
        NEWS_URL,
    )
    (index_dir / "index.html").write_text(wrap_html(index_page), encoding="utf-8")

    article_body = f'''<article class="article-page news-article">
<p class="eyebrow">Trial opening · September 17, 2026</p>
<h1>Cornell opens Smart-Start trial for dogs with B-cell lymphoma</h1>
<p>Cornell University Hospital for Animals has opened enrollment in a new treatment study for dogs with B-cell lymphoma. Smart-Start is not a sample-collection or observational study. Every enrolled dog receives an anticancer pre-treatment selected according to the biology of that dog’s tumor, followed by standard CHOP chemotherapy.</p>
<p>The pre-treatment is either an oral drug given four times over a 14-day period or an injectable drug given at Cornell on five consecutive days. There is no placebo. After the pre-treatment period, dogs return for routine CHOP chemotherapy visits.</p>
<h2>Who may qualify</h2>
<p>The study is for dogs diagnosed with B-cell lymphoma that are seen by Cornell’s oncology service in Ithaca, New York. Dogs must not have received previous lymphoma treatment other than prednisolone, and owners must be willing to proceed with standard-of-care CHOP chemotherapy. Cornell makes the final eligibility decision after reviewing the dog’s records.</p>
<h2>What the study covers</h2>
<p>Tests and procedures performed specifically for the study are covered. Owners remain responsible for ordinary clinical care, but Cornell provides a 10% discount on standard-of-care chemotherapy visits and an additional $1,000 toward chemotherapy costs.</p>
<p>Enrollment was confirmed on Cornell’s active canine clinical-trials list and the study’s current appointment page on September 17, 2026. Owners can contact Cornell Oncology or the Clinical Trials Coordinator at 607-253-3060 or <a href="mailto:vet-research@cornell.edu">vet-research@cornell.edu</a>.</p>
<div class="article-cta"><a href="{OFFICIAL_URL}" target="_blank" rel="noopener">Read the official Cornell trial page</a></div>
<p><a href="{MATCHER_URL}">Check this and other current cancer treatment trials in Vet Trial Finder</a></p>
<div class="article-byline"><p><strong>Published:</strong> September 17, 2026</p><p><strong>Recruitment status checked:</strong> September 17, 2026</p><p><strong>Source:</strong> Cornell University College of Veterinary Medicine.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance and reviewed by Yuliia Dizhur. Trial eligibility and enrollment decisions are made by Cornell.</p></div>
</article>'''
    article_dir = index_dir / "cornell-smart-start-b-cell-lymphoma"
    article_dir.mkdir(parents=True, exist_ok=True)
    article_page = g.page(
        "Cornell Smart-Start B-Cell Lymphoma Trial | Vet Trial Finder",
        "Cornell has opened enrollment in a treatment trial for dogs with B-cell lymphoma using a biology-guided pre-treatment followed by CHOP chemotherapy.",
        article_body,
        ARTICLE_URL,
    )
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="Cornell opens Smart-Start trial for dogs with B-cell lymphoma"><meta property="og:description" content="A biology-guided pre-treatment is followed by standard CHOP chemotherapy. There is no placebo."><meta property="og:url" content="{ARTICLE_URL}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="Cornell opens Smart-Start trial for dogs with B-cell lymphoma"><meta name="twitter:description" content="Enrollment is open for Cornell’s Smart-Start treatment study.">'''
    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": "Cornell opens Smart-Start trial for dogs with B-cell lymphoma",
        "datePublished": "2026-09-17",
        "dateModified": "2026-09-17",
        "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"},
        "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"},
        "mainEntityOfPage": ARTICLE_URL,
    }
    article_page = article_page.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (article_dir / "index.html").write_text(wrap_html(article_page), encoding="utf-8")

    add_to_sitemap(root, (NEWS_URL, ARTICLE_URL))

    rendered = (article_dir / "index.html").read_text(encoding="utf-8")
    required = (
        "Cornell opens Smart-Start trial for dogs with B-cell lymphoma",
        "There is no placebo.",
        "$1,000 toward chemotherapy costs",
        OFFICIAL_URL,
        MATCHER_URL,
        f'<link rel="canonical" href="{ARTICLE_URL}">',
        '"@type": "NewsArticle"',
    )
    missing = [marker for marker in required if marker not in rendered]
    if missing:
        raise AssertionError(f"Cornell news validation failed: {missing}")


if __name__ == "__main__":
    generate_news_section(Path(__file__).resolve().parent / "site")
