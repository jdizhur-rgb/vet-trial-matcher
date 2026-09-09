"""Download official center-page imagery into the static site at build time."""
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import mimetypes,re
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

PAGES={
"Auburn University College of Veterinary Medicine":"https://www.vetmed.auburn.edu/clinical-services/bailey-small-animal-teaching-hospital/oncology/",
"University of Pennsylvania School of Veterinary Medicine":"https://www.vet.upenn.edu/research/research-centers-and-institute/penn-vet-cancer-center/",
"NC State College of Veterinary Medicine":"https://cvm.ncsu.edu/animal-cancer-center/",
"University of Missouri College of Veterinary Medicine":"https://cvm.missouri.edu/",
"University of Wisconsin–Madison School of Veterinary Medicine":"https://www.vetmed.wisc.edu/",
"Purdue University College of Veterinary Medicine":"https://cancer.research.purdue.edu/research/veterinary-medicine/",
"Ohio State University College of Veterinary Medicine":"https://vmc.vet.osu.edu/services/integrated-oncology-services",
"Texas A&M School of Veterinary Medicine":"https://vetmed.tamu.edu/news/press-releases/clinical-trials-oncology/",
"Louisiana State University School of Veterinary Medicine":"https://www.lsu.edu/vetmed/blog/2026/cancer_research.php",
"Washington State University College of Veterinary Medicine":"https://hospital.vetmed.wsu.edu/small-animal/cats-and-dogs/oncology/",
"Iowa State University College of Veterinary Medicine":"https://vetmed.iastate.edu/vmc/small-animal/specialty-care/oncology/isu-pet-cancer-clinic/",
"Kansas State University College of Veterinary Medicine":"https://www.vet.k-state.edu/academics/clinical-sciences/faculty-staff/faculty/azuma-c/",
"Oregon State University Carlson College of Veterinary Medicine":"https://vetmed.oregonstate.edu/research/oncology-clinical-trials",
"University of Tennessee College of Veterinary Medicine":"https://vetmed.tennessee.edu/vmc/medical-oncology/",
"Mississippi State University College of Veterinary Medicine":"https://www.vetmed.msstate.edu/cs",
"Tufts University Cummings School of Veterinary Medicine":"https://vet.tufts.edu/foster-hospital-small-animals/specialty-services/oncology",
"University of Georgia College of Veterinary Medicine":"https://vet.uga.edu/hospital-and-primary-care/hospital/cora-nunnally-miller-small-animal-hospital/dogs-cats/oncology/",
"Oklahoma State University College of Veterinary Medicine":"https://vetmed.okstate.edu/about/departments/physiological-sciences/oncology_cancer_cell_biology",
"UT Southwestern Veterinary Research and Oncology Clinic":"https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/",
"UC Davis Veterinary Center for Clinical Trials":"https://ccah.vetmed.ucdavis.edu/areas-study/cancer/cancer-clinical-studiestrials",
"Colorado Animal Specialty & Emergency (CASE)":"https://www.coloradoanimalspecialty.com/clinical-studies",
"MedVet Clinical Studies Center":"https://www.medvet.com/clinical-studies/",
"Veterinary Referral Center of Central Oregon":"https://vrcvet.com/clinical-trials/",
"Virginia-Maryland College of Veterinary Medicine / Virginia Tech":"https://research.vetmed.vt.edu/clinical-trials/current-studies.html",
"Anivive Lifesciences multicenter":"https://www.anivive.com/",
"Atlantic Veterinary Internal Medicine & Oncology":"https://www.avim.us/",
"Aurelius Biotherapeutics":"https://aureliusbio.com/",
"CARE Center Cincinnati":"https://carecentervets.com/oncology-services-care-center-cincinnati/",
"First Coast Veterinary Specialists & Emergency":"https://www.fcvets.com/",
"Gulf Coast Veterinary Specialists":"https://www.gcvs.com/services/medical-oncology",
"Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)":"https://www.hopkinsmedicine.org/radiology/veterinarians",
"Massachusetts Veterinary Referral Hospital":"https://www.massvethospital.com/services/oncology",
"Metropolitan Veterinary Hospital":"https://www.metropolitanvet.com/services/oncology",
"Mission Veterinary Emergency & Specialty":"https://www.missionveterinaryspecialists.com/services/oncology",
"Overland Park Veterinary Emergency & Specialty":"https://www.overlandparkveterinaryspecialists.com/services/oncology",
"Peak Veterinary Referral Center":"https://www.peakveterinary.com/services",
"Pet Emergency and Specialty Center of Marin":"https://pescm.com/san-rafael-ca/our-story/",
"SAGE":"https://www.sagecenters.com/services/oncology",
"SAGE Veterinary Centers":"https://www.sagecenters.com/services/oncology",
"Schwarzman Animal Medical Center":"https://www.amcny.org/pet-owners/specialties/oncology/",
"Southeast Veterinary Oncology & Internal Medicine":"https://www.southeastveterinaryoncologyandinternalmedicine.com/",
"Summit Veterinary Referral Center":"https://www.summitvets.com/services",
"Veterinary Specialty Hospital":"https://www.vshsd.com/services/oncology",
"WVRC Grafton":"https://www.wvrcwi.com/services/oncology",
"WVRC Racine Kenosha":"https://www.wvrcwi.com/services/oncology",
"WVRC Waukesha":"https://www.wvrcwi.com/services/oncology",
"Ethos Veterinary Health / Ethos Discovery":"https://www.ethosvet.com/clinical-studies/",
}
DIRECT={
"University of Minnesota College of Veterinary Medicine":"https://vetmed.umn.edu/sites/vetmed.umn.edu/files/styles/folwell_full/public/2024-09/trials-vet-modiano.jpg.avif?itok=mBlyuZZ9",
"Michigan State University College of Veterinary Medicine":"https://cvm.msu.edu/assets/images/hospital/_imageFit350/oncology-2024-photo.jpg",
"University of Florida College of Veterinary Medicine":"https://vetmed-research-a2.sites.medinfo.ufl.edu/wordpress/files/2018/04/Brody_June2015-935x1120.jpg",
"University of Illinois College of Veterinary Medicine":"https://vetmed.illinois.edu/wp-content/uploads/2021/04/pc-radiation-selting.jpg",
"Cornell University College of Veterinary Medicine":"https://www.vet.cornell.edu/sites/default/files/styles/nodecontent_default/public/cute%20terrier.jpg?itok=bnfSQ3QL",
}
STATIC=Path(__file__).resolve().parent/'static'/'images'/'centers'; STATIC.mkdir(parents=True,exist_ok=True)
PREFIX='https://jdizhur-rgb.github.io/vet-trial-matcher/images/centers/'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def candidates(page):
 req=Request(page,headers={'User-Agent':'Mozilla/5.0 VetTrialFinder/1.0'}); text=urlopen(req,timeout=12).read(1200000).decode('utf-8','replace'); out=[]
 for pat in (r'<meta[^>]+property=["\']og:image[^"\']*["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',r'<img[^>]+(?:src|data-src)=["\']([^"\']+)["\']'):
  for m in re.finditer(pat,text,re.I):
   u=urljoin(page,m.group(1).replace('&amp;','&')); low=u.lower()
   if u.startswith('https://') and not any(x in low for x in ('logo','icon','badge','sprite','.svg')): out.append(u)
 return out
def cache(name,page,direct=''):
 urls=([direct] if direct else [])
 try: urls+=candidates(page)
 except Exception as e: print('CENTER_IMAGE_PAGE_WARN',name,e)
 for u in urls:
  try:
   r=urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0 VetTrialFinder/1.0','Referer':page}),timeout=15); data=r.read(8000000); c=(r.headers.get_content_type() or '').lower()
   if len(data)<5000 or not c.startswith('image/'): continue
   ext=mimetypes.guess_extension(c) or '.jpg'; ext='.jpg' if ext=='.jpe' else ext; p=STATIC/(slug(name)+ext); p.write_bytes(data); print('CENTER_IMAGE_LOCAL',name,p.name); return PREFIX+p.name
  except Exception as e: print('CENTER_IMAGE_URL_WARN',name,e)
 return ''
for name in sorted(set(PAGES)|set(DIRECT)):
 page=PAGES.get(name,'https://www.vet.cornell.edu/'); local=cache(name,page,DIRECT.get(name,''))
 if not local: continue
 profile=PROFILES.get(name) or EXTRA_PROFILES.get(name)
 if profile is None:
  profile={'title':name,'about':f'{name} has veterinary cancer treatment or research opportunities represented in our current catalog.','links':[('Official website',page)]}; EXTRA_PROFILES[name]=profile; PROFILES[name]=profile
 profile.update({'image':local,'image_alt':f'Veterinary patient or cancer care program featured by {name}','image_caption':f'Photo: {name}.'})
