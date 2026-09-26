#!/usr/bin/env python3
"""Turn the Articles index into a searchable, categorized library."""
from pathlib import Path
import re
import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "site" / "articles" / "index.html"

CATEGORIES = {
    "diagnosis": {
        "slug": "diagnosis-and-treatment-decisions",
        "label": "Diagnosis and decisions",
        "title": "Veterinary cancer diagnosis and treatment decisions",
        "description": "Practical veterinary cancer articles about diagnosis, biopsy, surgery, pathology, margins and treatment decisions for dogs and cats.",
        "intro": "A useful treatment plan starts with knowing what the tumor is, where it is, and what the pathology can actually tell you. These articles cover the decisions that often come before and after surgery.",
    },
    "treatment": {
        "slug": "treatment-options",
        "label": "Treatment options",
        "title": "Veterinary cancer treatment options",
        "description": "Plain-language guides to veterinary cancer treatments for dogs and cats, including electrochemotherapy and cancer vaccines.",
        "intro": "These guides explain how specific cancer treatments work, what they are intended to do, where the evidence is uncertain, and what owners should ask before proceeding.",
    },
    "trials": {
        "slug": "clinical-trials-and-research",
        "label": "Clinical trials and research",
        "title": "Veterinary cancer clinical trials and research",
        "description": "Guides to veterinary cancer clinical trials, experimental treatment, current research directions and interpreting early results.",
        "intro": "Clinical trials can provide access to treatment, but an experimental result is not a promise. These articles explain how trials work and how to read claims about new veterinary cancer research.",
    },
    "safety": {
        "slug": "supplements-and-unproven-remedies",
        "label": "Supplements and unproven remedies",
        "title": "Cancer supplements and unproven remedies for dogs",
        "description": "Evidence and safety guides for dog cancer supplements, mushrooms, herbs, fenbendazole, ivermectin and remedies that may cause harm.",
        "intro": "Laboratory findings, testimonials and visible tissue damage are often presented as proof that a remedy works. These articles separate plausible supportive use from unsupported cancer-treatment claims and avoidable harm.",
    },
}

ARTICLE_CATEGORIES = {
    "pet-lump-diagnosis-before-surgery": "diagnosis",
    "surgical-margins-after-tumor-removal": "diagnosis",
    "electrochemotherapy": "treatment",
    "cancer-vaccines": "treatment",
    "clinical-trials-for-pets-with-cancer": "trials",
    "where-veterinary-cancer-trials-are-heading": "trials",
    "when-cancer-remedies-cause-harm": "safety",
    "mushrooms-herbs-supplements-dogs-with-cancer": "safety",
    "fenbendazole-ivermectin-dogs-with-cancer": "safety",
}


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    grid = re.search(r'<div class="directory-grid">(.*?)</div>', text, re.S)
    if not grid:
        raise AssertionError("Articles index is missing its directory grid")
    cards = re.findall(r'<a class="directory-card" href="([^"]+)">(.*?)</a>', grid.group(1), re.S)
    if not cards:
        raise AssertionError("Articles index has no article cards")

    rendered = []
    missing = []
    for url, body in cards:
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        category = ARTICLE_CATEGORIES.get(slug)
        if not category:
            missing.append(slug)
            continue
        rendered.append(
            f'<a class="directory-card article-catalog-card" data-article-category="{category}" href="{url}">{body}</a>'
        )
    if missing:
        raise AssertionError(f"Uncategorized articles: {missing}")

    category_links = ''.join(
        f'<a href="{SITE}/articles/{meta["slug"]}/">{meta["label"]}</a>'
        for meta in CATEGORIES.values()
    )
    catalog = (
        '<section class="article-library" aria-label="Article library">'
        '<label class="article-library-search" for="article-search"><strong>Find an article</strong>'
        '<input id="article-search" type="search" placeholder="Search by subject or treatment" autocomplete="off"></label>'
        '<nav class="article-library-filters" aria-label="Article categories">' + category_links + '</nav>'
        '<p id="article-library-status" class="article-library-status" aria-live="polite"></p>'
        '<div class="directory-grid article-catalog-grid">' + ''.join(rendered) + '</div>'
        '<button class="article-show-more" type="button" hidden>Show more</button></section>'
    )
    text = text[:grid.start()] + catalog + text[grid.end():]

    css = '''.article-library{margin-top:22px}.article-library-search{display:grid;gap:7px;max-width:620px;color:#315f7d}.article-library-search input{box-sizing:border-box;width:100%;padding:11px 13px;border:1px solid #b8c8d6;border-radius:9px;background:#fff;color:#17243b;font:inherit}.article-library-filters{display:flex;flex-wrap:wrap;gap:8px;margin:17px 0 8px}.article-library-filters a,.article-show-more{border:1px solid #d5e2ea;border-radius:999px;padding:8px 12px;background:#edf4f8;color:#315f7d!important;font:650 .92rem/1.3 system-ui,-apple-system,sans-serif;text-decoration:none;cursor:pointer}.article-library-status{min-height:1.35em;margin:7px 0 12px;color:#607086;font-size:.88rem}.article-catalog-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.article-catalog-card[hidden]{display:none!important}.article-show-more{display:block;margin:15px auto 0}.article-show-more[hidden]{display:none!important}@media(max-width:650px){.article-library-filters{display:grid;grid-template-columns:1fr 1fr}.article-library-filters a{border-radius:9px;text-align:center}.article-catalog-grid{grid-template-columns:1fr!important}.article-show-more{width:100%;border-radius:9px}}'''
    text = text.replace('</style>', css + '</style>', 1)

    script = '''<script>(()=>{const cards=[...document.querySelectorAll('.article-catalog-card')],input=document.getElementById('article-search'),more=document.querySelector('.article-show-more'),status=document.getElementById('article-library-status');let limit=6;function apply(){const q=input.value.toLowerCase().trim(),matches=cards.filter(card=>!q||card.textContent.toLowerCase().includes(q));cards.forEach(card=>card.hidden=true);matches.slice(0,limit).forEach(card=>card.hidden=false);more.hidden=matches.length<=limit;status.textContent=matches.length+(matches.length===1?' article':' articles');}input.addEventListener('input',()=>{limit=6;apply()});more.addEventListener('click',()=>{limit+=6;apply()});apply()})()</script>'''
    text = text.replace('</main>', script + '</main>', 1)
    PAGE.write_text(text, encoding="utf-8")

    sitemap = ROOT / "site" / "sitemap.xml"
    sitemap_text = sitemap.read_text(encoding="utf-8")
    for key, meta in CATEGORIES.items():
        category_cards = ''.join(card for card in rendered if f'data-article-category="{key}"' in card)
        url = f'{SITE}/articles/{meta["slug"]}/'
        body = (f'<div class="article-category-page"><h1>{meta["title"]}</h1><p class="lead">{meta["intro"]}</p>'
            f'<div class="directory-grid">{category_cards}</div><p><a href="{SITE}/articles/">Browse all veterinary cancer articles →</a></p></div>')
        destination = ROOT / "site" / "articles" / meta["slug"]
        destination.mkdir(parents=True, exist_ok=True)
        page = wrap_html(g.page(f'{meta["title"]} | Vet Trial Finder', meta["description"], body, url))
        destination.joinpath("index.html").write_text(page, encoding="utf-8")
        if url not in sitemap_text:
            sitemap_text = sitemap_text.replace('</urlset>', f'<url><loc>{url}</loc></url>\n</urlset>')
    sitemap.write_text(sitemap_text, encoding="utf-8")
    print(f"ARTICLE_CATALOG_OK articles={len(cards)} categories={len(CATEGORIES)}")


if __name__ == "__main__":
    main()
