#!/usr/bin/env python3
"""Owner-approved North Dakota guide from current canonical care records."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from oncology_state_pages import GUIDE_CSS, esc, listing
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/north-dakota'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncology and cancer care in North Dakota'
DESCRIPTION = 'Find local tumor surgery and chemotherapy for dogs and cats in North Dakota, with clinic contacts, official sources and current oncology intake restrictions.'


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((r for r in rows if r.get('country') == 'USA' and r.get('region') == 'ND'),
                  key=lambda r: (r.get('city', ''), r['name']))


def network_listing(row):
    email = row['email']
    checked = row.get('last_verified')
    return f'''<article class="ri-listing" id="{esc(row['source_id'])}" data-source-id="{esc(row['source_id'])}">
<h3>{esc(row['name'])}</h3><p class="ri-address">Network contact; treatment branch to confirm</p>
<ul class="ri-services" aria-label="Listed services"><li>Tumor surgery</li></ul>
<p>{esc(row.get('availability_note'))}</p><p class="ri-contacts"><a href="mailto:{esc(email)}">{esc(email)}</a><a href="{esc(row['website'])}" target="_blank" rel="noopener">Official network website</a></p>
<p class="ri-source-date">Directory record checked: <time datetime="{esc(checked)}">{esc(checked)}</time></p></article>'''


def generate(root):
    rows = state_rows()
    physical = [r for r in rows if r.get('location_type', 'physical') == 'physical']
    networks = [r for r in rows if r.get('location_type') == 'network']
    restricted = [r for r in physical if r.get('accepting_new_patients') is False]
    chemo = [r for r in physical if 'Chemotherapy' in r['services'] and r not in restricted]
    local = [r for r in physical if r not in restricted and r not in chemo]
    assert len(physical) + len(networks) == len(rows)
    assert all(r.get('source_id') and r.get('website') for r in rows)
    sections = ''
    ordered = []
    for anchor, heading, records, render in (
        ('chemotherapy', 'Local chemotherapy', chemo, listing),
        ('specialty-oncology', 'Specialty oncology and intake restrictions', restricted, listing),
        ('local-care', 'Local cancer care and tumor surgery', local, listing),
        ('network-contact', 'Network contact: confirm the treatment branch', networks, network_listing),
    ):
        if records:
            ordered.extend(records)
            sections += f'<section id="{anchor}"><h2>{heading}</h2><div class="ri-listings">' + ''.join(render(r) for r in records) + '</div></section>'
    # Reuse the approved Rhode Island layout without altering its page or source dates.
    body = f'''<div class="ri-care-guide"><style>{GUIDE_CSS}</style>
<p><a href="/matcher/centers/">Find oncology care</a> / North Dakota</p>
<h1>{TITLE}</h1>
<p class="lead">Local options for dogs and cats with cancer include tumor surgery, general veterinary cancer care and chemotherapy. The listings below show what each clinic publishes and where access still needs to be confirmed.</p>
<div class="ri-summary"><p><strong>{len(physical)} physical locations</strong> and {len(networks)} network contact. A listed clinic may provide only some parts of cancer care.</p>
<nav aria-label="On this page"><a href="#chemotherapy">Chemotherapy</a><a href="#specialty-oncology">Specialty oncology</a><a href="#local-care">Local care and surgery</a><a href="#network-contact">Network contact</a></nav></div>
<p>State Ave Veterinary Clinic in Dickinson lists oncology consultations and treatment. Its clinic recruitment advertisement also lists chemotherapy. Confirm the available protocol, treating veterinarian and appointment before travelling. <a href="https://www.stateavevet.com/" target="_blank" rel="noopener">Read the clinic’s information</a>.</p>
<p><strong>Red River Animal Emergency Hospital &amp; Referral Center in Fargo is not accepting new oncology patients.</strong> Its separate surgery service lists oncologic procedures and veterinary referrals. Contact the hospital to confirm whether it can accept the surgical case before travelling; the surgery listing does not mean medical oncology intake has reopened. <a href="https://rraeh.com/services/oncology/" target="_blank" rel="noopener">Oncology intake notice</a> · <a href="https://rraeh.com/services/rraeh-surgery-service/" target="_blank" rel="noopener">Surgery service</a>.</p>
<p>Several general practices elsewhere in the state publish tumor or mass removal. Others list cancer care without specifying the treatment. These are useful local contacts, but the listings do not establish an oncologist at every clinic. Chemotherapy, radiation and electrochemotherapy are shown only when confirmed in the directory.</p>
{sections}
<section><h2>Planning care in North Dakota</h2><p>Before arranging a trip, ask whether the clinic treats your pet’s particular cancer, which veterinarian would see the case and whether a referral is required. Confirm the records to send, costs and appointment availability. For surgery, discuss the procedure and its limits; a published mass-removal service does not establish that every tumor can be treated there.</p><p>If specialist assessment and ongoing treatment will take place at different clinics, ask both teams who will manage the treatment plan, monitoring and follow-up. Use the <a href="/matcher/centers/">oncology care finder</a> to compare services in other states, or explore <a href="/online-oncology-consultations/">oncology teleconsultations</a>. The clinician and access conditions for each remote service need to be checked separately.</p><p>You can also <a href="/matcher/">search cancer clinical trials</a> or read the <a href="/cancer-types/">cancer guides for dogs and cats</a>. Clinical-trial sites and eligibility are separate from this local-care directory.</p></section>
<div class="ri-notice"><p><strong>About this list:</strong> North Dakota coverage was reviewed on October 24, 2026. Individual record dates appear above. This is a selection of locations with published cancer-related services, not a complete census of every practice in the state. An unlisted service has not been confirmed in this directory; it is not proof that the clinic does not offer it. The network contact is listed once because its surgery service has not been allocated to individual branches.</p><p>Service information is compiled from clinic websites and professional public directories. Vet Trial Finder does not independently verify clinicians, licenses, credentials or quality of care. Inclusion is not a recommendation. Confirm the clinician, service, cost and current availability directly with the clinic.</p></div></div>'''
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
    print(f'ND_STATE_GUIDE_OK physical={len(physical)} network={len(networks)} restricted={len(restricted)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
