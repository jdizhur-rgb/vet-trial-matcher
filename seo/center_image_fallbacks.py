"""Second-pass official imagery for centers whose primary page blocks image fetching."""
from pathlib import Path
import center_image_localizer as base
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

# Alternate pages are still first-party/official and are chosen because they expose
# a usable patient/oncology image more reliably than the primary program page.
ALT_PAGES = {
    "UC Davis Veterinary Center for Clinical Trials": "https://nutrition.vetmed.ucdavis.edu/news/clinical-trials-dogs-glioma-brain-tumors",
    "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)": "https://www.hopkinsmedicine.org/radiology/veterinarians/procedures",
    "MedVet Clinical Studies Center": "https://www.medvet.com/specialty/medical-oncology/",
    "Veterinary Referral Center of Central Oregon": "https://vrcvet.com/veterinary-oncology/",
    "CARE Center Cincinnati": "https://carecentervets.com/oncology-services-care-center-cincinnati/",
    "Louisiana State University School of Veterinary Medicine": "https://www.lsu.edu/vetmed/veterinary_hospital/oncology.php",
    "Purdue University College of Veterinary Medicine": "https://vet.purdue.edu/hospital/small-animal/services/oncology.php",
}

def attach(name, local, page):
    if not local:
        return
    p = PROFILES.get(name) or EXTRA_PROFILES.get(name)
    if p is None:
        p = {"title": name, "about": f"{name} has veterinary cancer treatment or research opportunities represented in our current catalog.", "links": [("Official website", page)]}
        EXTRA_PROFILES[name] = p
        PROFILES[name] = p
    p.update({"image": local, "image_alt": f"Veterinary patient or cancer care program featured by {name}", "image_caption": f"Photo: {name}."})

for name, page in ALT_PAGES.items():
    p = PROFILES.get(name) or EXTRA_PROFILES.get(name)
    if p and p.get("image"):
        continue
    attach(name, base.cache(name, page), page)

# Catalog punctuation/branding variants should reuse the already-downloaded image
# from the same official organization rather than trigger another network request.
ALIASES = {
    "Anivive Lifesciences — multicenter": "Anivive Lifesciences multicenter",
    "WVRC – Grafton": "WVRC Grafton",
    "WVRC – Waukesha": "WVRC Waukesha",
    "WVRC – Racine/Kenosha": "WVRC Racine Kenosha",
    "Colorado Animal Specialty & Emergency (CASE) / Ethos Discovery": "Colorado Animal Specialty & Emergency (CASE)",
}
for alias, target in ALIASES.items():
    src = PROFILES.get(target) or EXTRA_PROFILES.get(target)
    if src and src.get("image"):
        q = dict(src)
        q["title"] = q.get("title") or alias
        EXTRA_PROFILES[alias] = q
        PROFILES[alias] = q
