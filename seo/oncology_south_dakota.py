#!/usr/bin/env python3
"""Owner-requested South Dakota guide, using published care identities and dates."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from oncology_state_pages import GUIDE_CSS, esc, listing
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/south-dakota'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncology and cancer care in South Dakota'
DESCRIPTION = 'Find local chemotherapy and tumor surgery for dogs and cats in South Dakota. Compare clinic services, addresses, phone numbers, official sources and appointment limits.'


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((r for r in rows if r.get('country') == 'USA' and r.get('region') == 'SD'),
                  key=lambda r: (r.get('city', ''), r['name']))


def generate(root):
    rows = state_rows()
    assert rows and all(r.get('source_id') and r.get('website') and r.get('last_verified') for r in rows)
    assert all(r.get('location_type', 'physical') == 'physical' for r in rows)
    restricted = [r for r in rows if r.get('accepting_new_patients') is False]
    chemo = [r for r in rows if 'Chemotherapy' in r['services'] and r not in restricted]
    local = [r for r in rows if r not in chemo and r not in restricted]
    groups = [('chemotherapy', 'Local chemotherapy', chemo),
              ('local-care', 'Local cancer care and tumor surgery', local),
              ('intake-restrictions', 'Locations with intake restrictions', restricted)]
    sections, navigation, ordered = '', '', []
    for anchor, heading, records in groups:
        if not records:
            continue
        ordered.extend(records)
        navigation += f'<a href="#{anchor}">{heading}</a>'
        sections += f'<section id="{anchor}"><h2>{heading}</h2><div class="ri-listings">' + ''.join(listing(r) for r in records) + '</div></section>'
    body = f'''<div class="ri-care-guide"><style>{GUIDE_CSS}</style>
<p><a href="/matcher/centers/">Find oncology care</a> / South Dakota</p>
<h1>{TITLE}</h1>
<p class="lead">Local chemotherapy and tumor surgery for dogs and cats in South Dakota, with clinic contacts and published service limits. Check the proposed treatment and appointment before arranging a long trip.</p>
<div class="ri-summary"><p><strong>{len(rows)} physical locations</strong> · {len(chemo)} physical locations list chemotherapy</p><nav aria-label="On this page">{navigation}</nav></div>
<section><h2>Finding cancer care in South Dakota</h2>
<p>Most locations below are general veterinary practices that publish tumor or mass-removal surgery. These services can be part of cancer care, but a surgery listing does not establish that the clinic can manage every tumor or has a board-certified veterinary oncologist. This review did not establish a resident board-certified medical oncologist, local radiation treatment or electrochemotherapy in South Dakota; it does not establish that none is available.</p>
<p>Upleash Veterinary Hospital in Sioux Falls and Dunes Animal Hospital in Dakota Dunes list local chemotherapy. Ask which veterinarian would manage your pet’s cancer, which drugs can be given there and whether an outside oncologist will help plan treatment. Upleash also lists tumor surgery; its optional oncology consultation does not establish an on-site medical oncologist. A chemotherapy listing does not confirm every protocol or an available appointment.</p>
<p>Visiting surgery at All Creatures Veterinary Hospital in Rapid City is coordinated through the hospital. Prairie View’s Highmore location publishes small-animal appointments and surgery about twice monthly. Confirm the proposed tumor operation and visit date; these schedules do not establish the same cancer service at every branch.</p></section>
{sections}
<section><h2>Before booking surgery or chemotherapy</h2>
<p>Ask whether the clinic treats your pet’s particular cancer, which veterinarian would see the case, whether a referral is required and which records to send. Confirm consultation, procedure and follow-up costs. For a mass removal, ask about the planned surgical margins, pathology and whether the case needs a specialist referral.</p>
<p>If a local veterinarian and an outside oncologist will share care, confirm who will provide the treatment plan, administer medication, review blood tests and handle problems between visits. Scheduled cancer care and emergency access are separate services.</p>
<p>For options beyond South Dakota, use the <a href="/matcher/centers/">oncology care finder</a> to compare neighboring states, including Minnesota, North Dakota, Nebraska, Iowa, Wyoming and Montana. The <a href="/veterinary-oncology/north-dakota/">North Dakota guide</a> and <a href="/veterinary-oncology/wyoming/">Wyoming guide</a> describe their listed local services and limits. <a href="/online-oncology-consultations/">Oncology teleconsultations</a> may offer specialist review; check whether each service accepts owners directly or requires a local veterinarian and whether it can advise on your case across state lines.</p>
<p>You can also <a href="/matcher/">search cancer clinical trials</a> or read the <a href="/cancer-types/">cancer guides for dogs and cats</a>. Trial eligibility and enrollment are separate from these clinic listings.</p></section>
<div class="ri-notice"><p><strong>About this list:</strong> South Dakota coverage was reviewed on November 1, 2026. Individual record dates appear above. Page publication is not a new clinic verification. This is a selection of locations with published cancer-related services, not a complete census of every practice in the state. Specific services, branch allocation or primary-source information remain unconfirmed at other reviewed practices. An unlisted service is not proof that a clinic does not offer it.</p>
<p>Some records rely partly on indexed copies of clinic-authored pages where direct access was unavailable. At Heartland and Pet Pawz, the current assigned operating veterinarian requires confirmation; professional-license records do not establish present employment or appointment assignment.</p>
<p>Service information is compiled from clinic websites and professional public directories. Vet Cancer Care Finder does not independently verify clinicians, licenses, credentials or quality of care. Inclusion is not a recommendation. Confirm the clinician, service, cost and current availability directly with the clinic.</p></div></div>'''
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
    print(f'SD_STATE_GUIDE_OK physical={len(rows)} chemotherapy={len(chemo)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
