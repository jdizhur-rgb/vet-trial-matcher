#!/usr/bin/env python3
"""Build the production SEO site with strict validation and production settings."""
from __future__ import annotations

import re
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
from center_page_enhancements import enhance_center_pages
from finalize_cancer_pages import finalize_cancer_pages
from help_center import generate_help_center
from about_page import generate_about_page
from site_shell import apply_site_shell
from about_site_integration import integrate_about


def main():
    generate_seo_strict.main()
    enhance_center_pages(SEO_DIR / "site")
    finalize_cancer_pages(SEO_DIR / "site")
    generate_cancer_coverage.main()
    generate_help_center(SEO_DIR / "site")
    generate_about_page(SEO_DIR / "site")
    ensure_center_images.main()
    out = SEO_DIR / "site"
    apply_site_shell(out)
    home = out / "index.html"
    if home.exists():
        text = home.read_text(encoding="utf-8")
        text = re.sub(r'<section class="share-panel">.*?</section>', '', text, count=1, flags=re.S)
        home.write_text(text, encoding="utf-8")
    integrate_about(out)
    (out / "CNAME").write_text(f"{DOMAIN}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
