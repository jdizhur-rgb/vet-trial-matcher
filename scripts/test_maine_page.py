#!/usr/bin/env python3
"""Check the Maine guide against the care catalog and published route policy."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from oncology_maine import STATE_PATH, URL, state_rows
from test_oncology_state_page import Guide


def main():
    site = ROOT / 'seo/site'
    source = (site / STATE_PATH / 'index.html').read_text()
    rows = state_rows()
    by_id = {row['source_id']: row for row in rows}
    parser = Guide()
    parser.feed(source)
    assert parser.headings == 1
    assert len(parser.ids) == len(rows) == len(set(parser.ids))
    assert set(parser.ids) == set(by_id)
    assert sorted(parser.dates) == sorted(row['last_verified'] for row in rows)
    assert all(row['website'] in parser.links for row in rows)
    assert f'<link rel="canonical" href="{URL}">' in source
    assert not re.search(r'<meta[^>]+name="robots"[^>]+noindex', source)
    assert f'<loc>{URL}</loc>' in (site / 'sitemap.xml').read_text()
    assert URL in (site / 'search/index.html').read_text()
    assert f'/{STATE_PATH}/' in (site / 'matcher/centers/index.html').read_text()

    sections = dict(re.findall(r'<section id="([^"]+)">(.*?)</section>', source, re.S))
    cards = dict(re.findall(r'<article[^>]+data-source-id="([^"]+)"[^>]*>(.*?)</article>', source, re.S))
    specialty = {
        'portland-veterinary-emergency-and-specialty-care',
        'maine-veterinary-medical-center',
    }
    assert set(re.findall(r'data-source-id="([^"]+)"', sections['specialty-care'])) == specialty
    assert '422 US Route 1' in cards['portland-veterinary-emergency-and-specialty-care']
    assert '739 Warren' not in cards['portland-veterinary-emergency-and-specialty-care']
    assert 'me-lucerne-veterinary-hospital' in sections['local-chemotherapy']
    assert '<li>Chemotherapy</li>' not in cards['me-veazie-veterinary-clinic']
    assert 'existing patients' in sections['intake-restrictions']
    assert 'me-animal-welfare-society-kennebunk' in sections['intake-restrictions']
    assert 'me-dirigo-veterinary-care' in sections['intake-restrictions']
    assert 'me-maine-vets-mobile-pet-care' in sections['mobile-care']
    assert 'Dexter, ME</p>' in cards['me-heart-of-maine-veterinary-surgery-dexter']
    for identity, row in by_id.items():
        card = cards[identity]
        assert ('<li>Chemotherapy</li>' in card) == ('Chemotherapy' in row['services'])
        assert f'datetime="{row["last_verified"]}"' in card
        assert 'tel:' + ''.join(c for c in row['phone'] if c.isdigit() or c == '+') in card
        assert '<img' not in card and 'data-lat' not in card
    assert 'Port City' in sections['radiation-and-trials']
    assert '<li>Radiation oncology</li>' not in source
    assert 'coverage was reviewed on November 9, 2026' in source

    objects = [json.loads(match) for match in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)]
    item_list = next(obj for obj in objects if obj.get('@type') == 'ItemList')
    items = item_list['itemListElement']
    assert item_list['numberOfItems'] == len(items) == len(rows)
    assert [(item['position'], item['url'], item['name']) for item in items] == [
        (i, URL + '#' + identity, by_id[identity]['name']) for i, identity in enumerate(parser.ids, 1)
    ]
    print(f'ME_STATE_PAGE_PASS listings={len(rows)} with matching identities, dates, contacts and index links')


if __name__ == '__main__':
    main()
