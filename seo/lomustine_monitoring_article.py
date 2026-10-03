#!/usr/bin/env python3
"""Generate the practical owner guide to lomustine monitoring."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html


SLUG = "lomustine-ccnu-cbc-monitoring"
URL = f"{SITE}/articles/{SLUG}/"
IMAGE = f"{SITE}/assets/social/lomustine-cbc-monitoring.jpg?v=20261003-2"
CBC_IMAGE = f"{SITE}/assets/social/lomustine-cbc-result.jpg"


def generate_lomustine_monitoring_article(root: Path) -> None:
    title = "Lomustine dose changes are common. Monitoring should be too."
    description = "Nearly half of 1,136 dogs treated with lomustine needed a dose delay or reduction. What owners should know about CBC nadirs, neutropenia and liver monitoring."

    source_assets = Path(__file__).resolve().parent / "assets" / "social"
    built_assets = root / "assets" / "social"
    built_assets.mkdir(parents=True, exist_ok=True)
    for name in ("lomustine-cbc-monitoring.jpg", "lomustine-cbc-result.jpg"):
        shutil.copy2(source_assets / name, built_assets / name)

    body = f'''<article class="article-page news-article">
<p class="eyebrow">Chemotherapy monitoring · October 3, 2026</p>
<h1>{title}</h1>
<figure style="margin:18px 0 24px"><img src="{IMAGE}" alt="A senior dog with an owner while a veterinary professional prepares a blood sample" width="1774" height="887" style="display:block;width:100%;height:auto;border-radius:12px"></figure>
<p>A preliminary study presented at the 2026 Veterinary Cancer Society conference reviewed 1,136 dogs treated with single-agent lomustine, also called CCNU, for lymphoma, mast cell tumor or histiocytic sarcoma. Treatment was delayed, the dose was reduced, or both in <strong>47.7% of dogs</strong>. When a reason was documented, 94.5% of the changes were related to toxicity. Neutropenia accounted for 51.2% and hepatobiliary abnormalities for 36.0%.</p>
<p>That does not mean lomustine is an inappropriate treatment. It means the starting dose is not a promise that every dog can safely continue at the same dose. Bloodwork is how the oncology team learns how that individual dog handles it.</p>

<h2>CBC and the nadir</h2>
<p>A <strong>CBC</strong>, or complete blood count, measures red blood cells, white blood cells and platelets. For chemotherapy monitoring, the absolute neutrophil count is especially important. Neutrophils are white blood cells that help fight bacterial infection.</p>
<p>The <strong>nadir</strong> is the period when blood-cell counts are expected to reach their lowest point after chemotherapy. The 2026 AAHA oncology guidelines say that the CBC nadir after lomustine generally occurs around day 7 in dogs, but it can vary from one to three weeks. The exact schedule should be set by the treating team for that dog and protocol. A dog acting normal at home does not show what the neutrophil count is.</p>

<h2>What low neutrophils mean</h2>
<p>A low neutrophil count is called neutropenia. The lower the count, the less protection the dog has against bacterial infection. Mild neutropenia may require monitoring and a treatment delay rather than antibiotics. The AAHA action plan says that a dog with 1,000–2,000 neutrophils/µL and no fever can usually be monitored; below 1,000/µL, oral antibiotics are recommended. A dog with fever or signs of illness and fewer than 1,500 neutrophils/µL should be hospitalized for intravenous fluids and antibiotics. <strong>Febrile neutropenia is an oncology emergency.</strong> These are clinical guidelines, not instructions to start leftover antibiotics at home.</p>

<figure class="article-captioned" style="margin:22px auto;max-width:720px"><img src="{CBC_IMAGE}" alt="Anonymized CBC excerpt showing WBC 3.50 and neutrophils 0.48 K per microliter, both below the reference range" width="1040" height="810" style="display:block;width:100%;height:auto;border:1px solid #d9e1ea;border-radius:10px"><figcaption>CBC one week after Yasha’s first lomustine dose: neutrophils 0.48 K/µL (480/µL).</figcaption></figure>
<p>This is why the nadir CBC matters in practice. My dog Yasha looked well one week after his first lomustine dose, but his CBC showed grade 4 neutropenia at 480 neutrophils/µL. He received antibiotics, and the next lomustine dose was reduced. Without the scheduled blood test, there was no reliable outward sign that his count had fallen that far.</p>
<p>I recently spoke with another owner whose dog had been switched from CHOP to lomustine through an oncology service. She had not been told to arrange bloodwork around the expected nadir and planned to raise it with the oncologist. There may have been a communication failure or a different intended schedule, but an owner should not have to guess whether and when a post-treatment CBC is needed.</p>

<h2>The monitoring plan to ask for</h2>
<ul>
<li>When should the CBC be checked after each dose, including the expected nadir check?</li>
<li>Which neutrophil result would trigger antibiotics, a delay or a dose reduction?</li>
<li>Which symptoms or temperature require an immediate emergency call?</li>
<li>Can the primary veterinarian draw the CBC and send the result to oncology?</li>
<li>When will a chemistry panel be checked?</li>
</ul>
<p><strong>Liver values must also be monitored throughout lomustine treatment.</strong> Liver injury may appear after earlier tests were normal and can become cumulative with repeated doses. ALT and ALP are among the values commonly followed, but the oncology team should specify the full chemistry schedule.</p>
<p>The practical point is simple: before the first lomustine dose, or immediately when a dog is switched to it, the owner should leave with a written plan for the nadir CBC, liver testing and urgent warning signs, not only the date of the next chemotherapy appointment.</p>

<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> October 3, 2026</p><p><strong>Last updated:</strong> October 3, 2026</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>

<h2>Sources</h2>
<ul class="article-sources">
<li><a href="https://onlinelibrary.wiley.com/doi/full/10.1111/vco.70098" target="_blank" rel="noopener">2026 VCS conference abstracts: multi-institutional lomustine study</a>.</li>
<li><a href="https://www.aaha.org/resources/2026-aaha-oncology-guidelines-for-dogs-and-cats/section-5-therapeutic-interventions/therapeutic-modalities-chemotherapy/" target="_blank" rel="noopener">2026 AAHA oncology guidelines: chemotherapy monitoring and nadir action plan</a>.</li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/32969725/" target="_blank" rel="noopener">Biochemical, functional and histopathologic characterization of lomustine-induced liver injury in dogs</a>.</li>
</ul>
</article>'''

    directory = root / "articles" / SLUG
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(f"{title} | Vet Trial Finder", description, body, URL)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="{g.esc(title)}"><meta property="og:description" content="{g.esc(description)}"><meta property="og:url" content="{URL}"><meta property="og:image" content="{IMAGE}"><meta property="og:image:secure_url" content="{IMAGE}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1774"><meta property="og:image:height" content="887"><meta property="og:image:alt" content="A dog with an owner during a veterinary blood test"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{g.esc(title)}"><meta name="twitter:description" content="{g.esc(description)}"><meta name="twitter:image" content="{IMAGE}">'''
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "image": [IMAGE],
        "datePublished": "2026-10-03",
        "dateModified": "2026-10-03",
        "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"},
        "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"},
        "mainEntityOfPage": URL,
    }
    rendered = rendered.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (directory / "index.html").write_text(wrap_html(rendered), encoding="utf-8")

    index = root / "articles" / "index.html"
    if not index.exists():
        raise AssertionError("Articles index is required before adding the lomustine article")
    index_text = index.read_text(encoding="utf-8")
    if URL not in index_text:
        card = f'''<a class="directory-card" href="{URL}"><strong>{title}</strong><span>What CBC nadirs, neutropenia, dose changes and liver monitoring mean for owners.</span></a>'''
        index_text = index_text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1)
        index.write_text(index_text, encoding="utf-8")

    sitemap = root / "sitemap.xml"
    sitemap_text = sitemap.read_text(encoding="utf-8")
    if URL not in sitemap_text:
        sitemap.write_text(sitemap_text.replace("</urlset>", f"<url><loc>{URL}</loc></url>\n</urlset>"), encoding="utf-8")

    article = (directory / "index.html").read_text(encoding="utf-8")
    required = ("47.7% of dogs", "0.48 K/µL", "Febrile neutropenia is an oncology emergency", '"@type": "Article"', 'property="og:image:type"')
    missing = [marker for marker in required if marker not in article]
    if missing:
        raise AssertionError(f"Lomustine article validation failed: {missing}")


if __name__ == "__main__":
    generate_lomustine_monitoring_article(Path(__file__).resolve().parent / "site")
