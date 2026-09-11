from pathlib import Path
import json

d=Path('data')
rows={r['id']:dict(r) for r in json.loads((d/'trials_base.json').read_text())}
for p in [d/'trial_updates.json']+sorted(d.glob('catalog_patch_*.json')):
    if not p.exists():
        continue
    doc=json.loads(p.read_text())
    for rid in doc.get('delete',[]):
        rows.pop(rid,None)
    for q in doc.get('upsert',[]):
        old=dict(rows.get(q['id'],{}))
        for k,v in q.items():
            if k in {'requires','excludes'} and isinstance(v,dict):
                n=dict(old.get(k,{})); n.update(v); old[k]=n
            else:
                old[k]=v
        rows[q['id']]=old

fixes={
    'umn-glioma-zika-autologous-vax': {'St. Paul':'St Paul'},
    'umn-glioma-nanoparticle-gene': {'St. Paul':'St Paul'},
    'eu-ch-sinonasal-heterogeneous-rt': {'Zurich':'Zürich'},
    # LEAH's marketing page labels the partner institution "Minneapolis, MN",
    # while the University of Minnesota Veterinary Medical Center where study
    # care is delivered is at 1365 Gortner Ave in St Paul. Preserve the actual
    # treatment-site geography in the structured location field.
    'leah-bcell-cart-2026': {'Minneapolis':'St Paul'},
}

up=[]
for rid,map_ in fixes.items():
    r=rows[rid]
    sites=[]; changed=False
    for s in r.get('sites') or []:
        if not isinstance(s,dict):
            sites.append(s); continue
        ns=dict(s)
        city=ns.get('city')
        if city in map_:
            ns['city']=map_[city]; changed=True
            if rid=='leah-bcell-cart-2026' and city=='Minneapolis':
                ns['site_scope']='LEAH lists the partner institution as Minneapolis; treatment-site address is University of Minnesota Veterinary Medical Center, 1365 Gortner Ave, St Paul, MN 55108.'
        sites.append(ns)
    if changed:
        up.append({'id':rid,'sites':sites,'location_model':'static active/inactive sites','location_verified':'2026-09-11'})

out={'upsert':up,'delete':[]}
Path('/tmp/location-normalization-patch.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('NORMALIZED_RECORDS',len(up))
for q in up:
    print('NORMALIZED',q['id'])