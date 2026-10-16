"""Compare actual complete current public records, not old fingerprints."""
import json,hashlib,re
from pathlib import Path
P=Path(__file__).parent;ROOT=P.parents[2];OLD=P.parent/'daily-20261015T030225-0400'
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
a=[json.loads(l) for l in (P/'attempts.jsonl').read_text().splitlines()];latest={x['url']:x for x in a}
def payload(u):return json.loads(read(ROOT/latest[u]['evidence_file'])['text'])
def sig(s):return hashlib.sha256(json.dumps({k:s.get(k) for k in ['name','status','description','visible_sc_items','absolute_url']},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
studies={}
for skip in [0,500]:
    u=f'https://veterinaryclinicaltrials.org/avma/studies/search/json/?skip={skip}&take=500';d=payload(u)
    for s in d['studies']:studies[s['id']]=s
assert len(studies)==d['total'],(len(studies),d['total'])
oldrows=read(OLD/'registry-comparison.json')['rows'];rows=[];changed=[]
for old in oldrows:
    s=studies.get(old['registry_id'])
    same=bool(s and s['name']==old['title'] and s['status']==old['status'] and hashlib.sha256(s['description'].encode()).hexdigest()==old['current_description_sha256'])
    r={'registry_id':old['registry_id'],'current_title':s['name'] if s else None,'current_status':s['status'] if s else None,'same_title_status_and_entire_description':same,'canonical_id':old.get('canonical_id'),'previous_disposition':old.get('classification_retained_from_prior_manual_review'),'current_description_sha256':hashlib.sha256(s['description'].encode()).hexdigest() if s else None}
    rows.append(r)
    if not same:changed.append({'previous':old,'current':s})
tagged={s['id'] for s in studies.values() if s['status']=='Recruiting' and any(t.get('tag_path')=='primary-field-19_oncology-1' for t in s['visible_sc_items']) and any(t.get('label') in ('Canine','Feline') for t in s['visible_sc_items'])}
new=tagged-{r['registry_id'] for r in oldrows}
write(P/'registry-comparison.json',{'total':len(studies),'tagged_recruiting_oncology':len(tagged),'current_review_signals':len(rows),'rows':rows,'changed':changed,'new_tagged_signals':[studies[i] for i in sorted(new)],'evidence':[latest[f'https://veterinaryclinicaltrials.org/avma/studies/search/json/?skip={skip}&take=500']['evidence_file'] for skip in [0,500]],'provider_status_limit':'Registry sameness does not reconfirm provider intake; use current institution decisions and retained precise gaps.'})
for name,url in [('csu','https://clinicaltrials.csuveterinaryhealth.org/csuvet/studies/search/json/?skip=0&take=500'),('ucd','https://studypages.com/ucdavisvet/studies/search/json/?skip=0&take=500'),('mars','https://studypages.com/marsveterinaryclinicaltrials/studies/search/json/?skip=0&take=500')]:
    cur=payload(url);prev=[json.loads(l) for l in (OLD/'attempts.jsonl').read_text().splitlines() if json.loads(l)['url']==url and json.loads(l).get('http_status')==200][-1];before=json.loads(read(ROOT/prev['evidence_file'])['text']);old={s['id']:s for s in before['studies']};changes=[{'id':s['id'],'current':s,'previous':old.get(s['id'])} for s in cur['studies'] if s['id'] not in old or sig(s)!=sig(old[s['id']])]
    assert len(cur['studies'])==cur['total']
    write(P/(name+'-comparison.json'),{'total':cur['total'],'current_ids':[s['id'] for s in cur['studies']],'changed':changes,'missing':sorted(set(old)-{s['id'] for s in cur['studies']}),'evidence':latest[url]['evidence_file'],'explicit_whole_record_description_comparison':True})
    print(name,'total',cur['total'],'changed',len(changes))
trials={}
for page,url in [(1,'https://vettrials.org/api/trials?limit=1000'),(2,'https://vettrials.org/api/trials?limit=100&page=2'),(3,'https://vettrials.org/api/trials?limit=100&page=3')]:
    d=payload(url)
    records=d['data']['trials']
    for s in records:trials[s['id']]=s
    print('vettrials page',page,len(records),'keys',list(d))
old={r['id']:r for r in read(OLD/'vettrials-full-current.json')['all_records']}
keys=['title','sourceUrl','avmaRegistryId','species','conditionCategory','status','summary','description','eligibility','intervention','location','sourceId']
changes=[{'id':s['id'],'current':s,'previous':old.get(s['id'])} for s in trials.values() if s['id'] not in old or any(s.get(k)!=old[s['id']].get(k) for k in keys)]
write(P/'vettrials-comparison.json',{'total':len(trials),'current_ids':sorted(trials),'changed':changes,'missing':sorted(set(old)-set(trials)),'old_reviewed_signal_ids':[r['aggregator_id'] for r in read(OLD/'vettrials-reconciliation.json')['rows']],'comparison_keys':keys,'fresh_pages_evidence':[latest[u]['evidence_file'] for u in latest if 'vettrials.org/api/' in u]})
print('AVMA',len(studies),'signals',len(rows),'changed',len(changed),'new',len(new));print('VetTrials',len(trials),'changed',len(changes))
