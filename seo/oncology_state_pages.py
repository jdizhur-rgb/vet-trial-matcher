#!/usr/bin/env python3
"""One owner-approved state guide, generated from the canonical care directory."""
from __future__ import annotations

import html
import json
from pathlib import Path

import generate_seo as g
from site_shell import wrap_html

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = 'veterinary-oncology/rhode-island'
URL = 'https://vettrialfinder.com/' + STATE_PATH + '/'
TITLE = 'Veterinary oncologists and cancer care in Rhode Island'
DESCRIPTION = 'Find veterinary oncology, chemotherapy, electrochemotherapy and tumor surgery in Rhode Island. Compare local services, addresses, phone numbers and official sources.'


GUIDE_CSS = '''.ri-care-guide{max-width:1000px;margin:0 auto}.ri-care-guide .lead{max-width:850px}
.ri-care-guide .ri-summary{padding:16px 20px;background:#edf4f8;border:1px solid #d5e2ea;border-radius:10px;margin:22px 0}
.ri-care-guide .ri-summary p{margin:0}.ri-care-guide .ri-summary nav{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:12px}
.ri-listings{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.ri-care-guide .ri-listing{margin:0;padding:20px;border:1px solid #d9e2ea;border-radius:10px;min-width:0}
.ri-care-guide .ri-listing h3{margin:0 0 8px;font-size:1.15rem;line-height:1.35}
.ri-address,.ri-source-date{color:#607086}.ri-source-date{font-size:.8rem}
.ri-services{display:flex;flex-wrap:wrap;gap:7px;list-style:none;padding:0;margin:14px 0}
.ri-services li{padding:4px 9px;background:#edf4f8;border-radius:6px;color:#315f7d;font-size:.84rem}
.ri-contacts{display:flex;flex-wrap:wrap;gap:10px 20px}.ri-contacts a{overflow-wrap:anywhere}
.ri-care-guide section{margin:30px 0}.ri-care-guide .ri-notice{padding-top:18px;border-top:1px solid #d9e2ea;font-size:.88rem;color:#607086}
@media(max-width:650px){.ri-listings{grid-template-columns:1fr}.ri-care-guide .ri-listing{padding:17px}.ri-care-guide .ri-summary{padding:15px}}'''

def esc(value):
    return html.escape(str(value or ''), quote=True)


def state_rows():
    rows = json.loads((ROOT / 'data/oncology_centers.json').read_text())['centers']
    return sorted((r for r in rows if r.get('country') == 'USA' and r.get('region') == 'RI'
                   and r.get('location_type', 'physical') == 'physical'),
                  key=lambda r: (r['city'], r['name']))


def listing(row):
    identity = row['source_id']
    labels = {'Surgery': 'Tumor surgery', 'ECT': 'Electrochemotherapy (ECT)'}
    services = ''.join(f'<li>{esc(labels.get(s, s))}</li>' for s in row['services'])
    note = f'<p>{esc(row["availability_note"])}</p>' if row.get('availability_note') else ''
    address = ', '.join(str(row.get(k) or '') for k in ('street', 'city', 'region', 'postal_code'))
    # Keep inherited source dates; generating this guide is not a new clinic check.
    checked = f'<p class="ri-source-date">Directory record checked: <time datetime="{esc(row["last_verified"])}">{esc(row["last_verified"])}</time></p>' if row.get('last_verified') else ''
    phone = str(row.get('phone') or '')
    dial = ''.join(c for c in phone if c.isdigit() or c == '+')
    return f'''<article class="ri-listing" id="{esc(identity)}" data-source-id="{esc(identity)}">
<h3>{esc(row['name'])}</h3><p class="ri-address">{esc(address)}</p>
<ul class="ri-services" aria-label="Listed services">{services}</ul>{note}
<p class="ri-contacts"><a href="tel:{esc(dial)}">{esc(phone)}</a><a href="{esc(row['website'])}" target="_blank" rel="noopener">Official clinic website</a></p>{checked}</article>'''


def generate(root):
    rows = state_rows()
    assert rows and all(r.get('source_id') and r.get('website') for r in rows)
    specialist = [r for r in rows if 'Medical oncology' in r['services']]
    treatment = [r for r in rows if r not in specialist and set(r['services']) & {'Chemotherapy', 'ECT', 'Electrochemotherapy'}]
    other = [r for r in rows if r not in specialist and r not in treatment]
    chemo = sum(bool(set(r['services']) & {'Chemotherapy', 'Chemotherapy administration and monitoring'}) for r in rows)
    ect = sum(bool(set(r['services']) & {'ECT', 'Electrochemotherapy'}) for r in rows)
    sections = ''
    for anchor, heading, records in (
        ('oncology', 'Dedicated veterinary oncology', specialist),
        ('chemotherapy-ect', 'Local chemotherapy and electrochemotherapy', treatment),
        ('local-care', 'Local cancer care and tumor surgery', other),
    ):
        if records:
            sections += f'<section id="{anchor}"><h2>{heading}</h2><div class="ri-listings">' + ''.join(listing(r) for r in records) + '</div></section>'
    body = f'''<div class="ri-care-guide">
<style>
{GUIDE_CSS}
</style>
<p><a href="/matcher/centers/">Find oncology care</a> / Rhode Island</p>
<h1>Veterinary oncology and cancer care in Rhode Island</h1>
<p class="lead">Where to find a veterinary oncologist, chemotherapy, electrochemotherapy (ECT), and local tumor surgery for dogs and cats in Rhode Island.</p>
<div class="ri-summary"><p><strong>{len(rows)} listed locations</strong> · {chemo} list chemotherapy · {ect} lists electrochemotherapy</p>
<nav aria-label="On this page"><a href="#oncology">Dedicated oncology</a><a href="#chemotherapy-ect">Chemotherapy and ECT</a><a href="#local-care">Local care and surgery</a></nav></div>
<p>These clinics offer different levels of care. A general practice that removes tumors is not the same as a dedicated oncology service. The listings below separate specialist oncology from local cancer care and show the services recorded in our directory.</p>
<p>Ocean State Veterinary Specialists in East Greenwich has a dedicated oncology service and administers chemotherapy. Its team coordinates with nearby radiation facilities; radiation treatment is not listed here as an on-site service. <a href="https://osvs.net/oncology/" target="_blank" rel="noopener">Read the hospital’s oncology information</a>.</p>
<p>Wood River Animal Hospital in Wyoming lists chemotherapy, electrochemotherapy and cancer vaccines. Confirm the treating veterinarian, the specific treatment and appointment availability directly with the hospital. <a href="https://www.woodriveranimalhospitalinc.com/services" target="_blank" rel="noopener">Read its published services</a>.</p>
{sections}
<section><h2>Before making an appointment</h2><p>Ask whether the clinic treats your pet’s particular cancer and which veterinarian would see the case. Confirm whether a referral is needed, which records to send, and the consultation and treatment costs. A service listed on a website does not establish that every procedure is suitable for every tumor.</p><p>For care outside Rhode Island, use the <a href="/matcher/centers/">oncology care finder</a> to compare other states and services. You can also <a href="/matcher/">search cancer clinical trials</a> or read our <a href="/cancer-types/">cancer guides for dogs and cats</a>. Trial locations and eligibility are separate from the clinic listings on this page.</p></section>
<div class="ri-notice"><p><strong>About this list:</strong> Rhode Island coverage was reviewed on October 23, 2026. Individual record dates appear above. This is a selection of locations with published cancer-related services, not a complete census of every practice in the state. An unlisted service has not been confirmed in this directory; it is not proof that the clinic does not offer it.</p><p>Service information is compiled from clinic websites and professional public directories. Vet Trial Finder does not independently verify clinicians, licenses, credentials or quality of care. Inclusion is not a recommendation. Confirm the clinician, service, cost and current availability directly with the clinic.</p></div></div>'''
    text = g.page(TITLE, DESCRIPTION, body, URL)
    schema = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': TITLE,
              'numberOfItems': len(rows), 'itemListElement': [
                  {'@type': 'ListItem', 'position': i, 'name': r['name'], 'url': URL + '#' + r['source_id']}
                  for i, r in enumerate(specialist + treatment + other, 1)]}
    social = (f'<meta property="og:type" content="website"><meta property="og:title" content="{esc(TITLE)}">'
              f'<meta property="og:description" content="{esc(DESCRIPTION)}"><meta property="og:url" content="{URL}">')
    text = text.replace('</head>', social + '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script></head>', 1)
    dest = root / STATE_PATH / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(wrap_html(text), encoding='utf-8')
    print(f'RI_STATE_GUIDE_OK locations={len(rows)} chemotherapy={chemo} ECT={ect}')


if __name__ == '__main__':
    generate(ROOT / 'seo/site')
