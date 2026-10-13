#!/usr/bin/env python3
"""Run and persist the required no-change daily validation/build gates."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
TZ = ZoneInfo("America/New_York")

COMMANDS = [
    ("evidence_redact", ["python", "scripts/check_evidence_keys.py", "--redact", str(RUN.relative_to(ROOT))]),
    ("evidence_keys", ["python", "scripts/check_evidence_keys.py"]),
    ("catalog_sanitation", ["python", "scripts/validate_catalog_sanitation.py"]),
    ("trials_catalog", ["python", "scripts/validate_trials_catalog.py"]),
    ("source_inventory", ["python", "scripts/validate_source_inventory.py"]),
    ("full_catalog_audit", ["python", "scripts/full_catalog_audit.py"]),
    ("matcher_loading", ["node", "scripts/test_matcher_catalog_loading.js"]),
    ("matcher_protocol_sources", ["node", "scripts/test_matcher_protocol_sources.js"]),
    ("matcher_selection_node", ["node", "scripts/test_matcher_selection.js"]),
    ("matcher_selection_python", ["python", "scripts/test_matcher_selection.py"]),
    ("build_matcher_data", ["python", "scripts/build_matcher_data.py"]),
    ("matcher_logic", ["node", "scripts/test_matcher_logic.js"]),
    ("build_static_site", ["python", "scripts/build_static_site.py"]),
    ("production_sync", ["python", "scripts/validate_production_sync.py"]),
]

results = []
for name, cmd in COMMANDS:
    started = datetime.now(TZ).isoformat()
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    output = (proc.stdout + proc.stderr).strip()
    (RUN / f"{name}.txt").write_text(output + ("\n" if output else ""))
    results.append({"name": name, "command": cmd, "started_at": started,
                    "finished_at": datetime.now(TZ).isoformat(), "returncode": proc.returncode,
                    "status": "PASS" if proc.returncode == 0 else "FAIL",
                    "output_file": f"research/audit-runs/{RUN.name}/{name}.txt"})
    print(name, results[-1]["status"], flush=True)

summary = {"run_id": RUN.name, "created_at": datetime.now(TZ).isoformat(), "results": results,
           "overall": "PASS" if all(x["returncode"] == 0 for x in results) else "FAIL"}
(RUN / "validation-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
raise SystemExit(summary["overall"] != "PASS")
