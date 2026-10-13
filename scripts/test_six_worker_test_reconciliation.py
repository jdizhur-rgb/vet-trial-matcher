#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
supp = json.loads((ROOT / "data/oncology_centers_supplemental.json").read_text(encoding="utf-8"))["centers"]
public = json.loads((ROOT / "data/oncology_centers.json").read_text(encoding="utf-8"))["centers"]
inventory = json.loads((ROOT / "data/oncology_care_source_inventory.json").read_text(encoding="utf-8"))["sources"]
tele = (ROOT / "seo/oncology_teleconsultations.py").read_text(encoding="utf-8")


def by_id(rows, key, value):
    found = [row for row in rows if row.get(key) == value]
    assert len(found) == 1, (key, value, len(found))
    return found[0]


new_ids = {
    "bay-state-veterinary-emergency-specialty-services",
    "ottawa-animal-emergency-specialty-hospital",
    "king-animal-hospital",
    "bristol-vet-specialists",
    "hokkaido-university-veterinary-medical-center",
}
for source_id in new_ids:
    source_row = by_id(inventory, "id", source_id)
    source_center = by_id(supp, "source_id", source_id)
    public_center = by_id(public, "source_id", source_id)
    assert source_row["last_checked"] == "2026-10-13"
    assert source_row["content_sufficient"] is True
    assert source_center["coordinates_unknown"] is True
    assert public_center["latitude"] is None and public_center["longitude"] is None

assert by_id(supp, "source_id", "southern-colorado-veterinary-internal-medicine-and-oncology")["services"] == ["Medical oncology", "Chemotherapy"]
assert "SRT" in by_id(supp, "source_id", "colorado-state-university")["services"]
assert "Immunotherapy" in by_id(supp, "source_id", "cornell-university-hospital-for-animals")["services"]
assert by_id(supp, "source_id", "southeast-veterinary-oncology-and-internal-medicine")["phone"] == "904-567-7519"
assert by_id(supp, "source_id", "bluepearl-pet-hospital-framingham")["clinician_review"][-1]["name"] == "Zoe Fautz"
assert "Microsoft Teams" in tele
assert "DVM, DVSc, DACVIM (Oncology); Christopher Pinard" in tele

deferred_domains = {
    "chestergates.org.uk",
    "liverpool.ac.uk",
    "nagoya-gan-center.com",
    "jsamc.jp",
}
published_domains = {row.get("website", "").split("/")[2].removeprefix("www.") for row in supp if "://" in row.get("website", "")}
assert deferred_domains.isdisjoint(published_domains), deferred_domains & published_domains

addresses = [
    (row.get("street", "").casefold(), row.get("city", "").casefold(), row.get("country", "").casefold())
    for row in public
    if row.get("street") and row.get("city")
]
assert len(addresses) == len(set(addresses)), "duplicate normalized physical address"
audit = json.loads((ROOT / "data/oncology_center_audit.json").read_text(encoding="utf-8"))
assert audit["final_location_count"] == len(public)
print(f"SIX_WORKER_TEST_RECONCILIATION_OK centers={len(public)} new={len(new_ids)}")
