"""Apply two current-primary filter corrections; preserve the frozen baseline."""
import json,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
reviews=read(P/'ovc-source-derived-review.json');cat=read(ROOT/'data/trials_base.json');base=read(ROOT/'data/protocol_selection_baseline.json');cases=read(ROOT/'data/protocol_selection_cases.json');changes=[]
for review in reviews:
    t=next(t for t in cat if t['id']==review['trial_id']);before=json.loads(json.dumps(t));review['reviewed_at']=datetime.now(ZoneInfo('America/New_York')).isoformat()
    if t['id']=='ca-ovc-oral-melanoma-palladia':t['treatment_approaches']=['targeted_therapy']
    else:
        t['requires']['appendicular_location']=True
        t['special_requirement']='The osteosarcoma must be in the distal radius (lower forelimb); an appendicular/limb answer alone does not establish this location. The study team must confirm exact anatomy and any prior chemotherapy/bisphosphonate use.'
    t['verified']='2026-10-16'
    selection={k:t.get(k) for k in base['signature_fields']};review['selection_sha256']=hashlib.sha256(json.dumps(selection,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    assert not any(r['trial_id']==t['id'] for r in cases['reviews'])
    cases['reviews'].append({k:review[k] for k in ('trial_id','source_url','reviewed_at','criteria','cases','selection_sha256')});changes.append({'trial_id':t['id'],'before':before,'after':t})
write(ROOT/'data/trials_base.json',cat);write(ROOT/'data/protocol_selection_cases.json',cases);write(P/'ovc-source-derived-review.json',reviews);write(P/'ovc-canonical-changes.json',changes)
