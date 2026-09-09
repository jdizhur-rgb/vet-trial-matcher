"""Central physical-location directory for institution pages and study sites.

All center-page and participating-site addresses must come from this file.
Keys are canonical display names; ALIASES resolves catalog/site spelling variants.
"""

LOCATIONS = {
    # Universities / teaching hospitals
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
    "WVRC Grafton": "WVRC Grafton, 1381 Port Washington Rd, Grafton, WI 53024",
}

ALIASES = {
    "Massachusetts Veterinary Referral Hospital (MVRH)": "Massachusetts Veterinary Referral Hospital",
    "Gulf Coast Veterinary Specialists (GCVS)": "Gulf Coast Veterinary Specialists",
    "SAGE": "SAGE Veterinary Centers",
    "Colorado Animal Specialty & Emergency (CASE) / Ethos Discovery": "Colorado Animal Specialty & Emergency (CASE)",
    "Veterinary Specialty Hospital": "Veterinary Specialty Hospital - Sorrento Valley",
}

def normalize(value):
    return " ".join(str(value or "").lower().replace("&", " and ").replace("/", " ").replace("(", " ").replace(")", " ").split())

_INDEX = {normalize(k): v for k, v in LOCATIONS.items()}
for alias, canonical in ALIASES.items():
    if canonical in LOCATIONS:
        _INDEX[normalize(alias)] = LOCATIONS[canonical]

def address_for(name):
    """Return a verified physical address for a canonical name or known alias."""
    return _INDEX.get(normalize(name), "")
