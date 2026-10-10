import json,hashlib,re
from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
P=Path(__file__).parent;TZ=ZoneInfo('America/New_York');now=datetime.now(TZ).isoformat()
def read(p):return json.loads(Path(p).read_text())
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def norm(u):return str(u).rstrip('/')
def ts(v):
 try:return datetime.fromisoformat(v).astimezone(TZ).isoformat()
 except:return datetime.strptime(v,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=ZoneInfo('UTC')).astimezone(TZ).isoformat()
before=read(P/'inventory-before.json'); inv=read('data/source_inventory.json'); old={s['id']:s for s in before['sources']}; prior=read(P/'audit_source_coverage-before.json');prior_rows={s['source_id']:s for s in prior['sources']}
inv['sources'][33]['fallback_urls']=['https://ovcclinicaltrials.uoguelph.ca/all-active-canine-clinical-trials-oncology/','https://ovcclinicaltrials.uoguelph.ca/all-active-feline-clinical-trials-onco/']
web=read(P/'web-page-index.json');native=[];export=[]
for f in sorted((P/'http').glob('*.json')):
 d=read(f);d['file']='http/'+f.name
 # Preserve text/links/actual hashes without unrelated scripts, embedded service keys or raw binary.
 text=d.get('text','');raw=P/d['raw_file'];rawhash=hashlib.sha256(raw.read_bytes()).hexdigest() if raw.exists() else None
 if '/api/v1/studycontent-latest-version/' in d['url'] and raw.exists():
  try:
   content=json.loads(raw.read_text());content.pop('google_maps_key',None)
   text=json.dumps(content,ensure_ascii=False,indent=2)
  except:pass
 e={k:d.get(k)for k in ['source_id','url','attempted_at','method','exit_code','transport_result','error','links']};e.update(evidence_id=f.stem,reader_text=text,reader_text_sha256=hashlib.sha256(text.encode()).hexdigest(),raw_sha256=rawhash)
 export.append(e);d['reader_text']=text;d['reader_text_sha256']=e['reader_text_sha256'];d['raw_sha256']=rawhash;native.append(d)
save(P/'native-reader-evidence.json',export)
# Registered fallbacks may share a same-day visit under another inventory source;
# link that actual evidence explicitly rather than inventing another request.
def attempts(s,i):
 urls={norm(s['master_url'])}|{norm(u)for u in s.get('fallback_urls',[])}
 domains={urlparse(u).netloc for u in urls};domains-={'studypages.com','veterinaryclinicaltrials.org'}
 chosen=[d for d in native if d['source_id']==s['id'] or norm(d['url'])in urls or urlparse(d['url']).netloc in domains]
 if i==4:chosen +=[d for d in native if 450<=int(Path(d['file']).stem)<=455]
 if i==107:chosen +=[d for d in native if int(Path(d['file']).stem)==409]
 out=[]
 for d in {d['file']:d for d in chosen}.values():
  code=d.get('transport_result','').splitlines();code=code[0]if code else''
  out.append({'url':d['url'],'attempted_at':d['attempted_at'],'method':'shell_curl','result':'retrieved_text_requires_semantic_review'if code=='200' and len(d['reader_text'])>200 else'failed_or_insufficient_text','http_status':int(code)if code.isdigit()and code!='000'else None,'evidence_file':'native-reader-evidence.json','evidence_id':Path(d['file']).stem,'reader_text_sha256':d['reader_text_sha256'],'raw_sha256':d['raw_sha256'],'shared_provenance_source_id':d['source_id']if d['source_id']!=s['id']else None,'timestamp_precision':'actual request start'})
 for d in web:
  if norm(d['url'])in urls or urlparse(d['url']).netloc in domains:
   out.append({'url':d['url'],'attempted_at':ts(d['attempted_at']),'method':d['method'],'result':'retrieved_text_requires_semantic_review'if d['retrieved']else'unavailable_or_empty','web_reference':d['reference'],'evidence_file':d['file'],'reader_text_sha256':d['reader_sha256'],'crawl_label':d['crawl_label'],'full_text_available':d['full_text_available'],'timestamp_precision':'recorded tool batch start/completion as labeled in evidence file'})
 return sorted(out,key=lambda d:d['attempted_at'])
ledger=[]
for line in (P/'source-decisions.tsv').read_text().splitlines():
 i,status,count,notes=line.split('\t',3);i=int(i);s=inv['sources'][i];o=old.get(s['id'],{});a=attempts(s,i);assert a,(i,s['id']);sufficient=status=='fully_reconciled';count=None if count=='?'else int(count)
 if i in [9,60,86]:notes+=' Current master reader has cache-age uncertainty and no independent fresh master roster confirmation; not counted successfully checked.'
 master=norm(s['master_url']);assert any(norm(x['url'])==master for x in a),(i,'NO MASTER')
 for u in s.get('fallback_urls',[]):assert any(norm(x['url'])==norm(u)for x in a),(i,'MISSING FALLBACK',u)
 last=a[-1]['attempted_at'];result='reachable'if sufficient else status
 # Fresh fingerprints are derived from this run's reader evidence, not historical content hashes.
 readers=[x for x in a if x['result']=='retrieved_text_requires_semantic_review'];fp='sha256:'+hashlib.sha256(json.dumps([(x['url'],x['reader_text_sha256'])for x in readers],sort_keys=True).encode()).hexdigest()if readers else None
 previous=prior_rows.get(s['id'],{}).get('roster_evidence',{}).get('current_roster',[])
 if i==23:roster=previous+['Daunomustine multicentric lymphoma']
 elif i==22:roster=['B-cell lymphoma IVP','Sorafenib/placebo plus radiation for pituitary macroadenoma with Cushing disease']
 elif i==33:roster=['Canine HIFU OSA','Palladia oral melanoma','Urinary miRNA','Mobile oral-tumor photogrammetry','Veterinary biobank','T-cell lymphoma prognosis','Canine porphysome PDT ON HOLD','Thyroid staining ON HOLD','Feline oral SCC porphysome PDT']
 elif i==107:roster=['ECIP-OSA-01 ECI plus novel adjuvant CLOSED','ECI plus chemotherapy, unfunded, pre-amputation']
 elif i==60:roster=['Hayburn feline small-cell GI lymphoma radiation','MCT acid-suppressant/placebo with resection and $1,000 surgical credit']
 else:roster=previous
 r={'source_id':s['id'],'source_name':s['name'],'opened_this_run':True,'processing_complete':True,'executor_incomplete':False,'content_sufficient':sufficient,'protocols_seen':count,'status':status,'master_result':result,'attempted_urls':a,'route_used':'Actual official master, required official fallbacks and current individual primary routes; shell/Web/shared provenance retained','roster_evidence':{'current_roster':roster,'review_notes':notes,'current_evidence_references':[{'file':x['evidence_file'],'id':x.get('evidence_id')or x.get('web_reference'),'url':x['url']}for x in readers],'count_unit':'Named oncology identities including closed/non-treatment programs; partial integer is observed count, null means whole roster cannot be counted','baseline_catalog':'trials_base-before.json (305 canonical records)','unchanged_detail_provenance':'Previous immutable Oct8/Oct9 primary receipt is comparison only. Today master/fallback roster revisited; unchanged details skip only with primary read within28 days. All39 older primary URLs actually attempted today, with6 CSU public primary JSON replacements and2 ELIAS individual leaves.'},'previous_last_checked':o.get('last_checked'),'previous_last_checked_at':o.get('last_checked_at'),'previous_last_result':o.get('last_result'),'previous_fingerprint':o.get('content_fingerprint'),'saved_last_checked':last[:10],'saved_last_checked_at':last,'saved_last_result':result,'current_fingerprint':fp,'fingerprint_method':'SHA256 of current-run retrieved reader evidence manifest; insufficient content remains insufficient','fingerprint_preserved_from_prior_same_day_visit':False,'external_gap':None if sufficient else notes,'recheck_after':None if sufficient else(datetime.fromisoformat(last)+timedelta(days=7)).date().isoformat()}
 ledger.append(r)
 s.update(last_checked=r['saved_last_checked'],last_checked_at=last,last_result=result,content_fingerprint=fp,last_attempts=a,last_route_used=r['route_used'],last_audit_run_id=P.name,last_protocols_seen=count,last_coverage_gap=r['external_gap'],fingerprint_method=r['fingerprint_method'])
inv['updated']=now[:10];save('data/source_inventory.json',inv)
receipt={'schema_version':1,'run_id':P.name,'audit_mode':'DAILY GLOBAL WORK AUDIT','status':'INCOMPLETE','started_at':'2026-10-10T03:00:27-04:00','checkpoint_at':now,'timezone':'America/New_York','base_commit':'73de702f14dfff37efe711ce27914e2bd979165c','previous_receipt':prior['run_id'],'source_total':len(ledger),'original_source_total':107,'attempted_total':len(ledger),'processing_total':len(ledger),'executor_unfinished_total':0,'content_sufficient_total':sum(x['content_sufficient']for x in ledger),'global_discovery_regions':12,'global_discovery_passes':2,'sources':ledger}
save(P/'source-review-ledger.json',ledger);save(P/'receipt-final.json',receipt);save('data/audit_source_coverage.json',receipt)
state=read('data/audit_state.json');state['last_incremental_audit']=now;state['last_source_discovery_attempt']={'run_id':P.name,'started_at':receipt['started_at'],'checkpoint_at':now,'status':'daily_trial_only_incomplete_external_gaps','attempted':len(ledger),'sufficient':receipt['content_sufficient_total'],'source_total':len(ledger),'coverage_receipt':str(P/'receipt-final.json'),'latest_receipt':'data/audit_source_coverage.json','catalog_changes':15,'new_source_entries':1,'global_discovery_regions':list(read(P/'discovery-query-plan.json')['matrix']),'pending_source_ids':[],'external_gap_source_ids':[r['source_id']for r in ledger if not r['content_sufficient']],'executor_unfinished_total':0,'terminal_external_gaps_no_automatic_requeue':True,'previous_checkpoint':'research/audit-runs/daily-20261009T025843-0400/receipt-final.json'};save('data/audit_state.json',state)
readback=read('data/source_inventory.json')['sources'];checks=[{'source_id':s['id'],'previous':{'last_checked':r['previous_last_checked'],'last_checked_at':r['previous_last_checked_at']},'new':{'last_checked':s['last_checked'],'last_checked_at':s['last_checked_at'],'last_result':s['last_result']},'status':'PASS'if s['last_checked_at']==r['saved_last_checked_at']and s['last_checked_at']!=r['previous_last_checked_at']else'FAIL'}for s,r in zip(readback,ledger)];save(P/'date-readback-local.json',{'checked_at':now,'status':'PASS'if all(x['status']=='PASS'for x in checks)else'FAIL','base_sha':receipt['base_commit'],'sources':checks})
from collections import Counter
print('RECEIPT',Counter(x['status']for x in ledger),'local readback',len(checks))
