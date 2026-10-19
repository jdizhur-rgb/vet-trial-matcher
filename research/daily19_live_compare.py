"""Compare actual browser-rendered results, not just JSON presence or totals."""
from daily19 import ROOT,RUN,read,write,now
import collections,json,subprocess
expected=read(RUN/'expected-live-searches.json');checks=[]
for c in expected['cases']:
 d=read(RUN/('live-'+c['country']+'.json'));want=collections.Counter((x['title'],x['center']) for x in c['records']);got=collections.Counter((x['title'],x['heading'].split(' · ',1)[1]) for x in d['records']);fields={x['name']:x['value'] for x in d['fields']}
 criteria=fields['species']=='Dog' and fields['country']==c['country'] and fields['cancer']=='Cancer — any type' and fields['diagnosis_status']=="I don't know" and all(fields[x]=='' for x in ['age','weight','zip_code','approach']) and len(d['preferences'])==6 and all(x['checked'] for x in d['preferences'])
 checks.append({'country':c['country'],'actual_browser_at':d['at'],'actual_count':len(d['records']),'expected_count':c['count'],'whole_rendered_roster_equal':want==got,'missing':list((want-got).elements()),'extra':list((got-want).elements()),'all_requested_controls_verified':criteria,'closed_vgs002_absent':not any(x['title']=='Fully canine anti-PD-1 immunotherapy for canine urothelial carcinoma' for x in d['records']),'status':'PASS' if want==got and criteria else 'FAIL','evidence_file':str((RUN/('live-'+c['country']+'.json')).relative_to(ROOT))})
write(RUN/'live-search-evidence.json',{'comparison_at':now(),'method':'Real production browser UI search plus DOM-rendered headings and card links; expected current catalog calculated independently in Work. No injected results or hidden application state.','production_code_commit':'99d76c53051bda21c88da3bd46dd46caff250a39','cases':checks,'overall':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'})
logs=read(RUN/'validators.json')
for c in [['python','scripts/validate_source_inventory.py'],['python','scripts/validate_audit_receipt.py',str(RUN.relative_to(ROOT)/'receipt-final.json')],['python','scripts/validate_audit_gap_review.py',str(RUN.relative_to(ROOT)/'gap-review.json'),'--receipt',str(RUN.relative_to(ROOT)/'receipt-final.json')],['python','scripts/check_evidence_keys.py']]:
 at=now();p=subprocess.run(c,cwd=ROOT,text=True,capture_output=True);logs.append({'command':c,'started_at':at,'finished_at':now(),'exit_code':p.returncode,'output':p.stdout+p.stderr,'scope':'Final receipt bookkeeping recheck; no source revisits.'})
write(RUN/'validators.json',logs);print(json.dumps(checks,ensure_ascii=False))
