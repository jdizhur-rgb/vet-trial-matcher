from pathlib import Path
import json, re, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from seo.center_directory import addresses_for

d=Path('data')
rows={r['id']:dict(r) for r in json.loads((d/'trials_base.json').read_text())}
for p in [d/'trial_updates.json']+sorted(d.glob('catalog_patch_*.json')):
    if not p.exists(): continue
    doc=json.loads(p.read_text())
    for rid in doc.get('delete',[]): rows.pop(rid,None)
    for q in doc.get('upsert',[]):
        old=dict(rows.get(q['id'],{})); old.update(q); rows[q['id']]=old

SPECIAL={
    'Metropolitan Veterinary Hospital — Cleveland, OH': 'Metropolitan Veterinary Hospital - Cleveland East, 734 Alpha Drive, Highland Heights, OH 44143',
    'Metropolitan Veterinary Hospital — Akron, OH': 'Metropolitan Veterinary Hospital, 1053 S Cleveland-Massillon Rd, Akron, OH 44321',
    'Veterinary Emergency + Referral Center — Honolulu, HI': 'Veterinary Emergency + Referral Center of Hawaii, 345 N Nimitz Hwy, Unit C, Honolulu, HI 96817',
    '中興梅西動物醫院 — Kaohsiung, Taiwan': '梅西動物醫療中心, 高雄市左營區文府路498號, Kaohsiung, Taiwan',
}
# These labels cannot safely be collapsed to one current street address without
# an explicit site-level source. Keep them visible for manual verification.
SKIP={
    'Metropolitan Veterinary Hospital — Akron/Cleveland, OH',
    'Atlantic Veterinary Internal Medicine & Oncology — Columbia, MD',
}

active=[r for r in rows.values() if r.get('available_for_matching',True) and r.get('status_confidence') in {'current','confirmed_current'} and r.get('study_type','treatment') in {'treatment','other_treatment_access'}]
up=[]; skipped=[]
for r in active:
    out=[]; changed=False
    for s in r.get('sites') or []:
        if not isinstance(s,dict) or s.get('status','active')!='active': out.append(s); continue
        text=(s.get('label') or s.get('address') or s.get('hospital') or '').strip()
        if re.search(r'\d',text): out.append(s); continue
        if text in SKIP:
            out.append(s); skipped.append((r['id'],text)); continue
        found=[]
        if text in SPECIAL:
            found=[SPECIAL[text]]
        else:
            names=[(s.get('hospital') or '').strip(), re.sub(r'^📍\s*','',text).split(' — ')[0].strip(), r.get('center','')]
            for name in names:
                if name and addresses_for(name): found=addresses_for(name); break
        if len(found)==1:
            ns=dict(s); ns['label']=found[0]; ns['address']=found[0]; ns['status']='active'; out.append(ns); changed=True
        else:
            out.append(s); skipped.append((r['id'],text))
    if changed:
        up.append({'id':r['id'],'sites':out,'location_model':'static active/inactive sites','location_verified':'2026-09-11'})
Path('/tmp/static-address-patch.json').write_text(json.dumps({'upsert':up,'delete':[]},ensure_ascii=False,indent=2)+'\n')
print('PATCH_RECORDS',len(up))
print('SKIPPED',len(skipped))
for x in skipped: print('SKIP',x[0],'|',x[1])