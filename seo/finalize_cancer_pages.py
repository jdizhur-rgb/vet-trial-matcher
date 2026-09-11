#!/usr/bin/env python3
"""Final consistency pass for generated English cancer pages."""
from __future__ import annotations
import re
from pathlib import Path

SUMMARY_COUNT_RE = re.compile(r'<p class="option-count">(?P<count>\d+) option(?:s)? currently in our catalog\.</p>')
ZERO_SUMMARIES = (
    'No active listings in our catalog right now.',
    'No active listings are currently represented in our catalog',
)
CARD_RE = re.compile(r'<article class="card"><h3>')


def _is_english_cancer_page(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).parts
    return len(rel) == 4 and rel[0] in {'north-america', 'uk-europe'} and rel[1] in {'dogs', 'cats'} and rel[3] == 'index.html'


def finalize_cancer_pages(root: Path) -> int:
    root = Path(root)
    checked = 0
    for path in root.rglob('index.html'):
        if not _is_english_cancer_page(path, root):
            continue
        checked += 1
        text = path.read_text(encoding='utf-8')
        cards = len(CARD_RE.findall(text))
        positive = SUMMARY_COUNT_RE.search(text)
        zero = any(summary in text for summary in ZERO_SUMMARIES)

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

    if not checked:
        raise AssertionError('No English cancer pages found for final consistency pass')
    print('CANCER_PAGE_CONSISTENCY_OK', checked)
    return checked


if __name__ == '__main__':
    finalize_cancer_pages(Path(__file__).resolve().parent / 'site')
