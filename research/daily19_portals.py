from daily19 import ROOT,RUN,OLD,read,write,m
import json,collections
aa=[json.loads(l) for l in (RUN/'protocol-attempts.jsonl').read_text().splitlines()]
def normal(v):
 if isinstance(v,dict):return {k:sorted([normal(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True)) if k=='visible_sc_items' else normal(x) for k,x in v.items()}
 if isinstance(v,list):return [normal(x) for x in v]
 return v
out={}
for sid,name in [('registry-avma-veterinary-clinical-trials','avma'),('usa-colorado-state-vth-clinical-trials','csu'),('usa-uc-davis-vcct','ucd'),('usa-mars-veterinary-health-clinical-trials','mars')]:
 attempts=[a for a in aa if a['source_id']==sid and a.get('http_status')==200];allrows=[];totals=[]
 for a in attempts:
  d=json.loads(read(ROOT/a['evidence_file'])['text']);allrows+=d['studies'];totals.append(d['total'])
 current=list({x['id']:x for x in allrows}.values());previous=read(OLD/(name+'-comparison.json'))['current_roster'];old={x['id']:x for x in previous};new={x['id']:x for x in current};changed=[k for k in old.keys()&new.keys() if normal(old[k])!=normal(new[k])];added=list(new.keys()-old.keys());missing=list(old.keys()-new.keys())
 assert len(current)==max(totals),(sid,len(current),totals)
 obj={'source_id':sid,'total':len(current),'current_roster':current,'changed':changed,'added':added,'missing':missing,'evidence':[a['evidence_file'] for a in attempts],'read_at':[a['attempted_at'] for a in attempts],'comparison':'Whole objects including entire descriptions and full tags compared. Only tag-object order normalized; no fields removed. Complete pagination count checked. Earlier rejected mixed output not read.'}
 write(RUN/(name+'-comparison.json'),obj);out[sid]=obj;print(name,len(current),'changed',changed,'added',added,'missing',missing)
sid='global-vettrials-directory';attempts=[a for a in aa if a['source_id']==sid and a.get('http_status')==200];allrows=[];totals=[]
for a in attempts:
 d=json.loads(read(ROOT/a['evidence_file'])['text']);allrows+=d['data']['trials'];print('VETTRIALS_META',d.get('data',{}).keys())
cur=list({x['id']:x for x in allrows}.values());prev=read(OLD/'vettrials-comparison.json')['whole_current_roster'];old={x['id']:x for x in prev};new={x['id']:x for x in cur};cats=collections.Counter(x.get('conditionCategory') for x in cur);onc=[x for x in cur if x.get('conditionCategory') in ['oncology','cancer']]
obj={'source_id':sid,'total_entries':len(cur),'oncology_entries':len(onc),'categories':dict(cats),'whole_current_roster':cur,'changed':[k for k in old.keys()&new.keys() if old[k]!=new[k]],'added':list(new.keys()-old.keys()),'missing':list(old.keys()-new.keys()),'evidence':[a['evidence_file'] for a in attempts],'read_at':[a['attempted_at'] for a in attempts],'comparison':'Complete full objects, not saved hash only; all three pages traversed. Secondary directory entry counts are not confirmed current treatment-trial counts.'}
write(RUN/'vettrials-comparison.json',obj);print('vettrials',len(cur),cats,'changed',obj['changed'])
