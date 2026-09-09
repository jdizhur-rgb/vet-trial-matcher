"""Central physical-location directory for institution pages and study sites.

All center-page and participating-site addresses come from this file whenever
we know the physical location. Catalog spelling variants are resolved through
one shared normalizer so address lookup behaves the same everywhere.
"""
from __future__ import annotations
import re

LOCATIONS = {
    # Universities / teaching hospitals — USA
    "Colorado State University Flint Animal Cancer Center": "Flint Animal Cancer Center, 300 W Drake Rd, Fort Collins, CO 80523",
    "Auburn University College of Veterinary Medicine": "Bailey Small Animal Teaching Hospital, 1220 Wire Rd, Auburn, AL 36849",
    "Cornell University College of Veterinary Medicine": "Cornell University Hospital for Animals, 930 Campus Rd, Ithaca, NY 14853",
    "Iowa State University College of Veterinary Medicine": "Lloyd Veterinary Medical Center, 1809 S Riverside Dr, Ames, IA 50011",
    "Kansas State University College of Veterinary Medicine": "Veterinary Health Center, 1800 Denison Ave, Manhattan, KS 66506",
    "Louisiana State University School of Veterinary Medicine": "LSU Veterinary Teaching Hospital, 1909 Skip Bertman Dr, Baton Rouge, LA 70803",
    "Michigan State University College of Veterinary Medicine": "Michigan State University Veterinary Medical Center, 736 Wilson Rd, East Lansing, MI 48824",
    "Mississippi State University College of Veterinary Medicine": "Animal Health Center, 240 Wise Center Dr, Mississippi State, MS 39762",
    "NC State College of Veterinary Medicine": "NC State Veterinary Hospital, 1052 William Moore Dr, Raleigh, NC 27607",
    "Ohio State University College of Veterinary Medicine": "The Ohio State University Veterinary Medical Center, 601 Vernon L Tharp St, Columbus, OH 43210",
    "Oklahoma State University College of Veterinary Medicine": "Boren Veterinary Medical Teaching Hospital, 2065 W Farm Rd, Stillwater, OK 74078",
    "Oregon State University Carlson College of Veterinary Medicine": "Lois Bates Acheson Veterinary Teaching Hospital, Magruder Hall, 700 SW 30th St, Corvallis, OR 97331",
    "Purdue University College of Veterinary Medicine": "Purdue University Veterinary Hospital, 625 Harrison St, West Lafayette, IN 47907",
    "Texas A&M School of Veterinary Medicine": "Texas A&M Small Animal Teaching Hospital, 408 Raymond Stotzer Pkwy, College Station, TX 77845",
    "Tufts University Cummings School of Veterinary Medicine": "Henry and Lois Foster Hospital for Small Animals, 200 Westboro Rd, North Grafton, MA 01536",
    "UC Davis Veterinary Center for Clinical Trials": "UC Davis Veterinary Medical Teaching Hospital, 1 Garrod Dr, Davis, CA 95616",
    "University of Florida College of Veterinary Medicine": "UF Small Animal Hospital, 2015 SW 16th Ave, Gainesville, FL 32608",
    "University of Georgia College of Veterinary Medicine": "UGA Veterinary Teaching Hospital, 2200 College Station Rd, Athens, GA 30602",
    "University of Illinois College of Veterinary Medicine": "University of Illinois Veterinary Teaching Hospital, 1008 W Hazelwood Dr, Urbana, IL 61802",
    "University of Minnesota College of Veterinary Medicine": "University of Minnesota Veterinary Medical Center, 1365 Gortner Ave, St Paul, MN 55108",
    "University of Missouri College of Veterinary Medicine": "University of Missouri Veterinary Health Center, 900 E Campus Dr, Columbia, MO 65211",
    "University of Pennsylvania School of Veterinary Medicine": "Penn Vet Ryan Veterinary Hospital, 3900 Spruce St, Philadelphia, PA 19104",
    "University of Tennessee College of Veterinary Medicine": "UT Veterinary Medical Center, 2407 River Dr, Knoxville, TN 37996",
    "University of Wisconsin–Madison School of Veterinary Medicine": "UW Veterinary Care, 2015 Linden Dr, Madison, WI 53706",
    "Virginia-Maryland College of Veterinary Medicine / Virginia Tech": "Veterinary Teaching Hospital, 245 Duck Pond Dr, Blacksburg, VA 24061",
    "Washington State University College of Veterinary Medicine": "WSU Veterinary Teaching Hospital, 205 Ott Rd, Pullman, WA 99164",

    # Universities / teaching hospitals — international
    "University of Évora Veterinary Hospital": "Hospital Veterinário, Universidade de Évora, Herdade da Mitra, Apartado 94, 7002-554 Évora, Portugal",
    "University of Zurich Veterinary Hospital": "Universitäres Tierspital Zürich, Winterthurerstrasse 204, 8057 Zürich, Switzerland",
    "University of Milan Veterinary Teaching Hospital (Lodi)": "Ospedale Veterinario Universitario, Via dell'Università 6, 26900 Lodi LO, Italy",
    "Ontario Veterinary College — University of Guelph": "Ontario Veterinary College, University of Guelph, 50 Stone Rd E, Guelph, ON N1G 2W1, Canada",
    "Hospital for Sick Children": "The Hospital for Sick Children, 555 University Ave, Toronto, ON M5G 1X8, Canada",
    "University Hospital for Companion Animals — University of Copenhagen": "University Hospital for Companion Animals, Dyrlægevej 16, 1870 Frederiksberg C, Denmark",
    "Ghent University Faculty of Veterinary Medicine": "Ghent University Faculty of Veterinary Medicine, Salisburylaan 133, 9820 Merelbeke, Belgium",
    "AniCura Ospedale Veterinario I Portoni Rossi": "Ospedale Veterinario I Portoni Rossi, Via Roma 57/A, 40069 Zola Predosa BO, Italy",

    # Independent / specialty / research centers
    "Aurelius Biotherapeutics": "Aurelius Biotherapeutics, 720 Virginia St, Bellingham, WA 98225",
    "Colorado Animal Specialty & Emergency (CASE)": "Colorado Animal Specialty & Emergency, 2972 Iris Ave, Boulder, CO 80301",
    "Overland Park Veterinary Emergency & Specialty": "Overland Park Veterinary Emergency & Specialty, 8301 W 163rd St, Overland Park, KS 66223",
    "Massachusetts Veterinary Referral Hospital": "Massachusetts Veterinary Referral Hospital, 20 Cabot Rd, Woburn, MA 01801",
    "Peak Veterinary Referral Center": "Peak Veterinary Referral Center, 158 Hurricane Ln, Williston, VT 05495",
    "Mission Veterinary Emergency & Specialty": "Mission Veterinary Emergency & Specialty, 5914 Johnson Dr, Mission, KS 66202",
    "Gulf Coast Veterinary Specialists": "Gulf Coast Veterinary Specialists, 8042 Katy Fwy, Houston, TX 77024",
    "First Coast Veterinary Specialists & Emergency": "First Coast Veterinary Specialists & Emergency, 301 Jacksonville Dr, Jacksonville Beach, FL 32250",
    "Summit Veterinary Referral Center": "Summit Veterinary Referral Center, 2505 S 80th St, Tacoma, WA 98409",
    "CARE Center Cincinnati": "CARE Center, 6995 E Kemper Rd, Cincinnati, OH 45249",
    "SAGE Veterinary Centers": "SAGE Veterinary Centers, 600 Alabama St, San Francisco, CA 94110",
    "Schwarzman Animal Medical Center": "Schwarzman Animal Medical Center, 510 E 62nd St, New York, NY 10065",
    "Veterinary Specialty Hospital - Sorrento Valley": "Veterinary Specialty Hospital, 10435 Sorrento Valley Rd, San Diego, CA 92121",
    "Pet Emergency and Specialty Center of Marin": "Pet Emergency and Specialty Center of Marin, 901 Francisco Blvd E, San Rafael, CA 94901",
    "Veterinary Referral Center of Central Oregon": "VRCCO East, 62889 NE Oxford Ct, Bend, OR 97701",
    "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)": "Johns Hopkins CIGAT, 600 N Wolfe St, Park 311, Baltimore, MD 21287",
    "Metropolitan Veterinary Hospital - Akron": "Metropolitan Veterinary Hospital, 1053 S Cleveland-Massillon Rd, Akron, OH 44321",
    "WVRC Grafton": "WVRC Grafton, 1381 Port Washington Rd, Grafton, WI 53024",
    "WVRC Racine Kenosha": "WVRC Racine/Kenosha, 1123 58th Ave, Somers, WI 53144",
    "WVRC Waukesha": "WVRC Waukesha, W239 N1046 Pewaukee Rd, Waukesha, WI 53188",

    # MedVet study locations
    "MedVet Salt Lake City": "MedVet Salt Lake City, 331 W Bearcat Dr, Salt Lake City, UT 84115",
    "MedVet Cincinnati": "MedVet Cincinnati, 3964 Red Bank Rd, Cincinnati, OH 45227",
    "MedVet Cleveland": "MedVet Cleveland, 20400 Emerald Pkwy, Cleveland, OH 44135",
    "MedVet Pittsburgh": "MedVet Pittsburgh, 2810 Washington Rd, McMurray, PA 15317",
    "MedVet Chicago": "MedVet Chicago, 3305 N California Ave, Chicago, IL 60618",
}

ALIASES = {
    # Common network/site spelling variants
    "Massachusetts Veterinary Referral Hospital (MVRH)": "Massachusetts Veterinary Referral Hospital",
    "Gulf Coast Veterinary Specialists (GCVS)": "Gulf Coast Veterinary Specialists",
    "SAGE": "SAGE Veterinary Centers",
    "SAGE – San Francisco": "SAGE Veterinary Centers",
    "Colorado Animal Specialty & Emergency (CASE) / Ethos Discovery": "Colorado Animal Specialty & Emergency (CASE)",
    "CASE": "Colorado Animal Specialty & Emergency (CASE)",
    "Veterinary Specialty Hospital": "Veterinary Specialty Hospital - Sorrento Valley",
    "Veterinary Referral Center of Central Oregon / CASTR Alliance": "Veterinary Referral Center of Central Oregon",
    "Veterinary Referral Center of Central Oregon (VRCCO)": "Veterinary Referral Center of Central Oregon",
    "WVRC Racine/Kenosha": "WVRC Racine Kenosha",
    "Metropolitan Veterinary Hospital": "Metropolitan Veterinary Hospital - Akron",

    # University catalog variants — all resolve to the same physical teaching hospital
    "University of Florida": "University of Florida College of Veterinary Medicine",
    "University of Florida Veterinary Hospitals": "University of Florida College of Veterinary Medicine",
    "University of Illinois": "University of Illinois College of Veterinary Medicine",
    "University of Illinois Veterinary Teaching Hospital": "University of Illinois College of Veterinary Medicine",
    "University of Pennsylvania": "University of Pennsylvania School of Veterinary Medicine",
    "University of Pennsylvania School of Veterinary Medicine — Comparative Immunotherapy Program": "University of Pennsylvania School of Veterinary Medicine",
    "University of Minnesota": "University of Minnesota College of Veterinary Medicine",
    "University of Minnesota Veterinary Medical Center": "University of Minnesota College of Veterinary Medicine",
    "University of Minnesota Canine Brain Tumor Program": "University of Minnesota College of Veterinary Medicine",
    "Tufts University": "Tufts University Cummings School of Veterinary Medicine",
    "Tufts Cummings School of Veterinary Medicine": "Tufts University Cummings School of Veterinary Medicine",
    "Cummings School of Veterinary Medicine, Tufts University": "Tufts University Cummings School of Veterinary Medicine",
    "Michigan State University": "Michigan State University College of Veterinary Medicine",
    "Michigan State University Veterinary Medical Center": "Michigan State University College of Veterinary Medicine",
    "Cornell University": "Cornell University College of Veterinary Medicine",
    "University of Georgia": "University of Georgia College of Veterinary Medicine",
    "Purdue University": "Purdue University College of Veterinary Medicine",
    "Purdue University Veterinary Hospital": "Purdue University College of Veterinary Medicine",
    "Ohio State University": "Ohio State University College of Veterinary Medicine",
    "Ohio State University Veterinary Medical Center": "Ohio State University College of Veterinary Medicine",
    "The Ohio State University Veterinary Medical Center": "Ohio State University College of Veterinary Medicine",
    "Texas A&M University": "Texas A&M School of Veterinary Medicine",
    "Texas A&M Small Animal Teaching Hospital": "Texas A&M School of Veterinary Medicine",
    "Texas A&M Veterinary Medical Teaching Hospital": "Texas A&M School of Veterinary Medicine",
    "Colorado State University": "Colorado State University Flint Animal Cancer Center",
    "Colorado State University Veterinary Teaching Hospital": "Colorado State University Flint Animal Cancer Center",
    "University of Missouri Veterinary Health Center": "University of Missouri College of Veterinary Medicine",
    "LSU Veterinary Teaching Hospital": "Louisiana State University School of Veterinary Medicine",
    "Washington State University Veterinary Teaching Hospital": "Washington State University College of Veterinary Medicine",
    "UC Davis Veterinary Medical Teaching Hospital": "UC Davis Veterinary Center for Clinical Trials",

    # International variants
    "University of Zurich — Division of Radiation Oncology": "University of Zurich Veterinary Hospital",
    "Universitäres Tierspital Zürich / University of Zurich": "University of Zurich Veterinary Hospital",
    "AniCura I Portoni Rossi / University of Teramo": "AniCura Ospedale Veterinario I Portoni Rossi",
    "Ontario Veterinary College": "Ontario Veterinary College — University of Guelph",
    "University Hospital for Companion Animals, University of Copenhagen": "University Hospital for Companion Animals — University of Copenhagen",
}


def normalize(value):
    """One punctuation-insensitive key for catalog, directory and aliases."""
    text = str(value or "").lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


_INDEX = {normalize(k): v for k, v in LOCATIONS.items()}
for alias, canonical in ALIASES.items():
    if canonical in LOCATIONS:
        _INDEX[normalize(alias)] = LOCATIONS[canonical]


def address_for(name):
    """Return a verified physical address for a canonical name or known alias."""
    return _INDEX.get(normalize(name), "")


def address_is_complete(address, country=""):
    """Country-aware physical-address validation used by build and preflight."""
    text = " ".join(str(address or "").split())
    if not text or not re.search(r"\d", text):
        return False
    country_key = normalize(country)
    if country_key in {"usa", "united states", "united states of america"}:
        return bool(re.search(r"\b[A-Z]{2}\s+\d{5}(?:-\d{4})?\b", text, re.I))
    if country_key == "canada":
        return bool(re.search(r"\b[A-Z]\d[A-Z][ -]?\d[A-Z]\d\b", text, re.I))
    if country_key in {"uk", "united kingdom", "great britain", "england", "scotland", "wales"}:
        return bool(re.search(r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", text, re.I))
    return len([p for p in text.split(",") if p.strip()]) >= 3
