#!/usr/bin/env python3
"""Validate that generated Help content matches current site features."""
from pathlib import Path


PAGE = Path(__file__).resolve().parent / 'seo' / 'site' / 'help' / 'index.html'


def main() -> None:
    text = PAGE.read_text(encoding='utf-8')
    required = (
        'How do I use the trial finder?',
        'What do the result labels mean?',
        'Can I save or share the results?',
        '<h2>Oncology centers and trial centers</h2>',
        'How do I find oncology care or an ECT center?',
        'What are Trial Centers?',
        'How do I find an online oncology consultation?',
        'This directory does not have ZIP-code distance sorting.',
        'How do I browse trial centers by location?',
        '<h2>Other Treatments</h2>',
        'What is included under Other Treatments?',
        'Is Vet Cancer Care Finder really free?',
        'A clear “no matches” is more useful than showing a study that does not fit.',
        'mailto:info@vettrialfinder.com',
    )
    # Shared sentence-case normalization can run while the shell is assembled.
    # Verify the required content without depending on obsolete Title Case.
    missing = [item for item in required if item.casefold() not in text.casefold()]
    if missing:
        raise AssertionError(f'Help content missing: {missing}')
    details = text.count('<details>')
    if details != 25:
        raise AssertionError(f'Expected 25 Help accordions, found {details}')
    if 'help-actions' in text:
        raise AssertionError('Help page still contains redundant navigation buttons')
    print('HELP_CONTENT_OK details=', details)


if __name__ == '__main__':
    main()
