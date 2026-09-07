from pathlib import Path
import json,re,sys
from difflib import SequenceMatcher
from urllib.parse import urlsplit,urlunsplit

BASE=Path('data/trials_base.json'); UPD=Path('data/trial_updates.json')

def norm(s):
    s=str(s or '').lower().replace('–','-').replace('—','-')
    s=re.sub(r'\b(university|college|school|veterinary|medicine|medical|center|centre|hospital|clinic|clinical|trial|study|current|recruiting|actively|canine|feline|dogs?|cats?|for|with|of|the|and|a|an|phase|pilot)\b',' ',s)
    return ' '.join(re.findall(r'[a-z0-9]+',s))

def urlkey(u):
    if isinstance(u,list): u=u[0] if u else ''
    if not u:return ''
    try:
        q=urlsplit(str(u)); return (q.netloc.lower().removeprefix('www.')+q.path.rstrip('/').lower())
    except:return ''

def species(x):
    v=x.get('species',[]); v=v if isinstance(v,list) else re.split(r'[/,;]',str(v)); return {norm(z) for z in v if z}

def cancers(x):
    v=x.get('cancers',[]); v=v if isinstance(v,list) else [v]; return {norm(z) for z in v if z}

def center(x): return norm(x.get('center',''))

def title(x): return norm(x.get('title',''))

def tokens(s): return set(norm(s).split())

def overlap(a,b):
    return len(a&b)/max(1,min(len(a),len(b)))

def same_real_study(a,b):
    # Exact protocol/source route is strongest evidence.
    ua,ub=urlkey(a.get('url')),urlkey(b.get('url'))
    if ua and ua==ub:return True,'same-url'
    ta,tb=title(a),title(b); ca,cb=center(a),center(b)
    if not ta or not tb:return False,''
    ts=SequenceMatcher(None,ta,tb).ratio(); cs=SequenceMatcher(None,ca,cb).ratio() if ca and cb else 0
    ct=overlap(cancers(a),cancers(b)) if cancers(a) and cancers(b) else 0
    sp=bool(species(a)&species(b))
    # Same/near-same center plus highly similar title.
    if sp and cs>=.62 and ts>=.72:return True,f'center-title:{cs:.2f}/{ts:.2f}'
    # Distinctive treatment-token match catches renamed imports from same institution.
    distinctive={'palbociclib','z-007','z007','cotc033','trike','car-inkt','carinkt','r3lcmv','lcmv','histotripsy','hifu','carboplatin','adam12','vinorelbine','tigilanol','ferumoxytol'}
    da=tokens(ta)&distinctive; db=tokens(tb)&distinctive
    if sp and da and da==db and cs>=.45 and (ct>=.5 or 'solid tumors' in ta or 'solid tumors' in tb):return True,f'distinctive:{sorted(da)}'
    return False,''

def quality(x):
    return (bool(x.get('verified')), x.get('status_confidence') in {'confirmed_current','current'}, bool(x.get('contacts')), len(str(x.get('notes',''))), len(str(x.get('title',''))))

base=json.loads(BASE.read_text()); upd=json.loads(UPD.read_text())
if isinstance(base,dict): base=base.get('trials',base.get('records',[]))
upserts=upd.get('upsert',[]); deleted=set(upd.get('delete',[]))
# Effective records, with upserts overriding base IDs.
byid={x['id']:x for x in base if x.get('id') not in deleted}
for x in upserts:
    if x.get('id') not in deleted: byid[x['id']]=x
rows=[x for x in byid.values() if x.get('study_type')=='treatment' and x.get('available_for_matching') is True]

pairs=[]
for i,a in enumerate(rows):
    for b in rows[i+1:]:
        same,why=same_real_study(a,b)
        if same:pairs.append((a,b,why))

# Resolve only pairs that our gate itself classifies as the same real study.
removed=set(); report=[]
for a,b,why in pairs:
    if a['id'] in removed or b['id'] in removed:continue
    keep,drop=(a,b) if quality(a)>=quality(b) else (b,a)
    removed.add(drop['id']); report.append({'keep':keep['id'],'drop':drop['id'],'reason':why,'keep_title':keep.get('title'),'drop_title':drop.get('title')})

if removed:
    upd['upsert']=[x for x in upserts if x.get('id') not in removed]
    upd['delete']=sorted(set(upd.get('delete',[]))|removed)
    UPD.write_text(json.dumps(upd,ensure_ascii=False,indent=2)+'\n')

# Rebuild and require zero duplicates under the SAME rule after mutation.
upd2=json.loads(UPD.read_text()); deleted=set(upd2.get('delete',[])); byid={x['id']:x for x in base if x.get('id') not in deleted}
for x in upd2.get('upsert',[]):
    if x.get('id') not in deleted:byid[x['id']]=x
rows=[x for x in byid.values() if x.get('study_type')=='treatment' and x.get('available_for_matching') is True]
left=[]
for i,a in enumerate(rows):
    for b in rows[i+1:]:
        same,why=same_real_study(a,b)
        if same:left.append((a['id'],b['id'],why))
print(json.dumps({'effective_matchable_treatments':len(rows),'duplicates_removed':len(report),'removed':report,'duplicates_remaining':left},ensure_ascii=False,indent=2))
if left:sys.exit(2)
