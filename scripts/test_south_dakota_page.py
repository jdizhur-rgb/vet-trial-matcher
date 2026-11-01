#!/usr/bin/env python3
"""SD guide: canonical identities/dates, conservative services and discoverability."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from oncology_south_dakota import STATE_PATH, URL, state_rows
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
    sections = dict(re.findall(r'<section id="([^"]+)">(.*?)</section>', source, re.S))
    ids = lambda text: set(re.findall(r'data-source-id="([^"]+)"', text))
    chemo = {r['source_id'] for r in rows if 'Chemotherapy' in r['services'] and r.get('accepting_new_patients') is not False}
    assert ids(sections['chemotherapy']) == chemo
    assert {'upleash-veterinary-hospital', 'dunes-animal-hospital'} <= chemo
    assert 'sd-best-care-pet-hospital' not in chemo
    assert f'{len(rows)} physical locations' in source
    for row in rows:
        card = re.search(r'<article[^>]+id="' + re.escape(row['source_id']) + r'".*?</article>', source, re.S)[0]
        assert 'tel:' + ''.join(c for c in row['phone'] if c.isdigit() or c == '+') in card
        assert row['postal_code'] in card and '<img' not in card and 'data-lat' not in card
        assert ('<li>Tumor surgery</li>' in card) == ('Surgery' in row['services'])
        assert ('<li>Chemotherapy</li>' in card) == ('Chemotherapy' in row['services'])
    assert 'about twice monthly' in sections['local-care']
    assert 'Vermillion branch explicitly sends surgery to Yankton' in sections['local-care']
    assert 'no immunotherapy service tag is added' in sections['local-care']
    assert 'Surgical laser use is distinct from radiation therapy' in sections['local-care']
    assert 'not a complete census' in source
    assert 'coverage was reviewed on November 1, 2026' in source
    assert 'Page publication is not a new clinic verification' in source
    assert 'professional-license records do not establish present employment' in source
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        obj = json.loads(match[1])
        if obj.get('@type') == 'ItemList':
            assert obj['numberOfItems'] == len(rows)
            assert {x['name'] for x in obj['itemListElement']} == {r['name'] for r in rows}
            assert all(x['url'].startswith(URL + '#') for x in obj['itemListElement'])
            break
    else:
        raise AssertionError('Missing clinic ItemList')
    print(f'SD_STATE_PAGE_PASS physical={len(rows)} chemotherapy={len(chemo)}; identities, dates, service limits and indexing preserved')


if __name__ == '__main__':
    main()
