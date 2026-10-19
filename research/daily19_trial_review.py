"""Separate fresh page comparison, retained criteria and uncompleted full review."""
from daily19 import ROOT,RUN,read,write,now,m
import json,collections,copy
from seo.catalog_selection import current_public
before=read(RUN/'before-trials_base.json');after=read(ROOT/'data/trials_base.json');b={r['id']:r for r in before};c={r['id']:r for r in after}
public=read(RUN/'public-frozen.json');current={r['id'] for r in current_public(after)};old={r['trial_id']:r for r in read(RUN/'prior-trial-review.json')['trials']}
native=read(RUN/'accepted-master-attempts.json')+[json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()];web=read(RUN/'accepted-Web-attempts.json')
comp=read(RUN/'accepted-master-comparisons.json')+read(RUN/'individual-full-comparisons.json');islands=read(RUN/'public-protocol-islands.json');restricted={m.route_key(r['url']):r for r in read(RUN/'restrictions-frozen.json')}
rows=[]
for record in public:
 tid=record['id'];prior=old.get(tid,{});u=record.get('source_url') or record['url'];k=m.route_key(u)
 attempts=[a for a in native+web if m.route_key(a['url'])==k]
 comparisons=[x for x in comp if m.route_key(x['url'])==k];island=next((x for x in islands if x['trial_id']==tid),None)
 equal=any(x.get('same_full_text') and x.get('same_full_links') or x.get('same_entire_text') and x.get('same_entire_semantic_linkset') for x in comparisons)
 outcome='BLOCKED' if k in restricted and not attempts else 'PARTIAL'
 if equal and prior.get('outcome') in ['VERIFIED_CURRENT','VERIFIED_UNCHANGED']:outcome='VERIFIED_UNCHANGED'
 if tid not in current:outcome='CLOSED_CONFIRMED'
 decision='Current permitted whole content compared where available; original independent clinical-review scope and timestamps retained. No full fresh clinical review inferred from equal source content, JSON presence or a registry record.'
 if island:decision+=' Complete published StudyPages protocol object independently extracted and compared; no object changes. Empty published site rosters remain unknown, not full multicenter verification.'
 if outcome=='BLOCKED':decision='Exact previously denied primary route not retried. Permitted independent institutional/sponsor signals remain separately attributed; clinical criteria not newly verified.'
 if tid not in current:decision='Exact AVMA VCT23005729 Completed and whole sponsor VGS-002 Ethos/BARC Closed. Fresh VSH page still OPEN with three historical sites; conflict retained. Conservative matching disabled, not a fresh full clinical-criteria review.'
 rows.append({'trial_id':tid,'title':record['title'],'public_at_start':True,'public_at_end':tid in current,'outcome':outcome,'decision':decision,'primary_url':u,'actual_current_primary_attempts':attempts,'current_whole_comparisons':comparisons,'public_island_comparison':island,'inherited_route_gate':restricted.get(k),'previous_verified':b[tid].get('verified'),'new_verified':c[tid].get('verified'),'retained_independent_review':prior.get('retained_independent_review'),'previous_protocol_question':prior.get('decision'),'full_fresh_clinical_review_today':False,'not_a_new_visit':not bool(attempts),'clinical_or_funding_dates_unchanged':b[tid].get('verified')==c[tid].get('verified') and b[tid].get('funding_verified')==c[tid].get('funding_verified')})
pending=read(RUN/'pending-frozen.json');remaining=[tid for tid in pending['remaining_ids'] if tid in current]
progress={**pending,'remaining':len(remaining),'remaining_ids':remaining,'confirmed_completed_removed':pending['confirmed_completed_removed']+1,'today_full_fresh_reviews':0,'today_confirmed_completions':['penn-anti-pd1-urothelial-carcinoma'],'not_fresh_reviews_from_unchanged_pages':True}
write(RUN/'independent40-progress.json',progress)
write(RUN/'trial-review.json',{'summary':{'run_id':RUN.name,'reviewed_at':now(),'frozen_public_total':len(public),'end_public_total':len(current),'all_frozen_ids_preserved':all(tid in c for tid in b),'per_trial_outcomes':dict(collections.Counter(r['outcome'] for r in rows)),'prior40':progress,'fresh_individual_full_clinical_reviews_today':0,'source_coverage_is_not_clinical_completion':True,'clinical_full_fresh_gate':'INCOMPLETE'},'trials':rows})
vsh=next(a for a in native if a.get('source_id')=='discovery:vgs002-vsh');write(RUN/'vgs002-site-conflict.json',{'at':now(),'exact_primary_attempt':vsh,'published_status':'OPEN','whole_published_roster':['CASE Boulder CO','Metropolitan Cleveland East Highland Heights OH','VSH North County San Marcos CA'],'canonical_historical_roster':['CASE Boulder CO','VSH North County San Marcos CA'],'disposition':'Entire Ethos and BARC sponsor programme is closed and exact AVMA record Completed. Do not activate the newly observed third historical site. Preserve current site-page conflict and prior canonical sites rather than turn a closed cohort into active access.','closure_evidence':['vgs002-closure.json','vgs002-completed-amendment.json'],'full_clinical_review_complete':False})
print('frozen',len(public),'current',len(current),'prior40remaining',len(remaining),collections.Counter(r['outcome'] for r in rows))
