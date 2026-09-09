"""Cache official center imagery into the generated static site.

Runs after usercustomize. Images are discovered only from each center's official
website and copied to seo/static/images/centers so rendered pages do not depend
on third-party hotlinks.
"""
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import mimetypes, re

import usercustomize as uc
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

FALLBACK_PAGES = {
    "Anivive Lifesciences multicenter": "https://www.anivive.com/",
    "Atlantic Veterinary Internal Medicine & Oncology": "https://www.avim.us/",
    "Aurelius Biotherapeutics": "https://aureliusbio.com/",
    "CARE Center Cincinnati": "https://carecentervets.com/oncology-services-care-center-cincinnati/",
    "First Coast Veterinary Specialists & Emergency": "https://www.fcvets.com/",
    "Gulf Coast Veterinary Specialists": "https://www.gcvs.com/services/medical-oncology",
    "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)": "https://www.hopkinsmedicine.org/radiology/veterinarians",
    "Massachusetts Veterinary Referral Hospital": "https://www.massvethospital.com/services/oncology",
    "Metropolitan Veterinary Hospital": "https://www.metropolitanvet.com/services/oncology",
    "Mission Veterinary Emergency & Specialty": "https://www.missionveterinaryspecialists.com/services/oncology",
    "Overland Park Veterinary Emergency & Specialty": "https://www.overlandparkveterinaryspecialists.com/services/oncology",
    "Peak Veterinary Referral Center": "https://www.peakveterinary.com/services",
    "Pet Emergency and Specialty Center of Marin": "https://pescm.com/san-rafael-ca/our-story/",
    "SAGE": "https://www.sagecenters.com/services/oncology",
    "SAGE Veterinary Centers": "https://www.sagecenters.com/services/oncology",
    "Schwarzman Animal Medical Center": "https://www.amcny.org/pet-owners/specialties/oncology/",
    "Southeast Veterinary Oncology & Internal Medicine": "https://www.southeastveterinaryoncologyandinternalmedicine.com/",
    "Summit Veterinary Referral Center": "https://www.summitvets.com/services",
    "Veterinary Referral Center of Central Oregon": "https://vrcvet.com/clinical-trials/",
    "Veterinary Specialty Hospital": "https://www.vshsd.com/services/oncology",
    "WVRC Grafton": "https://www.wvrcwi.com/services/oncology",
    "WVRC Racine Kenosha": "https://www.wvrcwi.com/services/oncology",
    "WVRC Waukesha": "https://www.wvrcwi.com/services/oncology",
    "Ethos Veterinary Health / Ethos Discovery": "https://www.ethosvet.com/clinical-studies/",
}

STATIC = Path(__file__).resolve().parent / "static" / "images" / "centers"
STATIC.mkdir(parents=True, exist_ok=True)
SITE_PREFIX = "https://jdizhur-rgb.github.io/vet-trial-matcher/images/centers/"

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def candidates(page):
    req=Request(page,headers={"User-Agent":"Mozilla/5.0 VetTrialFinder/1.0"})
    with urlopen(req,timeout=12) as r:
        text=r.read(1_200_000).decode("utf-8","replace")
    pats=[
      r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)',
      r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::secure_url)?["\']',
      r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
      r'<img[^>]+(?:src|data-src)=["\']([^"\']+)["\'][^>]*>',
    ]
    out=[]
    for pat in pats:
        for m in re.finditer(pat,text,re.I):
            u=urljoin(page,m.group(1).replace('&amp;','&').strip())
            low=u.lower()
            if u.startswith('https://') and not any(x in low for x in ('logo','icon','avatar','badge','sprite','svg')):
                out.append(u)
    return out

def cache(name,page,direct=""):
    urls=[direct] if direct else []
    try: urls += candidates(page)
    except Exception as e: print('CENTER_IMAGE_PAGE_WARN',name,e)
    for u in urls:
        if not u: continue
        try:
            req=Request(u,headers={"User-Agent":"Mozilla/5.0 VetTrialFinder/1.0","Referer":page})
            with urlopen(req,timeout=15) as r:
                data=r.read(8_000_000); ctype=(r.headers.get_content_type() or '').lower()
            if len(data)<5000 or not ctype.startswith('image/'): continue
            ext=mimetypes.guess_extension(ctype) or '.jpg'
            if ext=='.jpe': ext='.jpg'
            path=STATIC/(slug(name)+ext); path.write_bytes(data)
            print('CENTER_IMAGE_LOCAL',name,path.name,len(data))
            return SITE_PREFIX+path.name
        except Exception as e: print('CENTER_IMAGE_URL_WARN',name,u,e)
    return ''

all_pages=dict(uc.OFFICIAL_IMAGE_PAGES); all_pages.update(FALLBACK_PAGES)
direct={name:url for name,(url,_alt) in uc.IMAGES.items()}
for name,page in all_pages.items():
    local=cache(name,page,direct.get(name,''))
    if not local: continue
    profile=PROFILES.get(name) or EXTRA_PROFILES.get(name)
    if profile is None:
        profile={"title":name,"about":f"{name} has veterinary cancer treatment or research opportunities represented in our current catalog.","links":[("Official website",page)]}
        EXTRA_PROFILES[name]=profile
        PROFILES[name]=profile
    profile.update({"image":local,"image_alt":f"Veterinary patient or cancer care program featured by {name}","image_caption":f"Photo: {name}."})
