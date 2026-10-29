#!/usr/bin/env python3
"""MA guide: exact identities, local modality scope, intake and discoverability."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from oncology_massachusetts import STATE_PATH, URL, state_rows
from test_oncology_state_page import Guide


def ids(section):
    return set(re.findall(r'data-source-id="([^"]+)"', section))


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
    sections = dict(re.findall(r'<section id="([^"]+)">(.*?)</section>', source, re.S))
    physical = [r for r in rows if r.get('location_type', 'physical') == 'physical']
    mobile = [r for r in rows if r.get('location_type') == 'mobile']
    networks = [r for r in rows if r.get('location_type') == 'network']
    restricted = [r for r in physical if r.get('accepting_new_patients') is False]
    chemo = [r for r in physical if 'Chemotherapy' in r['services'] and r not in restricted]
    assert ids(sections['chemotherapy']) == {r['source_id'] for r in chemo}
    assert ids(sections['mobile-care']) == {r['source_id'] for r in mobile}
    assert ids(sections['network-contacts']) == {r['source_id'] for r in networks}
    assert ids(sections['intake-restrictions']) == {r['source_id'] for r in restricted}
    assert f'{len(physical)} physical locations' in source
    assert f'{len(chemo)} physical locations list chemotherapy' in source
    assert 'ma-brookside-greenfield' not in ids(sections['local-care'])
    assert 'ma-brookside-greenfield' in ids(sections['intake-restrictions'])
    assert 'not accepting new clients' in sections['intake-restrictions']
    assert {'ma-sturbridge-general', 'ma-vsc-sturbridge'} <= ids(sections['local-care'])
    assert 'ma-south-coastal-network' not in ids(sections['chemotherapy'])
    assert 'ma-mspca-community-program' in ids(sections['network-contacts'])
    assert 'ma-moves-powers-ne-ma' in ids(sections['mobile-care'])
    assert 'ma-offshore-nantucket' in ids(sections['local-care'])
    for row in rows:
        card = re.search(r'<article[^>]+id="' + re.escape(row['source_id']) + r'".*?</article>', source, re.S)[0]
        assert '<img' not in card and 'data-lat' not in card
        assert '<a href="tel:">' not in card
        if row.get('location_type', 'physical') == 'physical':
            assert row['postal_code'] in card
        else:
            assert not row.get('street') and not row.get('postal_code')
            assert 'data-location-type="' + row['location_type'] + '"' in card
        if row.get('email') and row.get('location_type') in ('mobile', 'network'):
            assert 'mailto:' + row['email'] in parser.links
        if row['source_id'] == 'ma-offshore-nantucket':
            assert '<li>Chemotherapy</li>' not in card and '<li>Tumor surgery</li>' not in card
    assert 'not a complete census' in source
    assert 'Page publication is not a new clinic verification' in source
    assert 'indexed copies of primary pages' in source
    assert 'does not independently verify clinicians, licenses, credentials or quality of care' in source
    assert 'clinical-trial' not in sections['chemotherapy'].lower()
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        obj = json.loads(match[1])
        if obj.get('@type') == 'ItemList':
            assert obj['numberOfItems'] == len(rows)
            assert len(obj['itemListElement']) == len(rows)
            assert {r['name'] for r in obj['itemListElement']} == {r['name'] for r in rows}
            assert all(x['url'].startswith(URL + '#') for x in obj['itemListElement'])
            break
    else:
        raise AssertionError('Missing clinic ItemList')
    print(f'MA_STATE_PAGE_PASS physical={len(physical)} mobile={len(mobile)} network={len(networks)}; exact identities, inherited dates, service limits and indexing preserved')


if __name__ == '__main__':
    main()
