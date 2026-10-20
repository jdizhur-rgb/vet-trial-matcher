"""Real rendered production roster and requested form controls, not JSON existence."""
from daily20 import ROOT,RUN,read,write,now
import collections,json
pair=read(RUN/'live-pair.json');expected=read(RUN/'expected-live-searches.json');checks=[]
for c in expected['cases']:
 d=pair[c['country']];want=collections.Counter((x['title'],x['center']) for x in c['records']);got=collections.Counter((x['title'],x['heading'].split(' · ',1)[1]) for x in d['records']);fields={x['name']:x['value'] for x in d['fields']}
 criteria=fields['species']=='Dog' and fields['country']==c['country'] and fields['cancer']=='Cancer — any type' and fields['diagnosis_status']=="I don't know" and all(fields[x]=='' for x in ['age','weight','zip_code','approach']) and len(d['preferences'])==6 and all(x['checked'] for x in d['preferences'])
 checks.append(dict(country=c['country'],actual_browser_at=d['at'],actual_count=len(d['records']),expected_count=c['count'],whole_rendered_roster_equal=want==got,missing=list((want-got).elements()),extra=list((got-want).elements()),all_requested_controls_verified=criteria,status='PASS' if want==got and criteria else 'FAIL',evidence_file=str((RUN/'live-pair.json').relative_to(ROOT))))
result=dict(comparison_at=now(),method='Real production browser search via visible UI, complete DOM-rendered headings/card links; Work independently calculated expected roster from current built catalog; no injected results or hidden state.',production_commit=read(RUN/'publication.json')['main_commit'],cases=checks,overall='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL');write(RUN/'live-search-evidence.json',result);print(json.dumps(result))
