#!/usr/bin/env python3
"""Systematic SEO generator guard: strict diagnosis mapping for every generated page."""
from __future__ import annotations

import json
import re
from pathlib import Path

import generate_seo as g


def _phrase_present(phrase: str, text: str) -> bool:
    phrase = g.norm(phrase)
    text = g.norm(text)
    if not phrase or not text:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", text) is not None


def canonical_cancer(value):
    raw = g.norm(value)
    if not raw:
        return None
    if any(_phrase_present(term, raw) for term in g.GENERIC_WORDS):
        return None
    for key, aliases in g.CANONICAL_RULES:
        if any(_phrase_present(alias, raw) for alias in aliases):
            return key
    return None


def cancer_values(row):
    value = row.get("cancers", [])
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return []


def row_cancers(row):
    return {mapped for mapped in (canonical_cancer(v) for v in cancer_values(row)) if mapped}


def audit_matrix():
    rows = g.load_effective()
    matrix = {}
    errors = []
    for region, countries in g.REGIONS.items():
        for species_key, species_name in g.SPECIES.items():
            for row in rows:
                if row.get("country") not in countries or not g.species_ok(row, species_name):
                    continue
                for cancer in row_cancers(row):
                    key = f"{region}/{species_key}/{g.slugify(cancer)}"
                    matrix.setdefault(key, []).append(row["id"])
    for page in g.OUT.glob("*/*/*/index.html"):
        rel = str(page.parent.relative_to(g.OUT)).replace("\\", "/")
        expected = matrix.get(rel, [])
        if not expected:
            errors.append(f"orphan page: {rel}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        card_count = text.count('class="card"')
        if card_count != len(expected):
            errors.append(f"card-count mismatch {rel}: html={card_count} matrix={len(expected)}")
    for rel, ids in matrix.items():
        page = g.OUT / rel / "index.html"
        if not page.exists(): errors.append(f"missing page: {rel} ({len(ids)} records)")
    for row in rows:
        values = [g.norm(v) for v in cancer_values(row)]
        if any("paraganglioma" in v for v in values) and "glioma" in row_cancers(row):
            errors.append(f"paraganglioma leaked into glioma: {row['id']}")
    if errors:
        raise AssertionError("SEO matrix audit failed:\n" + "\n".join(errors[:50]))
    audit = {"effective_treatment_records": len(rows), "matrix_cells": len(matrix), "assignments": sum(len(v) for v in matrix.values()), "cells": {k: sorted(v) for k, v in sorted(matrix.items())}}
    (g.OUT / "mapping-audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"STRICT_MATRIX_OK records={audit['effective_treatment_records']} cells={audit['matrix_cells']} assignments={audit['assignments']}")


CENTER_RULES = (
    ("Colorado State University Flint Animal Cancer Center", ("colorado state university", "flint animal cancer center")),
    ("University of Florida College of Veterinary Medicine", ("university of florida",)),
    ("Michigan State University College of Veterinary Medicine", ("michigan state university",)),
    ("Auburn University College of Veterinary Medicine", ("auburn university",)),
    ("University of Pennsylvania School of Veterinary Medicine", ("university of pennsylvania", "penn vet")),
    ("Tufts University Cummings School of Veterinary Medicine", ("tufts university", "tufts cummings")),
    ("NC State College of Veterinary Medicine", ("nc state", "north carolina state university")),
    ("University of Wisconsin–Madison School of Veterinary Medicine", ("university of wisconsin", "wisconsin madison")),
    ("University of Missouri College of Veterinary Medicine", ("university of missouri",)),
    ("University of Illinois College of Veterinary Medicine", ("university of illinois",)),
    ("Purdue University College of Veterinary Medicine", ("purdue university",)),
    ("Cornell University College of Veterinary Medicine", ("cornell university",)),
    ("University of Minnesota College of Veterinary Medicine", ("university of minnesota",)),
    ("Ohio State University College of Veterinary Medicine", ("ohio state university", "the ohio state university")),
    ("Texas A&M School of Veterinary Medicine", ("texas a&m", "texas a and m")),
    ("Louisiana State University School of Veterinary Medicine", ("louisiana state university", "lsu")),
    ("University of Georgia College of Veterinary Medicine", ("university of georgia",)),
    ("University of Tennessee College of Veterinary Medicine", ("university of tennessee",)),
    ("Washington State University College of Veterinary Medicine", ("washington state university",)),
    ("Iowa State University College of Veterinary Medicine", ("iowa state university",)),
    ("Kansas State University College of Veterinary Medicine", ("kansas state university",)),
    ("Oklahoma State University College of Veterinary Medicine", ("oklahoma state university",)),
    ("Oregon State University Carlson College of Veterinary Medicine", ("oregon state university",)),
    ("Mississippi State University College of Veterinary Medicine", ("mississippi state university",)),
)

CSU_CENTER = "Colorado State University Flint Animal Cancer Center"


def canonical_center(value):
    text = g.norm(value)
    for name, aliases in CENTER_RULES:
        if any(g.norm(alias) in text for alias in aliases): return name
    return None


def center_overview(center):
    if center != CSU_CENTER: return ""
    return (
        '<div class="center-overview" style="text-align:justify;text-justify:inter-word">'
        '<h2 style="text-align:left">About the Flint Animal Cancer Center</h2>'
        '<figure style="margin:16px 0 22px;text-align:left">'
        '<img src="https://vetmedbiosci.colostate.edu/psrl/wp-content/uploads/sites/15/2021/04/08007_00004-1.jpg" alt="Colorado State University Translational Medicine Institute research facility" loading="lazy" style="width:100%;max-height:430px;object-fit:cover;border-radius:14px;display:block">'
        '<figcaption style="font-size:.86rem;color:#607086;margin-top:7px">Colorado State University Translational Medicine Institute, home to research programs that collaborate with the Flint Animal Cancer Center. Photo: Colorado State University.</figcaption>'
        '</figure>'
        '<p>Colorado State University’s Flint Animal Cancer Center in Fort Collins combines multidisciplinary cancer care with comparative oncology research. Its program includes clinical trials, laboratory research and a cancer biorepository, with work designed to improve cancer prevention, diagnosis and treatment in pets while also informing human cancer research.</p>'
        '<h2 style="text-align:left">Cancer research &amp; team</h2>'
        '<p>Research at CSU spans medical, surgical and radiation oncology, immunology and immunotherapy, cancer genomics and translational drug development. The center is directed by veterinary oncologist <strong>Susan Lana, DVM</strong>. <strong>Douglas Thamm, VMD</strong> directs clinical research, and the broader comparative oncology group includes specialists working across clinical trials, immunotherapy, genomics, radiation biology and surgical oncology.</p>'
        '<p><a href="https://vetmedbiosci.colostate.edu/cs/research-topic-directory/comparative-oncology-and-cancer-biology/" rel="noopener">Meet CSU comparative oncology researchers</a> · <a href="https://vetmedbiosci.colostate.edu/vth/clinical_trial_tag/oncology/" rel="noopener">See CSU oncology clinical trials</a></p>'
        '</div>'
    )


def generate_center_pages():
    rows = [r for r in g.load_effective() if r.get("country") == "USA"]
    grouped = {}
    for row in rows:
        center = canonical_center(row.get("center", ""))
        if center: grouped.setdefault(center, []).append(row)
    if not grouped: return
    center_links, index_items = [], []
    for center, hit in sorted(grouped.items()):
        slug = g.slugify(center.replace("College of Veterinary Medicine", "").replace("School of Veterinary Medicine", ""))
        path = f"centers/{slug}/"; url = f"{g.SITE}/{path}"
        cancers = sorted({c for r in hit for c in row_cancers(r)})
        cancer_text = ", ".join(g.display_name(c) for c in cancers) if cancers else "multiple cancer types"
        h1 = f"{center}: Veterinary Cancer Clinical Trials"
        body = (f'<h1>{g.esc(h1)}</h1>' + center_overview(center) + f'<p class="lead count-callout"><strong>{len(hit)} current treatment opportunities in our catalog.</strong><br><span>Current research represented here includes {g.esc(cancer_text)}.</span></p>' + '<div class="free"><strong>100% FREE</strong> — view trial details, contacts and official enrollment links.<br><small>No registration. No hidden results. No paid report.</small></div>' + f'<p><a class="cta" href="{g.FINDER}">Check your pet against these options</a></p>' + '<h2>Current treatment &amp; research opportunities</h2><p>These treatment-focused studies and advanced oncology options are drawn from our current catalog. Enrollment status and final eligibility are determined by the research team.</p>' + g.cards(hit))
        dest = g.OUT / path; dest.mkdir(parents=True, exist_ok=True)
        (dest / "index.html").write_text(g.page(h1, f"Current veterinary cancer clinical trials and treatment studies at {center}.", body, url), encoding="utf-8")
        center_links.append(url); index_items.append((center, path, len(hit)))
    index_url = f"{g.SITE}/centers/"
    index_body = ('<h1>Veterinary Cancer Clinical Trial Centers</h1><p class="lead">Browse U.S. veterinary universities and teaching hospitals with current treatment opportunities represented in our catalog.</p><div class="free"><strong>100% FREE</strong> — trial details, contacts and official enrollment links are available without registration or a paywall.</div><h2>Current research centers</h2><ul>' + ''.join(f'<li><a href="{g.SITE}/{p}">{g.esc(n)}</a> — {count} current opportunities</li>' for n,p,count in index_items) + '</ul>')
    center_dir = g.OUT / "centers"; center_dir.mkdir(parents=True, exist_ok=True)
    (center_dir / "index.html").write_text(g.page("Veterinary Cancer Clinical Trial Centers", "U.S. veterinary cancer clinical trial centers with current treatment opportunities.", index_body, index_url), encoding="utf-8")
    sitemap = g.OUT / "sitemap.xml"; text = sitemap.read_text(encoding="utf-8")
    additions = ''.join(f'<url><loc>{g.esc(u)}</loc></url>\n' for u in [index_url] + center_links)
    sitemap.write_text(text.replace('</urlset>', additions + '</urlset>'), encoding="utf-8")
    print(f"CENTER_PAGES_OK centers={len(grouped)}")


def main():
    g.canonical_cancer = canonical_cancer; g.row_cancers = row_cancers
    original_page = g.page
    def page_with_count_callout(title, desc, body, canonical, lang='en', alts=None):
        body = re.sub(r'<p class="lead">(\d+ [^<]*treatment[^<]*opportunit[^<]*\.) Trial names, locations and official source links are shown below\.</p>', r'<p class="lead count-callout"><strong>\1</strong><br><span>Trial names, locations and official source links are shown below.</span></p>', body, count=1, flags=re.I)
        rendered = original_page(title, desc, body, canonical, lang, alts)
        if lang == 'en':
            disease_start = rendered.find('<section class="disease">'); disease_end = rendered.find('</section>', disease_start); lead_start = rendered.find('<p class="lead')
            if disease_start != -1 and disease_end != -1 and lead_start != -1 and lead_start < disease_start:
                disease_end += len('</section>'); disease = rendered[disease_start:disease_end]; rendered = rendered[:lead_start] + disease + rendered[lead_start:disease_start] + rendered[disease_end:]
        if 'count-callout' in rendered:
            rendered = rendered.replace('.free{', '.count-callout{background:#fff;border:1px solid #d9e2ea;border-radius:12px;padding:13px 16px;margin:18px 0 12px}.count-callout strong{font-size:1.12rem;color:#17243b}.count-callout span{font-size:.96rem;color:#607086}.free{', 1)
        return rendered
    g.page = page_with_count_callout
    g.main(); generate_center_pages(); audit_matrix()


if __name__ == "__main__": main()
