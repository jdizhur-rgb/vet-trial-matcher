"""Official imagery for owner-facing center pages.

Direct, verified oncology images are preferred. For the remaining center profiles,
resolve the featured/social image from that center's own official oncology or
clinical-trials page at build time. No third-party stock imagery is used.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
import re
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

IMAGES = {
    "University of Minnesota College of Veterinary Medicine": ("https://vetmed.umn.edu/sites/vetmed.umn.edu/files/styles/folwell_full/public/2024-09/trials-vet-modiano.jpg.avif?itok=mBlyuZZ9", "Dog featured on the University of Minnesota canine cancer clinical trials page"),
    "Michigan State University College of Veterinary Medicine": ("https://cvm.msu.edu/assets/images/hospital/_imageFit350/oncology-2024-photo.jpg", "Veterinary oncology patient and team at Michigan State University"),
    "University of Florida College of Veterinary Medicine": ("https://vetmed-research-a2.sites.medinfo.ufl.edu/wordpress/files/2018/04/Brody_June2015-935x1120.jpg", "Dog featured by the University of Florida Veterinary Clinical Studies Program"),
    "University of Illinois College of Veterinary Medicine": ("https://vetmed.illinois.edu/wp-content/uploads/2021/04/pc-radiation-selting.jpg", "Dog receiving veterinary cancer care at the University of Illinois"),
    "Cornell University College of Veterinary Medicine": ("https://www.vet.cornell.edu/sites/default/files/styles/nodecontent_default/public/cute%20terrier.jpg?itok=bnfSQ3QL", "Dog featured on a Cornell veterinary cancer clinical trial page"),
}

OFFICIAL_IMAGE_PAGES = {
    "Auburn University College of Veterinary Medicine": "https://www.vetmed.auburn.edu/clinical-services/bailey-small-animal-teaching-hospital/oncology/",
    "University of Pennsylvania School of Veterinary Medicine": "https://www.vet.upenn.edu/research/research-centers-and-institute/penn-vet-cancer-center/",
    "NC State College of Veterinary Medicine": "https://cvm.ncsu.edu/animal-cancer-center/",
    "University of Missouri College of Veterinary Medicine": "https://cvm.missouri.edu/",
    "University of Wisconsin–Madison School of Veterinary Medicine": "https://www.vetmed.wisc.edu/",
    "Purdue University College of Veterinary Medicine": "https://cancer.research.purdue.edu/research/veterinary-medicine/",
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
    "UT Southwestern Veterinary Research and Oncology Clinic": "https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/",
    "UC Davis Veterinary Center for Clinical Trials": "https://ccah.vetmed.ucdavis.edu/areas-study/cancer/cancer-clinical-studiestrials",
    "Colorado Animal Specialty & Emergency (CASE)": "https://www.coloradoanimalspecialty.com/clinical-studies",
    "MedVet Clinical Studies Center": "https://www.medvet.com/clinical-studies/",
    "Veterinary Referral Center of Central Oregon": "https://vrcvet.com/clinical-trials/",
    "Virginia-Maryland College of Veterinary Medicine / Virginia Tech": "https://research.vetmed.vt.edu/clinical-trials.html",
}


def _profiles_for(name):
    out = []
    if name in PROFILES:
        out.append(PROFILES[name])
    if name in EXTRA_PROFILES and EXTRA_PROFILES[name] not in out:
        out.append(EXTRA_PROFILES[name])
    return out


def _official_host(page, image):
    p = (urlparse(page).hostname or "").lower().removeprefix("www.")
    i = (urlparse(image).hostname or "").lower().removeprefix("www.")
    # Allow the institution's own subdomains/CDN path, never an unrelated stock host.
    return bool(p and i and (i == p or i.endswith("." + p) or p.endswith("." + i)))


def _featured_image(page):
    try:
        req = Request(page, headers={"User-Agent": "Mozilla/5.0 VetTrialFinder/1.0"})
        with urlopen(req, timeout=8) as r:
            html = r.read(900_000).decode("utf-8", "replace")
        patterns = (
            r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::secure_url)?["\']',
            r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']',
        )
        for pattern in patterns:
            m = re.search(pattern, html, re.I)
            if m:
                image = urljoin(page, unescape(m.group(1)).strip())
                if image.startswith("https://") and _official_host(page, image):
                    return image
    except Exception as exc:
        print(f"CENTER_IMAGE_WARN {page}: {exc}")
    return ""


for _name, (_url, _alt) in IMAGES.items():
    for _profile in _profiles_for(_name):
        _profile.update({"image": _url, "image_alt": _alt, "image_caption": f"Photo: {_name}."})

# Resolve all remaining center images concurrently so this is one batch operation,
# not a growing list of one-off image hacks.
with ThreadPoolExecutor(max_workers=8) as _pool:
    _jobs = {_pool.submit(_featured_image, page): (name, page) for name, page in OFFICIAL_IMAGE_PAGES.items() if not any(p.get("image") for p in _profiles_for(name))}
    for _job in as_completed(_jobs):
        _name, _page = _jobs[_job]
        _url = _job.result()
        if not _url:
            print(f"CENTER_IMAGE_MISSING {_name} source={_page}")
            continue
        for _profile in _profiles_for(_name):
            _profile.update({"image": _url, "image_alt": f"Veterinary patient or oncology program featured by {_name}", "image_caption": f"Photo: {_name}."})
        print(f"CENTER_IMAGE_OK {_name} {_url}")
