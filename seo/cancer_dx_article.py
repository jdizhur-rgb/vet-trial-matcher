#!/usr/bin/env python3
"""Generate the owner-facing article about IDEXX Cancer Dx screening."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

IDEXX_PAGE = "https://www.idexx.com/en/veterinary/reference-laboratories/cancer-screening/"
IDEXX_EVIDENCE = "https://www.idexx.com/en/veterinary/reference-laboratories/cancer-screening/medical-evidence/"
IDEXX_MCT = "https://ir.idexx.com/news-events/press-releases/detail/403/idexx-advances-the-future-of-veterinary-cancer-care-with-comprehensive-mast-cell-tumor-testing-for-dogs"
IDEXX_INVESTOR_DAY = "https://ir.idexx.com/news-events/ir-calendar/detail/20260813-idexx-investor-day-2026"
IDEXX_IMAGE = "https://www.idexx.com/media/filer_public_thumbnails/filer_public/28/83/28835924-79db-4e63-9c8f-da62871c7819/cancer-dx-masthead.jpg__1000x1000_q80_subsampling-2.jpg"


def generate_cancer_dx_article(root: Path) -> None:
    url = f"{SITE}/articles/cancer-dx-screening-older-dogs/"
    title = "Cancer screening from a routine blood draw"
    description = "What IDEXX Cancer Dx can and cannot tell owners of older dogs, and why the planned hemangiosarcoma addition is worth watching."
    body = f'''<article class="article-page">
<h1>{title}</h1>

<figure class="article-hero"><img src="{IDEXX_IMAGE}" alt="IDEXX Cancer Dx canine cancer screening" width="1000" height="1000" style="display:block;width:100%;height:auto;border-radius:12px"><figcaption>Official IDEXX Cancer Dx image. Source: IDEXX.</figcaption></figure>

<p>IDEXX has expanded its Cancer Dx blood test. It started with lymphoma, mast cell tumor detection was added in September 2026, and hemangiosarcoma is expected to join the panel in December.</p>

<p>For owners of older dogs, this is worth watching.</p>

<p>Cancer Dx can be added to routine senior bloodwork when samples are sent to an IDEXX Reference Laboratory. It does not require a separate blood draw. The idea is simple: look for cancer-associated biomarker patterns in dogs that may still appear completely healthy.</p>

<p>For lymphoma, IDEXX reports about 79% sensitivity and 99% specificity. So this is not a test that can rule out lymphoma. Some cases will be missed. But a positive result is uncommon in dogs without the disease.</p>

<p>There are also early data showing that the lymphoma signal can sometimes appear months before a dog is clinically diagnosed. IDEXX mentions detection as much as six to eight months earlier in some cases. “Up to eight months,” however, should not be read as the usual result. We still need more prospective data to know how useful that lead time is in everyday practice.</p>

<p>The mast cell tumor component is new, so there is much less clinical information available so far. That matters because many MCTs can simply be found on examination and sampled with a needle. We will need to see how often the blood test finds clinically important tumors that otherwise would have been missed.</p>

<h2>Hemangiosarcoma may be the more interesting addition</h2>

<p>A dog with splenic or cardiac HSA can look perfectly well while a tumor grows internally. Sometimes the first obvious sign is a bleed. A blood test capable of finding these dogs before that happens could have real practical value.</p>

<p>But that is also where the evidence will matter most.</p>

<p>Detecting a dog that already has a large splenic tumor is one thing. Detecting a small HSA in an apparently healthy dog early enough to change the outcome is another. We do not yet have the performance data for the new HSA component to know how well Cancer Dx will do this.</p>

<p>And a positive blood test is not a diagnosis or a map. If an HSA result comes back positive, the next step would still be to look for the disease, most likely with abdominal ultrasound and, depending on the situation, cardiac or other imaging.</p>

<p>Cancer Dx also does <strong>not</strong> mean that a negative result equals “no cancer.” It only screens for the cancers currently included in the panel. It will not rule out osteosarcoma, soft tissue sarcoma, histiocytic sarcoma or many other cancers.</p>

<p>That is why we see its current value mainly as an addition to senior screening, not a replacement for examination, imaging or investigating something that looks suspicious.</p>

<p>For an older dog already having regular bloodwork, adding a reasonably priced cancer screen is an interesting option. As the panel expands, it may become considerably more useful.</p>

<p>We are particularly interested in the hemangiosarcoma addition expected in December. Once IDEXX releases the validation data, we will look at how well it performs in apparently healthy dogs — not just dogs that already have obvious cancer — and update this article.</p>

<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 29, 2026</p><p><strong>Last updated:</strong> September 29, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and a dog owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance and information from veterinary hospitals and research teams.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>

<h2>Sources</h2>
<ul class="article-sources">
<li><a href="{IDEXX_PAGE}" rel="noopener">IDEXX Cancer Dx testing</a>. Current panel, screening population and performance information.</li>
<li><a href="{IDEXX_EVIDENCE}" rel="noopener">IDEXX Cancer Dx medical evidence</a>. Lymphoma validation and early-detection evidence.</li>
<li><a href="{IDEXX_MCT}" rel="noopener">IDEXX announcement on mast cell tumor detection</a>. 2026 panel expansion.</li>
<li><a href="{IDEXX_INVESTOR_DAY}" rel="noopener">IDEXX Investor Day 2026</a>. Cancer Dx expansion plans.</li>
</ul>
</article>'''

    directory = root / "articles" / "cancer-dx-screening-older-dogs"
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(f"{title} | Vet Trial Finder", description, body, url)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="{g.esc(title)}"><meta property="og:description" content="{g.esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{IDEXX_IMAGE}"><meta property="og:image:secure_url" content="{IDEXX_IMAGE}"><meta property="og:image:width" content="1000"><meta property="og:image:height" content="1000"><meta property="og:image:alt" content="IDEXX Cancer Dx canine cancer screening"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{g.esc(title)}"><meta name="twitter:description" content="{g.esc(description)}"><meta name="twitter:image" content="{IDEXX_IMAGE}">'''
    rendered = rendered.replace("</head>", social + "</head>", 1)
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "image": [IDEXX_IMAGE],
        "datePublished": "2026-09-29",
        "dateModified": "2026-09-29",
        "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/", "jobTitle": "Founder of Vet Trial Finder"},
        "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"},
        "mainEntityOfPage": url,
    }
    rendered = rendered.replace("</head>", f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (directory / "index.html").write_text(wrap_html(rendered), encoding="utf-8")

    index = root / "articles" / "index.html"
    if not index.exists():
        raise AssertionError("Articles index is required before adding Cancer Dx article")
    text = index.read_text(encoding="utf-8")
    if url not in text:
        card = f'''<a class="directory-card" href="{url}"><strong>Cancer screening from a routine blood draw</strong><span>What Cancer Dx can and cannot tell owners of older dogs, and why the planned HSA addition is worth watching.</span></a>'''
        text = text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1)
        index.write_text(text, encoding="utf-8")

    sitemap = root / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        if url not in text:
            text = text.replace("</urlset>", f"<url><loc>{url}</loc></url>\n</urlset>")
            sitemap.write_text(text, encoding="utf-8")

    article = (directory / "index.html").read_text(encoding="utf-8")
    required = (title, "79% sensitivity and 99% specificity", "Hemangiosarcoma may be the more interesting addition", 'property="og:image"', IDEXX_IMAGE, "Reviewed and edited by:")
    missing = [marker for marker in required if marker not in article]
    if missing:
        raise AssertionError(f"Cancer Dx article validation failed: {missing}")


if __name__ == "__main__":
    generate_cancer_dx_article(Path(__file__).resolve().parent / "site")
