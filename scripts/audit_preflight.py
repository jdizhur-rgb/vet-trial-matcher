#!/usr/bin/env python3
"""Deterministic audit preflight with blocking vs ancillary classification."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CORE=[
 ("catalog","scripts/validate_trials_catalog.py"),
 ("sources","scripts/validate_source_inventory.py"),
 ("hygiene","scripts/validate_repository_hygiene.py"),
]
ANCILLARY=[("streamlit","scripts/test_streamlit_pages.py")]
def run(name,path):
 p=subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,text=True,capture_output=True)
 return {"name":name,"ok":p.returncode==0,"returncode":p.returncode,"output":(p.stdout+p.stderr).strip()[-4000:]}
def main():
 results=[run(*x) for x in CORE+ANCILLARY]
 blocking=[r for r in results[:len(CORE)] if not r["ok"]]
 ancillary=[r for r in results[len(CORE):] if not r["ok"]]
 status="BLOCKING" if blocking else ("PASS_WITH_INCONCLUSIVE" if ancillary else "PASS")
 print(json.dumps({"status":status,"safe_to_continue":not blocking,"checks":results},indent=2))
 raise SystemExit(2 if blocking else 0)
if __name__=="__main__": main()
