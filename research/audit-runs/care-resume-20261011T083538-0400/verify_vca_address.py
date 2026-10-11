import importlib.util,json,urllib.request,sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));from scripts.check_evidence_keys import redact_text
s=importlib.util.spec_from_file_location('vca',ROOT/'scripts/research_vca_oncology.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
assert v.address_parts('12531 Old Seward Highway  Anchorage AK 99515')==('12531 Old Seward Highway','Anchorage','AK','99515')
assert v.address_parts('1612 N High Point Rd  Middleton WI 53562  Suite 100')==('1612 N High Point Rd Suite 100','Middleton','WI','53562')
assert v.address_parts('6650 Hawaii Kai Dr  Honolulu HI 96825  Suite 105')==('6650 Hawaii Kai Dr Suite 105','Honolulu','HI','96825')
assert v.address_parts('undetermined')==('','','','')
rows=[]
for u in ['https://vcahospitals.com/gentle-vets','https://vcahospitals.com/veterinary-specialty-center-middleton']:
 d={'url':u,'attempted_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),'method':'urllib official HTML identity extraction'}
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers=v.HEADERS),timeout=15) as res:body=res.read().decode('utf8','replace');d['http_status']=res.status
  raw=v.first(r"_mapAddress\s*=\s*'([^']+)'",body);d.update(raw_map_address=raw,parsed_address=v.address_parts(raw),name=v.first(r"_hospitalName\s*=\s*'([^']+)'",body),latitude=v.first(r"_lat\s*=\s*'([^']+)'",body),longitude=v.first(r"_lng\s*=\s*'([^']+)'",body));assert all(d['parsed_address'])
 except Exception as e:d['error']=str(e)
 rows.append(d)
(RUN/'vca-address-regression.json').write_text(redact_text(json.dumps({'unit_regressions':'PASS','live_identity_rechecks':rows},ensure_ascii=False,indent=2))+'\n');print(json.dumps(rows,ensure_ascii=False))
