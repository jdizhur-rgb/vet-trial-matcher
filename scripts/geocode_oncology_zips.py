#!/usr/bin/env python3
"""Build a reproducible ZIP-centroid cache for the oncology-center finder."""
from __future__ import annotations

import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "data" / "acvim_oncology_profiles.json"
OUTPUT = ROOT / "data" / "us_zip_centroids.json"
SEED = ROOT / "data" / "oncology_centers_seed.json"
SUPPLEMENTAL = ROOT / "data" / "oncology_centers_supplemental.json"

# Official-location coordinates used only when the public ZIP API is unavailable.
FALLBACK_COORDINATES = {
    "99645": {"latitude": 61.5997, "longitude": -149.1128, "city": "Palmer", "region": "AK"},
    "58104": {"latitude": 46.8065, "longitude": -96.8561, "city": "Fargo", "region": "ND"},
    "25313": {"latitude": 38.4204, "longitude": -81.7904, "city": "Cross Lanes", "region": "WV"},
    "82604": {"latitude": 42.8269, "longitude": -106.3899, "city": "Casper", "region": "WY"},
    "39762": {"latitude": 33.4560, "longitude": -88.7946, "city": "Mississippi State", "region": "MS"},
    "40243": {"latitude": 38.2445788, "longitude": -85.5412167, "city": "Louisville", "region": "KY"},
    "57105": {"latitude": 43.5149, "longitude": -96.7311, "city": "Sioux Falls", "region": "SD"},
    "96817": {"latitude": 21.3187, "longitude": -157.8717, "city": "Honolulu", "region": "HI"},
    "68127": {"latitude": 41.2048, "longitude": -96.0636, "city": "Omaha", "region": "NE"},
}


def fetch(postal_code: str) -> tuple[str, dict | None]:
    country = "pr" if postal_code.startswith("00") else "us"
    url = f"https://api.zippopotam.us/{country}/{postal_code}"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "VetTrialFinder/1.0 ZIP lookup"})
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
        place = payload["places"][0]
        return postal_code, {
            "latitude": float(place["latitude"]),
            "longitude": float(place["longitude"]),
            "city": place["place name"],
            "region": "PR" if country == "pr" else place["state abbreviation"],
        }
    except Exception:
        return postal_code, None


def main() -> None:
    profiles = json.loads(PROFILES.read_text(encoding="utf-8"))["profiles"]
    postal_codes = sorted({matches[-1] for row in profiles if (matches := re.findall(r"\b(\d{5})(?:-\d{4})?\b", row["address"]))})
    seed = json.loads(SEED.read_text(encoding="utf-8"))["centers"]
    supplemental = json.loads(SUPPLEMENTAL.read_text(encoding="utf-8"))["centers"]
    postal_codes = sorted(set(postal_codes) | {row["postal_code"] for row in supplemental if row.get("postal_code")})
    zips: dict[str, dict] = {
        row["postal_code"]: {
            "latitude": row["latitude"], "longitude": row["longitude"],
            "city": row["city"], "region": row["region"],
        }
        for row in seed
        if row["country"] == "USA" and row["postal_code"] and row["latitude"] is not None and row["longitude"] is not None
    }
    if OUTPUT.exists():
        zips.update(json.loads(OUTPUT.read_text(encoding="utf-8")).get("zips", {}))
    zips.update({postal: value for postal, value in FALLBACK_COORDINATES.items() if postal in postal_codes})
    needed = [postal for postal in postal_codes if postal not in zips]
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(fetch, postal): postal for postal in needed}
        for future in as_completed(futures):
            postal, result = future.result()
            if result:
                zips[postal] = result
    missing = sorted(set(postal_codes) - set(zips))
    assert not missing, missing
    payload = {"retrieved": date.today().isoformat(), "source": "Zippopotam.us", "zips": dict(sorted(zips.items()))}
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"ONCOLOGY_ZIPS_OK zips={len(zips)}")


if __name__ == "__main__":
    main()
