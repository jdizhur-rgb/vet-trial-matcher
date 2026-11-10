#!/usr/bin/env python3
"""Maine veterinary cancer care guide from the canonical care directory."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from oncology_massachusetts import service_listing
from oncology_state_pages import GUIDE_CSS, esc, listing
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/maine'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncology and cancer care in Maine'
DESCRIPTION = 'Find veterinary oncologists, chemotherapy and tumor removal for dogs and cats in Maine. Compare clinic locations, services and appointment restrictions.'


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((row for row in rows if row['country'] == 'USA' and row['region'] == 'ME'),
                  key=lambda row: (row['city'], row['name']))


def generate(root):
    rows = state_rows()
    assert rows and all(row['source_id'] and row['website'] and row['last_verified'] for row in rows)
    physical = [row for row in rows if row.get('location_type', 'physical') == 'physical']
    mobile = [row for row in rows if row.get('location_type') == 'mobile']
    assert len(physical) + len(mobile) == len(rows)
    restricted = [row for row in physical if row.get('accepting_new_patients') is False
                  or row['source_id'] == 'me-animal-welfare-society-kennebunk']
    active = [row for row in physical if row not in restricted]
    oncology = [row for row in active if 'Medical oncology' in row['services']]
    chemo = [row for row in physical if 'Chemotherapy' in row['services']]
    local_chemo = [row for row in active if row in chemo and row not in oncology]
    local = [row for row in active if row not in oncology and row not in local_chemo]
    groups = [
        ('specialty-care', 'Dedicated veterinary oncology', oncology, listing),
        ('local-chemotherapy', 'Local chemotherapy', local_chemo, listing),
        ('local-care', 'Local cancer care and tumor removal', local, listing),
        ('mobile-care', 'Mobile care and small-lump removal', mobile, service_listing),
        ('intake-restrictions', 'Clinics with intake restrictions', restricted, listing),
    ]

    sections, navigation, ordered = [], [], []
    for anchor, heading, records, render in groups:
        if not records:
            continue
        ordered.extend(records)
        navigation.append(f'<a href="#{anchor}">{heading}</a>')
        cards = ''.join(render(row) for row in records)
        sections.append(f'<section id="{anchor}"><h2>{heading}</h2><div class="ri-listings">{cards}</div></section>')

    body = f'''<div class="ri-care-guide"><style>{GUIDE_CSS}</style>
<p><a href="/matcher/centers/">Find oncology care</a> / Maine</p>
<h1>{TITLE}</h1>
<p class="lead">Where to find a veterinary oncologist, chemotherapy or tumor removal for dogs and cats in Maine. Each listing shows the services documented for that location and how to reach the clinic.</p>
<div class="ri-summary"><p><strong>{len(physical)} clinic locations</strong> · {len(chemo)} list chemotherapy · {len(mobile)} mobile service</p>
<nav aria-label="On this page">{''.join(navigation)}<a href="#radiation-and-trials">Radiation and clinical trials</a></nav></div>
<section><h2>Finding cancer care in Maine</h2>
<p>Portland Veterinary Emergency and Specialty Care moved its oncology and specialty surgery services to <strong>422 US Route 1 in Falmouth</strong> on November 2, 2026. Maine Veterinary Medical Center in Scarborough also lists an oncology team, chemotherapy and oncologic surgery. <a href="https://pvesc.com/locations/">PVESC locations</a> · <a href="https://mvmc.vet/pet-oncology-scarborough-me">Maine Veterinary Medical Center oncology</a></p>
<p>Lucerne Veterinary Hospital in Dedham offers chemotherapy injections at the clinic and oral medications to give at home. Veazie Veterinary Clinic lists mass removal. Its current chemotherapy availability still needs confirmation. <a href="https://lucernevet.com/services/pet-chemotherapy">Lucerne chemotherapy service</a> · <a href="https://veazievet.com/surgery/">Veazie surgery service</a></p>
<p>Many local practices list removal of masses or tumors. For a specific case, ask what the clinic can remove, how the tissue will be examined and when it refers to a specialist surgeon.</p></section>
{''.join(sections)}
<section id="radiation-and-trials"><h2>Radiation and clinical trials</h2>
<p>Our Maine review did not verify a local site delivering radiation therapy or electrochemotherapy. Port City Veterinary Referral Hospital in Portsmouth, New Hampshire, lists radiation oncology at its hospital. Confirm the referral process and where treatment takes place before arranging a visit. <a href="https://www.portcityvet.com/services/radiation-oncology">Port City radiation oncology</a></p>
<p>Use the <a href="/matcher/">clinical trial finder</a> to look for studies by diagnosis. For care across state lines, use the <a href="/matcher/centers/">oncology care finder</a>.</p></section>
<div class="ri-notice"><p><strong>Directory coverage.</strong> Maine coverage was reviewed on November 9, 2026 using clinic websites and public directories across all 16 counties. Individual record dates appear in the cards. Services and intake policies vary by clinic, and some could not be confirmed from public sources. Confirm the treating clinician, availability and cost directly with the clinic.</p></div></div>'''
    text = g.page(TITLE, DESCRIPTION, body, URL)
    schema = {
        '@context': 'https://schema.org', '@type': 'ItemList', 'name': TITLE,
        'numberOfItems': len(ordered),
        'itemListElement': [
            {'@type': 'ListItem', 'position': position, 'name': row['name'], 'url': URL + '#' + row['source_id']}
            for position, row in enumerate(ordered, 1)
        ],
    }
    social = (f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(TITLE)}">'
              f'<meta property="og:description" content="{esc(DESCRIPTION)}"><meta property="og:url" content="{URL}">')
    markup = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    text = text.replace('</head>', social + '<script type="application/ld+json">' + markup + '</script></head>', 1)
    destination = root / STATE_PATH / 'index.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(wrap_html(text), encoding='utf-8')
    print(f'ME_STATE_GUIDE_OK physical={len(physical)} mobile={len(mobile)} chemotherapy={len(chemo)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
