"""Ensure verified Austrian sites survive the actual catalog assembly intact."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
supplemental = json.loads((ROOT / "data/oncology_centers_supplemental.json").read_text())["centers"]
catalog = json.loads((ROOT / "data/oncology_centers.json").read_text())["centers"]
expected = {row["source_id"]: row for row in supplemental if row.get("country") == "Austria"}
actual = {row.get("source_id"): row for row in catalog if row.get("country") == "Austria"}
assert expected.keys() <= actual.keys(), f"Lost Austrian branches: {expected.keys() - actual.keys()}"
for source_id, row in expected.items():
    for field in ("name", "street", "city", "postal_code", "phone", "services", "location_type"):
        assert actual[source_id].get(field) == row.get(field), (source_id, field)
print(f"AUSTRIAN_CARE_IDENTITY_OK {len(expected)} distinct sites; branch addresses, phones and services preserved")
