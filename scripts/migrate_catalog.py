from __future__ import annotations
import ast, json
from pathlib import Path

PAGE = Path('pages/1_Clinical_Trial_Finder.py')
DATA = Path('data/trials_base.json')
LOADER = '''\n# Catalog data is stored separately from the Streamlit page.\nfrom pathlib import Path as _Path\nimport json as _json\n\ndef _load_trials():\n    _root = _Path(__file__).resolve().parents[1]\n    with (_root / "data" / "trials_base.json").open(encoding="utf-8") as _fh:\n        _base = _json.load(_fh)\n    _by_id = {t["id"]: t for t in _base}\n    _updates_path = _root / "data" / "trial_updates.json"\n    if _updates_path.exists():\n        with _updates_path.open(encoding="utf-8") as _fh:\n            _doc = _json.load(_fh)\n        for _trial_id in _doc.get("delete", []):\n            _by_id.pop(_trial_id, None)\n        for _patch in _doc.get("upsert", []):\n            _trial_id = _patch["id"]\n            if _trial_id in _by_id:\n                _by_id[_trial_id].update(_patch)\n            else:\n                _by_id[_trial_id] = _patch\n    return list(_by_id.values())\n\nTRIALS = _load_trials()\n'''

def main():
    src = PAGE.read_text(encoding='utf-8')
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    base = []
    remove = []
    assign = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'TRIALS' for t in node.targets):
            try:
                vals = ast.literal_eval(node.value)
            except Exception:
                continue
            if isinstance(vals, list):
                base.extend(vals); assign = node; remove.append((node.lineno, node.end_lineno))
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            f = node.value.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == 'TRIALS' and f.attr == 'extend':
                try: vals = ast.literal_eval(node.value.args[0])
                except Exception: continue
                if isinstance(vals, list): base.extend(vals); remove.append((node.lineno, node.end_lineno))
    if assign is None or not base:
        raise SystemExit('Could not locate static TRIALS catalog')
    # Remove the old incremental-update block; the new loader owns merging.
    start = next((i+1 for i,l in enumerate(lines) if '# Incremental catalog updates live in data/trial_updates.json.' in l), None)
    if start:
        end = start
        while end <= len(lines) and not (end > start and lines[end-1].startswith('# 2026-')):
            end += 1
        remove.append((start, end-1))
    # Rewrite from bottom to top so line numbers stay stable.
    for a,b in sorted(remove, reverse=True):
        del lines[a-1:b]
    insert_at = assign.lineno - 1
    # Account for any removed ranges before the original assignment (normally none).
    shift = sum(b-a+1 for a,b in remove if b < assign.lineno)
    insert_at -= shift
    lines.insert(insert_at, LOADER)
    DATA.write_text(json.dumps(base, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    PAGE.write_text(''.join(lines), encoding='utf-8')
    print(f'Migrated {len(base)} static records to {DATA}; page is {PAGE.stat().st_size} bytes')

if __name__ == '__main__':
    main()
