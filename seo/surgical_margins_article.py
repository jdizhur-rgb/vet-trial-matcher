#!/usr/bin/env python3
"""Generate the owner-facing article about surgical margins after tumor removal."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html


def generate_surgical_margins_article(root: Path) -> None:
    url = f"{SITE}/articles/surgical-margins-after-tumor-removal/"
    body = f'''<article class="article-page">
<h1>Clean, Close, and Dirty Margins After Tumor Removal</h1>

<p>Surgical margins show how close tumor cells are to the edge of the tissue that was removed. To evaluate them, a pathologist inks the outer surface of the specimen, takes sections from selected areas, and examines them under a microscope. Lateral margins are the margins around the tumor, while the deep margin is the margin beneath it. The deep margin may consist of subcutaneous tissue, fascia, muscle, or bone.</p>

<figure class="article-hero margin-diagram"><img src="{SITE}/assets/surgical-margins-diagram.jpg" alt="Diagram comparing clean, close, and positive surgical margins" width="1200" height="675"><figcaption><span><strong>Clean margin</strong>Tumor cells remain well away from the inked edge.</span><span><strong>Close margin</strong>Tumor cells are near the edge but do not reach it.</span><span><strong>Positive margin (dirty margin)</strong>Tumor cells reach the inked edge.</span></figcaption></figure>

<p>A pathologist does not examine every cell across the entire surface of the specimen, but representative sections. Margin assessment is therefore not absolute. The result also depends on whether the tissue was removed in one piece, whether it was damaged, and whether the surgeon marked the location of important areas. If the specimen is fragmented or not oriented, it may be impossible to determine which specific margin is close or infiltrated.</p>

<h2>Clean, close, and dirty margins</h2>

<p>A clean, negative, or complete margin means that tumor cells do not reach the inked surface in the sections examined. This is associated with a lower risk of local recurrence, but it does not guarantee that no tumor cells remain in the body. Margin status describes only the surgical site and says nothing about possible metastases.</p>

<p>A close margin means that there is tumor-free tissue between the tumor cells and the inked surface, but the distance is small. There is no single veterinary definition of a close margin. Studies and pathology laboratories use different cutoff values, and many reports simply state the distance in millimeters. For this reason, “tumor cells are less than one millimeter from the margin” and “tumor cells extend to the margin” are not equivalent. In the first case, the margin is technically free of tumor; in the second, it is infiltrated.</p>

<p>The distance is interpreted together with the type of tissue and the biology of the tumor. Fascia may provide a more reliable anatomical barrier than loose subcutaneous tissue. A close margin in a low-grade tumor does not always require additional treatment, while the same distance in an infiltrative tumor may be more concerning.</p>

<p>A dirty, positive, incomplete, or infiltrated margin means that tumor cells reach the inked surface in at least one of the sections examined. This indicates a higher probability that microscopic tumor cells may remain in the surgical field. However, the pathologist examines the removed specimen, not the tissue left in the body, and therefore cannot confirm that residual tumor is present or determine how much remains.</p>

<h2>What margins tell us about recurrence risk</h2>

<p>Margin status is associated with the probability of local recurrence, but it cannot predict exactly what will happen in an individual animal. In a study of dogs with cutaneous and subcutaneous soft tissue sarcomas, the estimated local recurrence rate at three years was 7 percent with tumor-free margins, 23 percent with clean but close margins, and 42 percent with infiltrated margins. The risk increased as the tumor approached the excision line, but recurrence did not occur in every animal with dirty margins and sometimes occurred after complete excision.</p>

<p>These figures cannot be applied to other tumors. The significance of a margin depends on the diagnosis, grade, growth pattern, and anatomical location. It is especially important to know which margin is infiltrated. A positive lateral margin on the skin side may sometimes be widened with a relatively limited repeat surgery. A positive deep margin toward the chest wall, a joint, or a major blood vessel may require a much more extensive procedure.</p>

<p>Margin status describes the completeness of local excision. It does not replace the tumor grade, mitotic count, or stage and cannot be used to assess the risk of metastasis.</p>

<p>The absence of a visible tumor on radiographs, ultrasound, or CT does not change the margin status. Diagnostic imaging can detect lesions of a certain size, but not individual cells in the surgical field.</p>

<p>Margin status provides important information about how completely the tumor was removed and the risk that it will return at the surgical site. But this finding alone is not enough to decide whether repeat surgery, radiation therapy, or observation is appropriate. Further decisions require the margins to be considered together with the tumor type, grade, mitotic activity, stage, location, and the animal’s overall condition.</p>

<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 16, 2026</p><p><strong>Last updated:</strong> September 16, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and a dog owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance and information from veterinary hospitals and research teams.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>

<h2>Sources</h2>
<ul class="article-sources"><li><a href="https://pubmed.ncbi.nlm.nih.gov/33331059/" rel="noopener">Abrams BE, et al. Variability in tumor margin reporting for soft tissue sarcoma and cutaneous mast cell tumors in dogs</a>. Veterinary Surgery. 2021.</li><li><a href="https://pubmed.ncbi.nlm.nih.gov/21139143/" rel="noopener">Dennis MM, et al. Prognostic factors for cutaneous and subcutaneous soft tissue sarcomas in dogs</a>. Veterinary Pathology. 2011.</li><li><a href="https://pubmed.ncbi.nlm.nih.gov/34438827/" rel="noopener">Scarpa F, et al. Surgical Margins in Canine Cutaneous Soft Tissue Sarcomas</a>. Animals. 2021.</li></ul>
</article>'''

    directory = root / 'articles' / 'surgical-margins-after-tumor-removal'
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(
        'Clean, Close, and Dirty Surgical Margins | Vet Trial Finder',
        'What clean, close, and dirty surgical margins mean after tumor removal in dogs and cats, and what margins can and cannot tell you about recurrence risk.',
        body,
        url,
    )
    styles = '''<style>.margin-diagram figcaption{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:10px}.margin-diagram figcaption span{display:block;text-align:center;line-height:1.35}.margin-diagram figcaption strong{display:block;color:#315f7d;font-size:.9rem;margin-bottom:3px}@media(max-width:560px){.margin-diagram figcaption{gap:7px}.margin-diagram figcaption span{font-size:.65rem}.margin-diagram figcaption strong{font-size:.7rem}}</style>'''
    rendered = rendered.replace('</head>', styles + '</head>', 1)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="Clean, Close, and Dirty Surgical Margins"><meta property="og:description" content="What surgical margins mean after tumor removal and what they can and cannot tell you about recurrence risk."><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/surgical-margins-diagram.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="675"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Clean, Close, and Dirty Surgical Margins"><meta name="twitter:description" content="What surgical margins mean after tumor removal and what they can and cannot tell you about recurrence risk."><meta name="twitter:image" content="{SITE}/assets/surgical-margins-diagram.jpg">'''
    rendered = rendered.replace('</head>', social + '</head>', 1)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': 'Clean, Close, and Dirty Margins After Tumor Removal',
        'image': [f'{SITE}/assets/surgical-margins-diagram.jpg'],
        'datePublished': '2026-09-16',
        'dateModified': '2026-09-16',
        'author': {'@type': 'Person', 'name': 'Yuliia Dizhur', 'url': f'{SITE}/about/', 'jobTitle': 'Founder of Vet Trial Finder'},
        'publisher': {'@type': 'Organization', 'name': 'Vet Trial Finder', 'url': f'{SITE}/'},
        'mainEntityOfPage': url,
    }
    rendered = rendered.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (directory / 'index.html').write_text(wrap_html(rendered), encoding='utf-8')

    index = root / 'articles' / 'index.html'
    if not index.exists():
        raise AssertionError('Articles index is required before adding the surgical-margins article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = f'''<a class="directory-card" href="{url}"><strong>Clean, Close, and Dirty Surgical Margins</strong><span>What margins mean after tumor removal and what they can — and cannot — tell you about recurrence risk.</span></a>'''
        if '<div class="directory-grid">' not in text:
            raise AssertionError('Articles index is missing the directory-grid container')
        text = text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1)
        index.write_text(text, encoding='utf-8')

    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        text = sitemap.read_text(encoding='utf-8')
        if url not in text:
            text = text.replace('</urlset>', f'<url><loc>{url}</loc></url></urlset>')
            sitemap.write_text(text, encoding='utf-8')

    article = (directory / 'index.html').read_text(encoding='utf-8')
    required = (
        '<h1 class="page-title">Clean, Close, and Dirty Margins After Tumor Removal</h1>',
        'A close margin means',
        'estimated local recurrence rate at three years was 7 percent',
        'this finding alone is not enough to decide',
        'Reviewed and edited by:',
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in required if marker not in article]
    if missing:
        raise AssertionError(f'Surgical-margins article validation failed: {missing}')


def main() -> None:
    generate_surgical_margins_article(Path(__file__).resolve().parent / 'site')


if __name__ == '__main__':
    main()
