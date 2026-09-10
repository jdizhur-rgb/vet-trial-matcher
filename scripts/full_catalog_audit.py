#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
BASELINE = '391d618cda5b08a7593b394a7fe2fb61365b02b2'  # first live counter commit
CURRENT = {'current','confirmed_current'}
TYPES = {'treatment','other_treatment_access'}

def merge(old, patch):
    out=dict(old)
    for k,v in patch.items():
        if k in {'requires','excludes'} and isinstance(v,dict):
            nested=dict(out.get(k,{}) if isinstance(out.get(k),dict) else {})
            nested.update(v); out[k]=nested
        else: out[k]=v
    return out

def load_worktree():
    rows={r['id']:r for r in json.loads((DATA/'trials_base.json').read_text())}
    paths=[DATA/'trial_updates.json']+sorted(DATA.glob('catalog_patch_*.json'))
    for p in paths:
        if not p.exists(): continue
        d=json.loads(p.read_text())
        for rid in d.get('delete',[]): rows.pop(rid,None)
        for patch in d.get('upsert',[]): rows[patch['id']]=merge(rows.get(patch['id'],{}),patch)
    return rows

def git_text(ref,path):
    try: return subprocess.check_output(['git','show',f'{ref}:{path}'],text=True,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError: return None

def load_ref(ref):
    txt=git_text(ref,'data/trials_base.json')
    if txt is None: return {}
    rows={r['id']:r for r in json.loads(txt)}
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',ref,'data'],text=True).splitlines()
    paths=['data/trial_updates.json']+sorted(p for p in names if re.fullmatch(r'data/catalog_patch_.*\.json',p))
    for p in paths:
        txt=git_text(ref,p)
        if txt is None: continue
        d=json.loads(txt)
        for rid in d.get('delete',[]): rows.pop(rid,None)
        for patch in d.get('upsert',[]): rows[patch['id']]=merge(rows.get(patch['id'],{}),patch)
    return rows

def active_finder(r):
    return r.get('available_for_matching',True) and r.get('status_confidence') in CURRENT and r.get('study_type','treatment') in TYPES

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()

def key_url(u):
    u=str(u or '').lower().split('?')[0].rstrip('/')
    return u

def main():
    cur=load_worktree(); base=load_ref(BASELINE)
    ca={k:v for k,v in cur.items() if active_finder(v)}
    ba={k:v for k,v in base.items() if active_finder(v)}
    print('CURRENT_EFFECTIVE_TOTAL',len(cur))
    print('CURRENT_ACTIVE_TREATMENTS',len(ca))
    print('BASELINE_ACTIVE_TREATMENTS',len(ba))
    added=sorted(set(ca)-set(ba)); removed=sorted(set(ba)-set(ca))
    print('ACTIVE_ADDED_SINCE_BASELINE',len(added))
    for x in added: print('ADD',x,'|',ca[x].get('center',''),'|',ca[x].get('title',''))
    print('ACTIVE_REMOVED_SINCE_BASELINE',len(removed))
    for x in removed: print('REM',x,'|',ba[x].get('center',''),'|',ba[x].get('title',''))

    legacy=[r for r in ca.values() if 'available_for_matching' not in r]
    print('ACTIVE_LEGACY_DEFAULT_TRUE',len(legacy))
    for r in sorted(legacy,key=lambda x:x['id']): print('LEGACY',r['id'],'|',r.get('center',''),'|',r.get('title',''))

    print('STATUS_COUNTS_ALL_EFFECTIVE')
    for k,n in Counter(str(r.get('status_confidence','<missing>')) for r in cur.values()).most_common(): print('STATUS',k,n)
    print('STUDY_TYPE_COUNTS_ALL_EFFECTIVE')
    for k,n in Counter(str(r.get('study_type','treatment')) for r in cur.values()).most_common(): print('TYPE',k,n)

    byurl=defaultdict(list)
    for r in ca.values():
        for fld in ('registry_url','url'):
            u=key_url(r.get(fld))
            if u: byurl[(fld,u)].append(r['id'])
    url_dups=[(k,ids) for k,ids in byurl.items() if len(ids)>1]
    print('EXACT_SHARED_URL_GROUPS',len(url_dups))
    for (fld,u),ids in sorted(url_dups): print('URLDUP',fld,'|',','.join(sorted(ids)),'|',u)

    title_groups=defaultdict(list)
    for r in ca.values(): title_groups[(norm(r.get('center')),norm(r.get('title')))].append(r['id'])
    exact_titles=[(k,ids) for k,ids in title_groups.items() if k[1] and len(ids)>1]
    print('EXACT_CENTER_TITLE_GROUPS',len(exact_titles))
    for (_,t),ids in sorted(exact_titles): print('TITLEDUP',','.join(sorted(ids)),'|',t)

    # conservative near-duplicate candidates: same normalized center + high title similarity
    vals=list(ca.values()); near=[]
    for i,a in enumerate(vals):
        caa=norm(a.get('center')); ta=norm(a.get('title'))
        if not caa or not ta: continue
        for b in vals[i+1:]:
            if norm(b.get('center'))!=caa: continue
            tb=norm(b.get('title'))
            if not tb: continue
            score=SequenceMatcher(None,ta,tb).ratio()
            if score>=0.86 and a['id']!=b['id']:
                near.append((score,a['id'],b['id'],a.get('title',''),b.get('title','')))
    print('NEAR_DUP_CANDIDATES',len(near))
    for score,a,b,ta,tb in sorted(near,reverse=True): print('NEARDUP',f'{score:.3f}',a,b,'|',ta,'||',tb)

    # deleted aliases from all cleanup patches must not survive effective catalog
    deleted=[]
    for p in sorted(DATA.glob('catalog_patch_*.json')):
        try: d=json.loads(p.read_text())
        except Exception: continue
        deleted += d.get('delete',[])
    survivors=sorted(set(deleted)&set(cur))
    print('DELETED_IDS_SURVIVING_EFFECTIVE',len(survivors))
    for x in survivors: print('DELETE_SURVIVOR',x)

    # basic completeness of every active record
    required=('id','title','center','species','cancers','status_confidence')
    incomplete=[]
    for r in ca.values():
        miss=[k for k in required if r.get(k) in (None,'',[])]
        if not (r.get('url') or r.get('registry_url')): miss.append('owner_facing_url')
        if miss: incomplete.append((r['id'],miss))
    print('ACTIVE_INCOMPLETE',len(incomplete))
    for rid,miss in incomplete: print('INCOMPLETE',rid,','.join(miss))

if __name__=='__main__': main()
