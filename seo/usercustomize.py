"""Center-page presentation: useful descriptions, imagery and location rules.

University/academic pages show the institution's veterinary hospital address once near
the overview. Specialty-center/network pages do not show a misleading roll-up address;
physical locations belong to the individual study cards (handled by sitecustomize.py).
"""
import re
import center_image_localizer
import center_image_fallbacks
import center_profiles
import center_profiles_extra
import generate_seo as g

STOCK=center_image_fallbacks.STOCK_LOCAL
FALLBACK={'image':STOCK,'image_alt':'Dog receiving veterinary care','image_caption':'Stock veterinary-care photo: Pexels.'}

CENTER_COPY={
 'Gulf Coast Veterinary Specialists':{'title':'Gulf Coast Veterinary Specialists','about':'Gulf Coast Veterinary Specialists (GCVS) is a multidisciplinary specialty and emergency hospital in Houston with dedicated medical and radiation oncology services. Its cancer team provides advanced diagnostics and treatment and participates in veterinary oncology research. The studies currently represented in our catalog are listed below.','links':[('GCVS Houston hospital','https://www.gcvs.com/locations/houston'),('GCVS oncology team','https://www.gcvs.com/gcvs-houston-team')]},
 'Massachusetts Veterinary Referral Hospital':{'title':'Massachusetts Veterinary Referral Hospital','about':'Massachusetts Veterinary Referral Hospital in Woburn is a multidisciplinary specialty and emergency hospital with a dedicated oncology service. Through the Ethos Veterinary Health research network, eligible cancer patients may have access to selected investigational studies alongside specialty care. Each study below shows the location where enrollment or treatment is offered.','links':[('Massachusetts Veterinary Referral Hospital','https://www.massvetreferral.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')]},
 'Peak Veterinary Referral Center':{'title':'Peak Veterinary Referral Center','about':'Peak Veterinary Referral Center in Williston, Vermont, provides oncology and other advanced referral services. Peak participates in selected veterinary clinical studies through the Ethos Veterinary Health network when a protocol is open locally. Study-specific locations are shown below.','links':[('Peak Veterinary Referral Center','https://www.peakveterinaryreferral.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')]},
 'Mission Veterinary Emergency & Specialty':{'title':'Mission Veterinary Emergency & Specialty','about':'Mission Veterinary Emergency & Specialty in Kansas provides specialty and emergency veterinary care, including oncology. The hospital can participate in selected clinical research through the Ethos Veterinary Health network. Enrollment and study visits depend on the individual protocol, so the participating address is shown with each study below.','links':[('Mission Veterinary Emergency & Specialty','https://www.missionvetspecialists.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')]},
 'First Coast Veterinary Specialists':{'title':'First Coast Veterinary Specialists & Emergency','about':'First Coast Veterinary Specialists & Emergency in Jacksonville Beach is a multidisciplinary referral hospital with veterinary oncology services. The hospital provides specialty cancer care and may serve as a participating site for selected clinical research protocols. Current studies and their locations are listed below.','links':[]},
 'Summit Veterinary Referral Center':{'title':'Summit Veterinary Referral Center','about':'Summit Veterinary Referral Center in Tacoma is a multidisciplinary specialty hospital with a dedicated oncology service. Its team provides advanced cancer diagnostics and treatment and may participate in selected veterinary oncology studies. Current research options and study locations are listed below.','links':[]},
 'CARE Center Cincinnati':{'title':'CARE Center Cincinnati','about':'CARE Center in Cincinnati is a specialty and emergency veterinary hospital offering advanced referral care, including oncology. Cancer research opportunities associated with this hospital are listed below with protocol-specific details, contacts and locations.','links':[]},
 'Overland Park Veterinary Emergency':{'title':'Overland Park Veterinary Emergency & Specialty','about':'Overland Park Veterinary Emergency & Specialty provides multidisciplinary specialty and emergency care, including oncology. Selected veterinary clinical studies may enroll through the hospital when it is a participating site. The exact study location is shown with each research option below.','links':[]},
 'Colorado Animal Specialty & Emergency':{'title':'Colorado Animal Specialty & Emergency (CASE)','about':'Colorado Animal Specialty & Emergency (CASE) in Boulder is a multidisciplinary specialty and emergency hospital with oncology services and an active clinical-studies program. CASE participates in veterinary cancer research through Ethos Discovery and other collaborations. Current studies and participating locations are listed below.','links':[('CASE clinical studies','https://www.coloradoanimalspecialty.com/clinical-studies')]},
}

class CenterProfiles(dict):
 def __missing__(self,key):
  lower=g.norm(key)
  if any(x in lower for x in ('university','college','johns hopkins','ut southwestern')):
   about=f'{key} is an academic veterinary or comparative-medicine center involved in companion-animal cancer research. The program combines clinical care with studies of new diagnostics and treatments; current research represented in our catalog is listed below with eligibility, contacts and participating locations.'
  elif any(x in lower for x in ('health','ethos','medvet','sage','network')):
   about=f'{key} is a veterinary specialty or research network involved in companion-animal clinical studies. Individual protocols may run at only selected hospitals, so each study below shows its participating location rather than a single network-wide address.'
  else:
   about=f'{key} is a veterinary specialty or research center involved in companion-animal cancer care and clinical research. Current studies are listed below with practical enrollment details, contacts and the location where each study is conducted.'
  p={'title':key,'about':about,'links':[],**FALLBACK};self[key]=p;return p

def fill_profiles(mapping):
 for actual,p in list(mapping.items()):
  na=g.norm(actual)
  for wanted,patch in CENTER_COPY.items():
   nw=g.norm(wanted)
   if nw in na or na in nw:
    p.update(patch);break
 for wanted,patch in CENTER_COPY.items():
  if not any(g.norm(wanted) in g.norm(k) or g.norm(k) in g.norm(wanted) for k in mapping):mapping[wanted]=dict(patch)
 for p in mapping.values():
  if isinstance(p,dict) and not p.get('image'):p.update(FALLBACK)
 return CenterProfiles(mapping)

center_profiles.PROFILES=fill_profiles(dict(center_profiles.PROFILES))
center_profiles_extra.EXTRA_PROFILES=fill_profiles(dict(center_profiles_extra.EXTRA_PROFILES))

# Academic pages: show the veterinary institution/hospital address once on the page.
# Non-academic specialty centers intentionally are NOT in this mapping; their addresses
# are rendered under the individual studies by sitecustomize.py.
ACADEMIC_PAGE_ADDRESSES={
 'auburn-university':'Bailey Small Animal Teaching Hospital, 1220 Wire Rd, Auburn, AL 36849',
 'colorado-state-university-flint-animal-cancer-center':'Flint Animal Cancer Center, 300 W Drake Rd, Fort Collins, CO 80523',
 'cornell-university':'Cornell University Hospital for Animals, 930 Campus Rd, Ithaca, NY 14853',
 'louisiana-state-university':'LSU Veterinary Teaching Hospital, 1909 Skip Bertman Dr, Baton Rouge, LA 70803',
 'michigan-state-university':'Michigan State University Veterinary Medical Center, 736 Wilson Rd, East Lansing, MI 48824',
 'nc-state':'NC State Veterinary Hospital, 1052 William Moore Dr, Raleigh, NC 27607',
 'ohio-state-university':'The Ohio State University Veterinary Medical Center, 601 Vernon L Tharp St, Columbus, OH 43210',
 'purdue-university':'Purdue University Veterinary Hospital, 625 Harrison St, West Lafayette, IN 47907',
 'texas-a-m':'Texas A&M Small Animal Teaching Hospital, 408 Raymond Stotzer Pkwy, College Station, TX 77845',
 'tufts-university-cummings':'Henry and Lois Foster Hospital for Small Animals, 200 Westboro Rd, North Grafton, MA 01536',
 'uc-davis-veterinary-center-for-clinical-trials':'UC Davis Veterinary Medical Teaching Hospital, 1 Garrod Dr, Davis, CA 95616',
 'university-of-florida':'UF Small Animal Hospital, 2015 SW 16th Ave, Gainesville, FL 32608',
 'university-of-georgia':'UGA Veterinary Teaching Hospital, 2200 College Station Rd, Athens, GA 30602',
 'university-of-illinois':'University of Illinois Veterinary Teaching Hospital, 1008 W Hazelwood Dr, Urbana, IL 61802',
 'university-of-minnesota':'University of Minnesota Veterinary Medical Center, 1365 Gortner Ave, St Paul, MN 55108',
 'university-of-missouri':'University of Missouri Veterinary Health Center, 900 E Campus Dr, Columbia, MO 65211',
 'university-of-pennsylvania':'Penn Vet Ryan Veterinary Hospital, 3900 Spruce St, Philadelphia, PA 19104',
 'washington-state-university':'WSU Veterinary Teaching Hospital, 205 Ott Rd, Pullman, WA 99164',
}

_previous_page=g.page
def page_with_center_address(title,desc,body,canonical,lang='en',alts=None):
 rendered=_previous_page(title,desc,body,canonical,lang,alts)
 if lang=='en' and '/centers/' in canonical and not canonical.rstrip('/').endswith('/centers'):
  slug=canonical.rstrip('/').rsplit('/',1)[-1]
  address=ACADEMIC_PAGE_ADDRESSES.get(slug)
  if address and '<section class="center-locations">' not in rendered:
   block='<section class="center-locations university-location"><h2>Location</h2><p>'+g.esc(address)+'</p></section>'
   overview=re.search(r'<div class="center-overview"[^>]*>.*?</div>',rendered,re.S)
   if overview:rendered=rendered[:overview.end()]+block+rendered[overview.end():]
   else:
    h1=re.search(r'</h1>',rendered,re.S)
    rendered=rendered[:h1.end()]+block+rendered[h1.end():] if h1 else block+rendered
 # Center-page heading was visually much too large. Keep disease SEO pages unchanged.
 if lang=='en' and '/centers/' in canonical:
  polish='.center-overview h2{margin-top:18px}.university-location{margin:14px 0 20px;padding:12px 15px;background:#f6f8fb;border-radius:10px}.university-location h2{font-size:1rem;margin:0 0 4px}.university-location p{margin:0;color:#42536a}@media(min-width:601px){main>h1{font-size:clamp(1.7rem,3.2vw,2.25rem);line-height:1.15;margin-top:24px}}'
  rendered=rendered.replace('</style>',polish+'</style>',1)
 return rendered
g.page=page_with_center_address
