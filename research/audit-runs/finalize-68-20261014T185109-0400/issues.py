"""Manual protocol/field triage; aliases share issues instead of duplicate queues."""
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
receipt=json.loads((RUN/'receipt-final.json').read_text());rows={r['source_id']:r for r in receipt['sources']};numbers={i+1:r for i,r in enumerate(receipt['sources'])}
catalog={r['id']:r for r in json.loads((ROOT/'data/trials_base.json').read_text())}
now=datetime.now(ZoneInfo('America/New_York')).isoformat();issues=[]
def add(key,source_numbers,ids,field,impact,question,decision,remaining=None,kind='protocol',proposal=None):
    sources=[numbers[n] for n in source_numbers]
    attempts=[a for s in sources for a in s['attempted_urls']+s.get('new_finalizer_attempts',[])]
    stamps=[a['attempted_at'] for a in attempts if a.get('attempted_at')]
    states=[{'record_id':i,'available_for_matching':catalog[i].get('available_for_matching'),'status_confidence':catalog[i].get('status_confidence'),'verified':catalog[i].get('verified')} for i in ids]
    issues.append({'issue_id':key,'impact':impact,'kind':kind,'source_ids':[s['source_id'] for s in sources],'record_ids':ids,'field':field,'affected_site': 'see question',
        'public_before':states,'public_after':states,'question':question,'remaining_fact':remaining or question,'decision':decision,
        'evidence':[{'source_id':s['source_id'],'completion_review':s['manual_completion_review_id'],'attempt_urls':list(dict.fromkeys(a['url'] for a in s['attempted_urls'])),'reconciliation':s['reconciliation']} for s in sources],
        'previous_primary_verified':{i:catalog[i].get('verified') for i in ids},'first_seen':None,
        'last_attempted_at':max(stamps,key=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))) if stamps else None,
        'reviewed_at':now,'processing_assessment':'completed_review' if decision=='resolved_verified' else 'external_blocker',
        'next_action':'Block 3: concrete owner status decision; no status change in block 2.' if proposal else ('No repeated deep search before new primary signal or 2026-10-21; daily visits continue.' if decision!='resolved_verified' else 'No reopening without a new conflicting primary signal.'),
        'recheck_after':None if decision=='resolved_verified' else '2026-10-21','proposed_not_applied':proposal})

eu=[
('fr-fregis-hepatic-tumor-thermoablation',[17,18],'Fregis: current protocol-level owner intake for hepatic thermoablation; Dissectron liver surgery is a distinct intervention.'),
('fr-fregis-chemodectoma-thermoablation',[17,18],'Fregis: current chemodectoma thermoablation study intake and actual protocol/contact; generic health information is not a trial invitation.'),
('fr-fregis-hepatic-embolization',[17,18],'Fregis: current hepatic embolization cohort, treating site and direct investigator enrollment route.'),
('eu-ch-sinonasal-heterogeneous-rt',[17,18,20],'Zurich: whether the old heterogeneous-dose sinonasal radiation cohort is presently accepting patients. Absence from two current lists does not prove closure.'),
('uk-rvc-insulinoma-toceranib',[17,18,22],'RVC-led toceranib insulinoma: current entry at one of the seven published centres despite elapsed project metadata; whole current site invitation remains unconfirmed.'),
('nl-utrecht-osteosarcoma-oncolytic-virus-access',[17,18,19],'Utrecht: present long-term oncolytic-virus access after enrollment completion, not a new recruiting trial; January statement and blocked master do not independently reconfirm current owner entry.')]
for rid,ns,q in eu:add('access-'+rid,ns,[rid],'current_owner_access','P0',q,'decision_required',proposal={'available_for_matching':False,'status_confidence':'unconfirmed','not_confirmed_closed':True})

add('leah-ohio-current-site',[5,59],['leah-bcell-cart-2026'],'Ohio institutional corroboration','P1','Sponsor lists Ohio as enrolling; Missouri and Minnesota are explicitly on hold. Obtain Ohio-specific corroboration and site criteria without closing the sponsor-verified route.','retained_with_field_gap')
add('mimic-owner-cost-alias',[14],['ethos-mimic-osa-lung'],'owner_cost','P1','Two current aliases disagree on full coverage versus subsidized low-cost care. Keep current narrower -2 OSA scope and conservative costs.','retained_with_field_gap')
for rid in ['china-dongjun-mct-new-drug-2026','china-dongjun-osa-new-drug-2026','china-dongjun-oral-scc-new-drug-2026']:
    for field,q in [('investigational_agent','Drug identity is not publicly disclosed; study-specific owner/vet invitation and free-drug screening route are present.'),('administering_site','The organizer does not name the administering hospital; intake assigns it after screening.'),('owner_cost','Free drug and lab/tumour monitoring do not establish payment for other veterinary care or travel.')]:
        add(rid+'-'+field,[38],[rid],field,'P1',q,'retained_with_field_gap')
add('gamgee-cost',[28],['au-gamgee-personalized-mrna-vaccine'],'owner_cost','P1','Exact sample, sequencing, vaccine, veterinary and travel costs are not published; do not infer fully funded care from active registration.','retained_with_field_gap')
add('gamgee-administering-vet',[28],['au-gamgee-personalized-mrna-vaccine'],'administering_site','P1','Treating clinic is assigned through prescreening; current study-specific Australian MCT pathway is present.','retained_with_field_gap')
add('medipaws-additional-sites',[32],['au-melbourne-hsa-autologous-vaccine-multicenter'],'additional_sites','P1','Sydney intake is verified. Which additional hospitals, if any, treat patients? Melbourne coordination is not a verified second site.','retained_with_field_gap')
add('kamogawa-cost',[41],['jp-multicenter-oral-melanoma-anti-pd1-2026'],'owner_cost','P1','All three sites are published; exact costs are explained individually and cannot be inferred.','retained_with_field_gap')
add('kamogawa-stage-medication',[41],['jp-multicenter-oral-melanoma-anti-pd1-2026'],'site_prescreening_eligibility','P1','Stage/current-medication rules remain individual prescreening questions; current oral-melanoma enrollment invitation is confirmed.','retained_with_field_gap')
add('penn-hs-consent-capacity',[26],['penn-atherton-steap1-car-t-hs'],'consent_capacity','P1','Revised HS consent and present slots require study prescreening under existing direct investigator evidence; no fresh email confirmation is claimed.','retained_with_field_gap')
add('penn-bcell-individual-screening',[26],['penn-bcell-car-t-registry'],'individual_eligibility','P1','Current funded stage II–V B-cell flyer is established; individualized eligibility remains with the Penn study team.','retained_with_field_gap')
add('metropolitan-push-list-sync',[67],['ethos-epush-hsa'],'sponsor_site_list_sync','P1','Direct Akron hospital enrollment invitation is verified; sponsor twelve-site list omits Metropolitan. Preserve the hospital-verified site, flag list synchronization.','retained_with_field_gap')
add('tufts-hcc-already-decided',[7],['tufts-z007-broad-solid-2026'],'HCC prescreening','P1','Owner already authorized HCC discoverability with explicit liver-disease/biopsy prescreening on October12. This is not a new undecided access conflict.','resolved_verified')
add('tufts-bg34-primary-reread',[7],['tufts-bg34-melanoma'],'denied_individual_route','P2','Primary suspension is inherited and record remains inactive. Individual denied route cannot be reread; do not reinterpret this as unverified access for the other Tufts trials.','watch_nonmatchable')

# All remaining insufficient sources get their exact source/candidate question.
# Three resource directories and the two LEAH rows intentionally share issues.
handled={5,7,14,17,18,19,20,22,38,59}
directory_group=[2,52,56]
add('shared-resource-directory-scope',directory_group,[],'source_completeness','P3','VCS/Perseus/Dog Cancer Foundation are non-exhaustive resource lists. Their real provider links were compared; Guardian404 and Hope hospital redirect supply no current trial. A comprehensive current trial roster is not published.','retained_with_field_gap',kind='source_only')
handled.update(directory_group)
for n,r in numbers.items():
    if r['content_sufficient'] or n in handled or n==35:continue
    ids=[] if n==1 else r['record_ids']
    impact=r['impact']
    for individual_ids in ([[i] for i in ids] if len(ids)>1 else [ids]):
        key='source-question-'+r['source_id']+('-'+individual_ids[0] if len(ids)>1 else '')
        question=(catalog[individual_ids[0]].get('title','')+': ' if len(ids)>1 else '')+r['completion_decision']['remaining_fact']
        add(key,[n],individual_ids,'current_protocol_or_source_fact',impact,question,'watch_nonmatchable' if impact=='P2' else 'retained_with_field_gap',kind='source_only' if not individual_ids and impact=='P3' else 'protocol_or_watch_lead')

for cohort in ['OSA post-amputation pilot','palliative solid-tumour IV/oral pilot','alleged NCSU bladder cohort']:
    add('immunocidin-'+cohort.split()[0].lower(),[35],[],'current_named_protocol','P2',cohort+': obtain a current named investigator protocol/site/eligibility and owner costs. CCA narrative is not a canonical record; manufacturer research describes historical studies and current product availability. Known NCSU bladder primary is IL12, not MCWF.','watch_nonmatchable',kind='candidate_not_in_catalog')
add('immunocidin-commercial-access-separate',[35],[],'commercial_treatment_access','P2','Current manufacturer product page supports veterinary ordering for canine mammary tumours. Assess separately for advanced-treatment editorial listing, not as a recruiting trial or a claimed trial addition.','watch_nonmatchable',kind='separate_treatment_access_review')
add('fregis-dissectron-new-lead',[17,18],[],'current_named_protocol','P2','Dissectron ultrasound-assisted HCC/liver surgery invitation is a different intervention from the three old Fregis records. Cached primary is three days old and same-URL native read failed; full current protocol/current access is not established.','watch_nonmatchable',kind='candidate_not_in_catalog')
add('paccal-completed-cohorts',[10,48],['bluepearl-hsa-paccal'],'recruitment_status','P2','Direct sponsor completion controls over stale owner/hospital labels. Dog HSA and cat solid-tumour recruitment are complete; no new cohort is confirmed.','resolved_verified')
add('ardent-recruitment-complete',[50],[],'recruitment_status','P2','Unleash explicitly states recruitment complete for the same K9-ACV/CD200AR-L OSA protocol. Older ongoing label does not require an open site/cost enrollment investigation.','resolved_verified')

assert len({r['issue_id'] for r in issues})==len(issues)
for r in issues:
    assert all(i in catalog for i in r['record_ids'])
    # Never invent an age for a legacy issue from inventory-addition dates.
    assert r['first_seen'] is None
(RUN/'issues.json').write_text(json.dumps({'run_id':RUN.name,'reviewed_at':now,'issues':issues},ensure_ascii=False,indent=2)+'\n')

# Resolve two old, precise questions using actual new primary comparison, while
# preserving their previous wording and provenance. No canonical trial is closed.
u=json.loads((ROOT/'data/audit_unresolved.json').read_text())
updates={'bluepearl-paccal-status-conflict-20260930':'paccal-completed-cohorts','ardent-k9-acv-cd200-osa-roster-20261005':'ardent-recruitment-complete'}
for r in u['items']:
    if r['id'] in updates:
        before=json.loads(json.dumps(r));r['previous_open_question']=before;r['status']='resolved';r['resolved_at']=now;r['resolution_issue_id']=updates[r['id']];r['resolution_evidence']=str((RUN/'issues.json').relative_to(ROOT));r['recheck_after']=None
        r['reason']='Resolved from the exact current primary protocol/sponsor comparison. Recruitment is complete; the pre-existing inactive catalog disposition is retained. Stale ongoing owner-page wording alone does not reopen it. See the preserved previous question and linked issue evidence.'
(ROOT/'data/audit_unresolved.json').write_text(json.dumps(u,ensure_ascii=False,indent=2)+'\n')

from collections import Counter
print(json.dumps({'issues':len(issues),'decisions':dict(Counter(r['decision'] for r in issues)),'impacts':dict(Counter(r['impact'] for r in issues)),'material_active_core_records':sorted({i for r in issues if r['impact']=='P0' for i in r['record_ids']}),'old_questions_resolved':len(updates)},indent=2))
