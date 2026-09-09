#!/usr/bin/env python3
"""Owner-facing polish for generated English cancer landing pages.

This deliberately post-processes only diagnosis pages. It does not touch the
trial catalog, matcher, URLs/canonicals, translated pages, or center pages.
"""
from __future__ import annotations

import html
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

CSS = r'''
.cancer-page{max-width:860px}.cancer-page h1{font-size:clamp(1.9rem,4.4vw,2.65rem);max-width:780px;margin-bottom:8px}.cancer-page .eyebrow{margin:0 0 22px;color:#607086;font-size:.94rem;font-weight:650;letter-spacing:.01em}.cancer-summary{background:#fff;border:1px solid #d9e2ea;border-radius:14px;padding:17px 19px;margin:18px 0 14px;box-shadow:0 1px 2px rgba(23,36,59,.04)}.cancer-summary .opportunity-count{display:block;font-size:1.22rem;line-height:1.3;margin-bottom:6px}.cancer-summary p{margin:.35rem 0;color:#42536a}.cancer-summary .summary-detail{font-size:.94rem;color:#607086}.cancer-page .free{margin-top:14px}.cancer-page .disease{margin-top:28px}.cancer-page .disease h2{font-size:1.24rem;margin-top:20px}.cancer-page .section-intro{color:#42536a;max-width:760px}.cancer-page .card h3{font-size:1.2rem}@media(max-width:600px){.cancer-page h1{font-size:1.85rem}.cancer-summary{padding:15px 16px}.cancer-page .disease h2{font-size:1.15rem}}
'''.strip()


def _is_english_cancer_page(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).parts
    return (
        len(rel) == 4
        and rel[0] in {'north-america', 'uk-europe'}
        and rel[1] in {'dogs', 'cats'}
        and rel[3] == 'index.html'
    )


def _content_key(label: str) -> str:
    return label.strip().lower()


def _enhance(text: str) -> tuple[str, bool]:
    m = H1_RE.search(text)
    if not m:
        return text, False

    label_html = m.group('label')
    label = html.unescape(re.sub(r'<.*?>', '', label_html))
    species = m.group('species')
    region_html = m.group('region')
    region = html.unescape(region_html)

    lead = LEAD_RE.search(text)
    if not lead:
        return text, False
    count = lead.group('count')

    old_h1 = m.group(0)
    new_h1 = (
        f'<div class="cancer-page"><h1>{label_html} Clinical Trials for {species}</h1>'
        f'<p class="eyebrow">{region_html} · Free cancer trial and treatment search</p>'
    )
    text = text.replace(old_h1, new_h1, 1)

    summary = (
        f'<div class="cancer-summary"><strong class="opportunity-count">{count} current treatment opportunities</strong>'
        f'<p>Clinical trials and advanced cancer treatment studies currently represented in our catalog for {label_html}.</p>'
        '<p class="summary-detail">See locations, key eligibility, costs when provided, contacts and official enrollment links below.</p></div>'
    )
    text = LEAD_RE.sub(summary, text, count=1)

    # Replace the complete educational section from one centrally maintained
    # owner-facing source. This keeps every diagnosis page systematic and avoids
    # hand-editing generated HTML files.
    info = CONTENT.get(_content_key(label))
    if info:
        about, treatment, factors = info
        disease = (
            f'<section class="disease"><h2>About {label_html}</h2><p>{html.escape(about)}</p>'
            f'<h2>How it is usually treated</h2><p>{html.escape(treatment)}</p>'
            f'<h2>What can affect treatment choices</h2><p>{html.escape(factors)}</p></section>'
        )
        text, n = DISEASE_RE.subn(disease, text, count=1)
        if n != 1:
            raise AssertionError(f'Could not replace disease section for {label}')
    else:
        # Fail rather than silently leave a newly introduced cancer with the old
        # generic copy. New canonical cancers must receive reviewed owner copy.
        raise AssertionError(f'Missing owner-facing cancer content for {label}')

    text = text.replace(
        '<h2>Treatment &amp; research</h2><p>Below are treatment-focused clinical trials and advanced oncology options currently represented in our live catalog.</p>',
        '<h2>Current clinical trials &amp; treatment options</h2><p class="section-intro">Browse the current listings below, then use the free matcher to check the study-specific criteria against your pet’s diagnosis and situation.</p>',
        1,
    )

    text = text.replace('</main>', '</div></main>', 1)

    title = f'{label} Clinical Trials for {species} | Free Pet Cancer Trial Finder'
    desc = (
        f'Find current {label} clinical trials and cancer treatment studies for {species.lower()} '
        f'in {region}. Free access to eligibility, locations, contacts and official enrollment links.'
    )
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.S)
    text = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{html.escape(desc, quote=True)}">',
        text,
        count=1,
        flags=re.S,
    )

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
