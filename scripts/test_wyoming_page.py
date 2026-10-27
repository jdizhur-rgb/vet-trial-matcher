#!/usr/bin/env python3
"""Check Wyoming guide scope, mobile identity, source dates and discoverability."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from oncology_wyoming import STATE_PATH, URL, state_rows
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
    mobile = [r for r in rows if r.get('location_type') == 'mobile']
    assert f'{len(physical)} physical locations' in source
    assert f'{len(mobile)} mobile services' in source
    sections = dict(re.findall(r'<section id="([^"]+)">(.*?)</section>', source, re.S))
    assert set(re.findall(r'data-source-id="([^"]+)"', sections['chemotherapy'])) == {
        r['source_id'] for r in physical if 'Chemotherapy' in r['services'] and r.get('accepting_new_patients') is not False}
    assert 'wy-jackson-animal-hospital' in sections['chemotherapy']
    assert 'wy-lifetime-animal-hospital' in sections['chemotherapy']
    assert 'wy-salt-creek-veterinary-clinic' in sections['local-care']
    salt = re.search(r'<article[^>]+id="wy-salt-creek-veterinary-clinic".*?</article>', source, re.S)[0]
    assert '<li>Chemotherapy</li>' not in salt and '<li>Tumor surgery</li>' not in salt
    for row in rows:
        card = re.search(r'<article[^>]+id="' + re.escape(row['source_id']) + r'".*?</article>', source, re.S)[0]
        dial = ''.join(c for c in row['phone'] if c.isdigit() or c == '+')
        assert 'tel:' + dial in card
        assert '<img' not in card and 'data-lat' not in card
        if row in mobile:
            assert row['source_id'] in sections['mobile-care']
            assert row['source_id'] not in sections['local-care']
            assert 'data-location-type="mobile"' in card
            assert not row['street'] and not row['postal_code']
            assert 'Mobile service' in card
        else:
            assert row['postal_code'] in card
    assert '411 Eagle Lane' in sections['mobile-care']
    assert '353 Eagle Lane' not in source
    assert 'northern Colorado' in sections['mobile-care']
    assert 'resident board-certified medical oncologist' in source
    assert 'their visits do not establish an on-site medical oncologist or radiation service' in source
    assert 'not a complete census' in source
    assert 'coverage was reviewed on October 26, 2026' in source
    assert 'Page publication is not a new clinic verification' in source
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        obj = json.loads(match[1])
        if obj.get('@type') == 'ItemList':
            assert obj['numberOfItems'] == len(rows)
            assert {r['name'] for r in obj['itemListElement']} == {r['name'] for r in rows}
            assert all(x['url'].startswith(URL + '#') for x in obj['itemListElement'])
            break
    else:
        raise AssertionError('Missing clinic ItemList')
    print(f'WY_STATE_PAGE_PASS physical={len(physical)} mobile={len(mobile)}; exact identities, dates, scope and indexing preserved')


if __name__ == '__main__':
    main()
