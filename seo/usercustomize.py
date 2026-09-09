"""Load official center imagery and guarantee a local stock fallback."""
import center_image_localizer
import center_image_fallbacks
import center_profiles
import center_profiles_extra

STOCK='https://jdizhur-rgb.github.io/vet-trial-matcher/images/centers/stock-veterinary-dog.jpg'

class CenterProfiles(dict):
 def __missing__(self,key):
  p={
   'title':f'About {key}',
   'about':f'{key} currently has veterinary cancer treatment or research opportunities represented in our catalog.',
   'image':STOCK,
   'image_alt':'Dog receiving veterinary care',
   'image_caption':'Stock veterinary-care photo: Pexels.',
   'links':[],
  }
  self[key]=p
  return p

# Keep every verified official image already collected; only unknown/unavailable centers use stock.
profiles=CenterProfiles(center_profiles.PROFILES)
profiles.update(center_profiles_extra.EXTRA_PROFILES)
for name,p in profiles.items():
 if isinstance(p,dict) and not p.get('image'):
  p.update({'image':STOCK,'image_alt':'Dog receiving veterinary care','image_caption':'Stock veterinary-care photo: Pexels.'})
center_profiles.PROFILES=profiles
center_profiles_extra.EXTRA_PROFILES=CenterProfiles(center_profiles_extra.EXTRA_PROFILES)
