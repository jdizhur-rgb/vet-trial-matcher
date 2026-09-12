"""Apply diagnosis-specific feline decision branches without duplicating page boilerplate.

Feline pages must never inherit canine decision branches just because a diagnosis
name exists in both species. If a reviewed feline guide has no dedicated branch set,
the page intentionally renders without a ``Where are you now?`` block.
"""
from __future__ import annotations

import practical_cancer_pages as pages
from feline_branch_content import FELINE_BRANCHES


def validate_feline_branch_coverage(practical: dict) -> list[str]:
    """Return reviewed feline diagnoses that still need dedicated branch content."""
    return sorted(set(practical) - set(FELINE_BRANCHES))


def activate_feline_branches() -> None:
    original = pages.section

    def section(label, key, pet, practical):
        if pet != 'cat':
            return original(label, key, pet, practical)

        # Never fall through to canine ADDITIONAL_BRANCHES for a cat.
        # A feline-specific branch set is used when reviewed; otherwise suppress
        # the decision-branch block entirely while retaining the feline prognosis,
        # next-step guidance, treatment copy and any relevant tests.
        old = pages.BRANCHES.get(key)
        if key in FELINE_BRANCHES:
            pages.BRANCHES[key] = FELINE_BRANCHES[key]
        else:
            pages.BRANCHES.pop(key, None)
        try:
            return original(label, key, pet, practical)
        finally:
            if old is None:
                pages.BRANCHES.pop(key, None)
            else:
                pages.BRANCHES[key] = old

    pages.section = section
