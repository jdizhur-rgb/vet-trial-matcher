import json
from pathlib import Path

DATA = Path('data')
UPDATES = DATA / 'trial_updates.json'
PATCHES = sorted(DATA.glob('catalog_patch_*_20260907.json'))

updates = json.loads(UPDATES.read_text(encoding='utf-8'))
upserts = {r['id']: r for r in updates.get('upsert', []) if r.get('id')}
deletes = set(updates.get('delete', []))

added = []
updated = []
for path in PATCHES:
    patch = json.loads(path.read_text(encoding='utf-8'))
    for rec in patch.get('upsert', []):
        rid = rec.get('id')
        if not rid:
            continue
        # Treatment staging records are intended for the live matcher unless
        # the patch explicitly says otherwise (e.g. a watchlist record).
        if rec.get('study_type') == 'treatment' and 'available_for_matching' not in rec:
            rec['available_for_matching'] = True
        if rid in upserts:
            merged = dict(upserts[rid])
            merged.update(rec)
            upserts[rid] = merged
            updated.append(rid)
        else:
            upserts[rid] = rec
            added.append(rid)
        deletes.discard(rid)
    for rid in patch.get('delete', []):
        if rid not in upserts:
            deletes.add(rid)
        else:
            # A same-day upsert wins over an older delete marker.
            deletes.discard(rid)

updates['upsert'] = list(upserts.values())
updates['delete'] = sorted(deletes)
UPDATES.write_text(json.dumps(updates, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(f'Applied {len(PATCHES)} patch files; new={len(set(added))}, refreshed={len(set(updated))}')
print('New IDs:', ', '.join(sorted(set(added))))
