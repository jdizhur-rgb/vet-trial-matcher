"""Owner-facing SEO presentation and study-specific participating locations."""
import re
import json
import generate_seo as g

_original_cards=g.cards
_original_page=g.page

_CURRENT_STATUS_CONFIDENCE={'current','confirmed_current'}
def _merge_catalog_record(old,patch):
 new=dict(old)
 for key,value in patch.items():
  if key in {'requires','excludes'} and isinstance(value,dict):
   nested=dict(new.get(key,{}) if isinstance(new.get(key),dict) else {})
   nested.update(value); new[key]=nested
  else:new[key]=value
 return new
def _live_effective_catalog():
 root=g.ROOT
 base=json.loads((root/'data'/'trials_base.json').read_text())
 rows={r['id']:r for r in base}
 patch_paths=[root/'data'/'trial_updates.json']+sorted((root/'data').glob('catalog_patch_*.json'))
 for path in patch_paths:
  if not path.exists():continue
  doc=json.loads(path.read_text())
  for rid in doc.get('delete',[]):rows.pop(rid,None)
  for patch in doc.get('upsert',[]):rows[patch['id']]=_merge_catalog_record(rows.get(patch['id'],{}),patch)
 return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True and r.get('status_confidence') in _CURRENT_STATUS_CONFIDENCE]
g.load_effective=_live_effective_catalog

_RAW_TITLE_SITE_FALLBACKS={
'canine b-cell lymphoma study':['Colorado Animal Specialty & Emergency (CASE) — Boulder, CO','Overland Park Veterinary & Specialty (OPVES) — Overland Park, KS','Veterinary Specialty Hospital — Sorrento Valley, CA'],
'canine epitheliotropic lymphosarcoma sample collection study':['Overland Park Veterinary Emergency and Specialty — Overland Park, KS','Nashville Veterinary Specialists — Nashville, TN','Gulf Coast Veterinary Specialists (GCVS) — Houston, TX','Peak Veterinary Referral Center — Williston, VT'],
'canine oncology sample study':['Charleston Veterinary Referral Center (CVRC) — Charleston, SC','Boston West Veterinary Emergency and Specialty — Natick, MA','Massachusetts Veterinary Referral Hospital (MVRH) — Woburn, MA','Metropolitan Veterinary Hospital — Cleveland, OH','Metropolitan Veterinary Hospital — Akron, OH','Pacific Northwest Pet ER & Specialty Center (PACWVETS) — Vancouver, WA','SAGE — San Francisco, CA','Southeast Veterinary Oncology & Internal Medicine — Jacksonville, FL','Upstate Vet Emergency + Specialty Care — Greenville, SC','Veterinary Specialty Hospital – North County — San Marcos, CA','Animal Medical Center of Plainfield — Plainfield, IL','Eastern Carolina Veterinary Medical Center — Wilmington, NC','Spanaway Veterinary Clinic — Spanaway, WA'],
'fine needle aspirate sample study wave 2':['Animal Emergency Hospital (AEH) — Bel Air, MD','Metropolitan Veterinary Hospital — Cleveland, OH','Boston West Veterinary Emergency & Specialty — Natick, MA','Metropolitan Veterinary Hospital — Akron, OH','Pacific Northwest Pet Emergency & Specialty Center (PACWVETS) — Vancouver, WA','Premier Vet Group — Orland Park, IL','SAGE San Francisco — San Francisco, CA','McAbee Veterinary Hospital — Winter Park, FL','Sumner Veterinary Hospital — Sumner, WA'],
'osteosarcoma vaccine study':['Colorado Animal Specialty & Emergency (CASE) — Boulder, CO','First Coast Veterinary Specialists & Emergency — Jacksonville Beach, FL','Metropolitan Veterinary Hospital — Cleveland, OH','Metropolitan Veterinary Hospital — Akron, OH','Massachusetts Veterinary Referral Hospital (MVRH) — Woburn, MA','Mission Veterinary Emergency & Specialty — Mission, KS','Peak Veterinary Referral Center — Williston, VT','Southeast Veterinary Oncology & Internal Medicine — Orange Park, FL','Veterinary Specialty Hospital – North County — San Marcos, CA'],
'canalevia real world data study':['Charleston Veterinary Referral Center (CVRC) — Charleston, SC','Colorado Animal Specialty & Emergency (CASE) — Boulder, CO','Gulf Coast Veterinary Specialists (GCVS) — Houston, TX','Metropolitan Veterinary Hospital — Akron, OH','Mission Veterinary Emergency & Specialty — Mission, KS','Peak Veterinary Referral Center — Williston, VT'],
'melanoma treatment study':['Metropolitan Veterinary Hospital — Cleveland, OH','Summit Veterinary Referral Center — Tacoma, WA','Veterinary Specialty Hospital — San Diego, CA'],
'experimental egfr/her2 tumor vaccine':['MedVet Salt Lake City — Salt Lake City, UT','MedVet Cincinnati — Cincinnati, OH (established patients only)','MedVet Cleveland — Cleveland, OH (established patients only)','MedVet Pittsburgh — Pittsburgh, PA (Pennsylvania residents only)']}
TITLE_SITE_FALLBACKS={g.norm(k):v for k,v in _RAW_TITLE_SITE_FALLBACKS.items()}

def _active(s):return isinstance(s,dict) and s.get('available_for_matching') is not False and not any(x in g.norm(s.get('status','')) for x in ('not enrolling','enrollment closed','closed','paused'))
def _site_label(s):
 name=str(s.get('hospital') or s.get('name') or '').strip(); address=str(s.get('address') or '').strip(); city=str(s.get('city') or '').strip(); state=str(s.get('state') or '').strip(); zipcode=str(s.get('zip') or s.get('zipcode') or '').strip(); location=str(s.get('location') or '').strip()
 geo=', '.join(x for x in (city,state) if x)+((' '+zipcode) if zipcode else '')
 detail=', '.join(x for x in (address,geo.strip()) if x)
 if location and g.norm(location) not in g.norm(detail):detail=', '.join(x for x in (detail,location) if x)
 return f'{name} — {detail}' if name and detail else name or detail
def _row_sites(row):
 vals=[_site_label(s) for s in row.get('sites',[]) if _active(s)] if isinstance(row.get('sites'),list) else []
 vals=[x for x in vals if x]
 if not vals:vals=list(TITLE_SITE_FALLBACKS.get(g.norm(row.get('title','')),[]))
 if not vals:
  address=str(row.get('address') or '').strip(); city=str(row.get('city') or '').strip(); state=str(row.get('state') or '').strip(); location=str(row.get('location') or '').strip(); direct=', '.join(x for x in (address,', '.join(x for x in (city,state) if x)) if x) or location
  if direct and g.norm(direct) not in ('multiple','usa','united states'):vals=[direct]
 out=[];seen=set()
 for value in vals:
  value=re.sub(r'\s+',' ',str(value)).strip(' ,');key=g.norm(value)
  if key and key not in ('multiple','co') and key not in seen:seen.add(key);out.append(value)
 return out
def _locations_html(row):
 sites=_row_sites(row)
 if not sites:return ''
 label='Location' if len(sites)==1 else 'Participating locations'
 return '<div class="study-locations"><p class="field-label">'+label+'</p><ul>'+''.join(f'<li>{g.esc(x)}</li>' for x in sites)+'</ul></div>'
def cards_with_locations(rows):
 rows=list(rows);html=_original_cards(rows);cards=re.findall(r'<article class="card">.*?</article>',html,flags=re.S)
 if len(cards)!=len(rows):return html
 out=[]
 for row,card in zip(rows,cards):
  card=card.replace('<b>Treatment:</b>','<b>What is being offered:</b>').replace('<b>Key eligibility:</b>','<b>Who may qualify:</b>').replace('<b>Important exclusions:</b>','<b>May not qualify if:</b>').replace('<b>Costs:</b>','<b>Costs / coverage:</b>')
  loc=_locations_html(row)
  if loc:card=card.replace('</article>',loc+'</article>')
  out.append(card)
 return ''.join(out)
def _remove_network_rollup(body):
 def repl(m):
  section=m.group(0)
  return section if section.count('<li>')==1 else ''
 return re.sub(r'<section class="center-locations">.*?</section>',repl,body,flags=re.S)
def _rebuild_center_body(body):
 body=_remove_network_rollup(body)
 body=re.sub(r'<h2>Current treatment &amp; research opportunities</h2><p>.*?</p>','<h2>Cancer treatment &amp; research options</h2><p class="section-intro">Details for each current option are below, including eligibility, costs, contacts and participating locations.</p>',body,count=1,flags=re.S)
 return body
def owner_page(title,desc,body,canonical,lang='en',alts=None):
 if lang=='en':
  if '/centers/' in canonical and not canonical.rstrip('/').endswith('/centers'):
   body=_rebuild_center_body(body);desc=desc.replace('Current veterinary cancer clinical trials and treatment studies','Dog and cat cancer treatment options, research studies and clinical trials')
  elif '/north-america/' in canonical:body=body.replace('<h2>Treatment &amp; research</h2>','<h2>Current treatment &amp; research options</h2>')
 rendered=_original_page(title,desc,body,canonical,lang,alts)
 css='.study-locations{margin:15px 0 4px;padding:12px 14px;background:#f6f8fb;border-radius:10px}.study-locations ul{margin:5px 0 0;padding-left:20px}.field-label{font-weight:750;margin:0}.section-intro{color:#42536a;margin-top:0}.card p{margin:.7rem 0}.card .meta{margin-top:.2rem}.free-note{font-size:.78rem;color:#607086;text-align:center;margin:-8px 0 24px}'
 return rendered.replace('</style>',css+'</style>',1)
g.cards=cards_with_locations
g.page=owner_page
