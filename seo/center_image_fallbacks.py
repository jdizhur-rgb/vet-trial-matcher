"""Second-pass official imagery plus a local free-stock fallback."""
from urllib.parse import urljoin
from urllib.request import Request,urlopen
import mimetypes
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

def attach(name,local,page,caption=None):
 if not local:return
 p=PROFILES.get(name) or EXTRA_PROFILES.get(name)
 if p is None:
  p={"title":name,"about":f"{name} has veterinary cancer treatment or research opportunities represented in our current catalog.","links":[("Official website",page)]};EXTRA_PROFILES[name]=p;PROFILES[name]=p
 p.update({"image":local,"image_alt":f"Veterinary patient image for {name}","image_caption":caption or f"Photo: {name}."})

for name,page in ALT_PAGES.items():
 p=PROFILES.get(name) or EXTRA_PROFILES.get(name)
 if not (p and p.get('image')):attach(name,base.cache(name,page),page)

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

# One neutral veterinary-care photo is enough for centers whose sites block automated image downloads.
# Pexels permits free website use. We cache it into the generated static site so pages never hotlink it.
STOCK_URL='https://images.pexels.com/photos/6235650/pexels-photo-6235650.jpeg?cs=srgb&fm=jpg'
STOCK_LOCAL=base.PREFIX+'stock-veterinary-dog.jpg'
try:
 p=base.STATIC/'stock-veterinary-dog.jpg'
 if not p.exists():
  data=urlopen(Request(STOCK_URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read(8000000)
  if len(data)>5000:p.write_bytes(data)
except Exception as e:print('STOCK_IMAGE_WARN',e)

for name,p in list(PROFILES.items())+list(EXTRA_PROFILES.items()):
 if isinstance(p,dict) and not p.get('image'):
  p.update({'image':STOCK_LOCAL,'image_alt':'Dog receiving veterinary care','image_caption':'Stock veterinary-care photo: Pexels.'})
