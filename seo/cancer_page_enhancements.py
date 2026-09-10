#!/usr/bin/env python3
"""Owner-facing polish for generated English cancer landing pages.

This deliberately post-processes only diagnosis pages. It does not touch the
trial catalog, matcher, URLs/canonicals, translated pages, or center pages.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from cancer_owner_content import CONTENT

H1_RE = re.compile(
    r'<h1>(?P<label>.+?): Clinical Trials and Cancer Treatment Studies for '
    r'(?P<species>Dogs|Cats) in (?P<region>USA &amp; Canada|UK &amp; Europe)</h1>'
)
LEAD_RE = re.compile(
    r'<p class="lead">(?P<count>\d+) current treatment opportunities in our catalog\. '
    r'Trial names, locations and official source links are shown below\.</p>'
)
DISEASE_RE = re.compile(r'<section class="disease">.*?</section>', re.S)
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)">')

RELATED = {
    'histiocytic sarcoma': ('soft tissue sarcoma', 'hemangiosarcoma', 'lymphoma'),
    'lymphoma': ('leukemia', 'multiple myeloma'),
    'mast cell tumor': ('soft tissue sarcoma', 'melanoma'),
    'soft tissue sarcoma': ('histiocytic sarcoma', 'osteosarcoma', 'hemangiosarcoma'),
    'hemangiosarcoma': ('soft tissue sarcoma', 'histiocytic sarcoma'),
    'osteosarcoma': ('soft tissue sarcoma',),
    'oral melanoma': ('melanoma', 'oral squamous cell carcinoma', 'squamous cell carcinoma'),
    'melanoma': ('oral melanoma', 'mast cell tumor'),
    'oral squamous cell carcinoma': ('squamous cell carcinoma', 'oral melanoma'),
    'squamous cell carcinoma': ('oral squamous cell carcinoma', 'oral melanoma'),
    'urothelial carcinoma': ('prostate cancer',),
    'prostate cancer': ('urothelial carcinoma',),
    'glioma': ('meningioma',),
    'meningioma': ('glioma',),
    'hepatocellular carcinoma': ('primary lung tumor',),
    'primary lung tumor': ('hepatocellular carcinoma',),
    'mammary carcinoma': ('soft tissue sarcoma',),
    'thyroid carcinoma': ('chemodectoma',),
    'chemodectoma': ('thyroid carcinoma',),
    'leukemia': ('lymphoma', 'multiple myeloma'),
    'multiple myeloma': ('lymphoma', 'leukemia'),
    'nasal tumor': ('squamous cell carcinoma',),
}

CSS = r'''
.cancer-page{max-width:860px}.cancer-page h1{font-size:clamp(1.9rem,4.4vw,2.65rem);max-width:780px;margin-bottom:8px}.cancer-page .eyebrow{margin:0 0 22px;color:#607086;font-size:.94rem;font-weight:650;letter-spacing:.01em}.cancer-summary{background:#fff;border:1px solid #d9e2ea;border-radius:14px;padding:17px 19px;margin:18px 0 14px;box-shadow:0 1px 2px rgba(23,36,59,.04)}.cancer-summary .opportunity-count{display:block;font-size:1.22rem;line-height:1.3;margin-bottom:6px}.cancer-summary p{margin:.35rem 0;color:#42536a}.cancer-summary .summary-detail{font-size:.94rem;color:#607086}.cancer-page .free{margin-top:14px}.cancer-page .disease{margin-top:28px}.cancer-page .disease h2{font-size:1.24rem;margin-top:20px}.cancer-page .section-intro{color:#42536a;max-width:760px}.cancer-page .card h3{font-size:1.2rem}.related-cancers{margin:30px 0 4px;padding:18px 20px;background:#fff;border:1px solid #d9e2ea;border-radius:14px}.related-cancers h2{margin:0 0 9px;font-size:1.18rem}.related-cancers ul{margin:0;padding-left:20px}.related-cancers li{margin:.3rem 0}@media(max-width:600px){.cancer-page h1{font-size:1.85rem}.cancer-summary{padding:15px 16px}.cancer-page .disease h2{font-size:1.15rem}.related-cancers{padding:15px 16px}}
'''.strip()


def _is_english_cancer_page(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).parts
    return len(rel) == 4 and rel[0] in {'north-america', 'uk-europe'} and rel[1] in {'dogs', 'cats'} and rel[3] == 'index.html'


def _content_key(label: str) -> str:
    return label.strip().lower()


def _display(key: str) -> str:
    return ' '.join(w.upper() if w in {'scc', 'aml'} else w.capitalize() for w in key.split())


def _slug(key: str) -> str:
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', key.lower())).strip('-')


def _json_ld(title: str, desc: str, canonical: str, label: str, species: str, region: str) -> str:
    root = canonical.split('/north-america/', 1)[0] if '/north-america/' in canonical else canonical.split('/uk-europe/', 1)[0]
    region_path = 'north-america' if 'USA' in region else 'uk-europe'
    species_path = species.lower()
    graph = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage',
                '@id': canonical + '#webpage',
                'url': canonical,
                'name': title,
                'description': desc,
                'about': {'@type': 'Thing', 'name': label},
                'isPartOf': {'@type': 'WebSite', '@id': root + '/#website', 'url': root + '/', 'name': 'Vet Trial Finder'},
            },
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Vet Trial Finder', 'item': root + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': region, 'item': f'{root}/{region_path}/'},
                    {'@type': 'ListItem', 'position': 3, 'name': species, 'item': f'{root}/{region_path}/{species_path}/'},
                    {'@type': 'ListItem', 'position': 4, 'name': label, 'item': canonical},
                ],
            },
        ],
    }
    payload = json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return f'<script type="application/ld+json">{payload}</script>'


def _enhance(text: str) -> tuple[str, bool]:
    m = H1_RE.search(text)
    if not m:
        return text, False
    label_html = m.group('label')
    label = html.unescape(re.sub(r'<.*?>', '', label_html))
    key = _content_key(label)
    species = m.group('species')
    region_html = m.group('region')
    region = html.unescape(region_html)
    lead = LEAD_RE.search(text)
    canonical_match = CANONICAL_RE.search(text)
    if not lead or not canonical_match:
        return text, False
    count = lead.group('count')
    canonical = html.unescape(canonical_match.group(1))

    text = text.replace(m.group(0), f'<div class="cancer-page"><h1>{label_html} Clinical Trials for {species}</h1><p class="eyebrow">{region_html} · Free cancer trial and treatment search</p>', 1)

    if count == '0':
        summary = '<div class="cancer-summary"><strong class="opportunity-count">No current treatment opportunities in our catalog</strong>'+f'<p>We do not currently have an active {label_html} trial or advanced treatment listing for this species and region.</p>'+'<p class="summary-detail">The cancer information on this page remains available, and new studies can be added here when enrollment opens.</p></div>'
    else:
        summary = f'<div class="cancer-summary"><strong class="opportunity-count">{count} current treatment opportunities</strong>'+f'<p>Clinical trials and advanced cancer treatment studies currently represented in our catalog for {label_html}.</p>'+'<p class="summary-detail">See locations, key eligibility, costs when provided, contacts and official enrollment links below.</p></div>'
    text = LEAD_RE.sub(summary, text, count=1)

    info = CONTENT.get(key)
    if info:
        about, treatment, factors = info
        disease = f'<section class="disease"><h2>About {label_html}</h2><p>{html.escape(about)}</p>'+f'<h2>How it is usually treated</h2><p>{html.escape(treatment)}</p>'+f'<h2>What can affect treatment choices</h2><p>{html.escape(factors)}</p></section>'
        text, n = DISEASE_RE.subn(disease, text, count=1)
        if n != 1:
            raise AssertionError(f'Could not replace disease section for {label}')
    else:
        raise AssertionError(f'Missing owner-facing cancer content for {label}')

    disease_match = DISEASE_RE.search(text)
    if disease_match:
        disease_block = disease_match.group(0)
        text = text[:disease_match.start()] + text[disease_match.end():]
        anchor = text.find('<div class="cancer-summary">')
        if anchor < 0:
            raise AssertionError(f'Could not locate cancer summary for {label}')
        text = text[:anchor] + disease_block + text[anchor:]

    research_intro = ('<h2>Current clinical trials &amp; treatment options</h2><p class="section-intro">No active listings are currently represented in our catalog for this species and region. We keep this page available so new opportunities can appear here when they open.</p>' if count == '0' else '<h2>Current clinical trials &amp; treatment options</h2><p class="section-intro">Browse the current listings below, then use the free matcher to check the study-specific criteria against your pet’s diagnosis and situation.</p>')
    text = text.replace('<h2>Treatment &amp; research</h2><p>Below are treatment-focused clinical trials and advanced oncology options currently represented in our live catalog.</p>', research_intro, 1)

    related = RELATED.get(key, ())
    if related:
        prefix = canonical.rstrip('/').rsplit('/', 1)[0]
        links = ''.join(f'<li><a href="{html.escape(prefix + "/" + _slug(x) + "/", quote=True)}">{html.escape(_display(x))}</a></li>' for x in related)
        related_html = f'<nav class="related-cancers" aria-label="Related cancer types"><h2>Related cancer types</h2><ul>{links}</ul></nav>'
        text = text.replace('</main>', related_html + '</div></main>', 1)
    else:
        text = text.replace('</main>', '</div></main>', 1)

    title = f'{label} Clinical Trials for {species} | Vet Trial Finder'
    if count == '0':
        desc = f'Learn about {label} in {species.lower()}, common treatment approaches and factors that affect care. Check Vet Trial Finder for new clinical trials and treatment studies.'
    else:
        noun = 'option' if count == '1' else 'options'
        desc = f'Find {count} current {label} clinical trial and treatment {noun} for {species.lower()} in {region}. Free eligibility details, locations, contacts and official links.'
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{html.escape(desc, quote=True)}">', text, count=1, flags=re.S)
    text = text.replace('</head>', _json_ld(title, desc, canonical, label, species, region) + '</head>', 1)
    if CSS not in text:
        text = text.replace('</style>', CSS + '</style>', 1)
    return text, True


def enhance_cancer_pages(root: Path) -> int:
    root = Path(root)
    changed = 0
    for path in root.rglob('index.html'):
        if not _is_english_cancer_page(path, root):
            continue
        old = path.read_text(encoding='utf-8')
        new, ok = _enhance(old)
        if ok and new != old:
            path.write_text(new, encoding='utf-8')
            changed += 1
    if not changed:
        raise AssertionError('Cancer page enhancement matched no English diagnosis pages')
    print('CANCER_PAGES_ENHANCED', changed)
    return changed
