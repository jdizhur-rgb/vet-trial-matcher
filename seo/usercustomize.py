"""Load official center imagery, stock fallback, and physical center addresses."""
import re
import center_image_localizer
import center_image_fallbacks
import center_profiles
import center_profiles_extra
import generate_seo as g

STOCK=center_image_fallbacks.STOCK_LOCAL
FALLBACK={'image':STOCK,'image_alt':'Dog receiving veterinary care','image_caption':'Stock veterinary-care photo: Pexels.'}

class CenterProfiles(dict):
 def __missing__(self,key):
  p={'title':f'About {key}','about':f'{key} currently has veterinary cancer treatment or research opportunities represented in our catalog.','links':[],**FALLBACK}
  self[key]=p
  return p

def fill_images(mapping):
 for p in mapping.values():
  if isinstance(p,dict) and not p.get('image'): p.update(FALLBACK)
 return CenterProfiles(mapping)

center_profiles.PROFILES=fill_images(dict(center_profiles.PROFILES))
center_profiles_extra.EXTRA_PROFILES=fill_images(dict(center_profiles_extra.EXTRA_PROFILES))

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
