"""Compatibility wrapper. HS content now uses the shared cancer-page architecture."""
from pathlib import Path
from cancer_page_polish import install

install()


def apply_canine_hs_guide(root: Path) -> int:
    return 0
