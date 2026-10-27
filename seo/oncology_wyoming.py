#!/usr/bin/env python3
"""Owner-approved Wyoming guide; inherit canonical identities and source dates."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from oncology_state_pages import GUIDE_CSS, esc, listing
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/wyoming'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncology and cancer care in Wyoming'
DESCRIPTION = 'Find local chemotherapy, tumor surgery and mobile veterinary cancer care for dogs and cats in Wyoming, with clinic contacts, official sources and service limits.'


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((r for r in rows if r.get('country') == 'USA' and r.get('region') == 'WY'),
                  key=lambda r: (r.get('city', ''), r['name']))


def mobile_listing(row):
    phone = row.get('phone', '')
    dial = ''.join(c for c in phone if c.isdigit() or c == '+')
    checked = row.get('last_verified')
    labels = {'Surgery': 'Tumor surgery', 'ECT': 'Electrochemotherapy (ECT)'}
    services = ''.join(f'<li>{esc(labels.get(s, s))}</li>' for s in row['services'])
    email = f'<a href="mailto:{esc(row["email"])}">{esc(row["email"])}</a>' if row.get('email') else ''
    return f'''<article class="ri-listing" id="{esc(row['source_id'])}" data-source-id="{esc(row['source_id'])}" data-location-type="mobile">
<h3>{esc(row['name'])}</h3><p class="ri-address">Mobile service · {esc(row.get('service_area'))}</p>
<ul class="ri-services" aria-label="Listed services">{services}</ul>
<p>{esc(row.get('availability_note'))}</p><p class="ri-contacts"><a href="tel:{esc(dial)}">{esc(phone)}</a>{email}<a href="{esc(row['website'])}" target="_blank" rel="noopener">Official service website</a></p>
<p class="ri-source-date">Directory record checked: <time datetime="{esc(checked)}">{esc(checked)}</time></p></article>'''


def generate(root):
    rows = state_rows()
    physical = [r for r in rows if r.get('location_type', 'physical') == 'physical']
    mobile = [r for r in rows if r.get('location_type') == 'mobile']
    restricted = [r for r in physical if r.get('accepting_new_patients') is False]
    chemo = [r for r in physical if 'Chemotherapy' in r['services'] and r not in restricted]
    local = [r for r in physical if r not in chemo and r not in restricted]
    assert len(physical) + len(mobile) == len(rows)
    assert rows and all(r.get('source_id') and r.get('website') and r.get('last_verified') for r in rows)
    groups = [
        ('chemotherapy', 'Local chemotherapy', chemo, listing),
        ('local-care', 'Local cancer care and tumor surgery', local, listing),
        ('mobile-care', 'Mobile and visiting surgical services', mobile, mobile_listing),
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
<p><a href="/matcher/centers/">Find oncology care</a> / Wyoming</p>
<h1>{TITLE}</h1>
<p class="lead">Local chemotherapy, tumor surgery and mobile surgical care for dogs and cats in Wyoming. Compare published services and clinic contacts before arranging an appointment or a long trip.</p>
<div class="ri-summary"><p><strong>{len(physical)} physical locations</strong> and {len(mobile)} mobile services · {len(chemo)} physical locations list chemotherapy</p><nav aria-label="On this page">{navigation}</nav></div>
<section><h2>Finding specialist cancer care in Wyoming</h2>
<p>The listings below include general veterinary practices as well as visiting surgical services. A clinic that removes tumors or administers chemotherapy does not necessarily have a board-certified veterinary oncologist. This guide does not confirm a resident board-certified medical oncologist in Wyoming.</p>
<p>Local chemotherapy listings include practices in Casper, Cody and Jackson. Ask which veterinarian would manage your pet’s cancer, which treatment can be given locally and whether an outside oncologist will help plan the care. A published chemotherapy service does not establish that every drug or protocol is available.</p>
<p>VCA Spring Creek in Jackson Hole publishes visits by Bridger Veterinary Specialists surgeons Joshua Jackson and Jason Wheeler. These are surgical specialists; their visits do not establish an on-site medical oncologist or radiation service. Confirm the current schedule and whether the proposed tumor surgery can be performed there. <a href="https://vcahospitals.com/spring-creek/services/advanced-care/soft-tissue-surgery" target="_blank" rel="noopener">Read the hospital’s surgery information</a>.</p></section>
{sections}
<section><h2>Planning care across a large state</h2>
<p>Before travelling, ask whether the clinic treats your pet’s particular cancer, whether a referral is required and which records to send. Confirm the consultation, treatment and monitoring costs, the treating veterinarian and current appointment availability. A mass-removal listing does not establish that every tumor or complex operation can be managed at that clinic.</p>
<p>If a specialist and a local veterinarian will share the care, ask both teams who will provide the treatment plan, give medication, review blood tests and handle problems between visits. Mobile services need a confirmed location and travel schedule; they are listed once here rather than as separate offices in every town they may visit.</p>
<p>For specialist care beyond Wyoming, use the <a href="/matcher/centers/">oncology care finder</a> to compare options in neighboring states, including Colorado, Montana, Utah and Idaho. <a href="/online-oncology-consultations/">Oncology teleconsultations</a> may offer another route to specialist review; check whether each service accepts owners directly or requires a local veterinarian, and what it can provide across state lines.</p>
<p>You can also <a href="/matcher/">search cancer clinical trials</a> or read the <a href="/cancer-types/">cancer guides for dogs and cats</a>. Trial locations, eligibility and treatment access are separate from these clinic listings.</p></section>
<div class="ri-notice"><p><strong>About this list:</strong> Wyoming coverage was reviewed on October 26, 2026. Individual record dates appear above. Page publication is not a new clinic verification. This is a selection of locations with published cancer-related services, not a complete census of every practice in the state. An unlisted service has not been confirmed in this directory; it is not proof that a clinic does not offer it. Specific local services remain unconfirmed at several practices reviewed during discovery.</p>
<p>Service information is compiled from clinic websites and professional public directories. Vet Trial Finder does not independently verify clinicians, licenses, credentials or quality of care. Inclusion is not a recommendation. Confirm the clinician, service, cost and current availability directly with the clinic.</p></div></div>'''
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
    print(f'WY_STATE_GUIDE_OK physical={len(physical)} mobile={len(mobile)} chemotherapy={len(chemo)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
