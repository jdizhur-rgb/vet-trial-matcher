#!/usr/bin/env python3
"""Build the browser matcher catalog from the canonical current catalog."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seo.center_directory import address_for  # noqa: E402
from seo.catalog_selection import current_public  # noqa: E402


SOURCE = ROOT / "data" / "trials_base.json"
OUTPUT = ROOT / "seo" / "static" / "matcher-preview" / "trials.json"
def looks_like_address(value: str) -> bool:
    return any(char.isdigit() for char in value) and "," in value


def main() -> None:
    rows = json.loads(SOURCE.read_text(encoding="utf-8"))
    old = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else []
    old_by_id = {row["id"]: row for row in old}
    result = []

    for source in current_public(rows):
        row = copy.deepcopy(source)
        previous = old_by_id.get(row["id"], {})
        previous_sites = previous.get("sites", [])

        for site in row.get("sites", []):
            label = str(site.get("label") or "").strip()
            site_name = site.get("name") or site.get("hospital") or ""
            if not site.get("address"):
                if looks_like_address(label):
                    site["address"] = label
                elif looks_like_address(str(site.get("hospital") or "")):
                    site["address"] = site["hospital"]
                else:
                    site["address"] = address_for(site_name)
            cached = next(
                (
                    item
                    for item in previous_sites
                    if (item.get("name") or item.get("hospital")) == site_name
                    and "lat" in item
                    and "lon" in item
                ),
                None,
            )
            if cached:
                site["lat"], site["lon"] = cached["lat"], cached["lon"]
            if not site.get("address"):
                site.pop("address", None)

        if not row.get("sites") and not row.get("address"):
            row["address"] = address_for(row.get("center", ""))
        if not row.get("address"):
            row.pop("address", None)
        row.pop("available_for_matching", None)
        result.append(row)

    treatment = sum(row.get("study_type", "treatment") == "treatment" for row in result)
    access = sum(row.get("study_type") == "other_treatment_access" for row in result)
    assert len(result) == len({row["id"] for row in result})
    assert treatment + access == len(result)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(
        f"MATCHER_DATA_OK total={len(result)} "
        f"treatment={treatment} access={access}"
    )


if __name__ == "__main__":
    main()
