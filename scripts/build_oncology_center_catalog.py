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
    "SAGE Veterinary Centers|Redwood City|CA": "https://www.sagecenters.com/locations/redwood-city",
    "VCA Sacramento Veterinary Referral Center|Sacramento|CA": "https://vcahospitals.com/sacramento-veterinary-referral-center",
    "MedVet Silicon Valley|San Jose|CA": "https://www.medvet.com/",
    "Arista Advanced Pet Care Atlanta|Atlanta|GA": "https://aristapetcare.com/arista-locations/atlanta/",
    "University of Minnesota|St. Paul|MN": "https://vetmed.umn.edu/",
    "Garden State Veterinary Specialists and Veterinary Emergency and Referral Group|BROOKLYN|NY": "https://www.verg-brooklyn.com/",
    "VCA Veterinary Emergency Referral Center of Westbury|Westbury|NY": "https://vcahospitals.com/westbury",
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
    '06d195d2-0f7d-4157-89bf-c95f7fa2bdb5',  # e-packages-publish-20261012 superseded physical representation
    '1140042b-e301-49b2-bcb5-6cec82018ee5',  # e-packages-publish-20261012 superseded physical representation
    '12980c2e-b8d4-4657-a9be-bf672fc18c4e',  # e-packages-publish-20261012 superseded physical representation
    '19d436bf-c1e3-4b08-a774-aa0f67c27aca',  # e-packages-publish-20261012 superseded physical representation
    '1d44eada-3f74-43bc-810e-d278d1fb4e6e',  # e-packages-publish-20261012 superseded physical representation
    '266ed978-5285-4ff4-802c-164899cd86ac',  # e-packages-publish-20261012 superseded physical representation
    '35abd136-bcc7-4efd-be0d-8a8555182242',  # e-packages-publish-20261012 superseded physical representation
    '379cf4d2-477a-42dc-a87b-b3486de73f87',  # e-packages-publish-20261012 superseded physical representation
    '3d8e94c4-9bca-4e01-be85-59ef5e29df68',  # e-packages-publish-20261012 superseded physical representation
    '402d8a74-d685-450b-8efa-1e52851c4fb6',  # e-packages-publish-20261012 superseded physical representation
    '45f1d548-057b-408d-9ce8-b27868c71a11',  # e-packages-publish-20261012 superseded physical representation
    '518f3582-6526-48ff-8a50-1bb2020b541b',  # e-packages-publish-20261012 superseded physical representation
    '62bccb00-ab1c-447d-a223-74b8248556a1',  # e-packages-publish-20261012 superseded physical representation
    '6c01d834-8ec3-4152-a016-bb28daca2bb5',  # e-packages-publish-20261012 superseded physical representation
    '74e0bb52-3bbc-433d-8663-78fc9702b24a',  # e-packages-publish-20261012 superseded physical representation
    '81dc9b39-0b84-4b5f-9683-8bce785882f4',  # e-packages-publish-20261012 superseded physical representation
    '8eec7a25-d264-4aa5-a055-d72bb59436d9',  # e-packages-publish-20261012 superseded physical representation
    '98b70ab7-da05-4c49-bb63-987b65edc773',  # e-packages-publish-20261012 superseded physical representation
    'a36e569f-9dac-49a5-8c08-0ad3a8eaa24f',  # e-packages-publish-20261012 superseded physical representation
    'ad968a04-dba9-4e4e-9061-7637e8be3143',  # e-packages-publish-20261012 superseded physical representation
    'b38ae74a-4dee-4a24-805d-bd918c9c6328',  # e-packages-publish-20261012 superseded physical representation
    'b69b4dc5-1ee0-4833-96c9-d661cfb761aa',  # e-packages-publish-20261012 superseded physical representation
    'c46de335-7d83-48a1-8fc0-f69e0f7f1ada',  # e-packages-publish-20261012 superseded physical representation
    'ce6711a0-173b-4906-8de7-6d853f9c1318',  # e-packages-publish-20261012 superseded physical representation
    'da218912-28fc-46b1-bc5c-0487321580ac',  # e-packages-publish-20261012 superseded physical representation
    'e56bdb65-4bbd-4db1-98b5-5806f9bb2704',  # e-packages-publish-20261012 superseded physical representation
    'f07d39e1-f447-4e20-be06-3765e95e61d4',  # e-packages-publish-20261012 superseded physical representation
    'f2cbca2c-99f2-4472-9bfb-1b4d806ccf83',  # e-packages-publish-20261012 superseded physical representation
    'f68269d3-3433-4012-a41a-d87888e37593',  # e-packages-publish-20261012 superseded physical representation
    # C04: Jessica Chin's imported CT profile has another branch's NY address.
    # Keep raw history; current Norwalk service is retained in supplemental.
    "1973c738-08aa-4f6a-8af0-76b95e9677c5",
    # B02: Greenbrier/Chesapeake reception moved to Town Center Virginia Beach.
    # Keep the raw Brewer profile as history; supplemental retains current care.
    "23c8fa8f-68ba-4cad-a686-2c872c371136",
    # C01: current Holly Avenue/87122 site is retained in supplemental.
    # Preserve the raw old Montgomery and wrong-ZIP Holly profiles as history.
    "bf7bb6ec-d5f5-4049-9216-89f536f7b17d",
    "563a9e4c-d9fe-49a9-a10a-0667ad60b958",
    # A04: Allstadt returned to VSNT Fort Worth; preserve the current UTSW
    # treatment site in supplemental without stale VSNT/medical-oncologist identity.
    "68de357e-56dd-413b-88c1-b9d3fcd7466c",
    # A02: preserve raw evidence; retired Hammer and Breit's stale Renton
    # location must not reappear. Current NWVOS host locations are supplemental.
    "e59ef28d-0075-484b-9c12-b7b709decbc1",  # Hammer retired (owner decision)
    "832cface-e0f4-405b-a7c4-34ce3d5ad40b",  # Breit now at partner hospitals
    # A01 owner-approved reconciliation, 2026-10-11. Preserve raw profiles;
    # supplemental retains current treatment sites or mobile service areas.
    "738a7647-a210-47c7-93a3-05eda2d9a580",  # Four Seasons old 3120 address
    "1c1548ea-d273-49b8-b0a8-0a4d8f36dc89",  # same Four Seasons replacement site
    "f7f617b7-2ee6-4f20-b268-dcf94bc705f0",  # Upton: current host is 4055
    "90e2d1d4-3193-492d-9d70-0713df5a60e8",  # Hope WA mailing address
    "3935c200-6335-4680-9dcf-b03ad4f2bb74",  # Mobile Cancer Care mailbox
    "f25f8ffa-fba7-4778-bd6d-9ef48580f8cf",  # Ivaoes pharmaceutical company
    "44c4b36e-4420-40be-be7a-937169dd6780",  # LAVet: no current local oncology established
    # Current official roster confirms Ripoll at Bellevue WA; this raw profile
    # incorrectly combines Bellevue organization with the old Ventura address.
    "5a883725-1890-43bc-befb-4ab4369908aa",
    # Historical Olympia cancer-center address; official oncology route now
    # redirects to the verified BluePearl successor that moved in 2024.
    "1dabc90a-3f69-4fd4-b4a5-4d2d8114ae39",
    # ACRC official relocation notice and current two-location master replace
    # old Pearland with Woodlands and Texas Medical Center; preserve raw profiles.
    "1b35c69e-31e9-4dff-b796-21304c20c340",
    "d54203e4-328e-4ec5-8f94-dc035acd8f13",
    # Current official Fetch roster places Victoria Costa at Brandon. The
    # directory's Riverview address is not an official treatment location.
    "703f0037-e40f-4c7d-86e6-94a5172c26fc",
    # AVCC's current cancer department is at 8864 W State Road 84; retain the
    # verified replacement in supplemental data, not the stale 8920 address.
    "6cc55410-8adc-46e9-8f10-e304c782a22e",
    # Current 2026-10-11 national roster places Romansik in Littleton; the
    # retained seed record covers that location. Do not resurrect old Acton.
    "5063304a-4421-445d-97dc-cdf5100a19d7",
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
    # AVES moved in 2026; current official oncology pages and address are retained in supplemental data.
    "109599c1-82fd-40de-8cb5-1bfeaa9f2ae2",
    "457439a0-b477-455b-a4a2-d94efe77f904",
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
    # Official branch/contact review confirms these are distinct sites.
    # Similar clinic names and a shared Vienna postal code are not identity proof.
    separate_verified_sites = {
        frozenset(("tierplus-kagran", "tierplus-stadlau")),
        frozenset(("tierklinik-doebling-wien", "tierklinik-hutter-wien")),
        frozenset(("vetklinikum-wien", "veterinaria-wien-mauer")),
        frozenset(("tierarztpraxis-pragerstrasse-wien", "veterinaria-strebersdorf")),
        # 2026-10-16: two independently verified Hall practices, different
        # addresses, telephones and clinicians; shared 6060 is not identity.
        frozenset(("tierarztpraxis-gebhard-anker-hall", "tierarztpraxis-stadtgraben-hall")),
        frozenset(("tierarztpraxis-zekic-wien13", "tierarztpraxis-dorazio-wien-hietzing")),
        frozenset(("pfotentierklinik-wien", "veterinaria-wien-mauer")),
        frozenset(("pfotentierklinik-wien", "vetklinikum-wien")),
        frozenset(("tierarztzentrum-seepark-wien", "tierarztordination-schneeweiss-wien")),
        frozenset(("cz-eden-brno", "cz-animed-brno")),
        # Independently verified Saarwellingen practices: different clinicians,
        # streets and phones; the shared 66793 postal code is not identity.
        frozenset(("de-tierarztpraxis-am-steinhuebel", "de-joerg-waschbuesch-saarwellingen")),
    }
    if frozenset((seed.get("source_id"), candidate.get("source_id"))) in separate_verified_sites:
        return False
    same_zip = bool(seed["postal_code"] and seed["postal_code"] == candidate["postal_code"])
    same_city = bool(seed["city"] and seed["city"].casefold() == candidate["city"].casefold())
    # The two Akron hospitals are distinct despite similar names in one ZIP.
    # Limit this verified correction to their identities; other conflicts need
    # primary-source reconciliation before changing historical merge behavior.
    left_number, right_number = street_key(seed["street"])[0], street_key(candidate["street"])[0]
    # B01: the Malvern hospital (40 Three Tun Rd.) and radiation center
    # (50 Three Tun Rd.) share a telephone and ZIP but are separate sites.
    if (same_zip and seed["postal_code"] == "19355"
            and {left_number, right_number} == {"40", "50"}
            and all("bluepearl" in compact(x["name"]) for x in (seed, candidate))
            and all("threetun" in compact(x["street"]) for x in (seed, candidate))):
        return False
    akron_names = (norm(seed["name"]), norm(candidate["name"]))
    separate_akron_hospitals = (any(name.startswith("medvet") for name in akron_names)
                               and any(name.startswith("metropolitan") for name in akron_names))
    if (same_zip and seed["postal_code"] == "44321" and separate_akron_hospitals
            and left_number and right_number and left_number != right_number
            and phone_key(seed.get("phone", "")) and phone_key(candidate.get("phone", ""))
            and phone_key(seed["phone"]) != phone_key(candidate["phone"])
            and similarity(seed["name"], candidate["name"]) < 0.84):
        return False
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
        elif candidate.get("location_type") == "mobile" or candidate.get("coordinates_unknown"):
            # A service area/mailbox is not a fixed treatment or distance pin.
            coordinates = {"latitude": None, "longitude": None}
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
            if candidate.get("replace_coordinates") or candidate.get("location_type") == "mobile" or candidate.get("coordinates_unknown"):
                # Address corrections and mobile conversions must replace the
                # old coordinate point as well as the displayed address.
                existing.update({key: coordinates[key] for key in ("latitude", "longitude")})
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
