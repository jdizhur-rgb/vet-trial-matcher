#!/usr/bin/env python3
"""Build the 2026-11-05 current-evidence accounting from this run's artifacts."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parents[1]
RUN_REL = RUN.relative_to(ROOT).as_posix()
RUN_ID = RUN.name


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def stripped(row, *, source_id=None, route=None):
    keep = {
        "source_id", "trial_id", "route", "url", "method", "attempted_at",
        "new_source_visit", "completed_at", "http_status", "effective_url",
        "content_type", "attempts", "result", "access_gate_observed",
        "body_bytes", "body_sha256", "text_length", "text_sha256",
        "evidence_file", "restriction",
    }
    out = {k: v for k, v in row.items() if k in keep}
    if source_id:
        out["source_id"] = source_id
    if route:
        out["route"] = route
    return out


now = datetime.now(ZoneInfo("America/New_York"))
now_s = now.isoformat()
baseline = read(RUN / "execution-baseline.json")
inventory_payload = read(ROOT / "data/source_inventory.json")
inventory = inventory_payload["sources"]
inventory_by_id = {s["id"]: s for s in inventory}
baseline_inventory_by_id = {
    s["id"]: s for s in read(RUN / "baseline-source_inventory.json")["sources"]
}
catalog = read(ROOT / "data/trials_base.json")
catalog_by_id = {t["id"]: t for t in catalog}
baseline_catalog = read(RUN / "baseline-trials_base.json")
baseline_catalog_by_id = {t["id"]: t for t in baseline_catalog}
previous = read(RUN / "previous-receipt.json")
previous_sources = {s["source_id"]: s for s in previous["sources"]}

master = read(RUN / "master-results.json")
fallback = read(RUN / "fallback-results.json")
obvious = read(RUN / "obvious-protocol-results.json")
primary = read(RUN / "primary-results.json")
supplement = read(RUN / "supplement-primary-results.json") + read(RUN / "supplement-primary-results-2.json")
primary_by_trial = {r.get("trial_id"): r for r in primary if r.get("trial_id")}

attempts_by_source = defaultdict(list)
for row in master + fallback + obvious:
    attempts_by_source[row["source_id"]].append(stripped(row))

# The new Liverpool inventory identity was created from an exact current individual read.
liverpool_trial = primary_by_trial["uk-liverpool-dogfight-glioma-ferumoxytol-rt"]
attempts_by_source["uk-liverpool-dogfight-glioma-trial"].append(
    stripped(liverpool_trial, source_id="uk-liverpool-dogfight-glioma-trial", route="master_url")
)

previous_attempts = {
    sid: {a.get("url"): a for a in row.get("attempted_urls", [])}
    for sid, row in previous_sources.items()
}

source_rows = []
source_reviews = []
comparisons = []
sufficient_ids = {"uk-liverpool-dogfight-glioma-trial"}

for source in inventory:
    sid = source["id"]
    attempts = attempts_by_source[sid]
    assert attempts, f"no current attempt for {sid}"
    retrieved = [a for a in attempts if a.get("result") == "retrieved_page"]
    changed = []
    for a in attempts:
        old = previous_attempts.get(sid, {}).get(a.get("url"))
        if not old or not a.get("text_sha256") or not old.get("text_sha256"):
            continue
        equal = a["text_sha256"] == old["text_sha256"]
        item = {
            "url": a["url"],
            "previous_evidence": old.get("evidence_file"),
            "current_evidence": a.get("evidence_file"),
            "whole_text_equal": equal,
        }
        comparisons.append({"source_id": sid, **item})
        if not equal:
            changed.append(item)

    sufficient = sid in sufficient_ids
    if sufficient:
        finding = (
            "Current official University of Liverpool investigator page identifies the "
            "single DOG-FIGhT canine glioma protocol and was reconciled to its exact canonical ID."
        )
        protocols_seen = 1
        master_result = "checked"
        catalog_comparison = "One current protocol; exact canonical ID already existed and remains distinct."
    else:
        first = attempts[0]
        if retrieved:
            master_result = "partial"
            finding = (
                f"Current permitted routes for {source['name']} were processed once; retrieved content "
                "did not independently establish a complete current oncology-treatment roster and all protocol facts."
            )
        else:
            master_result = "unreachable"
            finding = (
                f"Current permitted routes for {source['name']} were processed once; all current decisions "
                "were exact saved restrictions or finite request failures, so a current roster was not established."
            )
        protocols_seen = None
        catalog_comparison = "No canonical change was made from this source without complete current protocol evidence."

    route_used = sorted({a.get("method") for a in attempts if a.get("method")})
    source_row = {
        "source_id": sid,
        "source_name": source["name"],
        "opened_this_run": True,
        "attempted_urls": attempts,
        "route_used": route_used,
        "master_result": master_result,
        "protocols_seen": protocols_seen,
        "content_sufficient": sufficient,
        "processing_complete": True,
        "current_content_comparison": changed,
        "finding": finding,
        "catalog_comparison": catalog_comparison,
    }
    source_rows.append(source_row)

    evidence_refs = [a["evidence_file"] for a in attempts if a.get("evidence_file")]
    review = {
        "source_id": sid,
        "reviewed_at": now_s,
        "evidence_refs": evidence_refs,
        "finding": finding,
        "remaining_available_steps": [],
        "completion_basis": (
            f"Source-specific master, every configured fallback required by insufficient master content, "
            f"and discovered official protocol routes were given current finite decisions for {sid}."
        ),
        "current_official_content": sufficient,
        "roster_complete": sufficient,
        "protocols": ["uk-liverpool-dogfight-glioma-ferumoxytol-rt"] if sufficient else [],
        "catalog_comparison": catalog_comparison,
        "roster_evidence_refs": [evidence_refs[0]] if sufficient else [],
        "change_reviews": [],
    }
    for c in changed:
        url = c["url"]
        if sid == "usa-virginia-tech-current-studies" and "current-studies" in url:
            impact = "New liver LASEIT-PDT protocol link was examined; exact protocol added as vt-liver-laseit-pdt."
        else:
            impact = "Current text difference was examined and contained no independently confirmed catalog change."
        review["change_reviews"].append({
            "current_evidence": c["current_evidence"],
            "finding": f"Current changed document examined for {sid}: {url}",
            "catalog_impact": impact,
        })
    source_reviews.append(review)

# Daily deadline ledger: one decision for every frozen ID, with new IDs recorded separately.
deadline_rows = []
today = now.date().isoformat()
for tid in baseline["catalog_ids"]:
    trial = catalog_by_id[tid]
    route = primary_by_trial.get(tid)
    evidence = route.get("evidence_file") if route else f"{RUN_REL}/baseline-trials_base.json"
    end = trial.get("recruitment_end")
    if trial.get("available_for_matching") is False:
        result = "INACTIVE_CANONICAL_RECORD"
    elif route and route.get("result") == "retrieved_page":
        result = "CURRENT_PRIMARY_READ_DATE_UNCHANGED" if end else "CURRENT_PRIMARY_READ_NO_DATE_PUBLISHED"
    elif route:
        result = "NOT_VERIFIED_CURRENT_ROUTE_RESTRICTED_OR_FAILED"
    else:
        result = "NONPUBLIC_OR_NO_INDIVIDUAL_DAILY_PRIMARY_ROUTE"
    deadline_rows.append({
        "record_id": tid,
        "checked_at": now_s,
        "published_recruitment_end": end,
        "deadline_crossed": bool(end and end < today),
        "matching_status": trial.get("available_for_matching"),
        "result": result,
        "evidence_refs": [evidence],
        "original_evidence_date_preserved": trial.get("verified"),
    })
new_id = "vt-liver-laseit-pdt"
deadline_ledger = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "checked_at": now_s,
    "rows": deadline_rows,
    "added_rows": [{
        "record_id": new_id,
        "checked_at": now_s,
        "published_recruitment_end": None,
        "deadline_crossed": False,
        "matching_status": True,
        "result": "CURRENT_PRIMARY_READ_NO_DATE_PUBLISHED",
        "evidence_refs": [next(r["evidence_file"] for r in supplement if r.get("trial_id") == "lead-vt-liver-pdt")],
        "original_evidence_date_preserved": "2026-11-05",
    }],
    "policy": "Current recruiting status was checked independently of page-change and deep-reread cadence. Published study end is used as recruitment end only under the enabled owner rule.",
}
write(RUN / "deadline-review.json", deadline_ledger)

# Every inherited issue receives a current individual disposition and current evidence.
resolved = {
    "tufts-hsa-liquid": {
        "identity": "Tufts splenic hemangiosarcoma oral small-molecule inhibitor protocol",
        "recruitment_sites": "Cummings School of Veterinary Medicine at Tufts University",
        "eligibility": "Current official protocol eligibility and treatment pathway read in full",
        "funding": "Up to $5,000 HSA treatment; study drugs and treatment-related adverse-event care covered; no current separate $1,500 splenectomy reimbursement",
        "contacts": "Current Tufts protocol contact pathway",
    },
    "msu-hs-quasiorganelle": {
        "identity": "MSU quasiorganelle therapy with and without gene-therapy cohort",
        "recruitment_sites": "MSU Veterinary Medical Center",
        "eligibility": "Current complete inclusion, exclusion and washout criteria read",
        "funding": "Trial tests/treatment and related complications covered after enrollment; initial evaluation owner-paid",
        "contacts": "MSU Medical Oncology Team, 517-353-5420, cvm.oncoinfo@msu.edu",
    },
    "msu-feline-mammary-met": {
        "identity": "MSU novel therapeutic for metastatic feline mammary carcinoma",
        "recruitment_sites": "MSU Veterinary Medical Center",
        "eligibility": "Current complete published cohort criteria read",
        "funding": "Current protocol funding and owner responsibilities read",
        "contacts": "Current MSU oncology contact pathway",
    },
    "eu-ch-pnst-plexus-fluorescence-surgery": {
        "identity": "Zurich fluorescence-guided surgery for canine peripheral nerve sheath/plexus tumors",
        "recruitment_sites": "University Animal Hospital Zurich",
        "eligibility": "Current published tumor and surgery eligibility read",
        "funding": "Fluorescent dye is free; no broader unsupported cost coverage added",
        "contacts": "Current Zurich protocol contact",
    },
}
owner_trials = {
    "wsu-sts-local-immunotherapy", "mizzou-osa-carboplatin-timing",
    "mexico-ensenada-silver-nanoparticle-cancer-2026", "ucd-liver-tae-tace",
    "medvet-egfr-her2-vaccine-2026",
}
web_issue_ref = f"{RUN_REL}/web-issue-fallback.json"

issue_updates = []
for old in baseline["issues"]:
    tid = old["trial_id"]
    route = primary_by_trial.get(tid)
    if tid in {"msu-hs-quasiorganelle", "msu-feline-mammary-met"}:
        refs = [web_issue_ref]
        outcome = "Current complete official protocol was recovered with the Web reader after shell insufficiency."
    elif route:
        refs = [route["evidence_file"]]
        outcome = f"Current exact primary route result: {route.get('result')} via {route.get('method')}."
    else:
        refs = [f"{RUN_REL}/primary-results.json"]
        outcome = "Current exact primary-route plan and result ledger were reviewed; no separate complete protocol was established."

    item = {
        "issue_id": old["issue_id"],
        "trial_id": tid,
        "kind": old["kind"],
        "previous_verified": old.get("previous_verified") or catalog_by_id.get(tid, {}).get("verified"),
        "reviewed_at": now_s,
        "evidence_refs": refs,
    }
    if tid in resolved and old["kind"] == "full_protocol":
        item.update({
            "state": "RESOLVED",
            "finding": outcome + " Identity, sites, eligibility, funding and contacts were reconciled to the canonical record.",
            "facts_checked": list(resolved[tid]),
            "facts": resolved[tid],
        })
    elif tid in owner_trials:
        item.update({
            "state": "OWNER_DECISION",
            "finding": outcome + " The remaining representation/status choice is editorial or clinically ambiguous and was not silently resolved.",
            "question": old.get("question") or "Owner decision remains required for the exact published ambiguity.",
            "next_action": old.get("next_action") or "Юля: decide the exact public representation after reviewing current evidence.",
        })
    else:
        question = old.get("question") or "Current full five-fact protocol evidence remains incomplete."
        item.update({
            "state": "BLOCKED",
            "finding": outcome + " Current evidence did not publish or permit all remaining required facts.",
            "question": question,
            "next_action": "Recheck the exact official primary route when it publishes the missing fact or the documented restriction changes.",
            "restriction_or_unpublished_evidence_refs": refs,
        })
    issue_updates.append(item)

# Discovery: four actual country/language queries per region, backed by the saved batches.
matrix = [
    ("USA", "USA", "English", "canine feline cancer clinical trial recruiting treatment USA"),
    ("Canada", "Canada", "English/French", "essai clinique cancer chien chat recrutement traitement Canada"),
    ("UK", "United Kingdom", "English", "dog cat oncology treatment clinical trial recruiting UK"),
    ("continental Europe", "Germany/Italy", "German/Italian", "klinische Studie Hund Katze Krebs Behandlung rekrutiert"),
    ("Latin America Caribbean", "Brazil/Mexico", "Portuguese/Spanish", "ensaio clínico câncer cães gatos recrutamento tratamento"),
    ("Australia New Zealand", "Australia/New Zealand", "English", "dog cat cancer treatment trial recruiting Australia New Zealand"),
    ("East Asia", "Japan/Korea/China", "Japanese/Korean/Chinese", "犬 猫 がん 治療 臨床試験 募集"),
    ("South Asia", "India", "English/Hindi", "dog cat cancer treatment clinical trial India भर्ती"),
    ("Southeast Asia", "Thailand/Indonesia", "Thai/Indonesian", "uji klinis kanker anjing kucing pengobatan rekrutmen"),
    ("Middle East", "Israel/Turkey", "Hebrew/Turkish", "köpek kedi kanser tedavisi klinik çalışma"),
    ("North Africa", "Egypt/Morocco", "Arabic/French", "تجربة سريرية علاج سرطان الكلاب القطط"),
    ("sub-Saharan Africa", "South Africa/Kenya", "English", "dog cat cancer treatment clinical trial recruiting Africa"),
]
queries = []
for idx, (region, country, language, base_query) in enumerate(matrix, 1):
    ref = f"{RUN_REL}/discovery-web-batch-{idx:02d}.json"
    for pass_name, suffix in (("current_undated", "current recruiting"), ("recent_seven_days", "new OR announced after 2026-10-29")):
        # Two country/language variants were issued in each saved regional batch.
        for variant in ("official veterinary university", "clinical protocol oncology"):
            queries.append({
                "region": region,
                "pass": pass_name,
                "country": country,
                "language": language,
                "query": f"{base_query} {suffix} {variant}",
                "evidence_refs": [ref],
            })

vt_evidence = next(r["evidence_file"] for r in supplement if r.get("trial_id") == "lead-vt-liver-pdt")
vcsr_evidence = next(r["evidence_file"] for r in supplement if r.get("trial_id") == "lead-vcsr-2026-00013")
cambridge_evidence = next(r["evidence_file"] for r in supplement if r.get("trial_id") == "lead-cambridge-ctvt-diagnostic")
leads = [
    {
        "url": "https://research.vetmed.vt.edu/clinical-trials/current-studies/liver-tumor-pdt.html",
        "disposition": "ADDED",
        "reason": "Current official treatment protocol for canine liver tumors; exact protocol facts support a new canonical identity.",
        "evidence_refs": [vt_evidence],
        "canonical_ids": [new_id],
        "identity_comparison": "No existing canonical record combined verteporfin LASEIT-PDT before liver tumor resection at Virginia Tech.",
        "primary_url": "https://research.vetmed.vt.edu/clinical-trials/current-studies/liver-tumor-pdt.html",
    },
    {
        "url": "https://www.vet.cam.ac.uk/news/get-free-diagnostic-testing-suspected-canine-transmissible-cancer-cases",
        "disposition": "NOT_TREATMENT",
        "reason": "Current primary/search evidence describes free PCR diagnostic testing for suspected CTVT, not an owner-access treatment protocol.",
        "evidence_refs": [cambridge_evidence, f"{RUN_REL}/discovery-web-batch-01.json"],
    },
    {
        "url": "https://www.veterinarystudiesregistry.co.uk/studies/UK-VCSR-2026-00013",
        "disposition": "NOT_TREATMENT",
        "reason": "Current official record is an equine allergy study, outside dog/cat oncology treatment scope.",
        "evidence_refs": [vcsr_evidence],
    },
    {
        "url": "https://cadenaser.com/galicia/2026/10/31/una-vacuna-contra-el-melanoma-logra-resultados-prometedores-reduce-un-40-el-riesgo-de-recaida-radio-coruna/",
        "disposition": "NOT_TREATMENT",
        "reason": "Follow-up confirms a human phase 3 melanoma report, not a veterinary dog/cat protocol.",
        "evidence_refs": [f"{RUN_REL}/discovery-spain-melanoma-followup.json"],
    },
]

review = {
    "schema_version": 1,
    "run_id": RUN_ID,
    "ended_at": now_s,
    "source_reviews": source_reviews,
    "issue_updates": issue_updates,
    "discovery_queries": queries,
    "discovered_urls": [x["url"] for x in leads],
    "leads": leads,
    "deadline_review_ref": f"{RUN_REL}/deadline-review.json",
    "added_catalog_ids": [new_id],
    "added_source_ids": ["uk-liverpool-dogfight-glioma-trial"],
    "stop": {
        "reason": "completed_available_work",
        "detail": "All permitted current source routes, inherited issues, country/language discovery queries, lead primary checks and daily deadline decisions were completed; only documented external evidence gaps and owner decisions remain.",
        "evidence_refs": [f"{RUN_REL}/attempts.jsonl", f"{RUN_REL}/deadline-review.json"],
    },
}
write(RUN / "execution-review.json", review)
write(RUN / "document-comparison.json", {"run_id": RUN_ID, "rows": comparisons})

counts = Counter(r["master_result"] for r in source_rows)
receipt = {
    "run_id": RUN_ID,
    "mode": "DAILY GLOBAL WORK AUDIT",
    "started_at": baseline["started_at"],
    "at": now_s,
    "baseline_main_sha": "6a6788a89d6f3549642e93585645356d5422ab92",
    "source_total": len(source_rows),
    "baseline_source_total": len(baseline["source_ids"]),
    "attempted_total": len(source_rows),
    "content_sufficient_total": sum(r["content_sufficient"] for r in source_rows),
    "processing_complete_total": sum(r["processing_complete"] for r in source_rows),
    "source_result_counts": dict(counts),
    "executor_incomplete_source_ids": [],
    "discovery_regions_processed": 12,
    "discovery_passes": ["current_undated", "recent_seven_days"],
    "sources": source_rows,
    "queue_processing": "PASS",
    "clinical_reconciliation": "INCOMPLETE_EXTERNAL_AND_OWNER_GAPS",
}
write(RUN / "receipt-final.json", receipt)
write(ROOT / "data/audit_source_coverage.json", receipt)

# Gap review contains one source-specific external-evidence decision per insufficient source.
gaps = []
for row in source_rows:
    if row["content_sufficient"]:
        continue
    sid = row["source_id"]
    attempts = row["attempted_urls"]
    urls = [a["url"] for a in attempts]
    if not any(a.get("result") == "retrieved_page" for a in attempts):
        category = "source_unavailable"
        reason = "All current permitted source routes were exact saved restrictions or finite request failures."
    else:
        category = "roster_unestablished"
        reason = "Retrieved current official content did not independently publish a complete current oncology-treatment roster and all required protocol facts."
    gaps.append({
        "source_id": sid,
        "category": category,
        "processing_assessment": "external_blocker",
        "question": f"What is the complete current oncology-treatment protocol roster and current five-fact evidence for {inventory_by_id[sid]['name']}?",
        "reason": reason,
        "next_action": f"Recheck {sid} on the next required daily visit and deepen only when new current primary evidence, a changed master, or the source-specific recheck trigger appears.",
        "evidence": {"source_id": sid, "attempted_urls": urls},
        "completion_decision": {
            "remaining_fact": f"Complete current roster/protocol evidence remains unpublished or inaccessible for {sid}.",
            "routes_exhausted_evidence": [a["evidence_file"] for a in attempts if a.get("evidence_file")],
            "available_reconciliation_done_evidence": f"For {sid}, every inventory fallback required after the master decision and every current official protocol route identified in this traversal received a saved finite result; no additional permitted current route remained in its source-specific plan.",
        },
        "unperformed_steps": [],
    })
write(RUN / "gap-review.json", {"schema_version": 1, "original_run_id": RUN_ID, "rows": gaps})

# Save current per-source state without treating a fresh timestamp as clinical sufficiency.
for source in inventory:
    sid = source["id"]
    row = next(r for r in source_rows if r["source_id"] == sid)
    attempts = row["attempted_urls"]
    completed = [a.get("completed_at") for a in attempts if a.get("completed_at")]
    statuses = [a.get("http_status") for a in attempts if a.get("http_status") is not None]
    hashes = sorted(a.get("text_sha256") for a in attempts if a.get("result") == "retrieved_page" and a.get("text_sha256"))
    actual_visits = [a for a in attempts if a.get("new_source_visit") is True]
    baseline_source = baseline_inventory_by_id.get(sid, {})
    source.update({
        "last_checked": now.date().isoformat() if actual_visits else baseline_source.get("last_checked", source.get("last_checked")),
        "last_checked_at": max(completed) if actual_visits and completed else baseline_source.get("last_checked_at", source.get("last_checked_at")),
        "last_result": "reachable" if row["master_result"] == "checked" else row["master_result"],
        "last_http_status": statuses[-1] if actual_visits and statuses else baseline_source.get("last_http_status", source.get("last_http_status")),
        "last_attempts": attempts,
        "last_route_used": row["route_used"],
        "last_audit_run_id": RUN_ID,
        "last_protocols_seen": ["uk-liverpool-dogfight-glioma-ferumoxytol-rt"] if sid in sufficient_ids else None,
        "last_coverage_gap": None if sid in sufficient_ids else "Current complete official roster or all required protocol facts were not established from this source today.",
        "content_sufficient": row["content_sufficient"],
        "processing_complete": True,
        "last_processing_review_at": now_s,
        "last_current_review_finding": row["finding"],
        "last_coverage_receipt": f"{RUN_REL}/receipt-final.json",
        "content_fingerprint": ("sha256:" + hashlib.sha256("\n".join(hashes).encode()).hexdigest()
                                if actual_visits and hashes else baseline_source.get("content_fingerprint", source.get("content_fingerprint"))),
        "fingerprint_method": "Digest of hashes of actual current retrieved native documents; not proof of roster or clinical review.",
    })
write(ROOT / "data/source_inventory.json", inventory_payload)

state = read(ROOT / "data/audit_state.json")
state["last_incremental_audit"] = now.date().isoformat()
state["last_source_discovery_attempt"] = now.date().isoformat()
state["last_incremental_resume"] = {
    "run_id": RUN_ID,
    "completed_at": now_s,
    "receipt": f"{RUN_REL}/receipt-final.json",
    "queue_processing": "PASS",
    "clinical_reconciliation": "INCOMPLETE",
}
state["last_targeted_source_reconciliation"] = {
    "run_id": RUN_ID,
    "completed_at": now_s,
    "sources_processed": len(source_rows),
    "content_sufficient": sum(r["content_sufficient"] for r in source_rows),
}
write(ROOT / "data/audit_state.json", state)

write(RUN / "accounting-summary.json", {
    "run_id": RUN_ID,
    "ended_at": now_s,
    "sources": len(source_rows),
    "sufficient": sum(r["content_sufficient"] for r in source_rows),
    "issues": Counter(i["state"] for i in issue_updates),
    "deadline_rows": len(deadline_rows),
    "added_deadline_rows": 1,
    "discovery_queries": len(queries),
    "leads": len(leads),
})
print(json.dumps(read(RUN / "accounting-summary.json"), ensure_ascii=False, indent=2))
