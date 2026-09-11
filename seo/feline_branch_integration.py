"""Apply diagnosis-specific feline decision branches without mixing canine logic."""
from __future__ import annotations

import practical_cancer_pages as pages
from feline_branch_content import FELINE_BRANCHES


def validate_feline_branch_coverage(practical: dict) -> list[str]:
    """Return diagnoses that do not yet have a feline-specific decision branch.

    Missing branch copy must never take the production site down. Those diagnoses
    continue to use the existing reviewed practical guide until dedicated branch
    content is added.
    """
    return sorted(set(practical) - set(FELINE_BRANCHES))


def _feline_section(label, key, pet, practical):
    return pages.build_section(label, key, pet, practical, FELINE_BRANCHES[key])


def activate_feline_branches() -> None:
    original = pages.section

    def section(label, key, pet, practical):
        if pet == 'cat' and key in FELINE_BRANCHES:
            return _feline_section(label, key, pet, practical)
        return original(label, key, pet, practical)

    pages.section = section
