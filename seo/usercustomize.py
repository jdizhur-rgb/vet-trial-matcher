"""Load official center imagery and guarantee a local stock fallback."""
import center_image_localizer
import center_image_fallbacks
import center_profiles
import center_profiles_extra

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

# Fill BOTH dictionaries because generate_seo_strict merges EXTRA_PROFILES over PROFILES.
# This makes an image mandatory regardless of which profile dictionary owns the center.
center_profiles.PROFILES=fill_images(dict(center_profiles.PROFILES))
center_profiles_extra.EXTRA_PROFILES=fill_images(dict(center_profiles_extra.EXTRA_PROFILES))
