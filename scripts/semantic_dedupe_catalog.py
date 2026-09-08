from pathlib import Path
import json,re,sys
from difflib import SequenceMatcher
BASE=Path('data/trials_base.json');UPD=Path('data/trial_updates.json');APPLY='--apply' in sys.argv

def norm(s):
 s=str(s or '').lower().replace('–','-').replace('—','-');s=re.sub(r'\b(university|college|school|veterinary|medicine|medical|center|centre|hospital|clinic|clinical|trial|study|current|recruiting|actively|canine|feline|dogs?|cats?|for|with|of|the|and|a|an|phase|pilot)\b',' ',s);return ' '.join(re.findall(r'[a-z0-9]+',s))
def vals(x,k):
 v=x.get(k,[]);v=v if isinstance(v,list) else re.split(r'[/,;]',str(v));return {norm(z) for z in v if z}
def center(x):return norm(x.get('center',''))
def title(x):return norm(x.get('title',''))
def toks(s):return set(norm(s).split())
def ov(a,b):return len(a&b)/max(1,min(len(a),len(b)))
def ids(x):
 text=' '.join(str(x.get(k,'')) for k in ('id','title','notes'));p=r'\b(?:COTC[- ]?\d{3}|Z[- ]?007|PIVOT[- ]?C|AKS[- ]?\d+[A-Z]?|BI\d{6})\b';return {re.sub(r'[^A-Z0-9]','',m.upper()) for m in re.findall(p,text,re.I)}
def same(a,b):
 ta,tb=title(a),title(b);ca,cb=center(a),center(b)
 if not ta or not tb:return False,''
 ts=SequenceMatcher(None,ta,tb).ratio();cs=SequenceMatcher(None,ca,cb).ratio() if ca and cb else 0;sp=bool(vals(a,'species')&vals(b,'species'));ct=ov(vals(a,'cancers'),vals(b,'cancers')) if vals(a,'cancers') and vals(b,'cancers') else 0;common=ids(a)&ids(b)
 if sp and any(x.startswith('COTC') for x in common):return True,f'protocol:{sorted(common)}'
 if sp and common and cs>=.72 and ct>=.5:return True,f'id+center+cancer:{sorted(common)}'
 if sp and cs>=.78 and ts>=.84 and ct>=.5:return True,f'center+title+cancer:{cs:.2f}/{ts:.2f}/{ct:.2f}'
 distinctive={'palbociclib','trike','carinkt','r3lcmv','adam12','vinorelbine','ferumoxytol'};da=toks(ta)&distinctive;db=toks(tb)&distinctive
 if sp and da and da==db and cs>=.72 and ct>=.5:return True,f'distinctive+center+cancer:{sorted(da)}'
 return False,''
def quality(x):return(bool(x.get('verified')),x.get('status_confidence') in {'confirmed_current','current'},bool(x.get('contacts')),len(str(x.get('notes',''))))
def load():
 base=json.loads(BASE.read_text());base=base.get('trials',base.get('records',[])) if isinstance(base,dict) else base;upd=json.loads(UPD.read_text());deleted=set(upd.get('delete',[]));byid={x['id']:x for x in base}
 # Effective catalog semantics: partial upserts MERGE onto base records; delete has final precedence.
 for x in upd.get('upsert',[]):byid[x['id']]={**byid.get(x['id'],{}),**x}
 for rid in deleted:byid.pop(rid,None)
 return base,upd,[x for x in byid.values() if x.get('study_type')=='treatment' and x.get('available_for_matching') is True]
base,upd,rows=load();pairs=[]
for i,a in enumerate(rows):
 for b in rows[i+1:]:
  ok,why=same(a,b)
  if ok:pairs.append((a,b,why))
removed=set();report=[]
for a,b,why in pairs:
 if a['id'] in removed or b['id'] in removed:continue
 keep,drop=(a,b) if quality(a)>=quality(b) else (b,a);removed.add(drop['id']);report.append({'keep':keep['id'],'drop':drop['id'],'reason':why,'keep_title':keep.get('title'),'drop_title':drop.get('title')})
print(json.dumps({'mode':'apply' if APPLY else 'audit','effective_matchable_treatments':len(rows),'probable_duplicates':len(report),'pairs':report},ensure_ascii=False,indent=2))
if not APPLY:sys.exit(1 if report else 0)
if removed:
 upd['upsert']=[x for x in upd.get('upsert',[]) if x.get('id') not in removed];upd['delete']=sorted(set(upd.get('delete',[]))|removed);UPD.write_text(json.dumps(upd,ensure_ascii=False,indent=2)+'\n')
_,_,rows=load();left=[]
for i,a in enumerate(rows):
 for b in rows[i+1:]:
  ok,why=same(a,b)
  if ok:left.append((a['id'],b['id'],why))
print(json.dumps({'post_apply_matchable_treatments':len(rows),'removed':len(removed),'duplicates_remaining':left},ensure_ascii=False,indent=2))
if left:sys.exit(2)
