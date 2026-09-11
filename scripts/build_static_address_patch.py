from pathlib import Path
import json, re
from seo.center_directory import addresses_for

d=Path('data')
rows={r['id']:dict(r) for r in json.loads((d/'trials_base.json').read_text())}
for p in [d/'trial_updates.json']+sorted(d.glob('catalog_patch_*.json')):
    if not p.exists(): continue
    doc=json.loads(p.read_text())
    for rid in doc.get('delete',[]): rows.pop(rid,None)
    for q in doc.get('upsert',[]):
        old=dict(rows.get(q['id'],{})); old.update(q); rows[q['id']]=old
active=[r for r in rows.values() if r.get('available_for_matching',True) and r.get('status_confidence') in {'current','confirmed_current'} and r.get('study_type','treatment') in {'treatment','other_treatment_access'}]
up=[]
for r in active:
    out=[]; changed=False
    for s in r.get('sites') or []:
        if not isinstance(s,dict) or s.get('status','active')!='active': out.append(s); continue
        text=(s.get('label') or s.get('address') or s.get('hospital') or '').strip()
        if re.search(r'\d',text): out.append(s); continue
        names=[(s.get('hospital') or '').strip(), re.sub(r'^📍\s*','',text).split(' — ')[0].strip(), r.get('center','')]
        found=[]
        for name in names:
            if name and addresses_for(name): found=addresses_for(name); break
        if len(found)==1:
            ns=dict(s); ns['label']=found[0]; ns['address']=found[0]; ns['status']='active'; out.append(ns); changed=True
        else: out.append(s)
    if changed: up.append({'id':r['id'],'sites':out,'location_model':'static active/inactive sites','location_verified':'2026-09-11'})
Path('/tmp/static-address-patch.json').write_text(json.dumps({'upsert':up,'delete':[]},ensure_ascii=False,indent=2)+'\n')
print('PATCH_RECORDS',len(up))