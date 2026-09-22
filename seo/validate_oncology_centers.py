#!/usr/bin/env python3
"""Validate the oncology-center source data and generated finder page."""
from __future__ import annotations

import json
import html
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "oncology_centers.json"
PAGE = ROOT / "seo" / "static" / "matcher-preview" / "centers" / "index.html"
PROFILES = ROOT / "data" / "acvim_oncology_profiles.json"
REQUIRED = {
    "name", "street", "city", "region", "postal_code", "country",
    "website", "services", "latitude", "longitude", "source",
}


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    centers = payload["centers"]
    profiles = json.loads(PROFILES.read_text(encoding="utf-8"))
    assert profiles["profile_count"] == 458, profiles["profile_count"]
    assert len(centers) >= 270, len(centers)
    assert payload.get("last_verified"), "last_verified is required"

    identities: set[tuple[str, str]] = set()
    for center in centers:
        missing = REQUIRED - center.keys()
        assert not missing, (center.get("name"), missing)
        identity = (center["name"].casefold(), center["postal_code"].casefold())
        assert identity not in identities, identity
        identities.add(identity)
        assert center["website"].startswith(("https://", "http://")), center["website"]
        parsed = urllib.parse.urlparse(center["website"])
        assert "." in parsed.netloc and "@" not in parsed.netloc and parsed.netloc != "www", center["website"]
        assert center["services"] and all(isinstance(x, str) and x for x in center["services"]), center["name"]
        if center["country"] == "USA":
            assert center["latitude"] is not None and center["longitude"] is not None, center["name"]

    page = PAGE.read_text(encoding="utf-8")
    assert "Find veterinary oncology centers near you" in page
    assert "ZIP code for nearest centers" in page
    assert "All services" in page
    assert "api.zippopotam.us/us/" in page
    assert page.count('<article class="p-card"') == len(centers)
    for center in centers:
        assert html.escape(center["name"]) in page, center["name"]

    forbidden = {"ACVIM", "FidoCure", "IDEXX", "IDEXX Laboratories", "Zoetis", "Self employed", "N/A"}
    assert not ({x["name"] for x in centers} & forbidden)
    states = {x["region"] for x in centers if x["country"] == "USA"}
    assert len(states) >= 43, states
    print(f"ONCOLOGY_CENTERS_OK centers={len(centers)} states={len(states)}")


if __name__ == "__main__":
    main()
