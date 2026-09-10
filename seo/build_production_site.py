#!/usr/bin/env python3
"""Build the production SEO site with strict validation and known site aliases."""
from __future__ import annotations

import sys
from pathlib import Path

SEO_DIR = Path(__file__).resolve().parent
if str(SEO_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_DIR))

import center_directory
from production_aliases import apply_aliases

apply_aliases(center_directory)

import generate_seo_strict
import generate_cancer_coverage
import ensure_center_images


def main():
    generate_seo_strict.main()
    generate_cancer_coverage.main()
    ensure_center_images.main()


if __name__ == "__main__":
    main()
