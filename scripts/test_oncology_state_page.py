#!/usr/bin/env python3
"""Verify the one approved state page against the actual public care catalog."""
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'seo'))
from oncology_state_pages import STATE_PATH, URL, state_rows


class Guide(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.headings = 0
        self.links = []
        self.dates = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1': self.headings += 1
        if 'data-source-id' in attrs: self.ids.append(attrs['data-source-id'])
        if tag == 'a': self.links.append(attrs.get('href', ''))
        if tag == 'time': self.dates.append(attrs.get('datetime'))


def main():
    site = ROOT / 'seo/site'
    source = (site / STATE_PATH / 'index.html').read_text()
    rows = state_rows()
    parser = Guide(); parser.feed(source)
    assert parser.headings == 1
    assert len(parser.ids) == len(rows) == len(set(parser.ids))
    assert set(parser.ids) == {r['source_id'] for r in rows}
    assert sorted(parser.dates) == sorted(r['last_verified'] for r in rows if r.get('last_verified'))
    assert f'<link rel="canonical" href="{URL}">' in source
    assert not re.search(r'<meta[^>]+name="robots"[^>]+noindex', source)
    assert f'<loc>{URL}</loc>' in (site / 'sitemap.xml').read_text()
    assert URL in (site / 'search/index.html').read_text()
    assert '/' + STATE_PATH + '/' in (site / 'matcher/centers/index.html').read_text()
    assert all(r['website'] in parser.links for r in rows)
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        obj = json.loads(match[1])
        if obj.get('@type') == 'ItemList':
            assert obj['numberOfItems'] == len(rows)
            assert {r['name'] for r in obj['itemListElement']} == {r['name'] for r in rows}
            assert all(x['url'].startswith(URL + '#') for x in obj['itemListElement'])
            break
    else: raise AssertionError('Missing clinic ItemList')
    foster = re.search(r'<article[^>]+id="ri-foster-veterinary-clinic".*?</article>', source, re.S)[0]
    assert 'Tumor surgery' not in foster and '<li>Chemotherapy</li>' not in foster
    assert 'not a complete census' in source
    assert 'PCC Providence' not in source
    print(f'RI_STATE_PAGE_PASS {len(rows)} exact catalog identities, source dates, canonical, sitemap, internal links and scope')


if __name__ == '__main__': main()
