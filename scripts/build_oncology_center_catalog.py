#!/usr/bin/env python3
"""Create the public oncology-center catalog from verified seed data and ACVIM profiles."""
from __future__ import annotations

import json
import re
import urllib.parse
from collections import Counter, defaultdict
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "data" / "acvim_oncology_profiles.json"
SEED = ROOT / "data" / "oncology_centers_seed.json"
OUTPUT = ROOT / "data" / "oncology_centers.json"
AUDIT = ROOT / "data" / "oncology_center_audit.json"
ZIP_COORDINATES = ROOT / "data" / "us_zip_centroids.json"
SUPPLEMENTAL = ROOT / "data" / "oncology_centers_supplemental.json"
US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
}

WEBSITE_OVERRIDES = {
    "SAGE Veterinary Centers|Redwood City|CA": "https://www.sagecenters.com/",
    "VCA Sacramento Veterinary Referral Center|Sacramento|CA": "https://vcahospitals.com/",
    "MedVet Silicon Valley|San Jose|CA": "https://www.medvet.com/",
    "Arista Advanced Pet Care Atlanta|Atlanta|GA": "https://aristapetcare.com/",
    "University of Minnesota|St. Paul|MN": "https://vetmed.umn.edu/",
    "Garden State Veterinary Specialists and Veterinary Emergency and Referral Group|BROOKLYN|NY": "https://www.verg-brooklyn.com/",
    "VCA Veterinary Emergency Referral Center of Westbury|Westbury|NY": "https://vcahospitals.com/",
    "Penn Vet Ryan Veterinary Hospital|Philadelphia|PA": "https://www.vet.upenn.edu/veterinary-hospitals/ryan-veterinary-hospital/",
}

STOPWORDS = {
    "and", "the", "inc", "llc", "ltd", "pc", "pllc", "hospital", "hospitals",
    "center", "centers", "centre", "veterinary", "animal", "pet", "specialty",
    "specialists", "services", "service", "medical", "clinic", "emergency",
}
GENERIC_CONSULTANTS = {
    "consultant", "consulting", "malone cancer vet", "pet cancer care consulting",
}
NONCLINICAL_ORGANIZATIONS = {
    "acvim", "ethos discovery", "fidocure", "hickory labradors", "idexx", "idexx laboratories",
    "joyful riches beyond grief", "n a", "self employed", "zoetis",
}
EXCLUDED_PROFILE_IDS = {
    # Ally moved to Lincoln; current official address is in supplemental data.
    "f1f24b52-a6ac-4373-a2eb-1d11a11824da",
    # Research-only/non-clinical affiliations, not patient-facing veterinary hospitals.
    "ffd34787-a279-4dca-a5ce-9600e1710e8e",  # University of Michigan NCRC
    "ed7125ae-ada5-44e2-8349-bef537b5edb3",  # Case Western biomedical research building
    # Stale organization label (Michigan State) attached to a Cornell address.
    "387cb6d0-f06e-499d-b0f4-366980006389",
    # Person/home or corporate mailing addresses, not patient-facing hospitals.
    "b6b3477f-2274-4428-a1b9-90572ffedc3b",  # Lisa G Barber, DVM
    "1bc5fa7c-2d9c-4ed3-bd77-3564e719abd8",  # Southern Veterinary Partners
    # No current patient-facing clinic or official treatment page could be verified.
    "b0c102e7-d4bd-40dc-ac6a-5c14b12c0f2e",  # Peoria Area Veterinary Group Cancer Clinic
    # Replaced below by the current official hospital record.
    "5cec7559-f8c8-4494-8228-3b1b17c68f7c",  # UVC -> The Oncology Service – Richmond
    # Duplicate Oregon State teaching-hospital profile at the same physical campus.
    "706e1ce9-99c9-4db0-b2bc-c933da75fa67",
    # Historical BluePearl Franklin address; the oncology service moved to Brentwood.
    "2ad235b1-8572-4512-bb8e-82237b0c284b",
}


def profile_id(profile: dict) -> str:
    match = re.search(r"[?&]id=([0-9a-f-]+)", profile.get("profile_url", ""), re.IGNORECASE)
    return match.group(1).lower() if match else ""


def norm(value: str) -> str:
    value = value.lower().replace("&", " and ")
    words = re.findall(r"[a-z0-9]+", value)
    return " ".join(x for x in words if x not in STOPWORDS)


def compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def domain(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    except ValueError:
        return ""


def valid_website(url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc.lower().split(":", 1)[0]
        return parsed.scheme in {"http", "https"} and "." in host and "@" not in host and host != "www"
    except ValueError:
        return False


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio() if a and b else 0.0


def address_parts(value: str) -> tuple[str, str, str, str]:
    lines = [" ".join(x.split()) for x in value.splitlines() if x.strip()]
    if not lines:
        return "", "", "", ""
    match = re.search(r"(.+?),\s*([A-Z]{2})(?:\s+(\d{5})(?:-\d{4})?)?$", lines[-1])
    if not match:
        return "", "", "", " ".join(lines)
    city, region, postal = match.group(1).strip(), match.group(2), match.group(3) or ""
    return city, region, postal, " ".join(lines[:-1])


def phone_key(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    return digits[-10:] if len(digits) >= 10 else ""


def street_key(value: str) -> tuple[str, str]:
    cleaned = norm(value)
    numbers = re.findall(r"\d+", cleaned)
    return (numbers[0] if numbers else "", cleaned)


def same_location(a: dict, b: dict) -> bool:
    acity, astate, azip, astreet = address_parts(a["address"])
    bcity, bstate, bzip, bstreet = address_parts(b["address"])
    if not astate or astate != bstate:
        return False
    same_city = bool(acity and acity.casefold() == bcity.casefold())
    ap, bp = phone_key(a["phone"]), phone_key(b["phone"])
    if ap and ap == bp:
        return True
    anumber, anorm = street_key(astreet)
    bnumber, bnorm = street_key(bstreet)
    if anumber and anumber == bnumber and similarity(anorm, bnorm) >= 0.62:
        return True
    if azip and bzip and azip != bzip:
        return bool(same_city and a["organization"] and b["organization"] and similarity(a["organization"], b["organization"]) >= 0.88)
    if a["organization"] and b["organization"] and similarity(a["organization"], b["organization"]) >= 0.78:
        return True
    adomain, bdomain = domain(a["website"]), domain(b["website"])
    if azip and azip == bzip and adomain and adomain == bdomain and similarity(a["organization"], b["organization"]) >= 0.45:
        return True
    return bool(same_city and similarity(a["organization"], b["organization"]) >= 0.88)


def clusters(profiles: list[dict]) -> list[list[dict]]:
    parent = list(range(len(profiles)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left, right = find(left), find(right)
        if left != right:
            parent[right] = left

    by_region: dict[str, list[int]] = defaultdict(list)
    for index, profile in enumerate(profiles):
        by_region[address_parts(profile["address"])[1]].append(index)
    for indices in by_region.values():
        for offset, left in enumerate(indices):
            for right in indices[:offset]:
                if same_location(profiles[left], profiles[right]):
                    union(left, right)
    grouped: dict[int, list[dict]] = defaultdict(list)
    for index, profile in enumerate(profiles):
        grouped[find(index)].append(profile)
    return list(grouped.values())


def choose_name(group: list[dict]) -> str:
    organizations = [x["organization"].strip() for x in group if x["organization"].strip()]
    usable = [x for x in organizations if norm(x) not in GENERIC_CONSULTANTS]
    if usable:
        keys = Counter(norm(x) for x in usable)
        winning = keys.most_common(1)[0][0]
        variants = [x for x in usable if norm(x) == winning]
        return max(variants, key=lambda x: (sum(ch.isalpha() for ch in x), len(x)))
    for profile in group:
        lines = [" ".join(x.split()) for x in profile["address"].splitlines() if x.strip()]
        if len(lines) > 1 and not re.match(r"^\d", lines[0]) and not re.search(r",\s*[A-Z]{2}", lines[0]):
            return lines[0]
    return ""


def choose_profile(group: list[dict], name: str) -> dict:
    def score(profile: dict) -> tuple[int, int, int, int]:
        city, region, postal, street = address_parts(profile["address"])
        return (
            int(bool(profile["website"])),
            int(bool(profile["phone"])),
            int(bool(postal)),
            int(bool(re.search(r"\d", street))),
        )
    return max(group, key=score)


def center_from_group(group: list[dict], organization_sites: dict[str, str], zip_coordinates: dict[str, dict]) -> dict | None:
    name = choose_name(group)
    chosen = choose_profile(group, name)
    city, region, postal, street = address_parts(chosen["address"])
    if not name or not region or not postal or norm(name) in NONCLINICAL_ORGANIZATIONS:
        return None
    if not re.search(r"\d", street):
        return None
    if re.match(r"^p\.?\s*o\.?\s+box\b", street, re.IGNORECASE):
        return None
    if street and similarity(street.split(" ")[0], name) > 0.8:
        street = " ".join(street.split(" ")[1:])
    websites = [x["website"] for x in group if valid_website(x["website"])]
    website = Counter(websites).most_common(1)[0][0] if websites else organization_sites.get(norm(name), chosen["profile_url"])
    phones = [x["phone"] for x in group if x["phone"]]
    phone = Counter(phones).most_common(1)[0][0] if phones else ""
    coordinates = zip_coordinates.get(postal)
    if not coordinates:
        return None
    return {
        "name": name,
        "street": street,
        "city": city,
        "region": region,
        "postal_code": postal,
        "country": "USA",
        "phone": phone,
        "website": website,
        "services": ["Medical oncology"],
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "source": "ACVIM VetSpecialists directory",
        "verification_url": chosen["profile_url"],
        "oncologist_count": len(group),
    }


def center_match(seed: dict, candidate: dict) -> bool:
    if seed["country"] != candidate["country"] or seed["region"] != candidate["region"]:
        return False
    same_zip = bool(seed["postal_code"] and seed["postal_code"] == candidate["postal_code"])
    same_city = bool(seed["city"] and seed["city"].casefold() == candidate["city"].casefold())
    if (
        phone_key(seed.get("phone", ""))
        and phone_key(seed.get("phone", "")) == phone_key(candidate.get("phone", ""))
        and (same_zip or same_city)
    ):
        return True
    if same_zip and seed.get("website") and candidate.get("website"):
        seed_url = seed["website"].lower().rstrip("/")
        candidate_url = candidate["website"].lower().rstrip("/")
        if seed_url == candidate_url:
            return True
    if same_zip and similarity(seed["name"], candidate["name"]) >= 0.48:
        return True
    if same_zip and street_key(seed["street"])[0] and street_key(seed["street"])[0] == street_key(candidate["street"])[0]:
        return True
    if same_city and similarity(seed["name"], candidate["name"]) >= 0.84:
        return True
    if same_city and street_key(seed["street"])[0] and street_key(seed["street"])[0] == street_key(candidate["street"])[0] and similarity(seed["street"], candidate["street"]) >= 0.55:
        return True
    return False


def main() -> None:
    profiles_payload = json.loads(PROFILES.read_text(encoding="utf-8"))
    seed_payload = json.loads(SEED.read_text(encoding="utf-8"))
    supplemental_payload = json.loads(SUPPLEMENTAL.read_text(encoding="utf-8"))
    zip_coordinates = json.loads(ZIP_COORDINATES.read_text(encoding="utf-8"))["zips"]
    site_candidates: dict[str, list[str]] = defaultdict(list)
    for profile in profiles_payload["profiles"]:
        if profile["organization"] and valid_website(profile["website"]):
            parsed = urllib.parse.urlparse(profile["website"])
            if parsed.netloc:
                site_candidates[norm(profile["organization"])].append(f"{parsed.scheme or 'https'}://{parsed.netloc}/")
    organization_sites = {key: Counter(urls).most_common(1)[0][0] for key, urls in site_candidates.items()}
    eligible_profiles = [
        profile for profile in profiles_payload["profiles"]
        if profile_id(profile) not in EXCLUDED_PROFILE_IDS
    ]
    grouped_profiles = clusters(eligible_profiles)
    acvim = [center for group in grouped_profiles if (center := center_from_group(group, organization_sites, zip_coordinates))]
    centers = list(seed_payload["centers"])
    matched = 0
    for candidate in acvim:
        existing = next((x for x in centers if center_match(x, candidate)), None)
        if existing:
            matched += 1
            existing["verification_url"] = candidate["verification_url"]
            existing["oncologist_count"] = max(existing.get("oncologist_count", 0), candidate["oncologist_count"])
            continue
        centers.append(candidate)
    supplemental_added = 0
    supplemental_matched = 0
    for candidate in supplemental_payload["centers"]:
        candidate = dict(candidate)
        coordinates = None
        if candidate.get("latitude") is not None and candidate.get("longitude") is not None:
            coordinates = {
                "latitude": candidate["latitude"],
                "longitude": candidate["longitude"],
            }
        elif candidate["country"] == "USA":
            coordinates = zip_coordinates.get(candidate["postal_code"])
        if not coordinates:
            raise SystemExit(f"Missing coordinates for supplemental center: {candidate['name']}")
        candidate["latitude"] = coordinates["latitude"]
        candidate["longitude"] = coordinates["longitude"]
        existing = next((x for x in centers if center_match(x, candidate)), None)
        if existing:
            supplemental_matched += 1
            existing.update({key: value for key, value in candidate.items() if key not in {"latitude", "longitude"}})
        else:
            supplemental_added += 1
            centers.append(candidate)
    for center in centers:
        override = WEBSITE_OVERRIDES.get(f"{center['name']}|{center['city']}|{center['region']}")
        if override:
            center["website"] = override
    centers.sort(key=lambda x: (x["country"] != "USA", x["region"], x["city"], x["name"]))
    payload = {
        "last_verified": date.today().isoformat(),
        "method": "Verified seed directory merged with unique physical locations in the ACVIM VetSpecialists oncology directory.",
        "centers": centers,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    excluded_groups = []
    for group in grouped_profiles:
        if center_from_group(group, organization_sites, zip_coordinates):
            continue
        excluded_groups.append({
            "profiles": len(group),
            "organizations": sorted({x["organization"] for x in group if x["organization"]}),
            "addresses": sorted({x["address"] for x in group if x["address"]}),
            "reason": "No usable physical US clinic location, excluded organization, or missing ZIP coordinates",
        })
    covered_states = {x["region"] for x in centers if x["country"] == "USA"} & US_STATES
    audit = {
        "generated": date.today().isoformat(),
        "source_profile_count": len(profiles_payload["profiles"]),
        "profile_clusters": len(grouped_profiles),
        "acvim_physical_locations": len(acvim),
        "seed_locations": len(seed_payload["centers"]),
        "seed_acvim_matches": matched,
        "supplemental_locations_reviewed": len(supplemental_payload["centers"]),
        "supplemental_locations_added": supplemental_added,
        "supplemental_locations_matched": supplemental_matched,
        "final_location_count": len(centers),
        "usa_location_count": sum(x["country"] == "USA" for x in centers),
        "usa_regions": sorted({x["region"] for x in centers if x["country"] == "USA"}),
        "usa_states_covered": len(covered_states),
        "usa_states_without_verified_location": sorted(US_STATES - covered_states),
        "excluded_profile_groups": excluded_groups,
    }
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ONCOLOGY_CENTER_CATALOG_OK profiles={len(profiles_payload['profiles'])} acvim_locations={len(acvim)} matched={matched} supplemental_added={supplemental_added} centers={len(centers)}")


if __name__ == "__main__":
    main()
