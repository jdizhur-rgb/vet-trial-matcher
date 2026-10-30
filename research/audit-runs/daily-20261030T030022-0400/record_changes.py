from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlsplit,unquote
import json,copy,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parents[2];O=R.parent/'daily-20261029T030505-0400'
def rd(p):return json.loads(p.read_text())
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
at=datetime.now(ZoneInfo('America/New_York')).isoformat();tid='jp-multicenter-oral-melanoma-anti-pd1-2026'
catalog=rd(R/'before-trials_base.json');trial=next(t for t in catalog if t['id']==tid);previous=copy.deepcopy(trial)
review={'trial_id':tid,'reviewed_at':at,'full_published_primary_read':True,'primary_evidence':['evidence/03e2438c9f826293b2.json','evidence/d990999446340c14f7.json'],'primary_urls':[trial['url'],'https://www.kamogawa-ac.jp/wp-content/uploads/2026/09/melanoma_2609.pdf'],'whole_published_multicenter_roster':trial['sites'],'species':'Dog','disease':'confirmed oral malignant melanoma','intervention':'investigational caninized anti-PD1 antibody, corporate registration trial','schedule':'six visits at two-week intervals','eligibility_scope':'Cytology/histopathology and site screening; stage, general health and concomitant medications are assessed by study team. No invented quantitative thresholds.','owner_costs':'Individually explained by site; no amount or guaranteed coverage published.','clinical_selection_changed':False,'funding_verified_previous':trial['funding_verified'],'funding_verified_new':trial['funding_verified'],'verified_previous':trial['verified'],'verified_new':'2026-10-30','limit':'Full public invitation and five-page participating-centre release reviewed; unpublished investigator protocol details remain site screening. Not an efficacy/safety endorsement.'}
wr(R/'kamogawa-pd1-full-published-review.json',review)
trial['verified']='2026-10-30';wr(ROOT/'data/trials_base.json',catalog)
cases=rd(ROOT/'data/protocol_selection_cases.json');cr=next(r for r in cases['reviews']if r['trial_id']==tid)
cr['reviewed_at']=at;cr['full_protocol_reverified']=True;cr['evidence_receipt']=str(R.relative_to(ROOT)/'kamogawa-pd1-full-published-review.json')
wr(ROOT/'data/protocol_selection_cases.json',cases)
access=rd(ROOT/'data/source_access_restrictions.json')
for d in map(json.loads,(R/'new-denials.jsonl').read_text().splitlines()):
 if not any(x['url']==d['url']for x in access['routes']):access['routes'].append(dict(d,reason='Fresh same-URL Web403 after ordinary native failure; do not retry or bypass.'))
access['updated']='2026-10-30';wr(ROOT/'data/source_access_restrictions.json',access)
html=ROOT/'seo/static/matcher/index.html';html.write_text(html.read_text().replace('clinical-audit-20261029','clinical-audit-20261030'))
queue=rd(O/'trial-review-queue.json');queue.update(run_id=R.name,reviewed_at=at,full_today=1)
restrictions=rd(R/'restrictions-frozen.json');denied={(urlsplit(x['url']).hostname,unquote(urlsplit(x['url']).path).rstrip('/'))for x in restrictions}
for r in queue['rows']:
 r['new_full_review']=r['trial_id']==tid
 if r['trial_id']==tid:r.update(status='FULL_PUBLISHED_PRIMARY_REVIEW',new_verified='2026-10-30',meaning='Fresh whole invitation, full PDF and complete3site roster read; clinical criteria unchanged, costs individually unpublished.')
 elif r['trial_id']in queue['old_pending_remaining']:
  k=(urlsplit(r['url']).hostname,unquote(urlsplit(r['url']).path).rstrip('/'))
  r['meaning']='Exact individual primary route retains an access/action gate; no retry, bypass or new primary date.'if k in denied else 'Current primary/intake question remains; see specific due-question decisions. No new full signoff or renewed verified date.'
  r['new_full_review']=False
wr(R/'trial-review-queue.json',queue)
wr(R/'protocol-questions-and-decisions.json',{'reviewed_at':at,'inherited_pending_protocol_count':31,'pending_trial_ids':queue['old_pending_remaining'],'new_active_trials':0,'full_published_primary_rereviews':1,'canonical_clinical_fields_changed':0,'prior_independent_cases_pending':13,'source_specific_questions':[
 {'trial_id':'jp-hokkaido-canine-oral-melanoma-anti-pdl1','remaining_fact':'Current invitation includes other canine malignancies as well as oral melanoma with lung metastases. Other cohorts and exclusion of localized disease not defined; costs unpublished. Preserve narrow scope and no new M0-negative clinical signoff.','source_evidence':'evidence/e25bb59dcd120f63a7.json'},
 {'trial_id':'uk-edinburgh-oral-melanoma-tigilanol-tiglate','remaining_fact':'Full official7Oct2024 news reread; eight-dog pilot/referral invitation, but present cohort intake, full criteria and actual owner cost allocation unconfirmed. Programme funding is not promised free care.','source_evidence':'evidence/3bd5ce6dcdda3bcdd7.json'},
 {'trial_id':'mizzou-osa-carboplatin-timing','remaining_fact':'No carboplatin/timing/osteosarcoma entry in current whole official oncology roster. Two actual search engines found general chemotherapy information only. Current intake and individual protocol remain unknown; disappearance alone is not closure.','source_evidence':['reviews.json','discovery-8.json','discovery-9.json']},
 {'trial_id':'mexico-ensenada-silver-nanoparticle-cancer-2026','remaining_fact':'Fresh whole secondary programme story repeats collaborator invitation, owner-paid screening and covered consult/radiograph/followup. Official search finds anticancer patent and scientific profile, not a current individual veterinary recruitment protocol. No verified date refreshed from news.','source_evidence':['evidence/085608cf4b27e9931e.json','discovery-8.json','discovery-9.json']},
 {'lead':'UFPel u10335/u7937','remaining_fact':'Present enrollment, study-specific owner referral/site allocation and cost terms unpublished; two therapeutic projects remain WATCH/nonmatchable. Eyelid group text also conflicts30/n35.','source_evidence':['evidence/4685e62502d930955d.json','evidence/828a781eeaf7b38fb6.json','evidence/b6bd5e22b046039bb2.json']},
 {'lead':'OVC oral tumour PDT','decision':'Current official canine index ON HOLD governs despite readable undated invitation and changed secondaryID; no activation.','source_evidence':['evidence/7f9a4d0d25144f52e7.json','evidence/1d5a6ab8ea92a83766.json']}
 ],'next_action':'Daily permitted source checks continue. Exact denied routes not retried; deeper questions only with new primary/master signal or due seven-day recheck. No outreach performed.'})
wr(R/'catalog-change-receipt.json',{'reviewed_at':at,'canonical_before_sha256':hashlib.sha256((R/'before-trials_base.json').read_bytes()).hexdigest(),'canonical_after_sha256':hashlib.sha256((ROOT/'data/trials_base.json').read_bytes()).hexdigest(),'changed_trials':[{'id':tid,'fields':['verified'],'before':previous['verified'],'after':trial['verified']}],'canonical_count_before':len(catalog),'canonical_count_after':len(catalog),'new_active_trials':0,'closed_or_hidden':0,'selection_baseline_changed':False,'editorial_or_UI_changed':False,'technical_change':'Existing JS cache query version refreshed to clinical-audit-20261030; script behavior unchanged.'})
print('Recorded one actual published-protocol review/date refresh; no clinical criteria, funding date or matching state changed.')
