"""Keep requested historical organization profiles independent of trial ownership.

Render existing effective records, never reactivate or duplicate catalog trials.
An organization/coordinator profile is not a physical enrollment location.
"""
from __future__ import annotations

from copy import deepcopy
import html
import re
from pathlib import Path

import generate_seo as g
import generate_seo_strict as centers
from site_shell import wrap_html


RETAINED = {
    "schwarzman-animal-medical-center": ("Schwarzman Animal Medical Center", None),
    "medvet-clinical-studies-center": ("MedVet Clinical Studies Center", "medvet-egfr-her2-vaccine-2026"),
    "anivive-lifesciences-multicenter": ("Anivive Lifesciences — multicenter", "anivive-sine-osa-carboplatin"),
    "louisiana-state-university-school-of-veterinary-medicine": ("Louisiana State University School of Veterinary Medicine", None),
    "european-multicenter-study-floryne-buishand": ("European multicenter study — Floryne Buishand", "uk-rvc-insulinoma-toceranib"),
}


def profile_rows(slug, effective_rows):
    _, trial_id = RETAINED[slug]
    rows = [deepcopy(row) for row in effective_rows if trial_id and row.get("id") == trial_id]
    if slug == "medvet-clinical-studies-center":
        for row in rows:
            row["sites"] = [site for site in row.get("sites", []) if
                            (site.get("hospital") or site.get("name") or "").startswith("MedVet ")
                            and centers.site_active(site)]
            row["contacts"] = "MedVet Clinical Studies — clinicalstudies@medvet.com"
            row["contact"] = row["contacts"]
            row["status"] = "Enrollment varies by MedVet hospital; confirm the site-specific requirements."
            row["intervention"] = (
                "Experimental EGFR/HER2 tumor vaccine for dogs with osteosarcoma, hemangiosarcoma "
                "or transitional cell carcinoma, given alongside appropriate standard care. "
                "The vaccine is not offered as a single-agent treatment in this study."
            )
            row["funding"] = (
                "The investigational vaccine is provided at no charge. Owners pay hospital visits, "
                "diagnostics and vaccine administration; this is not a fully funded study."
            )
            row["notes"] = (
                "MedVet Salt Lake City is enrolling. Cincinnati and Cleveland restrict enrollment "
                "to established patients; Pittsburgh restricts enrollment to Pennsylvania residents. "
                "Chicago is pausing enrollment and is not listed as an available site here."
            )
        rows = [row for row in rows if row["sites"]]
    return rows


def restore_center_profiles(root: Path, effective_rows) -> None:
    # If the main generator again publishes an organization, keep that live
    # page. The historical-URL pass supplies any necessary same-center alias.
    present = set()
    for page in (root / "centers").glob("*/index.html"):
        match = re.search(r"<h1\b[^>]*>(.*?)</h1>", page.read_text(encoding="utf-8"), re.S)
        if match:
            present.add(html.unescape(re.sub(r"<[^>]+>", "", match[1])).strip())
    restored = 0
    for slug, (name, _) in RETAINED.items():
        if name in present:
            continue
        rows = profile_rows(slug, effective_rows)
        profile = centers.profile(name)
        intro = profile["about"]
        sources = list(profile.get("links", []))
        kind = centers.center_type(name)
        if slug == "anivive-lifesciences-multicenter":
            sources = [("Anivive current studies", "https://www.anivive.com/trials")]
        if slug == "medvet-clinical-studies-center":
            kind = "Research organization / hospital network"
        if slug == "european-multicenter-study-floryne-buishand":
            intro = (
                "This profile follows the European multicenter insulinoma study associated with "
                "Floryne Buishand. It represents a research collaboration, rather than a single "
                "hospital. Visits take place at the participating hospitals listed in the study."
            )
        links = " ".join(f'<a href="{g.esc(url)}" rel="noopener">{g.esc(label)} →</a>' for label, url in sources)
        if rows:
            cancers = sorted({cancer for row in rows for cancer in centers.row_cancers(row)})
            facts = centers.owner_summary(name, rows, cancers, [])
            options = centers.center_cards(rows)
            notes = "".join(f'<p class="source-note">{g.esc(row["notes"])}</p>' for row in rows
                            if row.get("notes") and (row.get("intervention") or row.get("treatment")))
            availability = (
                f'<p class="center-kicker opportunity-count">{len(rows)} current cancer treatment or research opportunity</p>'
                '<p class="source-note">The study below is an existing catalog listing. '
                'Enrollment and visits are handled by the named hospitals, not by this profile.</p>'
            )
        else:
            facts = '<div class="center-facts"><p>No currently verified treatment opportunity is listed here.</p></div>'
            options = '<div class="opportunity-list"></div>'
            notes = (
                '<p class="source-note">This does not mean the institution has no studies or oncology services. '
                'Check its official pages and contact its team for current availability.</p>'
            )
            availability = '<p class="center-kicker opportunity-count">0 current verified treatment opportunities in our catalog</p>'
        body = (
            f'<div class="center-page"><h1>{g.esc(name)}</h1><p class="center-type">{g.esc(kind)}</p>'
            + availability
            + f'<div class="center-overview"><h2>{g.esc(profile["title"])}</h2>'
            + f'<div class="center-overview-copy"><p>{g.esc(intro)}</p><p class="center-source">{links}</p></div></div>'
            + facts + '<h2>Current catalog listings</h2>' + options + notes
            + '<details class="center-note"><summary>Before you contact the center</summary>'
            + '<p>Confirm enrollment, eligibility, visit location and owner costs directly with the study team.</p></details>'
            + f'<p><a class="center-search-link" href="{g.FINDER}">Check all options for your pet →</a></p></div>'
        )
        url = f"{g.SITE}/centers/{slug}/"
        text = wrap_html(g.page(
            f"{name} | Veterinary cancer research",
            f"Organization profile, current catalog listings and official sources for {name}.", body, url,
        ))
        if not rows:
            text = text.replace('</head>', '<meta name="robots" content="noindex, follow"></head>', 1)
        page = root / "centers" / slug / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(text, encoding="utf-8")
        restored += 1
    print(f"RETAINED_CENTER_PROFILES_OK restored={restored}")
