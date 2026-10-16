"""Apply the independently primary-derived, site-scoped Missouri correction."""
import json,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).parent;ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
review=read(P/'leah-source-derived-review.json')
at=datetime.now(ZoneInfo('America/New_York')).isoformat();review['reviewed_at']=at
cat=read(ROOT/'data/trials_base.json');t=next(t for t in cat if t['id']==review['trial_id']);before=json.loads(json.dumps(t))
mo=next(s for s in t['inactive_sites'] if 'Missouri' in s.get('hospital',''))
t['inactive_sites']=[s for s in t['inactive_sites'] if 'Missouri' not in s.get('hospital','')]
mo.update({'status':'Currently enrolling — confirmed by the current Missouri study-specific protocol','verified':'2026-10-16',
    'eligibility':'Dogs >10kg; naive or relapsed large-cell CD20+ B-cell lymphoma; clinically well; no primary GI/lung involvement; investigator laboratory screening; no listed immunomodulators; prednisone washout at least72hours.',
    'funding':'Study staging, treatment and rechecks covered; adverse-event allowance up to$4000; $2000 completion stipend for future/additional VHC treatment.',
    'schedule':'At least seven visits in the first21days and longer follow-up until progression/relapse.'})
t['sites'].append(mo)
t['status']='Missouri enrolling per current institutional protocol; Ohio State enrolling per sponsor with local slot to confirm; Minnesota on hold'
t['notes']='One LEAH CAR-T protocol with site-specific cohorts. On October16 the current Missouri study-specific invitation and fresh Web read both explicitly confirm enrolling dogs with spontaneous CD20+ large-cell B-cell lymphoma; the older cached Missouri ON HOLD version is superseded. Missouri includes naive and relapsed patients, >10kg, clinically well, no primary GI or lung involvement, investigator bloodwork clearance, no Apoquel/mycophenolate/cyclosporine/azathioprine and at least72hours off prednisone. It combines lymphodepleting chemotherapy and xenogeneic CAR-T; at least seven visits over21days then longer follow-up. Minnesota current individual protocol remains On hold; its10-50kg and48hour rules must not be generalized to Missouri. Ohio remains enrolling per sponsor; its current institutional index does not name this protocol, so confirm the Ohio slot and local criteria before travel. Missouri-specific eligibility/funding do not establish Ohio or Minnesota terms.'
t['funding']='Missouri: study-related initial staging, treatment and rechecks covered; up to$4000 for adverse events and a$2000 stipend for future/additional VHC treatment upon completion. Sponsor describes Ohio enrollment as fully funded; confirm the current Ohio coverage and slot. Minnesota is on hold; its historical stipend/criteria are not generalized to other sites.'
t['verified']='2026-10-16'
t['source_url']=review['source_url']
t['special_requirement']='Site-specific study-team screening is required. Missouri: >10kg, large-cell CD20+ B-cell lymphoma, clinically well, no primary GI/lung involvement, no listed immunomodulators, >=72h prednisone washout. Ohio criteria/slot must be confirmed. Minnesota is not currently enrolling.'
write(ROOT/'data/trials_base.json',cat)
base=read(ROOT/'data/protocol_selection_baseline.json')
selection={k:t.get(k) for k in base['signature_fields']}
review['selection_sha256']=hashlib.sha256(json.dumps(selection,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
cases=read(ROOT/'data/protocol_selection_cases.json');assert not any(r['trial_id']==t['id'] for r in cases['reviews'])
cases['reviews'].append({k:review[k] for k in ('trial_id','source_url','reviewed_at','criteria','cases','selection_sha256')});write(ROOT/'data/protocol_selection_cases.json',cases)
write(P/'leah-source-derived-review.json',review)
write(P/'leah-canonical-change.json',{'at':at,'before':before,'after':t,'new_trials':0,'changed_records':1,'whole_site_roster':['Ohio State sponsor-listed','Missouri institution-confirmed enrolling','Minnesota institution-confirmed hold'],'no_form_or_message_submitted':True})
print(t['id'],review['selection_sha256'])
