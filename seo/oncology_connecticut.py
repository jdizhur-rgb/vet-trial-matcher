#!/usr/bin/env python3
"""Owner-requested Connecticut guide, using published care identities and dates."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from oncology_massachusetts import service_listing
from oncology_state_pages import GUIDE_CSS, esc, listing
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/connecticut'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncology and cancer care in Connecticut'
DESCRIPTION = 'Find veterinary oncologists, radiation therapy, chemotherapy and tumor surgery for dogs and cats in Connecticut. Compare clinics and find cancer trials.'


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((r for r in rows if r.get('country') == 'USA' and r.get('region') == 'CT'),
                  key=lambda r: (r.get('city', ''), r['name']))


def generate(root):
    rows = state_rows()
    assert rows and all(r.get('source_id') and r.get('website') and r.get('last_verified') for r in rows)
    physical = [r for r in rows if r.get('location_type', 'physical') == 'physical']
    mobile = [r for r in rows if r.get('location_type') == 'mobile']
    restricted = [r for r in physical if r.get('accepting_new_patients') is False]
    active = [r for r in physical if r not in restricted]
    oncology = [r for r in active if {'Medical oncology', 'Radiation oncology'} & set(r['services'])]
    chemo = [r for r in active if 'Chemotherapy' in r['services']]
    local_chemo = [r for r in chemo if r not in oncology]
    local = [r for r in active if r not in oncology and r not in local_chemo]
    assert len(physical) + len(mobile) == len(rows)
    groups = [
        ('specialty-care', 'Medical and radiation oncology', oncology, listing),
        ('local-chemotherapy', 'Other clinics offering chemotherapy', local_chemo, listing),
        ('local-care', 'Local cancer care and tumor surgery', local, listing),
        ('mobile-care', 'Mobile oncology', mobile, service_listing),
        ('intake-restrictions', 'Locations with intake restrictions', restricted, listing),
    ]
    sections, navigation, ordered = '', '', []
    for anchor, heading, records, render in groups:
        if not records:
            continue
        ordered.extend(records)
        navigation += f'<a href="#{anchor}">{heading}</a>'
        sections += f'<section id="{anchor}"><h2>{heading}</h2><div class="ri-listings">' + ''.join(render(r) for r in records) + '</div></section>'
    body = f'''<div class="ri-care-guide"><style>{GUIDE_CSS}</style>
<p><a href="/matcher/centers/">Find oncology care</a> / Connecticut</p>
<h1>{TITLE}</h1>
<p class="lead">Find veterinary oncology, radiation therapy, chemotherapy and tumor surgery for dogs and cats in Connecticut. The listings show which services each location publishes and how to reach the clinic.</p>
<div class="ri-summary"><p><strong>{len(physical)} clinic locations</strong> · {len(chemo)} clinic locations list chemotherapy · {len(mobile)} mobile oncology service</p><nav aria-label="On this page">{navigation}<a href="#clinical-trials">Clinical trials</a></nav></div>
<section><h2>Finding cancer care in Connecticut</h2>
<p><a href="https://www.medvet.com/location/norwalk/">MedVet Norwalk</a> lists both medical and radiation oncology. Newtown Veterinary Specialists lists electrochemotherapy, a local tumor treatment. Ask the treating team which options are available for your pet’s diagnosis and where treatment would take place.</p>
<p>Pieper lists cancer care in both Middletown and Stratford. Check the card for the branch you plan to visit. Noank Mystic Veterinary Hospital also lists chemotherapy, so owners in southeastern Connecticut have a local contact to ask about the drugs and monitoring their pet would need.</p>
<p>Many clinics on this page list mass or tumor removal. Ask whether the veterinarian can perform the operation your pet needs, how the tissue will be examined and when the clinic refers a case to a specialist surgeon. If chemotherapy is planned, ask who will choose the protocol, review bloodwork and manage side effects.</p></section>
{sections}
<section id="clinical-trials"><h2>Cancer clinical trials in Connecticut</h2>
<p>Veterinary Cancer Concierge Services is a mobile oncology service in Fairfield County. Its <a href="/centers/veterinary-cancer-concierge-services/">clinical trial listing</a> includes a separate Stamford visit location for the experimental EGFR/HER2 vaccine study in dogs. Check the listing and the study team for current enrollment, eligibility, visit costs and required testing.</p>
<p>To look for other studies by diagnosis, use the <a href="/matcher/">clinical trial finder</a>. For care across state lines, use the <a href="/matcher/centers/">oncology care finder</a> or see the <a href="/veterinary-oncology/massachusetts/">Massachusetts</a> and <a href="/veterinary-oncology/rhode-island/">Rhode Island</a> guides.</p></section>
<div class="ri-notice"><p><strong>Directory coverage.</strong> Connecticut coverage was reviewed on November 6, 2026. Individual listing dates appear with the clinics. The review covered all 169 municipalities using public directories and clinic sources. Some branch-level services and current intake details still require confirmation. Confirm availability, referral requirements and costs with the clinic before booking.</p></div></div>'''
    text = g.page(TITLE, DESCRIPTION, body, URL)
    schema = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': TITLE,
              'numberOfItems': len(ordered), 'itemListElement': [
                  {'@type': 'ListItem', 'position': i, 'name': r['name'], 'url': URL + '#' + r['source_id']}
                  for i, r in enumerate(ordered, 1)]}
    social = (f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(TITLE)}">'
              f'<meta property="og:description" content="{esc(DESCRIPTION)}"><meta property="og:url" content="{URL}">')
    text = text.replace('</head>', social + '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script></head>', 1)
    dest = root / STATE_PATH / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(wrap_html(text), encoding='utf-8')
    print(f'CT_STATE_GUIDE_OK physical={len(physical)} mobile={len(mobile)} chemotherapy={len(chemo)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
