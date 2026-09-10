#!/usr/bin/env python3
"""SEO enhancements for generated veterinary cancer center pages."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from site_config import SITE

CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)">')
H1_RE = re.compile(r'<div class="center-page"><h1>(.*?)</h1>', re.S)
CENTER_ADDRESS_RE = re.compile(r'<div class="center-address">.*?<br>(.*?)</div>', re.S)
CANCERS_RE = re.compile(r'Current opportunities here include research or treatment options for <strong>(.*?)</strong>\.', re.S)
CARD_RE = re.compile(r'<article class="card">')

CSS = r'''
.center-seo-nav{margin:22px 0;padding:16px 18px;background:#fff;border:1px solid #d9e2ea;border-radius:12px}.center-seo-nav h2{font-size:1.12rem;margin:0 0 8px}.center-seo-nav ul{margin:0;padding-left:20px}.center-seo-nav li{margin:.28rem 0}.center-directory-link{margin:12px 0 20px;font-size:.94rem}
'''.strip()


def _plain(value: str) -> str:
    return html.unescape(re.sub(r'<.*?>', '', value)).strip()


def _slug(value: str) -> str:
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', value.lower())).strip('-')


def _json_ld(center: str, desc: str, canonical: str, address: str) -> str:
    org = {
        '@type': 'Organization',
        '@id': canonical + '#organization',
        'name': center,
        'url': canonical,
        'description': desc,
    }
    if address:
        org['address'] = address
    graph = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage',
                '@id': canonical + '#webpage',
                'url': canonical,
                'name': f'{center} Cancer Clinical Trials',
                'description': desc,
                'about': {'@id': canonical + '#organization'},
                'isPartOf': {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Vet Trial Finder'},
            },
            org,
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Vet Trial Finder', 'item': SITE + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Cancer Research Centers', 'item': SITE + '/centers/'},
                    {'@type': 'ListItem', 'position': 3, 'name': center, 'item': canonical},
                ],
            },
        ],
    }
    payload = json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return f'<script type="application/ld+json">{payload}</script>'


def _enhance(text: str) -> tuple[str, bool]:
    canonical_match = CANONICAL_RE.search(text)
    h1_match = H1_RE.search(text)
    if not canonical_match or not h1_match:
        return text, False
    canonical = html.unescape(canonical_match.group(1))
    center = _plain(h1_match.group(1))
    count = len(CARD_RE.findall(text))
    cancers_match = CANCERS_RE.search(text)
    cancers = []
    if cancers_match:
        raw = _plain(cancers_match.group(1))
        if raw.lower() != 'multiple cancer types':
            cancers = [x.strip() for x in raw.split(',') if x.strip()]
    address_match = CENTER_ADDRESS_RE.search(text)
    address = _plain(address_match.group(1).replace('<br>', ', ')) if address_match else ''

    count_phrase = f'{count} current cancer treatment and research option' + ('' if count == 1 else 's')
    cancer_phrase = ', '.join(cancers[:4]) if cancers else 'companion-animal cancers'
    desc = f'Explore {count_phrase} at {center}, including clinical trials and advanced treatment studies for {cancer_phrase}. Free study details and official links.'
    title = f'{center} Cancer Clinical Trials | Vet Trial Finder'
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{html.escape(desc, quote=True)}">', text, count=1, flags=re.S)

    region = 'north-america' if (' · USA<' in text or ' · Canada<' in text) else 'uk-europe'
    if cancers:
        links = ''.join(
            f'<li><a href="{SITE}/{region}/dogs/{_slug(cancer)}/">{html.escape(cancer)} clinical trials for dogs</a></li>'
            for cancer in cancers[:8]
        )
        nav = f'<nav class="center-seo-nav" aria-label="Cancer types at this center"><h2>Explore these cancer types</h2><ul>{links}</ul></nav>'
        anchor = '<h2>Cancer treatment &amp; research options</h2>'
        text = text.replace(anchor, nav + anchor, 1)
    text = text.replace('<p><a class="cta"', f'<p class="center-directory-link"><a href="{SITE}/centers/">← Browse all veterinary cancer research centers</a></p><p><a class="cta"', 1)

    if CSS not in text:
        text = text.replace('</style>', CSS + '</style>', 1)
    text = text.replace('</head>', _json_ld(center, desc, canonical, address) + '</head>', 1)
    return text, True


def enhance_center_pages(root: Path) -> int:
    root = Path(root)
    changed = 0
    centers = root / 'centers'
    for path in centers.glob('*/index.html'):
        old = path.read_text(encoding='utf-8')
        new, ok = _enhance(old)
        if ok and new != old:
            path.write_text(new, encoding='utf-8')
            changed += 1
    if not changed:
        raise AssertionError('Center page enhancement matched no center pages')
    print('CENTER_PAGES_ENHANCED', changed)
    return changed
