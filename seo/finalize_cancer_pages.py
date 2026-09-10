#!/usr/bin/env python3
"""Final consistency pass for generated English cancer pages.

Keeps the rendered availability summary synchronized with the actual trial cards
and removes duplicate empty-state messaging. This runs after the normal cancer
page enhancement step and fails the build if counts disagree.
"""
from __future__ import annotations

import re
from pathlib import Path

SUMMARY_COUNT_RE = re.compile(r'<strong class="opportunity-count">(?P<count>\d+) current treatment opportunities</strong>')
ZERO_SUMMARY = 'No current treatment opportunities in our catalog'
CARD_RE = re.compile(r'<article class="card"><h3>')
ZERO_SECTION = (
    '<h2>Current clinical trials &amp; treatment options</h2>'
    '<p class="section-intro">No active listings are currently represented in our catalog for this species and region. '
    'We keep this page available so new opportunities can appear here when they open.</p>'
)


def _is_english_cancer_page(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).parts
    return len(rel) == 4 and rel[0] in {'north-america', 'uk-europe'} and rel[1] in {'dogs', 'cats'} and rel[3] == 'index.html'


def finalize_cancer_pages(root: Path) -> int:
    root = Path(root)
    checked = 0
    changed = 0
    for path in root.rglob('index.html'):
        if not _is_english_cancer_page(path, root):
            continue
        checked += 1
        text = path.read_text(encoding='utf-8')
        cards = len(CARD_RE.findall(text))
        positive = SUMMARY_COUNT_RE.search(text)
        zero = ZERO_SUMMARY in text

        if cards:
            if not positive:
                raise AssertionError(f'{path}: {cards} trial cards but no positive availability summary')
            declared = int(positive.group('count'))
            if declared != cards:
                raise AssertionError(f'{path}: summary says {declared}, rendered cards={cards}')
            if zero:
                raise AssertionError(f'{path}: positive trial cards rendered with zero-state summary')
        else:
            if positive:
                raise AssertionError(f'{path}: positive availability summary but no trial cards')
            if not zero:
                raise AssertionError(f'{path}: no trial cards and no explicit zero-state summary')
            # The summary already explains that there are no current listings;
            # do not repeat the same information in a second empty-state block.
            new = text.replace(ZERO_SECTION, '', 1)
            if new != text:
                path.write_text(new, encoding='utf-8')
                text = new
                changed += 1
            if ZERO_SECTION in text:
                raise AssertionError(f'{path}: duplicate zero-state section survived finalization')

    if not checked:
        raise AssertionError('No English cancer pages found for final consistency pass')
    print('CANCER_PAGE_CONSISTENCY_OK', checked, 'ZERO_STATE_DEDUPED', changed)
    return checked


if __name__ == '__main__':
    finalize_cancer_pages(Path(__file__).resolve().parent / 'site')
