"""Normalize repeated evidence to references; never discard source evidence."""
from daily20 import ROOT,RUN,read,write,now
import hashlib,json
rel=str(RUN.relative_to(ROOT));full=read(RUN/'full-comparisons.json')
def cref(c):
 return {k:c.get(k) for k in ['source_id','url','same_entire_text','same_entire_semantic_linkset']}|{'comparison_file':rel+'/full-comparisons.json','comparison_index':full.index(c) if c in full else None,'actual_attempt':{k:c.get('actual_attempt',{}).get(k) for k in ['attempted_at','method','evidence_file']},'prior_evidence':c.get('prior_evidence')}
def compact_r(r):
 r['current_comparison_evidence']=[cref(c) for c in r.get('current_comparison_evidence',[])]
 if 'completion_decision' in r:
  d=r['completion_decision']['available_reconciliation_done_evidence'];d['current_full_comparisons']=[cref(c) for c in d.get('current_full_comparisons',[]) if 'comparison_file' not in c]
 if r['source_id']=='registry-avma-veterinary-clinical-trials':r['current_roster']=[{k:x.get(k) for k in ['id','name','status','absolute_url','vct_code']} for x in r['current_roster']];r['whole_current_object_receipt']=rel+'/avma-comparison.json'
 if r['source_id']=='global-vettrials-directory':r['current_roster']=[{k:x.get(k) for k in ['id','title','sourceUrl','enrollmentStatus','species']} for x in r['current_roster']];r['whole_current_object_receipt']=rel+'/vettrials-comparison.json'
 return r
receipt=read(RUN/'receipt-final.json');receipt['sources']=[compact_r(r) for r in receipt['sources']];receipt['evidence_normalized_at']=now();write(RUN/'receipt-final.json',receipt);write(ROOT/'data/audit_source_coverage.json',receipt)
gap=read(RUN/'gap-review.json')
for r in gap['rows']:
 d=r['completion_decision']['available_reconciliation_done_evidence'];d['current_full_comparisons']=[cref(c) for c in d.get('current_full_comparisons',[]) if 'comparison_file' not in c]
write(RUN/'gap-review.json',gap)
trial=read(RUN/'trial-review.json')
for r in trial['trials']:r['current_whole_comparisons']=[cref(c) for c in r['current_whole_comparisons']]
write(RUN/'trial-review.json',trial)
deviation=read(RUN/'execution-deviations.json');deviation['items'] +=[{'issue':'Transient exec-server transport disconnect during receipt finalization','observed_until':'2026-10-20T03:50:52-04:00','assessment':'Finite pwd recovery succeeded; same invocation and run continued without source traversal replay. Temporary failure draft retained as superseded; automation pause reversed after recovery.'}];write(RUN/'execution-deviations.json',deviation)
print('NORMALIZED',[(p.name,p.stat().st_size) for p in [RUN/'receipt-final.json',RUN/'gap-review.json',RUN/'trial-review.json']])
