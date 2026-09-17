#!/usr/bin/env python3
"""Generate the Vet Trial Finder news index and current trial updates."""

from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

NEWS_URL = f"{SITE}/news/"
MATCHER_URL = f"{SITE}/matcher/"
CORNELL_URL = f"{NEWS_URL}cornell-smart-start-b-cell-lymphoma/"
NC_STATE_URL = f"{NEWS_URL}nc-state-il12-bladder-cancer-deadline/"
WISCONSIN_URL = f"{NEWS_URL}wisconsin-ptcl-radiopharmaceutical-trial/"
CORNELL_OFFICIAL = "https://www.vet.cornell.edu/hospitals/clinical-trials/smart-start-therapy-canine-b-cell-lymphoma"
NC_STATE_OFFICIAL = "https://cvm.ncsu.edu/clinical-trial/now-enrolling-dogs-with-invasive-bladder-cancer/"
WISCONSIN_OFFICIAL = "https://uwveterinarycare.wisc.edu/veterinary-clinical-studies/oncology/"


def add_to_sitemap(root: Path, urls: tuple[str, ...]) -> None:
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        raise AssertionError("Sitemap is required before generating news")
    text = sitemap.read_text(encoding="utf-8")
    for url in urls:
        if url not in text:
            text = text.replace("</urlset>", f"<url><loc>{g.esc(url)}</loc></url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def write_article(root: Path, slug: str, title: str, description: str, body: str, source_name: str) -> None:
    url = f"{NEWS_URL}{slug}/"
    article_dir = root / "news" / slug
    article_dir.mkdir(parents=True, exist_ok=True)
    byline = f'''<div class="article-byline"><p><strong>Published:</strong> September 17, 2026</p><p><strong>Recruitment status checked:</strong> September 17, 2026</p><p><strong>Source:</strong> {source_name}.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance and reviewed by Yuliia Dizhur. Trial eligibility and enrollment decisions are made by the study team.</p></div>'''
    page = g.page(f"{title} | Vet Trial Finder", description, f'<article class="article-page news-article">{body}{byline}</article>', url)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="{g.esc(title)}"><meta property="og:description" content="{g.esc(description)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{g.esc(title)}"><meta name="twitter:description" content="{g.esc(description)}">'''
    schema = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": title, "datePublished": "2026-09-17", "dateModified": "2026-09-17", "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"}, "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"}, "mainEntityOfPage": url}
    page = page.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (article_dir / "index.html").write_text(wrap_html(page), encoding="utf-8")


def generate_news_section(root: Path) -> None:
    index_body = f'''<div class="registry-page news-index">
<h1>Veterinary oncology news</h1>
<p class="lead">Newly opened treatment trials, meaningful recruitment changes and other developments that may matter to owners looking for cancer treatment options.</p>
<div class="directory-grid">
<a class="directory-card" href="{NC_STATE_URL}"><strong>NC State bladder cancer immunotherapy trial closes enrollment September 30</strong><span>September 17, 2026. The fully funded eight-day IL-12 treatment study has no placebo group.</span></a>
<a class="directory-card" href="{WISCONSIN_URL}"><strong>Wisconsin recruits dogs with peripheral T-cell lymphoma for 90Y-NM600 therapy</strong><span>September 17, 2026. All enrolled dogs receive targeted radiopharmaceutical therapy; most study costs are covered after screening.</span></a>
<a class="directory-card" href="{CORNELL_URL}"><strong>Cornell opens Smart-Start trial for dogs with B-cell lymphoma</strong><span>September 17, 2026. A biology-guided pre-treatment is followed by standard CHOP chemotherapy; there is no placebo.</span></a>
</div></div>'''
    index_dir = root / "news"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_page = g.page("Veterinary Oncology News | Vet Trial Finder", "New veterinary cancer treatment trials, recruitment changes and other oncology developments for dogs and cats.", index_body, NEWS_URL)
    (index_dir / "index.html").write_text(wrap_html(index_page), encoding="utf-8")

    cornell_body = f'''<p class="eyebrow">Trial opening · September 17, 2026</p>
<h1>Cornell opens Smart-Start trial for dogs with B-cell lymphoma</h1>
<p>Cornell University Hospital for Animals has opened enrollment in a new treatment study for dogs with B-cell lymphoma. Smart-Start is not a sample-collection or observational study. Every enrolled dog receives an anticancer pre-treatment selected according to the biology of that dog’s tumor, followed by standard CHOP chemotherapy.</p>
<p>The pre-treatment is either an oral drug given four times over a 14-day period or an injectable drug given at Cornell on five consecutive days. There is no placebo. After the pre-treatment period, dogs return for routine CHOP chemotherapy visits.</p>
<h2>Who may qualify</h2><p>The study is for dogs diagnosed with B-cell lymphoma that are seen by Cornell’s oncology service in Ithaca, New York. Dogs must not have received previous lymphoma treatment other than prednisolone, and owners must be willing to proceed with standard-of-care CHOP chemotherapy.</p>
<h2>What the study covers</h2><p>Tests and procedures performed specifically for the study are covered. Owners remain responsible for ordinary clinical care, but Cornell provides a 10% discount on standard-of-care chemotherapy visits and an additional $1,000 toward chemotherapy costs.</p>
<p>Owners can contact Cornell Oncology or the Clinical Trials Coordinator at 607-253-3060 or <a href="mailto:vet-research@cornell.edu">vet-research@cornell.edu</a>.</p>
<div class="article-cta"><a href="{CORNELL_OFFICIAL}" target="_blank" rel="noopener">Read the official Cornell trial page</a></div><p><a href="{MATCHER_URL}">Check this and other current cancer treatment trials in Vet Trial Finder</a></p>'''
    write_article(root, "cornell-smart-start-b-cell-lymphoma", "Cornell opens Smart-Start trial for dogs with B-cell lymphoma", "Cornell has opened enrollment in a treatment trial for dogs with B-cell lymphoma using a biology-guided pre-treatment followed by CHOP chemotherapy.", cornell_body, "Cornell University College of Veterinary Medicine")

    nc_state_body = f'''<p class="eyebrow">Enrollment deadline · September 30, 2026</p>
<h1>NC State bladder cancer immunotherapy trial closes enrollment September 30</h1>
<p>NC State is still recruiting dogs with invasive urothelial carcinoma, also called transitional cell carcinoma, for an experimental IL-12 immunotherapy study. The official enrollment window ends September 30, 2026, so owners interested in screening have little time left to contact the study team.</p>
<p>The study lasts eight days, from Monday through the following Monday. Dogs receive the bladder immunotherapy under general anesthesia on day 1, remain hospitalized through day 3, and return for outpatient checks on days 4 and 8. There is no placebo group. Every enrolled dog receives the immunotherapy, and some dogs may be able to enroll again for additional doses.</p>
<h2>Who may qualify</h2><p>Dogs must weigh at least 8 kg (17.6 lb) and have muscle-invasive bladder urothelial carcinoma confirmed by cytology with a BRAF test or by biopsy. Metastatic disease is allowed. Dogs may be untreated or previously treated, but at least one month must have passed since radiation or chemotherapy. Other immunotherapy and prednisone are not allowed during enrollment.</p>
<h2>What the study covers</h2><p>Pre-staging, IL-12 treatment and study monitoring are provided at no cost. Coverage includes specified blood and urine testing, focused urinary-tract ultrasound, hospitalization, anesthesia and repeat bloodwork.</p>
<div class="article-cta"><a href="{NC_STATE_OFFICIAL}" target="_blank" rel="noopener">Read the official NC State trial page</a></div><p><a href="{MATCHER_URL}">Check current bladder cancer trials in Vet Trial Finder</a></p>'''
    write_article(root, "nc-state-il12-bladder-cancer-deadline", "NC State bladder cancer immunotherapy trial closes enrollment September 30", "NC State's fully funded IL-12 immunotherapy study for dogs with invasive bladder cancer is scheduled to close enrollment September 30, 2026.", nc_state_body, "NC State College of Veterinary Medicine")

    wisconsin_body = f'''<p class="eyebrow">New treatment trial · September 17, 2026</p>
<h1>Wisconsin recruits dogs with peripheral T-cell lymphoma for 90Y-NM600 therapy</h1>
<p>UW Veterinary Care is recruiting dogs with peripheral T-cell lymphoma for a dose-finding study of 90Y-NM600 targeted radiopharmaceutical therapy. NM600 is designed to carry radiation to cancer throughout the body. All enrolled dogs receive the treatment; this is not a placebo-controlled or masked trial.</p>
<p>Dogs with a response or stable disease at the day 21 assessment may qualify for another dose. Standard chemotherapy is not part of the study, and owners should discuss that distinction with the oncology team before deciding whether the protocol fits their dog.</p>
<h2>Who may qualify</h2><p>Dogs need peripheral T-cell lymphoma confirmed by flow cytometry or immunohistochemistry, a measurable tumor that can be biopsied, body weight of at least 10 kg (22 lb), and age over one year. Significant health problems that would make completion unlikely may exclude a dog.</p>
<h2>What the study covers</h2><p>The initial screening visit and initial laboratory work are owner-paid. After enrollment, the study covers required examination visits, laboratory work, tumor biopsy, PET-CT scans, hospitalization and all costs related to 90Y-NM600 treatment. Up to $1,000 is also available for treatment-related side effects.</p>
<p>Owners or veterinarians can contact UW Veterinary Care Oncology at 608-890-0422 or <a href="mailto:oncclinicaltrials@vetmed.wisc.edu">oncclinicaltrials@vetmed.wisc.edu</a>.</p>
<div class="article-cta"><a href="{WISCONSIN_OFFICIAL}" target="_blank" rel="noopener">Read the official Wisconsin trial listing</a></div><p><a href="{MATCHER_URL}">Check current lymphoma trials in Vet Trial Finder</a></p>'''
    write_article(root, "wisconsin-ptcl-radiopharmaceutical-trial", "Wisconsin recruits dogs with peripheral T-cell lymphoma for 90Y-NM600 therapy", "UW Veterinary Care is recruiting dogs with peripheral T-cell lymphoma for a funded study of targeted 90Y-NM600 radiopharmaceutical therapy.", wisconsin_body, "UW Veterinary Care")

    add_to_sitemap(root, (NEWS_URL, CORNELL_URL, NC_STATE_URL, WISCONSIN_URL))
    rendered = "\n".join((root / "news" / slug / "index.html").read_text(encoding="utf-8") for slug in ("cornell-smart-start-b-cell-lymphoma", "nc-state-il12-bladder-cancer-deadline", "wisconsin-ptcl-radiopharmaceutical-trial"))
    required = ("There is no placebo.", "$1,000 toward chemotherapy costs", "September 30, 2026", "There is no placebo group.", "90Y-NM600", "initial screening visit and initial laboratory work are owner-paid", CORNELL_OFFICIAL, NC_STATE_OFFICIAL, WISCONSIN_OFFICIAL, '"@type": "NewsArticle"')
    missing = [marker for marker in required if marker not in rendered]
    if missing:
        raise AssertionError(f"News validation failed: {missing}")


if __name__ == "__main__":
    generate_news_section(Path(__file__).resolve().parent / "site")
