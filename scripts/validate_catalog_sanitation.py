#!/usr/bin/env python3
"""Detect canonical-record structural debt without confusing it with public-catalog failure."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/"data"/"trials_base.json"; Q=ROOT/"data"/"audit_unresolved.json"
CORE=("title","center","country","species","cancers","status","study_type","url","verified","notes","status_confidence")
def main():
 rows=json.loads(CAT.read_text()); q=json.loads(Q.read_text())
 known={rid for item in q.get("items",[]) if item.get("status")=="open" for rid in item.get("record_ids",[])}
 partial=[]
 for r in rows:
  miss=[k for k in CORE if r.get(k) in (None,"",[])]
  if miss: partial.append((r["id"],miss))
 new=[x for x in partial if x[0] not in known]
 stale=sorted(known-{x[0] for x in partial})
 print(json.dumps({"records":len(rows),"partial_records":len(partial),"known_unresolved":len(partial)-len(new),"new_partial_records":new,"resolved_but_still_queued":stale},indent=2))
 if new: raise SystemExit("NEW_CANONICAL_PARTIAL_RECORDS")
if __name__=="__main__": main()
