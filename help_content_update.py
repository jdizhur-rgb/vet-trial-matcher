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
        'How do I find an oncologist or ECT center?',
        'What are Trial Centers?',
        'How do I find the nearest trial centers?',
        '<h2>Other Treatments</h2>',
        'What is included under Other Treatments?',
        'A clear “no matches” is more useful than showing a study that does not fit.',
        'mailto:info@vettrialfinder.com',
    )
    missing = [item for item in required if item not in text]
    if missing:
        raise AssertionError(f'Help content missing: {missing}')
    details = text.count('<details>')
    if details != 23:
        raise AssertionError(f'Expected 23 Help accordions, found {details}')
    if 'help-actions' in text:
        raise AssertionError('Help page still contains redundant navigation buttons')
    print('HELP_CONTENT_OK details=', details)


if __name__ == '__main__':
    main()
