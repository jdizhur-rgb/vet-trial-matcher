"""Small presentation directory for trial cards.

Canonical center names and physical addresses remain owned by center_directory.py.
This file only supplies shorter patient-facing labels and verified generic study
contacts when a trial record itself does not already contain a contact.
"""

DISPLAY_NAMES = {
    "Colorado State University Flint Animal Cancer Center": "Colorado State Flint Animal Cancer Center",
    "Auburn University College of Veterinary Medicine": "Auburn Vet Med",
    "Cornell University College of Veterinary Medicine": "Cornell Vet",
    "Iowa State University College of Veterinary Medicine": "Iowa State Vet Med",
    "Kansas State University College of Veterinary Medicine": "Kansas State Vet Med",
    "Louisiana State University School of Veterinary Medicine": "LSU Vet Med",
    "Michigan State University College of Veterinary Medicine": "Michigan State Vet Med",
    "Mississippi State University College of Veterinary Medicine": "Mississippi State Vet Med",
    "NC State College of Veterinary Medicine": "NC State Vet Hospital",
    "Ohio State University College of Veterinary Medicine": "Ohio State Vet Medical Center",
    "Oklahoma State University College of Veterinary Medicine": "Oklahoma State Vet Med",
    "Oregon State University Carlson College of Veterinary Medicine": "Oregon State Vet Med",
    "Purdue University College of Veterinary Medicine": "Purdue Vet Med",
    "Texas A&M School of Veterinary Medicine": "Texas A&M Vet Med",
    "Tufts University Cummings School of Veterinary Medicine": "Tufts Cummings Vet",
    "UC Davis Veterinary Center for Clinical Trials": "UC Davis Vet Clinical Trials",
    "University of Florida College of Veterinary Medicine": "University of Florida Vet Med",
    "University of Georgia College of Veterinary Medicine": "University of Georgia Vet Med",
    "University of Illinois College of Veterinary Medicine": "University of Illinois Vet Med",
    "University of Minnesota College of Veterinary Medicine": "University of Minnesota Vet Med",
    "University of Missouri College of Veterinary Medicine": "University of Missouri Vet Med",
    "University of Pennsylvania School of Veterinary Medicine": "Penn Vet",
    "University of Tennessee College of Veterinary Medicine": "University of Tennessee Vet Med",
    "University of Wisconsin–Madison School of Veterinary Medicine": "UW–Madison Vet Med",
    "Virginia-Maryland College of Veterinary Medicine / Virginia Tech": "Virginia Tech Vet Med",
    "Washington State University College of Veterinary Medicine": "Washington State Vet Med",
    "UT Southwestern Veterinary Research and Oncology Clinic": "UT Southwestern VROC",
    "Ontario Veterinary College — University of Guelph": "Ontario Veterinary College",
    "University of Zurich Veterinary Hospital": "University of Zurich Vet Hospital",
    "University of Milan Veterinary Teaching Hospital (Lodi)": "University of Milan Vet Hospital",
    "University of Évora Veterinary Hospital": "University of Évora Vet Hospital",
    "University Hospital for Companion Animals — University of Copenhagen": "University of Copenhagen Vet Hospital",
    "Ghent University Faculty of Veterinary Medicine": "Ghent University Vet Med",
    "National Taiwan University Veterinary Hospital": "National Taiwan University Vet Hospital",
    "National Chung Hsing University Veterinary Teaching Hospital": "National Chung Hsing University Vet Hospital",
    "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)": "Johns Hopkins CIGAT",
}

# Generic institutional study contacts are used only as a fallback when the
# individual trial has no contacts/contact field. Add entries only when verified.
CONTACTS = {
    "University of Pennsylvania School of Veterinary Medicine": "Penn Vet VCIC — vcic@vet.upenn.edu; 215-573-0302",
}


def display_name_for(canonical: str) -> str:
    return DISPLAY_NAMES.get(canonical, canonical)


def contact_for(canonical: str) -> str | None:
    return CONTACTS.get(canonical)
