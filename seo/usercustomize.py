"""Load official center imagery, stock fallback, useful center copy, and physical addresses."""
import re
import center_image_localizer
import center_image_fallbacks
import center_profiles
import center_profiles_extra
import generate_seo as g

STOCK=center_image_fallbacks.STOCK_LOCAL
FALLBACK={'image':STOCK,'image_alt':'Dog receiving veterinary care','image_caption':'Stock veterinary-care photo: Pexels.'}

CENTER_COPY={
 'Gulf Coast Veterinary Specialists':{'title':'About Gulf Coast Veterinary Specialists','about':'Gulf Coast Veterinary Specialists (GCVS) in Houston is a multidisciplinary specialty and emergency hospital with dedicated medical oncology and radiation oncology services. Its cancer team provides advanced diagnostics and treatment and participates in veterinary oncology research represented in our current catalog.','links':[('GCVS Houston hospital','https://www.gcvs.com/locations/houston'),('GCVS oncology team','https://www.gcvs.com/gcvs-houston-team')]},
 'Massachusetts Veterinary Referral Hospital':{'title':'About Massachusetts Veterinary Referral Hospital','about':'Massachusetts Veterinary Referral Hospital in Woburn is a multidisciplinary specialty and emergency hospital with a dedicated oncology service. The hospital participates in clinical research through the Ethos Veterinary Health network, giving eligible cancer patients access to selected investigational studies alongside specialty care.','links':[('Massachusetts Veterinary Referral Hospital','https://www.massvetreferral.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')]},
 'Peak Veterinary Referral Center':{'title':'About Peak Veterinary Referral Center','about':'Peak Veterinary Referral Center in Williston, Vermont, is a specialty hospital providing oncology and other advanced referral services. As part of the Ethos Veterinary Health network, Peak can serve as a participating site for selected veterinary clinical studies when a protocol is open locally.','links':[('Peak Veterinary Referral Center','https://www.peakveterinaryreferral.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')]},
 'Mission Veterinary Emergency & Specialty':{'title':'About Mission Veterinary Emergency & Specialty','about':'Mission Veterinary Emergency & Specialty in Mission, Kansas, provides specialty and emergency veterinary care including oncology. The hospital participates in selected clinical research through the Ethos Veterinary Health network, with enrollment and study visits handled according to each protocol.','links':[('Mission Veterinary Emergency & Specialty','https://www.missionvetspecialists.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')]},
 'First Coast Veterinary Specialists':{'title':'About First Coast Veterinary Specialists','about':'First Coast Veterinary Specialists & Emergency in Jacksonville Beach is a multidisciplinary referral hospital with veterinary oncology services. Cancer patients may be evaluated for specialty treatment and for selected clinical research protocols represented in our catalog.','links':[]},
 'Summit Veterinary Referral Center':{'title':'About Summit Veterinary Referral Center','about':'Summit Veterinary Referral Center in Tacoma is a multidisciplinary specialty hospital with a dedicated oncology service. The hospital provides advanced cancer diagnostics and treatment and may participate in selected veterinary oncology studies listed in our catalog.','links':[]},
 'CARE Center Cincinnati':{'title':'About CARE Center Cincinnati','about':'CARE Center in Cincinnati is a specialty and emergency veterinary hospital offering advanced referral care, including oncology. Current cancer research opportunities associated with this hospital are listed below with protocol-specific contacts and locations.','links':[]},
 'Overland Park Veterinary Emergency':{'title':'About Overland Park Veterinary Emergency & Specialty','about':'Overland Park Veterinary Emergency & Specialty in Kansas provides multidisciplinary specialty and emergency care, including oncology. Selected veterinary clinical studies may enroll through the hospital when it is listed as a participating site.','links':[]},
 'Colorado Animal Specialty & Emergency':{'title':'About Colorado Animal Specialty & Emergency','about':'Colorado Animal Specialty & Emergency (CASE) in Boulder is a multidisciplinary specialty and emergency hospital with oncology services and an active clinical-studies program. CASE participates in veterinary cancer research through Ethos Discovery and other research collaborations.','links':[('CASE clinical studies','https://www.coloradoanimalspecialty.com/clinical-studies')]},
}

class CenterProfiles(dict):
 def __missing__(self,key):
  lower=g.norm(key)
  if any(x in lower for x in ('university','college','johns hopkins','ut southwestern')):
   about=f'{key} is an academic veterinary or comparative-medicine center involved in companion-animal clinical research. Its current cancer studies are listed below with study-specific eligibility, contacts and participating locations.'
  elif any(x in lower for x in ('health','ethos','medvet','sage','network')):
   about=f'{key} is a veterinary specialty or research network involved in companion-animal clinical studies. Individual protocols may run at only selected hospitals, so participating locations are shown with each study below.'
  else:
   about=f'{key} is a veterinary specialty or research center involved in companion-animal cancer care or clinical research. Current studies associated with this center are listed below with eligibility, contacts and participating locations where available.'
  p={'title':f'About {key}','about':about,'links':[],**FALLBACK}; self[key]=p; return p

def fill_profiles(mapping):
 # Match copy by normalized name, not exact spelling. Center names in the catalog often
 # carry suffixes such as (GCVS), / Ethos Discovery, or & Emergency.
 for actual,p in list(mapping.items()):
  na=g.norm(actual)
  for wanted,patch in CENTER_COPY.items():
   nw=g.norm(wanted)
   if nw in na or na in nw:
    p.update(patch); break
 for wanted,patch in CENTER_COPY.items():
  if not any(g.norm(wanted) in g.norm(k) or g.norm(k) in g.norm(wanted) for k in mapping): mapping[wanted]=dict(patch)
 for p in mapping.values():
  if isinstance(p,dict) and not p.get('image'): p.update(FALLBACK)
 return CenterProfiles(mapping)

center_profiles.PROFILES=fill_profiles(dict(center_profiles.PROFILES))
center_profiles_extra.EXTRA_PROFILES=fill_profiles(dict(center_profiles_extra.EXTRA_PROFILES))

CENTER_PAGE_ADDRESSES={
 'auburn-university':'Bailey Small Animal Teaching Hospital, 1220 Wire Rd, Auburn, AL 36849','colorado-state-university-flint-animal-cancer-center':'Flint Animal Cancer Center, 300 W Drake Rd, Fort Collins, CO 80523','cornell-university':'Cornell University Hospital for Animals, 930 Campus Rd, Ithaca, NY 14853','louisiana-state-university':'LSU Veterinary Teaching Hospital, 1909 Skip Bertman Dr, Baton Rouge, LA 70803','michigan-state-university':'Michigan State University Veterinary Medical Center, 736 Wilson Rd, East Lansing, MI 48824','nc-state':'NC State Veterinary Hospital, 1052 William Moore Dr, Raleigh, NC 27607','ohio-state-university':'The Ohio State University Veterinary Medical Center, 601 Vernon L Tharp St, Columbus, OH 43210','purdue-university':'Purdue University Veterinary Hospital, 625 Harrison St, West Lafayette, IN 47907','texas-a-m':'Texas A&M Small Animal Teaching Hospital, 408 Raymond Stotzer Pkwy, College Station, TX 77845','tufts-university-cummings':'Henry and Lois Foster Hospital for Small Animals, 200 Westboro Rd, North Grafton, MA 01536','uc-davis-veterinary-center-for-clinical-trials':'UC Davis Veterinary Medical Teaching Hospital, 1 Garrod Dr, Davis, CA 95616','university-of-florida':'UF Small Animal Hospital, 2015 SW 16th Ave, Gainesville, FL 32608','university-of-georgia':'UGA Veterinary Teaching Hospital, 2200 College Station Rd, Athens, GA 30602','university-of-illinois':'University of Illinois Veterinary Teaching Hospital, 1008 W Hazelwood Dr, Urbana, IL 61802','university-of-minnesota':'University of Minnesota Veterinary Medical Center, 1365 Gortner Ave, St Paul, MN 55108','university-of-missouri':'University of Missouri Veterinary Health Center, 900 E Campus Dr, Columbia, MO 65211','university-of-pennsylvania':'Penn Vet Ryan Veterinary Hospital, 3900 Spruce St, Philadelphia, PA 19104','washington-state-university':'WSU Veterinary Teaching Hospital, 205 Ott Rd, Pullman, WA 99164','gulf-coast-veterinary-specialists':'Gulf Coast Veterinary Specialists, 8042 Katy Fwy, Houston, TX 77024','massachusetts-veterinary-referral-hospital':'Massachusetts Veterinary Referral Hospital, 20 Cabot Rd, Woburn, MA 01801','peak-veterinary-referral-center':'Peak Veterinary Referral Center, 158 Hurricane Ln, Williston, VT 05495','mission-veterinary-emergency-specialty':'Mission Veterinary Emergency & Specialty, 5914 Johnson Dr, Mission, KS 66202','overland-park-veterinary-emergency-specialty':'Overland Park Veterinary Emergency and Specialty, 8301 W 163rd St, Overland Park, KS 66223','first-coast-veterinary-specialists-emergency':'First Coast Veterinary Specialists & Emergency, 301 Jacksonville Dr, Jacksonville Beach, FL 32250','summit-veterinary-referral-center':'Summit Veterinary Referral Center, 2505 S 80th St, Tacoma, WA 98409','care-center-cincinnati':'CARE Center, 6995 E Kemper Rd, Cincinnati, OH 45249','case':'Colorado Animal Specialty & Emergency (CASE), 2972 Iris Ave, Boulder, CO 80301','sage':'SAGE Veterinary Centers, 600 Alabama St, San Francisco, CA 94110','sage-veterinary-centers':'SAGE Veterinary Centers, 600 Alabama St, San Francisco, CA 94110',
}

_previous_page=g.page
def page_with_center_address(title,desc,body,canonical,lang='en',alts=None):
 if lang=='en' and '/centers/' in canonical and not canonical.rstrip('/').endswith('/centers'):
  slug=canonical.rstrip('/').rsplit('/',1)[-1]; address=CENTER_PAGE_ADDRESSES.get(slug)
  if address and '<section class="center-locations">' not in body:
   block='<section class="center-locations"><h2>Location</h2><ul><li>'+g.esc(address)+'</li></ul></section>'
   overview=re.search(r'<div class="center-overview"[^>]*>.*?</div>',body,re.S)
   body=body[:overview.end()]+block+body[overview.end():] if overview else block+body
 return _previous_page(title,desc,body,canonical,lang,alts)
g.page=page_with_center_address
