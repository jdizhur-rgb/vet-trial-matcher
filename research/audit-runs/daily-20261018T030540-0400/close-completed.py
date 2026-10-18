"""Apply standing owner decision to two exact Completed AVMA protocol identities."""
import json,copy
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
registry=read(P/'avma-comparison.json'); cat=read(ROOT/'data/trials_base.json');by={r['id']:r for r in cat};changes=[]
for tid,rid,reason in [
 ('mizzou-vinorelbine-insulinoma',15959,'Whole current registry description explicitly names University of Missouri VHC, canine insulinoma, nonsurgical/postoperative persistent hypoglycemia, IV vinorelbine every two weeks, FreeStyle Libre and eight-week assessment. This is the existing canonical treatment identity, not inferred from listing absence.'),
 ('mizzou-epitheliotropic-laverdia',15930,'Exact naive canine cutaneous epitheliotropic lymphoma/verdinexor identity; AVMA investigator Shirley Chu is in the named primary research author group with canonical investigator Laura Yannai and University of Missouri (VCS2025 abstract indexed by publisher, saved status-identity-search-2.json). No separate phase/current invitation is published on today’s whole Missouri roster. Status itself comes from the fully retrieved current registry object, not the search snippet.')]:
  study=next(r for r in registry['current_roster'] if r['id']==rid)
  assert study.get('studypage_status')=='Completed' or 'Completed' in str(study)
  r=by[tid];before=copy.deepcopy(r)
  r.update(available_for_matching=False,status_confidence='confirmed_completed',status='Completed — AVMA registry; standing owner decision applied 2026-10-18',status_source=study['absolute_url'],status_decision_at=datetime.now(ZoneInfo('America/New_York')).isoformat(),status_decision_note=reason+' Owner explicitly instructed that AVMA Completed is completed. Historical eligibility and funding retained; no new intake inferred.',verified='2026-10-18')
  changes.append({'trial_id':tid,'registry_id':rid,'registry_record':study,'read_at':registry['read_at'],'evidence':registry['evidence'],'identity_reason':reason,'before':before,'after':copy.deepcopy(r),'disposition':'confirmed_completed_hidden_from_matching','individual_page_result':'Native timeout twice and same-URL Web inaccessible; no forbidden/alternate-route retry. Current full registry record is the status evidence.'})
write(ROOT/'data/trials_base.json',cat);write(P/'completed-status-decisions.json',changes)
print('Closed exact AVMA identities:',[x['trial_id'] for x in changes])
