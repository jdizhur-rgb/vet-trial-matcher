#!/usr/bin/env python3
"""Owner-approved Massachusetts guide from canonical care records."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from oncology_state_pages import GUIDE_CSS, esc, listing
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/massachusetts'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncology and cancer care in Massachusetts'
DESCRIPTION = 'Find veterinary oncology, chemotherapy, tumor surgery and visiting cancer care for dogs and cats in Massachusetts, with clinic contacts, sources and access limits.'


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((r for r in rows if r.get('country') == 'USA' and r.get('region') == 'MA'),
                  key=lambda r: (r.get('city', ''), r['name']))


def service_listing(row):
    kind = row['location_type']
    label = 'Mobile and visiting service' if kind == 'mobile' else 'Network contact; treatment branch to confirm'
    labels = {'Surgery': 'Tumor surgery', 'ECT': 'Electrochemotherapy (ECT)'}
    services = ''.join(f'<li>{esc(labels.get(s, s))}</li>' for s in row['services'])
    contacts = []
    if row.get('phone'):
        dial = ''.join(c for c in row['phone'] if c.isdigit() or c == '+')
        contacts.append(f'<a href="tel:{esc(dial)}">{esc(row["phone"])}</a>')
    if row.get('email'):
        contacts.append(f'<a href="mailto:{esc(row["email"])}">{esc(row["email"])}</a>')
    contacts.append(f'<a href="{esc(row["website"])}" target="_blank" rel="noopener">Official service website</a>')
    checked = row['last_verified']
    return f'''<article class="ri-listing" id="{esc(row['source_id'])}" data-source-id="{esc(row['source_id'])}" data-location-type="{esc(kind)}">
<h3>{esc(row['name'])}</h3><p class="ri-address">{label} · {esc(row.get('service_area'))}</p>
<ul class="ri-services" aria-label="Listed services">{services}</ul>
<p>{esc(row.get('availability_note'))}</p><p class="ri-contacts">{''.join(contacts)}</p>
<p class="ri-source-date">Directory record checked: <time datetime="{esc(checked)}">{esc(checked)}</time></p></article>'''


def generate(root):
    rows = state_rows()
    physical = [r for r in rows if r.get('location_type', 'physical') == 'physical']
    mobile = [r for r in rows if r.get('location_type') == 'mobile']
    networks = [r for r in rows if r.get('location_type') == 'network']
    restricted = [r for r in physical if r.get('accepting_new_patients') is False]
    chemo = [r for r in physical if 'Chemotherapy' in r['services'] and r not in restricted]
    local = [r for r in physical if r not in chemo and r not in restricted]
    assert len(physical) + len(mobile) + len(networks) == len(rows)
    assert rows and all(r.get('source_id') and r.get('website') and r.get('last_verified') for r in rows)
    groups = [
        ('chemotherapy', 'Local chemotherapy and oncology services', chemo, listing),
        ('local-care', 'Local cancer care and tumor surgery', local, listing),
        ('mobile-care', 'Mobile and visiting surgical services', mobile, service_listing),
        ('network-contacts', 'Network contacts: confirm the treatment branch', networks, service_listing),
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
<p><a href="/matcher/centers/">Find oncology care</a> / Massachusetts</p>
<h1>{TITLE}</h1>
<p class="lead">Find specialist oncology, local chemotherapy and tumor surgery for dogs and cats in Massachusetts. Compare published services, clinic contacts and the limits that matter before arranging treatment.</p>
<div class="ri-summary"><p><strong>{len(physical)} physical locations</strong>, {len(mobile)} visiting surgical service and {len(networks)} network contacts · {len(chemo)} physical locations list chemotherapy</p><nav aria-label="On this page">{navigation}</nav></div>
<section><h2>Choosing the right level of cancer care</h2>
<p>Massachusetts has dedicated oncology services as well as general veterinary practices that provide parts of cancer care. A mass-removal or chemotherapy listing does not establish a board-certified medical oncologist at every clinic. Ask which veterinarian will assess your pet and whether the proposed treatment can be delivered at that location.</p>
<p>Published specialist services include MSPCA-Angell in Boston, the Tufts Foster Hospital in North Grafton, Tufts VETS in Walpole, Massachusetts Veterinary Referral Hospital in Woburn, Ally Veterinary in Lincoln and specialist hospitals elsewhere in the state. Their listed treatments differ: use the individual cards to compare chemotherapy, electrochemotherapy, radiation and surgical services rather than assuming every hospital offers every method.</p>
<p>Some general practices administer chemotherapy locally. Others remove masses, help manage symptoms or coordinate specialist care. A published service does not establish that every drug, protocol or complex tumor operation is available or suitable for your pet.</p></section>
<section><h2>Lower-cost care and referral arrangements</h2>
<p>Second Chance in North Brookfield publishes mass-removal surgery and is open to owners at regular fees, with subsidized rates for households meeting its documented income requirements. The MSPCA community-clinic program has separate financial and clinical eligibility rules and branch-specific application routes. These are different programs; neither listing promises free or comprehensive specialist oncology.</p>
<p>Love Is Life Veterinary Clinic in Franklin publishes surgical care without an income requirement, with diagnostic work completed by the referring veterinarian beforehand and no overnight hospitalization. Confirm whether the proposed tumor operation meets the clinic’s case criteria.</p>
<p>South Coastal lists chemotherapy at practice level, but the treatment branch in Weymouth or Rockland needs confirmation. It appears once as a network contact below. Visiting surgery with MOVES Michelle Powers is arranged through your primary veterinarian and a host hospital, rather than a fixed Massachusetts office or an owner appointment portal.</p></section>
{sections}
<section><h2>Before arranging treatment</h2>
<p>Ask whether the clinic accepts your pet’s cancer and which veterinarian would see the case. Confirm referral requirements, records and pathology to send, consultation and treatment costs, appointment dates and monitoring between visits. For surgery, ask about the proposed margins, pathology review, recovery care and whether a specialist referral may be needed.</p>
<p>If a specialist and your local veterinarian share treatment, clarify who will prescribe or administer medication, review blood tests and handle urgent problems. Brookside in Greenfield currently states that it is not accepting new clients; its listing is separated under intake restrictions.</p>
<p>Use the <a href="/matcher/centers/">oncology care finder</a> to filter Massachusetts clinics by service or compare nearby states. You can also explore <a href="/online-oncology-consultations/">oncology teleconsultations</a>, <a href="/matcher/">search cancer clinical trials</a>, or read the <a href="/cancer-types/">cancer guides for dogs and cats</a>. Clinical-trial eligibility and enrollment are separate from these local-care listings.</p></section>
<div class="ri-notice"><p><strong>About this list:</strong> Massachusetts coverage was reviewed on October 28, 2026. Individual record dates appear above. Page publication is not a new clinic verification. This is a selection of locations with published cancer-related services, not a complete census of every practice in the state. Specific treatment or branch questions remain unresolved at some practices reviewed during discovery. An unlisted service is unconfirmed in this directory; it is not proof that a clinic does not offer it.</p>
<p>Some clinical descriptions were reviewed through indexed copies of primary pages when direct pages could not be retrieved. The individual notes retain those source limits. Service information is compiled from clinic websites, care-program partners and professional public directories. Vet Cancer Care Finder does not independently verify clinicians, licenses, credentials or quality of care. Inclusion is not a recommendation. Confirm the clinician, service, cost and current availability directly with the clinic. <a href="/how-we-verify/">How we verify listings</a>.</p></div></div>'''
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
    print(f'MA_STATE_GUIDE_OK physical={len(physical)} mobile={len(mobile)} network={len(networks)} chemotherapy={len(chemo)}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
