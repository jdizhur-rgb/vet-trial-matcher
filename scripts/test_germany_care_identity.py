#!/usr/bin/env python3
"""Keep the independently verified Saarwellingen treatment sites distinct."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
centers = json.loads((ROOT / "data/oncology_centers.json").read_text())["centers"]
expected = {
    "de-tierarztpraxis-am-steinhuebel": ("Zum Steinhübel 32", "+49 6838 8659550"),
    "de-joerg-waschbuesch-saarwellingen": ("Schloßstraße 46", "+49 6838 81242"),
}
for source_id, (street, phone) in expected.items():
    matches = [c for c in centers if c.get("source_id") == source_id]
    assert len(matches) == 1, (source_id, len(matches))
    c = matches[0]
    assert c["street"] == street and c["phone"] == phone, source_id
    assert c["postal_code"] == "66793" and c["country"] == "Germany", source_id
    assert {"Chemotherapy", "Surgery"} <= set(c["services"]), source_id
    assert c["latitude"] is None and c["longitude"] is None and c["coordinates_unknown"], source_id
assert "no new clients" in next(c for c in centers if c.get("source_id") == "de-tierarztpraxis-am-steinhuebel")["availability_note"]
assert "mast-cell" in next(c for c in centers if c.get("source_id") == "de-joerg-waschbuesch-saarwellingen")["availability_note"]
print("GERMANY_CARE_IDENTITY_OK two separate Saarwellingen providers; individual access limits preserved")
