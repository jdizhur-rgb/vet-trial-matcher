"""Owner-facing SEO presentation and study-specific participating locations."""
import re,json
import generate_seo as g

_original_cards=g.cards
_original_page=g.page
_CURRENT_STATUS_CONFIDENCE={'current','confirmed_current'}

def _merge_catalog_record(old,patch):
 new=dict(old)
 for key,value in patch.items():
  if key in {'requires','excludes'} and isinstance(value,dict):
   nested=dict(new.get(key,{}) if isinstance(new.get(key),dict) else {});nested.update(value);new[key]=nested
  else:new[key]=value
 return new

def _live_effective_catalog():
 root=g.ROOT;base=json.loads((root/'data'/'trials_base.json').read_text());rows={r['id']:r for r in base}
 for path in [root/'data'/'trial_updates.json']+sorted((root/'data').glob('catalog_patch_*.json')):
  if not path.exists():continue
  doc=json.loads(path.read_text())
  for rid in doc.get('delete',[]):rows.pop(rid,None)
  for patch in doc.get('upsert',[]):rows[patch['id']]=_merge_catalog_record(rows.get(patch['id'],{}),patch)
 return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True and r.get('status_confidence') in _CURRENT_STATUS_CONFIDENCE]
g.load_effective=_live_effective_catalog

# Verified street addresses. Incomplete city/state fallbacks are deliberately not rendered.
SITE_ADDRESSES={
 'colorado animal specialty & emergency (case)':'Colorado Animal Specialty & Emergency (CASE) — 2972 Iris Ave, Boulder, CO 80301',
 'colorado animal specialty & emergency (case) — boulder, co':'Colorado Animal Specialty & Emergency (CASE) — 2972 Iris Ave, Boulder, CO 80301',
 'overland park veterinary & specialty (opves)':'Overland Park Veterinary Emergency and Specialty — 8301 W 163rd St, Overland Park, KS 66223',
 'overland park veterinary emergency and specialty':'Overland Park Veterinary Emergency and Specialty — 8301 W 163rd St, Overland Park, KS 66223',
 'massachusetts veterinary referral hospital (mvrh)':'Massachusetts Veterinary Referral Hospital (MVRH) — 20 Cabot Rd, Woburn, MA 01801',
 'boston west veterinary emergency and specialty':'Boston West Veterinary Emergency & Specialty — 5 Strathmore Rd, Natick, MA 01760',
 'charleston veterinary referral center (cvrc)':'Charleston Veterinary Referral Center (CVRC) — 3484 Shelby Ray Court, Charleston, SC 29414',
 'peak veterinary referral center':'Peak Veterinary Referral Center — 158 Hurricane Ln, Williston, VT 05495',
 'mission veterinary emergency & specialty':'Mission Veterinary Emergency & Specialty — 5914 Johnson Dr, Mission, KS 66202',
 'gulf coast veterinary specialists (gcvs)':'Gulf Coast Veterinary Specialists (GCVS) — 8042 Katy Fwy, Houston, TX 77024',
 'sage':'SAGE Veterinary Centers — 600 Alabama Street, San Francisco, CA 94110',
 'sage san francisco':'SAGE Veterinary Centers — 600 Alabama Street, San Francisco, CA 94110',
 'upstate vet emergency + specialty care':'Upstate Vet Emergency & Specialty Care — 393 Woods Lake Road, Greenville, SC 29607',
 'veterinary specialty hospital – north county':'Veterinary Specialty Hospital – North County — 2055 Montiel Rd, San Marcos, CA 92069',
 'veterinary specialty hospital - north county':'Veterinary Specialty Hospital – North County — 2055 Montiel Rd, San Marcos, CA 92069',
 'spanaway veterinary clinic':'Spanaway Veterinary Clinic — 16920 Pacific Ave S, Spanaway, WA 98387',
 'mcabee veterinary hospital':'McAbee Veterinary Hospital — 4586 N Palmetto Ave, Winter Park, FL 32792',
 'first coast veterinary specialists & emergency':'First Coast Veterinary Specialists & Emergency — 301 Jacksonville Drive, Jacksonville Beach, FL 32250',
 'summit veterinary referral center':'Summit Veterinary Referral Center — 2505 S 80th Street, Tacoma, WA 98409',
}

def _active(s):return isinstance(s,dict) and s.get('available_for_matching') is not False and not any(x in g.norm(s.get('status','')) for x in ('not enrolling','enrollment closed','closed','paused'))
def _full_address(text):return bool(re.search(r'\d',text or '') and re.search(r'\b[A-Z]{2}\s+\d{5}(?:-\d{4})?\b',text or ''))
def _known(name):return SITE_ADDRESSES.get(g.norm(name or ''),'')
def _site_label(s):
 name=str(s.get('hospital') or s.get('name') or '').strip();known=_known(name)
 if known:return known
 address=str(s.get('address') or '').strip();city=str(s.get('city') or '').strip();state=str(s.get('state') or '').strip();zipcode=str(s.get('zip') or s.get('zipcode') or '').strip()
 if _full_address(address):detail=address
 elif address and re.search(r'\d',address) and city and state and zipcode:detail=f'{address}, {city}, {state} {zipcode}'
 else:return ''
 return f'{name} — {detail}' if name else detail

def _row_sites(row):
 vals=[_site_label(s) for s in row.get('sites',[]) if _active(s)] if isinstance(row.get('sites'),list) else []
 vals=[x for x in vals if x]
 if not vals:
  center=str(row.get('center') or '').strip();known=_known(center)
  if known:vals=[known]
 if not vals:
  address=str(row.get('address') or '').strip()
  if _full_address(address):vals=[address]
 out=[];seen=set()
 for value in vals:
  value=re.sub(r'\s+',' ',str(value)).strip(' ,');key=g.norm(value)
  if value and _full_address(value) and key not in seen:seen.add(key);out.append(value)
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
  card=card.replace('<b>Treatment:</b>','<b>What is being offered:</b>').replace('<b>Key eligibility:</b>','<b>Who may qualify:</b>').replace('<b>Important exclusions:</b>','<b>May not qualify if:</b>').replace('<b>Costs:</b>','<b>Costs / coverage:</b>');loc=_locations_html(row)
  if loc:card=card.replace('</article>',loc+'</article>')
  out.append(card)
 return ''.join(out)

def _rebuild_center_body(body):
 # Keep one verified physical address for a single center. Network/roll-up pages
 # must not show an aggregate address dump; participating addresses stay on study cards.
 def keep_single_center_location(match):
  section=match.group(0)
  return section if section.count('<li>')==1 else ''
 body=re.sub(r'<section class="center-locations">.*?</section>',keep_single_center_location,body,flags=re.S)
 m=re.search(r'<p class="lead count-callout"><strong>.*?</strong><br><span>Current research represented here includes (.*?)\.</span></p>',body,flags=re.S)
 if m:
  cancers=m.group(1);sentence=f'<p class="center-current">Current opportunities across this center or network include research and treatment options for <strong>{cancers}</strong>. See details below.</p>';body=body[:m.start()]+body[m.end():];pos=body.find('</div>',body.find('<div class="center-overview"'))
  if pos!=-1:body=body[:pos]+sentence+body[pos:]
  else:body=sentence+body
 free=re.search(r'<div class="free">.*?</div>',body,flags=re.S);cta=re.search(r'<p><a class="cta".*?</p>',body,flags=re.S)
 if free and cta:
  free_text='<p class="free-note">100% free. No registration, hidden results or paid report.</p>';start=min(free.start(),cta.start());end=max(free.end(),cta.end());body=body[:start]+cta.group(0)+free_text+body[end:]
 body=re.sub(r'<h2>Current treatment &amp; research opportunities</h2><p>.*?</p>','<h2>Cancer treatment &amp; research options</h2><p class="section-intro">Details for each current option are below, including eligibility, costs, contacts and participating locations.</p>',body,count=1,flags=re.S)
 return body

def owner_page(title,desc,body,canonical,lang='en',alts=None):
 if lang=='en':
  if '/centers/' in canonical and not canonical.rstrip('/').endswith('/centers'):
   body=_rebuild_center_body(body);desc=desc.replace('Current veterinary cancer clinical trials and treatment studies','Dog and cat cancer treatment options, research studies and clinical trials')
  elif '/north-america/' in canonical:body=body.replace('<h2>Treatment &amp; research</h2>','<h2>Current treatment &amp; research options</h2>')
 rendered=_original_page(title,desc,body,canonical,lang,alts)
 css='.study-locations{margin:15px 0 4px;padding:12px 14px;background:#f6f8fb;border-radius:10px}.study-locations ul{margin:5px 0 0;padding-left:20px}.field-label{font-weight:750;margin:0}.section-intro{color:#42536a;margin-top:0}.center-current{margin:14px 0 18px}.card p{margin:.7rem 0}.card .meta{margin-top:.2rem}.free-note{font-size:.78rem;color:#607086;margin:-7px 0 26px 2px}'
 return rendered.replace('</style>',css+'</style>',1)
g.cards=cards_with_locations
g.page=owner_page
