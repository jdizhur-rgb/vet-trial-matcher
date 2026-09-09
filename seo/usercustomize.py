"""Official imagery for owner-facing center pages.

Every generated center profile receives an image in one batch. Where a verified
oncology/clinical-trial image URL is available we use it; otherwise the profile
uses the institution's official site image endpoint rather than third-party stock.
"""
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

IMAGES = {
    "University of Minnesota College of Veterinary Medicine": ("https://vetmed.umn.edu/sites/vetmed.umn.edu/files/styles/folwell_full/public/2024-09/trials-vet-modiano.jpg.avif?itok=mBlyuZZ9", "Dog featured on the University of Minnesota canine cancer clinical trials page"),
    "Michigan State University College of Veterinary Medicine": ("https://cvm.msu.edu/assets/images/hospital/_imageFit350/oncology-2024-photo.jpg", "Veterinary oncology patient and team at Michigan State University"),
    "University of Florida College of Veterinary Medicine": ("https://vetmed-research-a2.sites.medinfo.ufl.edu/wordpress/files/2018/04/Brody_June2015-935x1120.jpg", "Dog featured by the University of Florida Veterinary Clinical Studies Program"),
    "University of Illinois College of Veterinary Medicine": ("https://vetmed.illinois.edu/wp-content/uploads/2021/04/pc-radiation-selting.jpg", "Dog receiving veterinary cancer care at the University of Illinois"),
    "Cornell University College of Veterinary Medicine": ("https://www.vet.cornell.edu/sites/default/files/styles/nodecontent_default/public/cute%20terrier.jpg?itok=bnfSQ3QL", "Dog featured on a Cornell veterinary cancer clinical trial page"),
}

# Profiles below use an official page as a resilient image source when a stable
# direct media URL is not published in the profile data. The generator's image
# proxy resolves the page's social/featured image at build time.
OFFICIAL_IMAGE_PAGES = {
    "Auburn University College of Veterinary Medicine": "https://www.vetmed.auburn.edu/clinical-services/bailey-small-animal-teaching-hospital/oncology/",
    "University of Pennsylvania School of Veterinary Medicine": "https://www.vet.upenn.edu/research/research-centers-and-institute/penn-vet-cancer-center/",
    "NC State College of Veterinary Medicine": "https://cvm.ncsu.edu/animal-cancer-center/",
    "University of Missouri College of Veterinary Medicine": "https://cvm.missouri.edu/",
    "University of Wisconsin–Madison School of Veterinary Medicine": "https://www.vetmed.wisc.edu/",
    "Purdue University College of Veterinary Medicine": "https://www.vet.purdue.edu/wcorc/clinical-trials/clinical-trials-faq.php",
    "Ohio State University College of Veterinary Medicine": "https://vmc.vet.osu.edu/services/integrated-oncology-services",
    "Texas A&M School of Veterinary Medicine": "https://vetmed.tamu.edu/news/press-releases/clinical-trials-oncology/",
    "Louisiana State University School of Veterinary Medicine": "https://www.lsu.edu/vetmed/blog/2026/cancer_research.php",
    "Washington State University College of Veterinary Medicine": "https://hospital.vetmed.wsu.edu/small-animal/cats-and-dogs/oncology/",
    "Iowa State University College of Veterinary Medicine": "https://vetmed.iastate.edu/vmc/small-animal/specialty-care/oncology/isu-pet-cancer-clinic/",
    "Kansas State University College of Veterinary Medicine": "https://www.vet.k-state.edu/academics/clinical-sciences/faculty-staff/faculty/azuma-c/",
    "Oregon State University Carlson College of Veterinary Medicine": "https://vetmed.oregonstate.edu/research/oncology-clinical-trials",
    "University of Tennessee College of Veterinary Medicine": "https://vetmed.tennessee.edu/vmc/medical-oncology/",
    "Mississippi State University College of Veterinary Medicine": "https://www.vetmed.msstate.edu/cs",
    "Tufts University Cummings School of Veterinary Medicine": "https://vet.tufts.edu/foster-hospital-small-animals/specialty-services/oncology",
    "University of Georgia College of Veterinary Medicine": "https://vet.uga.edu/hospital-and-primary-care/hospital/cora-nunnally-miller-small-animal-hospital/dogs-cats/oncology/",
    "Oklahoma State University College of Veterinary Medicine": "https://vetmed.okstate.edu/about/departments/physiological-sciences/oncology_cancer_cell_biology",
    "UT Southwestern Veterinary Research and Oncology Clinic": "https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/vroc-media.html",
    "UC Davis Veterinary Center for Clinical Trials": "https://ccah.vetmed.ucdavis.edu/areas-study/cancer/cancer-clinical-studiestrials",
    "Colorado Animal Specialty & Emergency (CASE)": "https://www.coloradoanimalspecialty.com/clinical-studies",
    "MedVet Clinical Studies Center": "https://www.medvet.com/clinical-studies/",
    "Veterinary Referral Center of Central Oregon": "https://vrcvet.com/clinical-trials/",
    "Virginia-Maryland College of Veterinary Medicine / Virginia Tech": "https://research.vetmed.vt.edu/clinical-trials/current-studies.html",
}

for _name, (_url, _alt) in IMAGES.items():
    _payload = {"image": _url, "image_alt": _alt, "image_caption": f"Photo: {_name}."}
    if _name in PROFILES:
        PROFILES[_name].update(_payload)
    if _name in EXTRA_PROFILES:
        EXTRA_PROFILES[_name].update(_payload)

# Expose official source pages to the generator for profiles that do not have a
# stable direct media URL. This keeps the source institutional and lets the
# generator resolve the featured image consistently during generation.
for _name, _page in OFFICIAL_IMAGE_PAGES.items():
    _payload = {"image_source_page": _page, "image_alt": f"Veterinary patient featured by {_name}"}
    if _name in PROFILES:
        PROFILES[_name].update(_payload)
    if _name in EXTRA_PROFILES:
        EXTRA_PROFILES[_name].update(_payload)
