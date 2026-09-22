#!/usr/bin/env python3
"""Audit current VCA hospital sitemaps for location-specific oncology services."""
from __future__ import annotations

import concurrent.futures
import html
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path


ROOT_SITEMAP = "https://vcahospitals.com/-/sitemap/sitemap-hospitals.xml"
OUTPUT = Path("/tmp/vca_oncology_scan.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; VetTrialFinder/1.0; research audit)"}


def fetch(url: str) -> tuple[str, str, str]:
    error = ""
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=60) as response:
                return url, response.read().decode("utf-8", "ignore"), ""
        except Exception as exc:  # noqa: BLE001 - audit records every network failure
            error = repr(exc)
            if attempt < 2:
                time.sleep(2 + attempt * 2)
    return url, "", error


def locations(xml: str) -> list[str]:
    return re.findall(r"<loc>(.*?)</loc>", xml, re.IGNORECASE)


def first(pattern: str, page: str) -> str:
    match = re.search(pattern, page, re.IGNORECASE | re.DOTALL)
    return html.unescape(match.group(1)).strip() if match else ""


def address_parts(value: str) -> tuple[str, str, str, str]:
    parts = [x.strip() for x in re.split(r"\s{2,}", value) if x.strip()]
    if len(parts) < 2:
        return "", "", "", ""
    locality = parts[-1]
    match = re.match(r"(.+?)\s+([A-Z]{2})\s+(\d{5})(?:-\d{4})?$", locality)
    if not match:
        return "", "", "", ""
    return " ".join(parts[:-1]), match.group(1), match.group(2), match.group(3)


def services_for(urls: list[str]) -> list[str]:
    values: list[str] = []
    if any(re.search(r"/(?:departments|services/advanced-care)/oncology/?$", x, re.I) for x in urls):
        values.extend(["Medical oncology", "Chemotherapy"])
    if any(re.search(r"/departments/radiation-oncology/?$", x, re.I) for x in urls):
        values.append("Radiation oncology")
    if not values and any(re.search(r"/services/advanced-care/chemotherapy/?$", x, re.I) for x in urls):
        values.append("Chemotherapy")
    return values


def verification_url(urls: list[str]) -> str:
    priorities = (
        r"/(?:departments|services/advanced-care)/oncology/?$",
        r"/departments/radiation-oncology/?$",
        r"/services/advanced-care/chemotherapy/?$",
    )
    for pattern in priorities:
        matches = [x for x in urls if re.search(pattern, x, re.I)]
        if matches:
            return min(matches, key=len)
    return ""


def main() -> None:
    _, root, error = fetch(ROOT_SITEMAP)
    if error:
        raise SystemExit(error)
    state_sitemaps = locations(root)
    all_urls: list[str] = []
    sitemap_errors: list[dict[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for url, body, error in executor.map(fetch, state_sitemaps):
            if error:
                sitemap_errors.append({"url": url, "error": error})
            all_urls.extend(locations(body))

    grouped: dict[str, list[str]] = {}
    for url in all_urls:
        parsed = urllib.parse.urlparse(url)
        parts = [x for x in parsed.path.split("/") if x]
        if not parts:
            continue
        relevant = bool(
            re.search(r"/(?:departments|services/advanced-care)/(?:oncology|radiation-oncology|chemotherapy)/?$", parsed.path, re.I)
        )
        if relevant:
            grouped.setdefault(parts[0], []).append(url)

    targets = [(slug, verification_url(urls), urls) for slug, urls in grouped.items()]
    pages: dict[str, tuple[str, str]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for url, body, error in executor.map(fetch, [x[1] for x in targets]):
            pages[url] = (body, error)

    records: list[dict] = []
    for slug, verify_url, urls in targets:
        page, error = pages[verify_url]
        name = first(r"_hospitalName\s*=\s*'([^']+)'", page)
        raw_address = first(r"_mapAddress\s*=\s*'([^']+)'", page)
        street, city, region, postal_code = address_parts(raw_address)
        latitude = first(r"_lat\s*=\s*'([^']+)'", page)
        longitude = first(r"_lng\s*=\s*'([^']+)'", page)
        phone = first(r'data-phone="([^"]+)"', page)
        records.append({
            "slug": slug,
            "name": name,
            "address": " ".join(raw_address.split()),
            "street": street,
            "city": city,
            "region": region,
            "postal_code": postal_code,
            "phone": phone,
            "latitude": float(latitude) if latitude else None,
            "longitude": float(longitude) if longitude else None,
            "services": services_for(urls),
            "website": f"https://vcahospitals.com/{slug}",
            "verification_url": verify_url,
            "source_urls": sorted(urls),
            "fetch_error": error,
        })

    records.sort(key=lambda x: (x["name"], x["slug"]))
    payload = {
        "audited": date.today().isoformat(),
        "source": ROOT_SITEMAP,
        "state_sitemaps": len(state_sitemaps),
        "sitemap_urls": len(set(all_urls)),
        "sitemap_errors": sitemap_errors,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "VCA_ONCOLOGY_SCAN_OK",
        f"sitemaps={len(state_sitemaps)}",
        f"urls={len(set(all_urls))}",
        f"records={len(records)}",
        f"fetch_errors={sum(bool(x['fetch_error']) for x in records)}",
        f"missing_identity={sum(not x['name'] or not x['street'] or not x['city'] for x in records)}",
        f"output={OUTPUT}",
    )


if __name__ == "__main__":
    main()
