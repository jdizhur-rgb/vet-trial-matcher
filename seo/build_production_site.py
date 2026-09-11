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

# Resolve program/alias names to canonical institutions before giving up on a
# verified address. This fixes cases such as Penn Vet program names while
# preserving the strict full-address validation already used in production.
_strict_row_locations = generate_seo_strict.row_locations


def _production_row_locations(row):
    locations = _strict_row_locations(row)
    if locations:
        return locations

    center = str(row.get("center") or "").strip()
    canonical = generate_seo_strict.canonical_center(center) if center else None
    country = str(row.get("country") or "").strip()
    for name in (canonical, center):
        if not name:
            continue
        for address in center_directory.addresses_for(name):
            if center_directory.address_is_complete(address, country):
                return [address]
    return []


generate_seo_strict.row_locations = _production_row_locations


def _fallback_location(row):
    """Best non-street location for display only; strict address audit stays intact."""
    country = str(row.get("country") or "").strip()
    for site in row.get("sites", []) if isinstance(row.get("sites"), list) else []:
        if not generate_seo_strict.site_active(site):
            continue
        city = str(site.get("city") or "").strip()
        state = str(site.get("state") or "").strip()
        if city or state:
            return ", ".join(x for x in (city, state, country) if x)
    city = str(row.get("city") or "").strip()
    state = str(row.get("state") or "").strip()
    if city or state:
        return ", ".join(x for x in (city, state, country) if x)
    return country


def _cards_with_consistent_location(rows):
    out = []
    for row in rows:
        p = [f'<article class="card"><h3>{generate_seo.esc(row.get("title"))}</h3><p class="meta"><strong>{generate_seo.esc(row.get("center"))}</strong> · {generate_seo.esc(row.get("country"))}</p>']
        if row.get("status"):
            p.append(f'<p class="status">{generate_seo.esc(row["status"])}</p>')
        treatment = generate_seo.prose(row.get("intervention") or row.get("treatment") or row.get("notes"))
        if treatment:
            p.append(f'<p><b>What is being offered:</b> {generate_seo.esc(treatment)}</p>')
        req = generate_seo.prose(row.get("requires"))
        exc = generate_seo.prose(row.get("excludes"))
        fund = generate_seo.prose(row.get("funding"))
        contact = generate_seo.contact_text(row)
        if req:
            p.append(f'<p><b>Who may qualify:</b> {generate_seo.esc(req)}</p>')
        if exc:
            p.append(f'<p><b>May not qualify if:</b> {generate_seo.esc(exc)}</p>')
        if fund:
            p.append(f'<p><b>Costs / coverage:</b> {generate_seo.esc(fund)}</p>')
        if contact:
            p.append(f'<p><b>Contact:</b> {generate_seo.esc(contact)}</p>')

        locations = _production_row_locations(row)
        if locations:
            p.append('<div class="study-locations"><p class="field-label">' + ('Location' if len(locations) == 1 else 'Participating locations') + '</p><ul>' + ''.join(f'<li>{generate_seo.esc(x)}</li>' for x in locations) + '</ul></div>')
        else:
            fallback = _fallback_location(row)
            if fallback:
                p.append('<div class="study-region"><p class="field-label">Location</p><ul><li>' + generate_seo.esc(fallback) + '</li></ul></div>')

        areas = generate_seo_strict.coverage_areas(row)
        if areas:
            p.append('<div class="enrollment-areas"><p class="field-label">Enrollment area</p><ul>' + ''.join(f'<li>{generate_seo.esc(x)}</li>' for x in areas) + '</ul><p class="coverage-note">The public study listing names a partner-hospital network rather than a specific hospital. Confirm the assigned hospital with the study team.</p></div>')
        if row.get("last_verified"):
            p.append(f'<p class="verified">Last verified: {generate_seo.esc(row["last_verified"])}</p>')
        if row.get("url"):
            p.append(f'<p><a class="official" href="{generate_seo.esc(row["url"])}" rel="noopener">Official study / enrollment information →</a></p>')
        p.append('</article>')
        out.append(''.join(p))
    return ''.join(out)


generate_seo.cards = _cards_with_consistent_location
generate_seo_strict.g.cards = _cards_with_consistent_location

# Match the existing Location styling without classifying region-only fallbacks
# as verified street addresses for the strict mapping audit.
_base_page = generate_seo.page


def _page_with_location_style(title, desc, body, canonical, lang='en', alts=None):
    rendered = _base_page(title, desc, body, canonical, lang, alts)
    return rendered.replace('</style>', '.study-region{margin:15px 0 4px;padding:12px 14px;background:#f6f8fb;border-radius:10px}.study-region ul{margin:5px 0 0;padding-left:20px}</style>', 1)


generate_seo.page = _page_with_location_style
generate_seo_strict.g.page = _page_with_location_style

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
