"""Load official center imagery, stock fallback, useful center copy, and physical addresses."""
import re
import center_image_localizer
import center_image_fallbacks
import center_profiles
import center_profiles_extra
import generate_seo as g

STOCK=center_image_fallbacks.STOCK_LOCAL
FALLBACK={'image':STOCK,'image_alt':'Dog receiving veterinary care','image_caption':'Stock veterinary-care photo: Pexels.'}

# Specific public-facing descriptions for hospital pages that previously fell through to a placeholder.
CENTER_COPY={
 'Gulf Coast Veterinary Specialists':{
  'title':'About Gulf Coast Veterinary Specialists',
  'about':'Gulf Coast Veterinary Specialists (GCVS) in Houston is a large multidisciplinary specialty and emergency hospital with dedicated medical oncology and radiation oncology services. Its cancer team provides advanced diagnostics and treatment and participates in veterinary oncology research represented in our current catalog.',
  'links':[('GCVS Houston hospital','https://www.gcvs.com/locations/houston'),('GCVS oncology team','https://www.gcvs.com/gcvs-houston-team')],
 },
 'Massachusetts Veterinary Referral Hospital':{
  'title':'About Massachusetts Veterinary Referral Hospital',
  'about':'Massachusetts Veterinary Referral Hospital in Woburn is a multidisciplinary specialty and emergency hospital with a dedicated oncology service. The hospital participates in clinical research through the Ethos Veterinary Health network, giving eligible cancer patients access to selected investigational studies alongside specialty care.',
  'links':[('Massachusetts Veterinary Referral Hospital','https://www.massvetreferral.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')],
 },
 'Peak Veterinary Referral Center':{
  'title':'About Peak Veterinary Referral Center',
  'about':'Peak Veterinary Referral Center in Williston, Vermont, is a specialty hospital providing oncology and other advanced referral services. As part of the Ethos Veterinary Health network, Peak can serve as a participating site for selected veterinary clinical studies when a protocol is open locally.',
  'links':[('Peak Veterinary Referral Center','https://www.peakveterinaryreferral.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')],
 },
 'Mission Veterinary Emergency & Specialty':{
  'title':'About Mission Veterinary Emergency & Specialty',
  'about':'Mission Veterinary Emergency & Specialty in Mission, Kansas, provides specialty and emergency veterinary care including oncology. The hospital participates in selected clinical research through the Ethos Veterinary Health network, with enrollment and study visits handled according to each protocol.',
  'links':[('Mission Veterinary Emergency & Specialty','https://www.missionvetspecialists.com/'),('Ethos clinical studies','https://www.ethosvet.com/clinical-studies/')],
 },
}

class CenterProfiles(dict):
 def __missing__(self,key):
  # Never publish the old catalog-placeholder sentence. Use a concise factual description
  # based on the center's role; study-specific claims remain in the cards below.
  lower=g.norm(key)
  if any(x in lower for x in ('university','college','johns hopkins','ut southwestern')):
   about=f'{key} is an academic veterinary or comparative-medicine program participating in companion-animal clinical research. The current cancer studies associated with this center are listed below with study-specific eligibility, contacts and participating locations.'
  elif any(x in lower for x in ('health','ethos','medvet','sage')):
   about=f'{key} is a veterinary specialty or research network participating in companion-animal clinical studies. Because individual protocols may run at only selected hospitals, the participating locations for each current cancer study are shown with that study below.'
  else:
   about=f'{key} is a veterinary specialty or research center participating in companion-animal cancer care or clinical research. Current studies associated with this center are listed below with study-specific eligibility, contacts and verified participating locations where available.'
  p={'title':f'About {key}','about':about,'links':[],**FALLBACK}
  self[key]=p
  return p

def fill_profiles(mapping):
 for name,patch in CENTER_COPY.items():
  if name in mapping: mapping[name].update(patch)
  else: mapping[name]={**patch}
 for p in mapping.values():
  if isinstance(p,dict) and not p.get('image'): p.update(FALLBACK)
 return CenterProfiles(mapping)

center_profiles.PROFILES=fill_profiles(dict(center_profiles.PROFILES))
center_profiles_extra.EXTRA_PROFILES=fill_profiles(dict(center_profiles_extra.EXTRA_PROFILES))

# One patient-facing physical address for true single-site university/center pages.
# Network/roll-up pages intentionally have no aggregate address here; their participating
# hospitals and full addresses are rendered inside the relevant study cards.
CENTER_PAGE_ADDRESSES={
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
 'gulf-coast-veterinary-specialists':'Gulf Coast Veterinary Specialists, 8042 Katy Fwy, Houston, TX 77024',
 'massachusetts-veterinary-referral-hospital':'Massachusetts Veterinary Referral Hospital, 20 Cabot Rd, Woburn, MA 01801',
 'peak-veterinary-referral-center':'Peak Veterinary Referral Center, 158 Hurricane Ln, Williston, VT 05495',
 'mission-veterinary-emergency-specialty':'Mission Veterinary Emergency & Specialty, 5914 Johnson Dr, Mission, KS 66202',
 'overland-park-veterinary-emergency-specialty':'Overland Park Veterinary Emergency and Specialty, 8301 W 163rd St, Overland Park, KS 66223',
 'first-coast-veterinary-specialists-emergency':'First Coast Veterinary Specialists & Emergency, 301 Jacksonville Dr, Jacksonville Beach, FL 32250',
 'summit-veterinary-referral-center':'Summit Veterinary Referral Center, 2505 S 80th St, Tacoma, WA 98409',
 'care-center-cincinnati':'CARE Center, 6995 E Kemper Rd, Cincinnati, OH 45249',
 'case':'Colorado Animal Specialty & Emergency (CASE), 2972 Iris Ave, Boulder, CO 80301',
}

_previous_page=g.page

def page_with_center_address(title,desc,body,canonical,lang='en',alts=None):
 if lang=='en' and '/centers/' in canonical and not canonical.rstrip('/').endswith('/centers'):
  slug=canonical.rstrip('/').rsplit('/',1)[-1]
  address=CENTER_PAGE_ADDRESSES.get(slug)
  if address and '<section class="center-locations">' not in body:
   block='<section class="center-locations"><h2>Location</h2><ul><li>'+g.esc(address)+'</li></ul></section>'
   overview=re.search(r'<div class="center-overview"[^>]*>.*?</div>',body,re.S)
   if overview: body=body[:overview.end()]+block+body[overview.end():]
   else: body=block+body
 return _previous_page(title,desc,body,canonical,lang,alts)

g.page=page_with_center_address
