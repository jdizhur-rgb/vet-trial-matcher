#!/usr/bin/env python3
"""Check ND identities, inherited dates, access scope and discoverability."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from oncology_north_dakota import STATE_PATH, URL, state_rows
from test_oncology_state_page import Guide


def main():
    site = ROOT / 'seo/site'
    source = (site / STATE_PATH / 'index.html').read_text()
    rows = state_rows()
    parser = Guide(); parser.feed(source)
    assert parser.headings == 1
    assert len(parser.ids) == len(rows) == len(set(parser.ids))
    assert set(parser.ids) == {r['source_id'] for r in rows}
    assert sorted(parser.dates) == sorted(r['last_verified'] for r in rows)
    assert all(r['website'] in parser.links for r in rows)
    assert f'<link rel="canonical" href="{URL}">' in source
    assert not re.search(r'<meta[^>]+name="robots"[^>]+noindex', source)
    assert f'<loc>{URL}</loc>' in (site / 'sitemap.xml').read_text()
    assert URL in (site / 'search/index.html').read_text()
    assert '/' + STATE_PATH + '/' in (site / 'matcher/centers/index.html').read_text()
    physical = [r for r in rows if r.get('location_type', 'physical') == 'physical']
    networks = [r for r in rows if r.get('location_type') == 'network']
    assert f'{len(physical)} physical locations' in source
    assert len(networks) == 1
    sections = dict(re.findall(r'<section id="([^"]+)">(.*?)</section>', source, re.S))
    red = 'red-river-animal-emergency-hospital-referral-center'
    assert red in sections['specialty-oncology'] and red not in sections['chemotherapy']
    assert 'not accepting new oncology patients' in source
    assert 'state-ave-veterinary-clinic' in sections['chemotherapy']
    assert 'nd-gilbertson-veterinary-clinic' in sections['local-care']
    gilbertson = re.search(r'<article[^>]+id="nd-gilbertson-veterinary-clinic".*?</article>', source, re.S)[0]
    assert '<li>Chemotherapy</li>' not in gilbertson and '<li>Immunotherapy</li>' not in gilbertson
    assert networks[0]['source_id'] in sections['network-contact']
    assert 'mailto:' + networks[0]['email'] in parser.links
    assert 'Network contact; treatment branch to confirm' in sections['network-contact']
    for row in physical:
        card = re.search(r'<article[^>]+id="' + re.escape(row['source_id']) + r'".*?</article>', source, re.S)[0]
        assert row['postal_code'] in card
        dial = ''.join(c for c in row['phone'] if c.isdigit() or c == '+')
        assert 'tel:' + dial in card
    assert 'not a complete census' in source
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        obj = json.loads(match[1])
        if obj.get('@type') == 'ItemList':
            assert obj['numberOfItems'] == len(rows)
            assert {r['name'] for r in obj['itemListElement']} == {r['name'] for r in rows}
            assert all(x['url'].startswith(URL + '#') for x in obj['itemListElement'])
            break
    else: raise AssertionError('Missing clinic ItemList')
    print(f'ND_STATE_PAGE_PASS physical={len(physical)} network={len(networks)}; identities, dates, restricted intake and indexing preserved')


if __name__ == '__main__':
    main()
