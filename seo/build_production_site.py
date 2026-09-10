#!/usr/bin/env python3
"""Build the production SEO site with strict validation and production settings."""
from __future__ import annotations

import sys
from pathlib import Path

SEO_DIR = Path(__file__).resolve().parent
if str(SEO_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_DIR))

import center_directory
from production_aliases import apply_aliases
from site_config import DOMAIN, SITE

apply_aliases(center_directory)

# The production build owns the public base URL. Modules importing generate_seo
# share this module object, so every generated canonical/sitemap link uses SITE.
import generate_seo
generate_seo.SITE = SITE

import generate_seo_strict
import generate_cancer_coverage
import ensure_center_images


def main():
    generate_seo_strict.main()
    generate_cancer_coverage.main()
    ensure_center_images.main()
    out = SEO_DIR / "site"
    (out / "CNAME").write_text(f"{DOMAIN}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
