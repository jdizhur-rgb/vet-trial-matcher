from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "catalog_patch_academic_sites_generated.json"


def load_center_directory():
    path = ROOT / "seo" / "center_directory.py"
    spec = importlib.util.spec_from_file_location("center_directory", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def load_catalog():
    base = json.loads((DATA / "trials_base.json").read_text(encoding="utf-8"))
    by_id = {t["id"]: dict(t) for t in base}
    patch_paths = [DATA / "trial_updates.json"] + sorted(DATA.glob("catalog_patch_*.json"))
    patch_paths = [p for p in patch_paths if p.name != OUT.name]
    for p in patch_paths:
        if not p.exists():
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(doc, list):
            # trial_updates.json is a list in this repo
            for tr in doc:
                if tr.get("id"):
                    old = dict(by_id.get(tr["id"], {}))
                    old.update(tr)
                    by_id[tr["id"]] = old
            continue
        for trial_id in doc.get("delete", []):
            by_id.pop(trial_id, None)
        for patch in doc.get("upsert", []):
            trial_id = patch.get("id")
            if not trial_id:
                continue
            old = dict(by_id.get(trial_id, {}))
            for key, value in patch.items():
                if key in {"requires", "excludes"} and isinstance(value, dict):
                    nested = dict(old.get(key, {}))
                    nested.update(value)
                    old[key] = nested
                else:
                    old[key] = value
            by_id[trial_id] = old
    return list(by_id.values())


def is_academic(canonical: str) -> bool:
    s = canonical.lower()
    return any(token in s for token in (
        "university", "college of veterinary medicine", "school of veterinary medicine",
        "nc state", "virginia-maryland college", "ontario veterinary college",
        "johns hopkins"
    ))


def parse_city_region(address: str, country: str, fallback_city: str = "", fallback_region: str = ""):
    if fallback_city and fallback_region:
        return fallback_city, fallback_region

    # US and Canada: final city + state/province before postal code.
    m = re.search(r",\s*([^,]+),\s*([A-Z]{2})\s+[A-Z0-9][A-Z0-9 -]{2,}$", address)
    if m:
        return m.group(1).strip(), m.group(2).strip()

    # UK entries commonly have county/region + postcode + UK.
    if country in {"UK", "United Kingdom"}:
        parts = [x.strip() for x in address.split(",")]
        if len(parts) >= 3:
            city = fallback_city or parts[-3]
            return city, fallback_region or "UK"

    # General international fallback: use catalog city when present, country as region label.
    if fallback_city:
        return fallback_city, fallback_region or country

    return "", ""


def main():
    cd = load_center_directory()
    out = []
    skipped = []

    for tr in load_catalog():
        trial_id = tr.get("id")
        center = str(tr.get("center") or "").strip()
        if not trial_id or not center or tr.get("sites"):
            continue

        try:
            canonical = cd.canonical_name_for(center)
            address = cd.address_for(center)
        except Exception:
            canonical = center
            address = None

        if not canonical or not address or not is_academic(canonical):
            continue

        country = str(tr.get("country") or "USA").strip()
        city, region = parse_city_region(
            address,
            country,
            str(tr.get("city") or "").strip(),
            str(tr.get("state") or "").strip(),
        )
        if not city or not region:
            skipped.append({"id": trial_id, "center": center, "address": address})
            continue

        out.append({
            "id": trial_id,
            "sites": [{
                "hospital": canonical,
                "name": canonical,
                "city": city,
                "state": region,
            }],
            "location_source": "seo/center_directory.py",
        })

    doc = {
        "generated_from": "seo/center_directory.py",
        "purpose": "Expose academic trial geography through the existing Participating sites UI without modifying the Finder page.",
        "upsert": sorted(out, key=lambda x: x["id"]),
        "delete": [],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ACADEMIC_SITES_PATCH {len(out)}")
    if skipped:
        print("ACADEMIC_SITES_SKIPPED", json.dumps(skipped, ensure_ascii=False))


if __name__ == "__main__":
    main()
