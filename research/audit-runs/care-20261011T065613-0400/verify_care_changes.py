import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[2]
sys.path.insert(0,str(ROOT/'seo'))
import oncology_teleconsultations as tele
spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/build_oncology_center_catalog.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
centers=json.loads((ROOT/'data/oncology_centers.json').read_text())['centers']
inventory=json.loads((ROOT/'data/oncology_care_source_inventory.json').read_text())['sources']
receipt=json.loads((RUN/'receipt-final.json').read_text())
assert len(centers)==438 and len(tele.ROWS)==59 and len(inventory)==506
assert len({s['id'] for s in inventory})==506
assert len({(c['name'],c['street'],c['city'],c['country']) for c in centers})==438
for c in centers:
    assert all(c.get(k) for k in ['name','city','region','country','services'])
    if c.get('latitude') is not None and c.get('longitude') is not None:
        assert -90 <= float(c['latitude']) <= 90 and -180 <= float(c['longitude']) <= 180
    else:
        old=json.loads((RUN/'oncology_centers.json.before').read_text())['centers']
        assert any(o['name']==c['name'] and o.get('latitude') is None for o in old), 'New missing coordinate'
for s in inventory:
    at=datetime.fromisoformat(s['last_checked_at'])
    assert at.utcoffset() is not None and at.date().isoformat()==s['last_checked']=='2026-10-11'
    assert s['last_result'] in {'success','partial','unreachable'}
    assert s['content_sufficient']==(s['last_result']=='success')
    assert s['master_url'].startswith('https://')
    assert isinstance(s['supporting_urls'],list)
assert len(receipt['sources'])==506 and receipt['attempted_total']==506
def find(needle): return [c for c in centers if needle.casefold() in c['name'].casefold()]
akron=find('MedVet Akron'); metro=[c for c in centers if 'Metropolitan' in c['name'] and c['postal_code']=='44321']
assert len(akron)==len(metro)==1 and not builder.center_match(akron[0],metro[0])
assert akron[0]['street'].startswith('1321') and metro[0]['street'].startswith('1053')
assert not [c for c in find('Animal Cancer Care Specialists') if c['city']=='Acton']
assert [c for c in find('Animal Cancer Care Specialists') if c['city']=='Littleton']
assert 'Radiation oncology' in find('Kyoto')[0]['services']
assert 'ECT' in find('Aihara')[0]['services']
assert 'ECT' in find('Southwater')[0]['services']
assert 'Radiation oncology' not in find('Missouri Animal Cancer Care')[0]['services']
assert not find('ACCESS Pasadena') and not find('Safe Haven')
assert not any(row[1]=='Russia' for row in tele.ROWS)
assert len({(r[1],r[2]) for r in tele.ROWS})==59
assert all(r[0] in tele.REGIONS for r in tele.ROWS)
assert sum(tele.access_key(r[5]).find('owner')>=0 for r in tele.ROWS)==45
assert all(tele.access_key(r[5])=='vet' for r in tele.ROWS if r[2].startswith(('Pet Cancer Consulting','CVS Collaborative')))
assert tele.access_key(next(r[5] for r in tele.ROWS if r[2]=='ARC Vets'))=='vet'
html=(ROOT/'seo/static/matcher/centers/index.html').read_text()
soup=BeautifulSoup(html,'html.parser')
cards=[dict(c.attrs) for c in soup.select('.p-card')]
assert len(cards)==438
for needle in ['Kyoto','Aihara','Southwater','MedVet Akron']:
    assert any(needle in c.get_text() for c in soup.select('.p-card'))
script=next(s.get_text() for s in soup.find_all('script') if 'function textFilter()' in s.get_text())
(RUN/'filter-test-fixture.json').write_text(json.dumps({'cards':cards,'script':script,'tele_script':tele.SCRIPT.removeprefix('<script>').removesuffix('</script>'),'tele_cards':[{'access':tele.access_key(r[5]),'specialty':r[6].lower(),'search':' '.join(r).lower(),'name':r[2]} for r in tele.ROWS]},ensure_ascii=False)+'\n')
print(json.dumps({'status':'PASS','centers':len(centers),'countries':dict(Counter(c['country'] for c in centers)),'teleconsultations':59,'care_sources':506,'identity_regressions':'PASS','coordinates_schema':'PASS','unique_ids':'PASS'},indent=2))
