"""Second-pass official imagery and exact catalog aliases."""
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request,urlopen
import mimetypes,re,shutil
import center_image_localizer as base
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

ALT_PAGES={
"UC Davis Veterinary Center for Clinical Trials":"https://www.vetmed.ucdavis.edu/news/surgery-and-chemotherapy-help-dog-cancer",
"Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)":"https://www.hopkinsmedicine.org/radiology/veterinarians/procedures",
"MedVet Clinical Studies Center":"https://www.medvet.com/specialty/medical-oncology/",
"Veterinary Referral Center of Central Oregon":"https://vrcvet.com/veterinary-oncology/",
"Care Center Cincinnati":"https://carecentervets.com/oncology-services-care-center-cincinnati/",
"Louisiana State University School of Veterinary Medicine":"https://www.lsu.edu/vetmed/news/2023/pet_cancer_awareness_month.php",
"Purdue University College of Veterinary Medicine":"https://cancer.research.purdue.edu/research/veterinary-medicine/",
}

def attach(name,local,page):
 if not local:return
 p=PROFILES.get(name) or EXTRA_PROFILES.get(name)
 if p is None:
  p={"title":name,"about":f"{name} has veterinary cancer treatment or research opportunities represented in our current catalog.","links":[("Official website",page)]};EXTRA_PROFILES[name]=p;PROFILES[name]=p
 p.update({"image":local,"image_alt":f"Veterinary patient or cancer care program featured by {name}","image_caption":f"Photo: {name}."})

for name,page in ALT_PAGES.items():
 p=PROFILES.get(name) or EXTRA_PROFILES.get(name)
 if not (p and p.get('image')):attach(name,base.cache(name,page),page)

# Exact catalog labels. These reuse an image downloaded from that same organization/network.
ALIASES={
"Anivive Lifesciences — multicenter":"Anivive Lifesciences multicenter",
"WVRC – Grafton":"WVRC Grafton","WVRC – Waukesha":"WVRC Waukesha","WVRC – Racine/Kenosha":"WVRC Racine Kenosha",
"Colorado Animal Specialty & Emergency (CASE)":"Colorado Animal Specialty & Emergency (CASE)","CASE":"Colorado Animal Specialty & Emergency (CASE)",
"Multicenter local T-cell-engager STS immunotherapy":"Washington State University College of Veterinary Medicine",
"Veterinary Emergency + Referral Center":"Ethos Veterinary Health / Ethos Discovery",
}
for alias,target in ALIASES.items():
 src=PROFILES.get(target) or EXTRA_PROFILES.get(target)
 if src and src.get('image'):
  q=dict(src);q['title']=alias;EXTRA_PROFILES[alias]=q;PROFILES[alias]=q

# Last-resort first-party branding for sites that block all page images. Kept local too.
FAVICON_PAGES={
"UC Davis Veterinary Center for Clinical Trials":"https://www.vetmed.ucdavis.edu/",
"Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)":"https://www.hopkinsmedicine.org/",
"MedVet Clinical Studies Center":"https://www.medvet.com/",
"Veterinary Referral Center of Central Oregon":"https://vrcvet.com/",
"Care Center Cincinnati":"https://carecentervets.com/",
"Louisiana State University School of Veterinary Medicine":"https://www.lsu.edu/",
"Purdue University College of Veterinary Medicine":"https://www.purdue.edu/",
}
def favicon(name,page):
 for path in ('favicon.ico','favicon.png','apple-touch-icon.png'):
  try:
   u=urljoin(page,path);r=urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=10);data=r.read(2000000);c=(r.headers.get_content_type() or '').lower()
   if len(data)<300:continue
   ext=mimetypes.guess_extension(c) or ('.ico' if path.endswith('.ico') else '.png');p=base.STATIC/(base.slug(name)+ext);p.write_bytes(data);return base.PREFIX+p.name
  except Exception:pass
 return ''
for name,page in FAVICON_PAGES.items():
 p=PROFILES.get(name) or EXTRA_PROFILES.get(name)
 if not (p and p.get('image')):attach(name,favicon(name,page),page)
