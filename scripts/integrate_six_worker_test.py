#!/usr/bin/env python3
"""Integrate the confirmed output of the 2026-10-12 six-worker care test.

The script is deliberately idempotent and field-scoped. It accepts either the
saved old value or the already-integrated new value and rejects every other
concurrent value.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "research" / "audit-runs" / "six-worker-test-publish-20261012"
SUPPLEMENTAL = ROOT / "data" / "oncology_centers_supplemental.json"
INVENTORY = ROOT / "data" / "oncology_care_source_inventory.json"
TELE = ROOT / "seo" / "oncology_teleconsultations.py"
RUN_ID = "six-worker-test-publish-20261012"
REVIEW_DATE = "2026-10-13"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


supplemental = read_json(SUPPLEMENTAL)
inventory = read_json(INVENTORY)
centers = supplemental["centers"]
sources = inventory["sources"]
applied: list[dict] = []
already_applied: list[dict] = []
deferred: list[dict] = []


def one_record(target_file: str, source_id: str) -> dict:
    rows = sources if target_file.endswith("oncology_care_source_inventory.json") else centers
    key = "id" if rows is sources else "source_id"
    matches = [row for row in rows if row.get(key) == source_id]
    if len(matches) != 1:
        raise AssertionError((target_file, source_id, len(matches)))
    return matches[0]


def apply_change(change: dict) -> None:
    source_id = change["source_id"]
    field = change["field"]
    if source_id == "medvet-new-orleans" and field == "sponsor_listed_treatment_access":
        deferred.append({
            "source_id": source_id,
            "field": field,
            "reason": "Sponsor listing is verified, but hospital-confirmed active booking and treatment delivery are not established. Preserve it in the audit receipt, not as a public service fact or new canonical field.",
        })
        return
    record = one_record(change["target_file"], source_id)
    current = record.get(field)
    if current == change["new_value"]:
        already_applied.append({"source_id": source_id, "field": field})
        return
    if current != change.get("old_value"):
        raise AssertionError({
            "source_id": source_id,
            "field": field,
            "expected_old": change.get("old_value"),
            "current": current,
        })
    record[field] = change["new_value"]
    applied.append({"source_id": source_id, "field": field})


for worker in (1, 2, 3, 4):
    payload = read_json(RUN / f"worker{worker}-proposed_changes.json")
    changes = payload["changes"] if isinstance(payload, dict) else payload
    for change in changes:
        if change["target_file"] == "seo/oncology_teleconsultations.py":
            continue
        apply_change(change)


tele_text = TELE.read_text(encoding="utf-8")
tele_replacements = [
    (
        "DVM, DACVIM (Oncology); founder and lead oncologist. Team also includes Mia Livaccari. Assigned virtual clinician is not specified.",
        "DVM, DVSc, DACVIM (Oncology); Christopher Pinard is founder and lead oncologist. Team also includes Mia Livaccari, DVM, MS, DACVIM (Oncology), confirmed in the current official clinic biography. Assigned virtual clinician is not specified.",
        "tele-12",
        "tele_tuple[4]",
    ),
    (
        "Referral from veterinarian; initial 45-minute remote conversation from home before travel or procedures.",
        "Referral from veterinarian; initial 45-minute remote conversation from home before travel or procedures. A scheduled Microsoft Teams link is sent for joining from phone or computer. The team provides recommended diagnostics and an estimate for services. Contact info@torontoacc.com or 416-627-8222 for booking; consultation fee, assigned clinician and eligible jurisdictions remain for confirmation.",
        "tele-12",
        "tele_tuple[7]",
    ),
]
for old, new, source_id, field in tele_replacements:
    if new in tele_text:
        already_applied.append({"source_id": source_id, "field": field})
    else:
        count = tele_text.count(old)
        if count != 1:
            raise AssertionError((source_id, field, "old value occurrences", count))
        tele_text = tele_text.replace(old, new)
        applied.append({"source_id": source_id, "field": field})
TELE.write_text(tele_text, encoding="utf-8")


def evidence_urls(worker: int, evidence_ids: list[str]) -> list[str]:
    payload = read_json(RUN / f"worker{worker}-evidence.json")
    if worker == 5:
        rows = payload["sources"]
    elif worker == 6:
        rows = payload
    else:
        raise AssertionError(worker)
    by_id = {row["evidence_id"]: row for row in rows}
    urls: list[str] = []
    for evidence_id in evidence_ids:
        row = by_id[evidence_id]
        url = row.get("official_url") or row.get("evidence_url") or row.get("url")
        if url and url not in urls:
            urls.append(url)
    return urls


selected_new: list[tuple[int, dict, str]] = []
worker5 = read_json(RUN / "worker5-proposed_changes.json")
for change in worker5["changes"]:
    selected_new.append((5, change, {
        "MA-Bay-State-Swansea": "bay-state-veterinary-emergency-specialty-services",
        "ON-Ottawa-OAESH": "ottawa-animal-emergency-specialty-hospital",
        "ON-King-Animal-Hospital": "king-animal-hospital",
    }[change["candidate_key"]]))

worker6 = read_json(RUN / "worker6-proposed_changes.json")
selected_worker6 = {
    "Bristol Vet Specialists": "bristol-vet-specialists",
    "Hokkaido University Veterinary Medical Center / 北海道大学動物医療センター": "hokkaido-university-veterinary-medical-center",
}
for change in worker6:
    if change["candidate_name"] in selected_worker6:
        selected_new.append((6, change, selected_worker6[change["candidate_name"]]))
    else:
        deferred.append({
            "candidate": change["candidate_name"],
            "reason": "Worker result marks core_fields_sufficient=false; keep the specific unanswered question in the saved proposal/result instead of publishing a partial clinic record.",
        })


new_inventory_meta = {
    "bay-state-veterinary-emergency-specialty-services": ("https://www.bsvess.com/oncology/", None),
    "ottawa-animal-emergency-specialty-hospital": ("https://oaesh.com/specialty-services/oncology/", None),
    "king-animal-hospital": ("https://www.kinganimalhospital.com/oncology/", None),
    "bristol-vet-specialists": ("https://www.bristolvetspecialists.co.uk/services/oncology/", "2026-10-13T02:51:43.119819+00:00"),
    "hokkaido-university-veterinary-medical-center": ("https://www.vetmed.hokudai.ac.jp/VMTH/department/oncology/", "2026-10-13T02:51:54.444404+00:00"),
}


def normalize_new_center(worker: int, change: dict, source_id: str) -> tuple[dict, list[str]]:
    value = dict(change["new_value"])
    if source_id == "king-animal-hospital" and value["phone"] == "1-888-622-7345":
        # The public validator stores North American numbers as ten digits;
        # dropping the domestic trunk prefix does not change the destination.
        value["phone"] = "888-622-7345"
    evidence_ids = change["supporting_evidence_ids"]
    urls = evidence_urls(worker, evidence_ids)
    center = {
        "name": value["name"],
        "street": value["street"],
        "city": value["city"],
        "region": value["region"],
        "postal_code": value["postal_code"],
        "country": value["country"],
        "phone": value["phone"],
        "website": value["website"],
        "services": value["services"],
        "latitude": None,
        "longitude": None,
        "coordinates_unknown": True,
        "coordinate_source": "Exact branch coordinates were not established in this bounded test; omitted from distance ranking",
        "source": f"Official branch service/team/contact review; {RUN_ID}",
        "verification_url": value.get("verification_url") or change["evidence_url"],
        "source_id": source_id,
        "last_verified": REVIEW_DATE,
        "supporting_urls": urls,
        "review_reference": f"research/audit-runs/{RUN_ID}/integration.json",
        "review_status": "complete",
        "review_questions": [],
    }
    if "availability_note" in value:
        center["availability_note"] = value["availability_note"]
    if "access" in value:
        center["access_note"] = value["access"]
    if "clinician_review" in value:
        center["clinician_review"] = value["clinician_review"]
    if "clinicians" in value:
        center["oncology_clinicians"] = value["clinicians"]
    return center, urls


def normalized_domain(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


for worker, change, source_id in selected_new:
    intended, urls = normalize_new_center(worker, change, source_id)
    matches = [row for row in centers if row.get("source_id") == source_id]
    if matches:
        if source_id == "king-animal-hospital" and matches[0].get("phone") == "1-888-622-7345":
            matches[0]["phone"] = intended["phone"]
        if matches != [intended]:
            raise AssertionError((source_id, "existing center differs", matches[0], intended))
        already_applied.append({"source_id": source_id, "field": "new_center"})
    else:
        domain = normalized_domain(intended["website"])
        collisions = [row for row in centers if normalized_domain(row.get("website", "")) == domain]
        if collisions:
            raise AssertionError((source_id, "domain collision", [x.get("source_id") for x in collisions]))
        address_collisions = [
            row for row in centers
            if (row.get("street", "").casefold(), row.get("city", "").casefold(), row.get("country", "").casefold())
            == (intended["street"].casefold(), intended["city"].casefold(), intended["country"].casefold())
        ]
        if address_collisions:
            raise AssertionError((source_id, "address collision", [x.get("source_id") for x in address_collisions]))
        centers.append(intended)
        applied.append({"source_id": source_id, "field": "new_center"})

    master_url, exact_checked_at = new_inventory_meta[source_id]
    source_record = {
        "id": source_id,
        "name": intended["name"],
        "source_type": "center",
        "master_url": master_url,
        "supporting_urls": [url for url in urls if url != master_url],
        "required_cadence": "weekly",
        "last_checked": REVIEW_DATE,
        "last_result": "success",
        "working_url": master_url,
        "content_sufficient": True,
        "last_run_id": RUN_ID,
        "last_review_run_id": RUN_ID,
        "last_review_note": "New physical oncology-care location verified from current official branch, service, team/contact and access sources; publication is limited to the confirmed fields in the saved worker evidence.",
        "needs_recheck": False,
        "review_questions": [],
    }
    if exact_checked_at:
        source_record["last_checked_at"] = exact_checked_at
        source_record["last_reviewed_at"] = exact_checked_at
        if worker == 6:
            evidence_payload = read_json(RUN / "worker6-evidence.json")
            master_evidence = next(x for x in evidence_payload if x["official_url"] == master_url)
            source_record["http_status"] = master_evidence["shell_http_status"]
            source_record["fingerprint_sha256"] = master_evidence["normalized_text_sha256"]
            source_record["fingerprint_method"] = "sha256-visible-text"
    existing_sources = [row for row in sources if row.get("id") == source_id]
    if existing_sources:
        if existing_sources != [source_record]:
            raise AssertionError((source_id, "existing source differs", existing_sources[0], source_record))
    else:
        source_domain_collisions = [
            row for row in sources
            if normalized_domain(row.get("master_url", "")) == normalized_domain(master_url)
        ]
        if source_domain_collisions:
            raise AssertionError((source_id, "inventory domain collision", [x.get("id") for x in source_domain_collisions]))
        sources.append(source_record)


exact_attempts = {
    "southeast-veterinary-oncology-and-internal-medicine": "2026-10-13T02:47:25.828903+00:00",
    "southeast-veterinary-oncology-and-internal-medicine-b729ffc6": "2026-10-13T02:47:25.829274+00:00",
    "southern-colorado-veterinary-internal-medicine-and-oncology": "2026-10-13T02:47:25.837867+00:00",
    "summit-veterinary-referral-center": "2026-10-13T02:47:33.727003+00:00",
    "gulf-coast-veterinary-specialists": "2026-10-13T02:46:10.568174+00:00",
    "colorado-animal-specialty-emergency-case": "2026-10-13T02:46:14.600052+00:00",
    "medvet-new-orleans": "2026-10-13T02:46:19.400848+00:00",
    "mash": "2026-10-13T02:46:21.501468+00:00",
    "carolina-veterinary-specialists": "2026-10-13T02:46:23.466951+00:00",
}


def later(left: str | None, right: str) -> bool:
    if not left:
        return True
    try:
        return datetime.fromisoformat(right) > datetime.fromisoformat(left)
    except ValueError:
        return False


reviewed_existing = 0
for worker in (1, 2, 3, 4):
    result = read_json(RUN / f"worker{worker}-result.json")
    for reviewed in result["records"]:
        source_id = reviewed["source_id"]
        source = one_record("data/oncology_care_source_inventory.json", source_id)
        if source.get("last_checked", "") <= REVIEW_DATE:
            source["last_checked"] = REVIEW_DATE
        exact = exact_attempts.get(source_id)
        if exact and later(source.get("last_checked_at"), exact):
            source["last_checked_at"] = exact
            source["last_reviewed_at"] = exact
        source["last_result"] = "success" if reviewed["fully_verified"] else "partial"
        source["content_sufficient"] = bool(reviewed["fully_verified"])
        source["last_run_id"] = RUN_ID
        source["last_review_run_id"] = RUN_ID
        questions = reviewed.get("unanswered_questions") or []
        source["review_questions"] = questions
        source["needs_recheck"] = bool(questions)
        decision = reviewed.get("decision") or reviewed.get("processing_assessment")
        source["last_review_note"] = decision or "Limited test reviewed current operation, branch identity, contact, clinicians/credentials, local services and access; unresolved count or assignment questions are preserved separately."
        reviewed_existing += 1


supplemental["last_verified"] = REVIEW_DATE
write_json(SUPPLEMENTAL, supplemental)
write_json(INVENTORY, inventory)

integration = {
    "run_id": RUN_ID,
    "research_baseline_sha": read_json(RUN / "setup.json")["baseline_sha"],
    "integration_baseline_sha": "fc7df09def2635289c637911f80258bbb5d5ba22",
    "all_six_workers_finished": True,
    "worker_result_validation": (
        "PASS"
        if not read_json(RUN / "validation.json")["errors"]
        and all(row["status"] == "PASS" for row in read_json(RUN / "validation.json")["workers"].values())
        else "FAIL"
    ),
    "existing_records_reviewed": reviewed_existing,
    "field_changes_applied": applied,
    "field_changes_already_present": already_applied,
    "integrated_change_count": len(applied) + len(already_applied),
    "new_centers_selected": [source_id for _, _, source_id in selected_new],
    "new_centers_selected_count": len(selected_new),
    "deferred": deferred,
    "source_date_policy": "Exact shell timestamps were applied only when saved. Date-only Web reviews advance last_checked without inventing last_checked_at; existing exact timestamps are preserved.",
    "publication_status": "pending",
}
write_json(RUN / "integration.json", integration)
print(json.dumps({
    "applied": len(applied),
    "already_applied": len(already_applied),
    "reviewed_existing": reviewed_existing,
    "new_centers": len(selected_new),
    "deferred": len(deferred),
}, sort_keys=True))
