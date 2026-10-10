#!/usr/bin/env python3
"""Validate receipts for discovery-FIRST weekly oncology care audits.

This is a structural evidence gate, not a claim that a search happened.
Every area and network needs run-local evidence; do not manufacture receipts.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

US_AREAS = set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VA VT WA WV WI WY DC PR".split())
GLOBAL_REGIONS = set("Canada UK Continental_Europe Latin_America_Caribbean Australia_New_Zealand Japan East_Asia_non_Japan South_Asia Southeast_Asia Middle_East North_Africa Sub_Saharan_Africa".split())
NETWORKS = set("PetCure BluePearl VCA Ethos MedVet_WestVet Thrive_VCG Universities".split())
SIGNALS = {"fresh", "current_undated"}
CATEGORIES = {"new_center", "new_service", "new_specialist", "new_teleconsult", "update", "duplicate", "rejected", "unresolved"}


def timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
        return parsed if parsed.tzinfo and parsed.utcoffset() is not None else None
    except ValueError:
        return None


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(payload: dict) -> tuple[list[str], list[str]]:
    """Return (invalid evidence problems, incomplete coverage reasons)."""
    invalid: list[str] = []
    missing: list[str] = []
    if payload.get("schema_version") != 1 or not nonempty(payload.get("run_id")):
        invalid.append("schema_version=1 and nonempty run_id required")
    start, end = timestamp(payload.get("started_at")), timestamp(payload.get("ended_at"))
    if not start or not end or start > end:
        invalid.append("valid timezone-aware started_at <= ended_at required")

    def check_searches(item: dict, name: str) -> None:
        searches = item.get("searches")
        if not isinstance(searches, list):
            invalid.append(f"{name}: searches must be an array")
            return
        types = set()
        for search in searches:
            if not isinstance(search, dict):
                invalid.append(f"{name}: non-object search")
                continue
            kind = search.get("signal")
            if kind not in SIGNALS:
                invalid.append(f"{name}: invalid search signal {kind!r}")
                continue
            types.add(kind)
            if not all(nonempty(search.get(field)) for field in ("query", "language", "method")):
                invalid.append(f"{name}: every search needs actual query, language, method")
            at = timestamp(search.get("attempted_at"))
            if not at or (start and end and not start <= at <= end):
                invalid.append(f"{name}: search has no current-run timestamp")
            if not isinstance(search.get("results_reviewed"), int) or search["results_reviewed"] < 0:
                invalid.append(f"{name}: results_reviewed must be a nonnegative integer")
            if not isinstance(search.get("result_urls"), list):
                invalid.append(f"{name}: result_urls array required (may be empty if zero hits)")
            elif not all(isinstance(url, str) and url.startswith("https://") for url in search["result_urls"]):
                invalid.append(f"{name}: result URLs must be HTTPS links")
        if types != SIGNALS:
            missing.append(f"{name}: missing fresh/current_undated independent searches")

    def check_areas(field: str, required: set[str], key: str) -> None:
        rows = payload.get(field)
        if not isinstance(rows, list):
            invalid.append(f"{field}: required array")
            return
        by_id: dict[str, dict] = {}
        for row in rows:
            if not isinstance(row, dict) or not nonempty(row.get(key)):
                invalid.append(f"{field}: malformed area")
                continue
            k = row[key]
            if k in by_id:
                invalid.append(f"{field}: duplicate {k}")
            by_id[k] = row
        for area in sorted(required - by_id.keys()):
            missing.append(f"{field}: NOT SEARCHED {area}")
        for area, row in by_id.items():
            if area not in required:
                invalid.append(f"{field}: unknown {area}")
            if row.get("status") not in ("complete", "partial", "not_checked"):
                invalid.append(f"{field} {area}: invalid status")
            if row.get("status") != "complete":
                missing.append(f"{field} {area}: {row.get('status')}")
            check_searches(row, f"{field} {area}")
            if field == "global_regions" and area in {"Japan", "Canada", "Latin_America_Caribbean"}:
                languages = {q.get("language","").casefold() for q in row.get("searches",[]) if isinstance(q,dict)}
                needed = {"Japan": {"ja", "japanese"}, "Canada": {"fr", "french"}, "Latin_America_Caribbean": {"es", "spanish", "pt", "portuguese"}}[area]
                if not languages.intersection(needed):
                    missing.append(f"{area}: mandatory native-language searches absent")

    check_areas("us_areas", US_AREAS, "area")
    check_areas("global_regions", GLOBAL_REGIONS, "region")

    rows = payload.get("network_traversals")
    if not isinstance(rows, list):
        invalid.append("network_traversals: array required")
    else:
        by_id: dict[str, dict] = {}
        for item in rows:
            if not isinstance(item, dict) or not nonempty(item.get("network")):
                invalid.append("network_traversals: malformed row")
                continue
            name = item["network"]
            if name in by_id:
                invalid.append(f"network_traversals: duplicate {name}")
            by_id[name] = item
        for name in sorted(NETWORKS - by_id.keys()):
            missing.append(f"network_traversals: NOT CHECKED {name}")
        for name, row in by_id.items():
            if name not in NETWORKS:
                invalid.append(f"network_traversals: unknown {name}")
            visits = row.get("attempts")
            if not isinstance(visits, list) or not visits:
                missing.append(f"network {name}: no actual URL attempts")
            else:
                for visit in visits:
                    if not isinstance(visit, dict) or not str(visit.get("url","")).startswith("https://"):
                        invalid.append(f"network {name}: missing official HTTPS URL")
                        continue
                    at = timestamp(visit.get("attempted_at"))
                    if not at or (start and end and not start <= at <= end):
                        invalid.append(f"network {name}: URL attempt outside current run")
                    if visit.get("outcome") not in {"success", "partial", "unreachable"}:
                        invalid.append(f"network {name}: invalid URL outcome")
            if row.get("status") not in ("complete", "partial", "unreachable", "not_checked"):
                invalid.append(f"network {name}: invalid status")
            if row.get("status") != "complete":
                missing.append(f"network {name}: roster/branches incomplete")
            counts = ("roster_locations", "candidate_oncology_locations", "branch_pages_checked", "confirmed_oncology", "unresolved_locations")
            if not all(isinstance(row.get(key),int) and row[key]>=0 for key in counts):
                missing.append(f"network {name}: missing numerical roster/branch counts")
            if row.get("master_sufficient") is False and len(row.get("attempts",[])) < 2:
                missing.append(f"network {name}: incomplete master without official fallback attempts")
            if name == "VCA" and not row.get("state_sitemaps_checked"):
                missing.append("VCA: no state-sitemap traversal evidence")
            if name == "Ethos" and not row.get("brands_checked"):
                missing.append("Ethos: no brand-by-brand traversal evidence")

    candidates = payload.get("candidates")
    if not isinstance(candidates, list):
        invalid.append("candidates must be an array, including [] for zero results")
    else:
        seen = set()
        for item in candidates:
            if not isinstance(item, dict) or not all(nonempty(item.get(field)) for field in ("id","name","official_url","classification")):
                invalid.append("candidate missing id/name/official_url/classification")
                continue
            if item["id"] in seen:
                invalid.append(f"duplicate candidate id {item['id']}")
            seen.add(item["id"])
            if item["classification"] not in CATEGORIES:
                invalid.append(f"candidate {item['id']}: bad classification")
            if not item["official_url"].startswith("https://"):
                invalid.append(f"candidate {item['id']}: official_url must be HTTPS")
            if item["classification"] in {"new_center","new_service","new_specialist","new_teleconsult"}:
                if not nonempty(item.get("verified_official_service_page")):
                    missing.append(f"candidate {item['id']}: no verified primary service page")
                if item.get("canonical_reconciled") is not True:
                    missing.append(f"candidate {item['id']}: not reconciled against full catalog")

    return invalid, missing


def test() -> None:
    start="2026-10-10T01:00:00-04:00"
    search=lambda lang: [{"signal":x,"query":f"actual oncology {x}","language":lang,"method":"web","attempted_at":start,"results_reviewed":0,"result_urls":[]} for x in ("fresh","current_undated")]
    p={"schema_version":1,"run_id":"test-current-run","started_at":start,"ended_at":"2026-10-10T03:00:00-04:00",
       "us_areas":[{"area":x,"status":"complete","searches":search("en")} for x in US_AREAS],
       "global_regions":[{"region":x,"status":"complete","searches":search({"Japan":"ja","Canada":"fr","Latin_America_Caribbean":"es"}.get(x,"en"))} for x in GLOBAL_REGIONS],
       "network_traversals":[{"network":x,"status":"complete","master_sufficient":True,"attempts":[{"url":"https://example.org/current","attempted_at":start,"outcome":"success"}],"roster_locations":0,"candidate_oncology_locations":0,"branch_pages_checked":0,"confirmed_oncology":0,"unresolved_locations":0,"state_sitemaps_checked":x=="VCA","brands_checked":x=="Ethos"} for x in NETWORKS],
       "candidates":[]}
    assert validate(p) == ([],[]), validate(p)
    p["us_areas"].pop()
    assert any("NOT SEARCHED" in x for x in validate(p)[1])
    p["us_areas"].append({"area":"DC","status":"complete","searches":search("en")})
    p["network_traversals"][0]["master_sufficient"]=False
    assert any("fallback" in x for x in validate(p)[1])
    print("weekly care discovery self-tests PASS")


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--receipt",type=Path,help="Actual run's care-discovery-receipt.json")
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        test()
        return 0
    if not args.receipt:
        parser.error("--receipt is required except for --self-test")
    if not args.receipt.exists():
        print(f"INCOMPLETE: missing real discovery receipt: {args.receipt}")
        return 2
    payload=json.loads(args.receipt.read_text(encoding="utf-8"))
    invalid, missing=validate(payload)
    print(f"CARE_DISCOVERY {'INVALID' if invalid else 'INCOMPLETE' if missing else 'PASS'}: {len(invalid)} invalid, {len(missing)} gaps")
    for message in (invalid+missing)[:200]:
        print(" -",message)
    return 1 if invalid else 2 if missing else 0


if __name__=="__main__":
    sys.exit(main())
