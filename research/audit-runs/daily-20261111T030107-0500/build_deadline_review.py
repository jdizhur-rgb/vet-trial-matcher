import json,hashlib
from pathlib import Path
from datetime import datetime,date
from zoneinfo import ZoneInfo
run='daily-20261111T030107-0500'; now=datetime.now(ZoneInfo('America/New_York')); today=now.date()
arr=json.load(open('data/trials_base.json')); rows=[]; counts={}
prior=json.load(open('research/audit-runs/daily-20261110T030237-0500/deadline-review.json')); prior_by={r['record_id']:r for r in prior['rows']}
for x in arr:
 c=[]
 for f in ('recruitment_end','enrollment_end','recruitment_deadline'):
  v=x.get(f)
  if isinstance(v,str) and len(v)>=10:
   try: d=date.fromisoformat(v[:10]); c.append({'field':f,'date':d.isoformat(),'basis':'canonical structured date','source':x.get(f+'_source') or x.get('recruitment_end_source'),'original_evidence_at':(x.get('recruitment_end_basis') or {}).get('original_read_at')})
   except: pass
 if not c and prior_by.get(x['id'],{}).get('deadline_candidates'):
  c=[]
  for y in prior_by[x['id']]['deadline_candidates']:
   z=dict(y); z['basis']=z.get('basis','previous primary evidence retained'); z['original_evidence_at']=z.get('original_evidence_at') or 'preserved in 2026-11-10 deadline ledger'; c.append(z)
 if not c: result='NO_PUBLISHED_RECRUITMENT_CUTOFF_FOUND_IN_CANONICAL'; ext='not triggered'
 else:
  earliest=min(date.fromisoformat(y['date']) for y in c)
  if earliest>=today: result='FUTURE_OR_TODAY'; ext='not triggered'
  elif x.get('available_for_matching'): result='CROSSED_ACTIVE_REQUIRES_EXTENSION_CHECK'; ext='required'
  else: result='CROSSED_NONMATCHABLE'; ext='not triggered: already nonmatchable'
 counts[result]=counts.get(result,0)+1
 rows.append({'record_id':x['id'],'available_for_matching':bool(x.get('available_for_matching')),'status':x.get('status'),'verified':x.get('verified'),'deadline_candidates':c,'result':result,'extension_check':ext})
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
out={'run_id':run,'evaluated_at':now.isoformat(),'local_date':today.isoformat(),'baseline_input_hashes':{'trials_base.json':sha('data/trials_base.json'),'source_inventory.json':sha('data/source_inventory.json')},'scope':'Daily clock comparison of all canonical recruitment dates. Original evidence dates are preserved; unchanged pages do not suppress deadline evaluation. Per owner policy, a published study end on a currently recruiting protocol is treated as recruitment end unless newer primary evidence supersedes it.','counts':counts,'records':rows,'rows':rows,'active_passed_structured_cutoffs':[r['record_id'] for r in rows if r['result']=='CROSSED_ACTIVE_REQUIRES_EXTENSION_CHECK'],'new_or_changed_today':['csu-feline-scgl-radiotherapy-iacuc8528']}
Path(f'research/audit-runs/{run}/deadline-review.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(counts,indent=2)); print('active crossed',out['active_passed_structured_cutoffs'])
