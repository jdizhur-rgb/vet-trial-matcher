from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "catalog_patch_academic_sites_generated.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def load_center_directory():
    return load_module(ROOT / "seo" / "center_directory.py", "center_directory")


def load_center_presentation():
    return load_module(ROOT / "seo" / "center_presentation.py", "center_presentation")


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

    m = re.search(r",\s*([^,]+),\s*([A-Z]{2})\s+[A-Z0-9][A-Z0-9 -]{2,}$", address)
    if m:
        return m.group(1).strip(), m.group(2).strip()

    if country in {"UK", "United Kingdom"}:
        parts = [x.strip() for x in address.split(",")]
        if len(parts) >= 3:
            city = fallback_city or parts[-3]
            return city, fallback_region or "UK"

    if fallback_city:
        return fallback_city, fallback_region or country

    return "", ""


def usable_contact(text: str) -> bool:
    text = str(text or "").strip()
    if not text:
        return False
    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text):
        return True
    if re.search(r"(?:\+?\d[\d .()/-]{7,}\d)", text):
        return True
    return False


def contact_score(text: str) -> tuple[int, int]:
    low = text.lower()
    institutional = sum(k in low for k in ("clinical", "trial", "oncology", "hospital", "vet", "research"))
    return institutional, -len(text)


def main():
    cd = load_center_directory()
    cp = load_center_presentation()
    catalog = load_catalog()
    out = []
    skipped = []

    # Reuse a real email/phone already verified elsewhere for the same institution.
    # This lets one good institutional trial-office contact repair sparse cards
    # without manually copying it into every trial record.
    center_contacts = {}
    for tr in catalog:
        center = str(tr.get("center") or "").strip()
        contact = str(tr.get("contacts") or tr.get("contact") or "").strip()
        if not center or not usable_contact(contact):
            continue
        try:
            canonical = cd.canonical_name_for(center) or center
        except Exception:
            canonical = center
        old = center_contacts.get(canonical)
        if old is None or contact_score(contact) > contact_score(old):
            center_contacts[canonical] = contact

    for tr in catalog:
        trial_id = tr.get("id")
        center = str(tr.get("center") or "").strip()
        if not trial_id or not center:
            continue

        try:
            canonical = cd.canonical_name_for(center) or center
            address = cd.address_for(center)
        except Exception:
            canonical = center
            address = None

        patch = {"id": trial_id}
        changed = False

        # Contact cleanup applies to every center, not just universities.
        current_contact = str(tr.get("contacts") or tr.get("contact") or "").strip()
        if not usable_contact(current_contact):
            fallback_contact = cp.contact_for(canonical) or center_contacts.get(canonical)
            if fallback_contact and usable_contact(fallback_contact):
                patch["contacts"] = fallback_contact
                patch["contact_source"] = "verified institution fallback"
                changed = True

        # Geography generation remains conservative: only single-site academic
        # records with no explicit sites get a generated participating-site line.
        if not tr.get("sites") and canonical and address and is_academic(canonical):
            country = str(tr.get("country") or "USA").strip()
            city, region = parse_city_region(
                address,
                country,
                str(tr.get("city") or "").strip(),
                str(tr.get("state") or "").strip(),
            )
            if city and region:
                display_name = cp.display_name_for(canonical)
                patch["sites"] = [{
                    "hospital": f"📍 {display_name}",
                    "name": canonical,
                    "city": city,
                    "state": region,
                }]
                patch["location_source"] = "seo/center_directory.py"
                changed = True
            else:
                skipped.append({"id": trial_id, "center": center, "address": address})

        if changed:
            out.append(patch)

    doc = {
        "generated_from": ["seo/center_directory.py", "seo/center_presentation.py", "effective catalog contacts"],
        "purpose": "Expose academic geography and propagate verified institution contacts across sparse trial cards without modifying trial matching logic.",
        "upsert": sorted(out, key=lambda x: x["id"]),
        "delete": [],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"CENTER_PRESENTATION_PATCH {len(out)}")
    print(f"CENTER_CONTACT_FALLBACKS {len(center_contacts)}")
    if skipped:
        print("ACADEMIC_SITES_SKIPPED", json.dumps(skipped, ensure_ascii=False))


if __name__ == "__main__":
    main()
