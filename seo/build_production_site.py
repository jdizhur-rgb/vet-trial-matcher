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
# The matcher URL is also overridden here so SEO-only URL changes never touch
# the isolated Streamlit production branch or matcher runtime.
import generate_seo
generate_seo.SITE = SITE
generate_seo.FINDER = "https://c-trials.streamlit.app/"

import generate_seo_strict
import generate_cancer_coverage
import ensure_center_images
from center_page_enhancements import enhance_center_pages
from finalize_cancer_pages import finalize_cancer_pages
from practical_cancer_pages import apply_practical_cancer_guides, apply_feline_practical_guides
from feline_practical_content import FELINE_PRACTICAL
from feline_practical_more import FELINE_MORE
from feline_branch_integration import activate_feline_branches
from hs_owner_page import apply_canine_hs_guide
from help_center import generate_help_center
from about_page import generate_about_page
from site_shell import apply_site_shell
from about_site_integration import integrate_about

# Keep location presentation consistent across treatment cards. The strict
# renderer prefers a verified full street address. If a record's center name is
# an alias (for example, a program name such as "Penn Vet ..."), resolve it to
# the canonical institution and use the directory address. If no verified
# street address is available, still show the best city/state/country location
# instead of omitting the Location block entirely.
_strict_row_locations = generate_seo_strict.row_locations


def _production_row_locations(row):
    locations = _strict_row_locations(row)
    if locations:
        return locations

    country = str(row.get("country") or "").strip()
    center = str(row.get("center") or "").strip()
    canonical = generate_seo_strict.canonical_center(center) if center else None

    for name in (canonical, center):
        if not name:
            continue
        address = center_directory.address_for(name)
        if address:
            return [address]

    for site in row.get("sites", []) if isinstance(row.get("sites"), list) else []:
        if not generate_seo_strict.site_active(site):
            continue
        city = str(site.get("city") or "").strip()
        state = str(site.get("state") or "").strip()
        place = ", ".join(x for x in (city, state, country) if x)
        if place:
            name = str(site.get("hospital") or site.get("name") or "").strip()
            return [f"{name}, {place}" if name else place]

    city = str(row.get("city") or "").strip()
    state = str(row.get("state") or "").strip()
    place = ", ".join(x for x in (city, state, country) if x)
    if place:
        return [place]
    return [country] if country else []


generate_seo_strict.row_locations = _production_row_locations

# Keep rare feline diagnoses in a separate evidence file so sparse feline data
# are never silently replaced with canine outcome figures. Missing dedicated
# decision branches fall back to the existing reviewed practical guide.
FELINE_PRACTICAL.update(FELINE_MORE)
activate_feline_branches()


def main():
    generate_seo_strict.main()
    enhance_center_pages(SEO_DIR / "site")
    finalize_cancer_pages(SEO_DIR / "site")
    apply_practical_cancer_guides(SEO_DIR / "site")
    apply_feline_practical_guides(SEO_DIR / "site")
    apply_canine_hs_guide(SEO_DIR / "site")
    generate_cancer_coverage.main()
    generate_help_center(SEO_DIR / "site")
    generate_about_page(SEO_DIR / "site")
    ensure_center_images.main()
    out = SEO_DIR / "site"
    # Safety guard: only independently reviewed feline diagnoses may use the owner guide.
    for feline in out.glob("*/cats/*/index.html"):
        key=feline.parent.name.replace('-', ' ')
        has_guide='class="disease owner-guide"' in feline.read_text(encoding="utf-8")
        assert has_guide == (key in FELINE_PRACTICAL), feline
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
