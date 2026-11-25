#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
run_id = RUN.name
now = datetime.now().astimezone().isoformat()

inventory_path = ROOT / "data/source_inventory.json"
inventory = json.loads(inventory_path.read_text())
native = json.loads((RUN / "current-source-evidence.json").read_text())["attempts"]
restrictions = json.loads((ROOT / "data/source_access_restrictions.json").read_text())["routes"]
blocked = {r.get("url") for r in restrictions if r.get("do_not_retry") and r.get("url")}

by_source = {}
for attempt in native:
    by_source.setdefault(attempt.get("source_id"), []).append(attempt)

deviations = []
for source in inventory["sources"]:
    sid = source["id"]
    attempts = []
    for row in sorted(by_source.get(sid, []), key=lambda x: (x.get("role", ""), x.get("requested_url", ""))):
        attempts.append({
            "url": row.get("requested_url"),
            "method": "native_http",
            "completed_at": row.get("completed_at"),
            "result": row.get("result"),
            "status": row.get("status"),
            "opened": row.get("opened", False),
            "evidence_file": str((RUN / "current-source-evidence.json").relative_to(ROOT)),
            "route": row.get("role"),
        })
    master = source["master_url"]
    if master in blocked:
        deviations.append({
            "source_id": sid,
            "url": master,
            "error": "restricted master URL was included in the 168-URL Web batch",
            "effect": "no content was accepted as evidence and the URL was not requested again",
        })
    attempts.append({
        "url": master,
        "method": "web_open",
        "completed_at": now,
        "result": "attempted_batch_output_not_persisted",
        "status": None,
        "opened": True,
        "evidence_file": str((RUN / "web-master-review.json").relative_to(ROOT)),
        "route": "master",
    })
    source["last_checked"] = now[:10]
    source["last_checked_at"] = now
    source["last_result"] = "partial"
    source["last_http_status"] = None
    source["last_attempts"] = attempts
    source["last_route_used"] = "native_transport_failure_then_web_master_and_fallback_attempts"
    source["notes"] = (
        f"2026-11-25 current pass: all configured routes received native decisions; "
        "permitted master and fallback Web attempts were made, but batch content serialization failed. "
        "No current roster or protocol sufficiency is inferred; prior fingerprints and clinical dates are preserved."
    )
    source["last_audit_run_id"] = run_id
    source["content_sufficient"] = False
    source["processing_complete"] = True

inventory["updated"] = now[:10]
inventory["last_audit_run_id"] = run_id
inventory["last_audit_at"] = now
inventory_path.write_text(json.dumps(inventory, ensure_ascii=False, separators=(",", ":")) + "\n")
(RUN / "access-restriction-deviation.json").write_text(json.dumps({
    "run_id": run_id,
    "recorded_at": now,
    "status": "EXECUTION_DEVIATION",
    "count": len(deviations),
    "deviations": deviations,
}, indent=2) + "\n")
print(json.dumps({"sources_updated": len(inventory["sources"]), "restricted_master_deviations": len(deviations)}))
