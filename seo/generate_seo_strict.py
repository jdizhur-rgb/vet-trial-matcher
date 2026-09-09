#!/usr/bin/env python3
"""Single owner-facing SEO rendering layer.

This module owns catalog merging, cards, page styling, center profiles and
location rules.  Legacy *customize modules must remain side-effect free.
"""
from __future__ import annotations
import html,json,re
from pathlib import Path
import generate_seo as g
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES
PROFILES.update(EXTRA_PROFILES)
CURRENT={'current','confirmed_current'}

def merge(old,patch):
    new=dict(old)
    for k,v in patch.items():
        if k in {'requires','excludes'} and isinstance(v,dict):
            x=dict(new.get(k,{}) if isinstance(new.get(k),dict) else {}); x.update(v); new[k]=x
        else:new[k]=v
    return new

def load_effective():
    base=json.loads((g.ROOT/'data'/'trials_base.json').read_text()); rows={r['id']:r for r in base}
    paths=[g.ROOT/'data'/'trial_updates.json']+sorted((g.ROOT/'data').glob('catalog_patch_*.json'))
    for path in paths:
        if not path.exists():continue
        doc=json.loads(path.read_text())
        for rid in doc.get('delete',[]):rows.pop(rid,None)
        for p in doc.get('upsert',[]):rows[p['id']]=merge(rows.get(p['id'],{}),p)
    return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True and r.get('status_confidence') in CURRENT]
g.load_effective=load_effective

def phrase(needle,text):
    needle=g.norm(needle);text=g.norm(text);return bool(needle and re.search(r'(?<![a-z0-9])'+re.escape(needle)+r'(?![a-z0-9])',text))
def canonical_cancer(v):
    raw=g.norm(v)
    if not raw or any(phrase(x,raw) for x in g.GENERIC_WORDS):return None
    for key,aliases in g.CANONICAL_RULES:
        if any(phrase(a,raw) for a in aliases):return key
    return None
def cancer_values(r):
    v=r.get('cancers',[]);return [v] if isinstance(v,str) else list(v) if isinstance(v,(list,tuple,set)) else []
def row_cancers(r):return {x for x in (canonical_cancer(v) for v in cancer_values(r)) if x}
g.canonical_cancer=canonical_cancer;g.row_cancers=row_cancers

SITE_ADDRESSES={
'aurelius biotherapeutics':'Aurelius Biotherapeutics, 720 Virginia Street, Bellingham, WA 98225',
'colorado animal specialty emergency case':'Colorado Animal Specialty & Emergency (CASE), 2972 Iris Ave, Boulder, CO 80301',
'overland park veterinary emergency specialty':'Overland Park Veterinary Emergency & Specialty, 8301 W 163rd St, Overland Park, KS 66223',
'massachusetts veterinary referral hospital mvrh':'Massachusetts Veterinary Referral Hospital, 20 Cabot Rd, Woburn, MA 01801',
'massachusetts veterinary referral hospital':'Massachusetts Veterinary Referral Hospital, 20 Cabot Rd, Woburn, MA 01801',
'peak veterinary referral center':'Peak Veterinary Referral Center, 158 Hurricane Ln, Williston, VT 05495',
'mission veterinary emergency specialty':'Mission Veterinary Emergency & Specialty, 5914 Johnson Dr, Mission, KS 66202',
'gulf coast veterinary specialists gcvs':'Gulf Coast Veterinary Specialists, 8042 Katy Fwy, Houston, TX 77024',
'gulf coast veterinary specialists':'Gulf Coast Veterinary Specialists, 8042 Katy Fwy, Houston, TX 77024',
'first coast veterinary specialists emergency':'First Coast Veterinary Specialists & Emergency, 301 Jacksonville Dr, Jacksonville Beach, FL 32250',
'summit veterinary referral center':'Summit Veterinary Referral Center, 2505 S 80th St, Tacoma, WA 98409',
'care center cincinnati':'CARE Center, 6995 E Kemper Rd, Cincinnati, OH 45249',
'sage':'SAGE Veterinary Centers, 600 Alabama St, San Francisco, CA 94110',
'sage veterinary centers':'SAGE Veterinary Centers, 600 Alabama St, San Francisco, CA 94110',
}
UNIVERSITY_ADDRESSES={
'Colorado State University Flint Animal Cancer Center':'Flint Animal Cancer Center, 300 W Drake Rd, Fort Collins, CO 80523',
'Auburn University College of Veterinary Medicine':'Bailey Small Animal Teaching Hospital, 1220 Wire Rd, Auburn, AL 36849',
'Cornell University College of Veterinary Medicine':'Cornell University Hospital for Animals, 930 Campus Rd, Ithaca, NY 14853',
'Louisiana State University School of Veterinary Medicine':'LSU Veterinary Teaching Hospital, 1909 Skip Bertman Dr, Baton Rouge, LA 70803',
'Michigan State University College of Veterinary Medicine':'Michigan State University Veterinary Medical Center, 736 Wilson Rd, East Lansing, MI 48824',
'NC State College of Veterinary Medicine':'NC State Veterinary Hospital, 1052 William Moore Dr, Raleigh, NC 27607',
'Ohio State University College of Veterinary Medicine':'The Ohio State University Veterinary Medical Center, 601 Vernon L Tharp St, Columbus, OH 43210',
'Purdue University College of Veterinary Medicine':'Purdue University Veterinary Hospital, 625 Harrison St, West Lafayette, IN 47907',
'Texas A&M School of Veterinary Medicine':'Texas A&M Small Animal Teaching Hospital, 408 Raymond Stotzer Pkwy, College Station, TX 77845',
'Tufts University Cummings School of Veterinary Medicine':'Henry and Lois Foster Hospital for Small Animals, 200 Westboro Rd, North Grafton, MA 01536',
'UC Davis Veterinary Center for Clinical Trials':'UC Davis Veterinary Medical Teaching Hospital, 1 Garrod Dr, Davis, CA 95616',
'University of Florida College of Veterinary Medicine':'UF Small Animal Hospital, 2015 SW 16th Ave, Gainesville, FL 32608',
'University of Georgia College of Veterinary Medicine':'UGA Veterinary Teaching Hospital, 2200 College Station Rd, Athens, GA 30602',
'University of Illinois College of Veterinary Medicine':'University of Illinois Veterinary Teaching Hospital, 1008 W Hazelwood Dr, Urbana, IL 61802',
'University of Minnesota College of Veterinary Medicine':'University of Minnesota Veterinary Medical Center, 1365 Gortner Ave, St Paul, MN 55108',
'University of Missouri College of Veterinary Medicine':'University of Missouri Veterinary Health Center, 900 E Campus Dr, Columbia, MO 65211',
'University of Pennsylvania School of Veterinary Medicine':'Penn Vet Ryan Veterinary Hospital, 3900 Spruce St, Philadelphia, PA 19104',
'Washington State University College of Veterinary Medicine':'WSU Veterinary Teaching Hospital, 205 Ott Rd, Pullman, WA 99164',
}

def full_address(s):return bool(re.search(r'\d',s or '') and re.search(r'\b[A-Z]{2}\s+\d{5}(?:-\d{4})?\b',s or ''))
def site_active(s):return isinstance(s,dict) and s.get('available_for_matching') is not False and not any(x in g.norm(s.get('status','')) for x in ('not enrolling','enrollment closed','closed','paused'))
def site_label(s):
    name=str(s.get('hospital') or s.get('name') or '').strip();known=SITE_ADDRESSES.get(g.norm(name),'')
    if known:return known
    a=str(s.get('address') or '').strip();city=str(s.get('city') or '').strip();state=str(s.get('state') or '').strip();z=str(s.get('zip') or s.get('zipcode') or '').strip()
    if full_address(a):detail=a
    elif a and re.search(r'\d',a) and city and state and z:detail=f'{a}, {city}, {state} {z}'
    else:return ''
    return f'{name}, {detail}' if name and g.norm(name) not in g.norm(detail) else detail

def row_locations(r):
    vals=[]
    for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
        if site_active(s):
            x=site_label(s)
            if x:vals.append(x)
    if not vals:
        known=SITE_ADDRESSES.get(g.norm(r.get('center','')),'')
        if known:vals.append(known)
    if not vals and full_address(str(r.get('address') or '')):vals.append(str(r['address']))
    out=[];seen=set()
    for x in vals:
        k=g.norm(x)
        if k not in seen:seen.add(k);out.append(x)
    return out

def cards(rows):
    out=[]
    for r in rows:
        p=[f'<article class="card"><h3>{g.esc(r.get("title"))}</h3><p class="meta"><strong>{g.esc(r.get("center"))}</strong> · {g.esc(r.get("country"))}</p>']
        if r.get('status'):p.append(f'<p class="status">{g.esc(r["status"])}</p>')
        treatment=g.prose(r.get('intervention') or r.get('treatment') or r.get('notes'))
        if treatment:p.append(f'<p><b>What is being offered:</b> {g.esc(treatment)}</p>')
        req=g.prose(r.get('requires'));exc=g.prose(r.get('excludes'));fund=g.prose(r.get('funding'));contact=g.contact_text(r)
        if req:p.append(f'<p><b>Who may qualify:</b> {g.esc(req)}</p>')
        if exc:p.append(f'<p><b>May not qualify if:</b> {g.esc(exc)}</p>')
        if fund:p.append(f'<p><b>Costs / coverage:</b> {g.esc(fund)}</p>')
        if contact:p.append(f'<p><b>Contact:</b> {g.esc(contact)}</p>')
        locs=row_locations(r)
        if locs:p.append('<div class="study-locations"><p class="field-label">'+('Location' if len(locs)==1 else 'Participating locations')+'</p><ul>'+''.join(f'<li>{g.esc(x)}</li>' for x in locs)+'</ul></div>')
        if r.get('last_verified'):p.append(f'<p class="verified">Last verified: {g.esc(r["last_verified"])}</p>')
        if r.get('url'):p.append(f'<p><a class="official" href="{g.esc(r["url"])}" rel="noopener">Official study / enrollment information →</a></p>')
        p.append('</article>');out.append(''.join(p))
    return ''.join(out)
g.cards=cards

base_page=g.page
def page(title,desc,body,canonical,lang='en',alts=None):
    rendered=base_page(title,desc,body,canonical,lang,alts)
    css='body{font-size:16px}.center-page h1{font-size:clamp(1.75rem,4vw,2.35rem);line-height:1.12;margin:24px 0 18px}.center-page .center-overview h2{font-size:1.3rem;margin-top:18px}.center-page .center-overview p{max-width:760px}.study-locations{margin:15px 0 4px;padding:12px 14px;background:#f6f8fb;border-radius:10px}.study-locations ul{margin:5px 0 0;padding-left:20px}.field-label{font-weight:750;margin:0}.university-address{background:#fff;border:1px solid #d9e2ea;border-radius:12px;padding:12px 15px;margin:14px 0 22px}.free-note{font-size:.8rem;color:#607086}.card p{margin:.7rem 0}@media(max-width:600px){.center-page h1{font-size:1.72rem}.center-page .center-overview h2{font-size:1.2rem}}'
    return rendered.replace('</style>',css+'</style>',1)
g.page=page

CENTER_RULES=(
('Colorado State University Flint Animal Cancer Center',('colorado state university','flint animal cancer center')),('University of Florida College of Veterinary Medicine',('university of florida',)),('Michigan State University College of Veterinary Medicine',('michigan state university',)),('Auburn University College of Veterinary Medicine',('auburn university',)),('University of Pennsylvania School of Veterinary Medicine',('university of pennsylvania','penn vet')),('Tufts University Cummings School of Veterinary Medicine',('tufts university','tufts cummings')),('NC State College of Veterinary Medicine',('nc state','north carolina state university')),('University of Missouri College of Veterinary Medicine',('university of missouri',)),('University of Illinois College of Veterinary Medicine',('university of illinois',)),('Purdue University College of Veterinary Medicine',('purdue university',)),('Cornell University College of Veterinary Medicine',('cornell university',)),('University of Minnesota College of Veterinary Medicine',('university of minnesota',)),('Ohio State University College of Veterinary Medicine',('ohio state university','the ohio state university')),('Texas A&M School of Veterinary Medicine',('texas a&m','texas a and m')),('Louisiana State University School of Veterinary Medicine',('louisiana state university','lsu')),('University of Georgia College of Veterinary Medicine',('university of georgia',)),('Washington State University College of Veterinary Medicine',('washington state university',)),('UC Davis Veterinary Center for Clinical Trials',('uc davis veterinary center for clinical trials','uc davis veterinary medical teaching hospital','uc davis')),('Aurelius Biotherapeutics',('aurelius biotherapeutics',)),('Ethos Veterinary Health / Ethos Discovery',('ethos veterinary health','ethos discovery')),('Colorado Animal Specialty & Emergency (CASE)',('colorado animal specialty','case / ethos discovery')),('Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)',('johns hopkins center for image-guided animal therapy',)),('SAGE Veterinary Centers',('sage san francisco','sage veterinary')),
)
def canonical_center(v):
    raw=str(v or '').strip();text=g.norm(raw)
    for name,aliases in CENTER_RULES:
        if any(g.norm(a) in text for a in aliases):return name
    return re.sub(r'\s+',' ',raw) if raw else None

def profile(center):
    if center=='Aurelius Biotherapeutics':
        return {'title':'About Aurelius Biotherapeutics','about':'Aurelius Biotherapeutics in Bellingham, Washington focuses on experimental adoptive T-cell immunotherapy for dogs with B-cell lymphoma. Its work grew from canine lymphoma research with MD Anderson Cancer Center, and its current program uses a dog’s own T cells as an individualized immune-cell treatment.','links':[('Official website','https://aureliusbio.com/')]}
    p=PROFILES.get(center)
    if p:return p
    if center in UNIVERSITY_ADDRESSES:return {'title':f'About {center}','about':f'{center} combines veterinary specialty care with clinical research. The cancer studies currently represented in our catalog are listed below with study-specific eligibility, contacts and enrollment information.','links':[]}
    return {'title':f'About {center}','about':f'{center} is involved in companion-animal cancer treatment or clinical research. Current opportunities are listed below with study-specific eligibility, contacts and participating locations.','links':[]}

def overview(center):
    p=profile(center);fig=''
    if p.get('image'):fig=f'<figure><img src="{g.esc(p["image"])}" alt="{g.esc(p.get("image_alt") or center)}" loading="lazy" style="width:100%;max-height:390px;object-fit:cover;border-radius:14px;display:block">'+(f'<figcaption style="font-size:.86rem;color:#607086;margin-top:7px">{g.esc(p.get("image_caption"))}</figcaption>' if p.get('image_caption') else '')+'</figure>'
    links=' · '.join(f'<a href="{g.esc(u)}" rel="noopener">{g.esc(l)}</a>' for l,u in p.get('links',[]))
    return f'<div class="center-overview"><h2>{g.esc(p["title"])}</h2>{fig}<p>{g.esc(p["about"])}</p>'+(f'<p>{links}</p>' if links else '')+'</div>'

def add(grouped,name,row):
    name=canonical_center(name)
    if not name:return
    b=grouped.setdefault(name,[])
    if not any(x.get('id')==row.get('id') for x in b):b.append(row)

def generate_centers():
    rows=[r for r in g.load_effective() if r.get('country')=='USA' and str(r.get('center','')).strip()];grouped={}
    for r in rows:
        add(grouped,r.get('center'),r)
        for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
            if site_active(s) and (s.get('hospital') or s.get('name')):add(grouped,s.get('hospital') or s.get('name'),r)
    links=[];items=[];used={}
    for center,hit in sorted(grouped.items()):
        slug=g.slugify(center.replace('College of Veterinary Medicine','').replace('School of Veterinary Medicine','')) or 'research-center'
        if slug in used and used[slug]!=center:slug=g.slugify(center)
        used[slug]=center;path=f'centers/{slug}/';url=f'{g.SITE}/{path}';cancers=sorted({c for r in hit for c in row_cancers(r)});ct=', '.join(g.display_name(c) for c in cancers) or 'multiple cancer types'
        addr=UNIVERSITY_ADDRESSES.get(center);address_html=f'<div class="university-address"><strong>Location</strong><br>{g.esc(addr)}</div>' if addr else ''
        body='<div class="center-page">'+f'<h1>{g.esc(center)}</h1>'+overview(center)+address_html+f'<p>Current opportunities here include research or treatment options for <strong>{g.esc(ct)}</strong>.</p><p><a class="cta" href="{g.FINDER}">Find cancer treatment options near you</a></p><p class="free-note">100% free. No registration, hidden results or paid report.</p><h2>Cancer treatment &amp; research options</h2>'+g.cards(hit)+'</div>'
        desc=f'Dog and cat cancer treatment options, research studies and clinical trials at {center}.'
        d=g.OUT/path;d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(g.page(center,desc,body,url),encoding='utf-8');links.append(url);items.append((center,path,len(hit)))
    iu=f'{g.SITE}/centers/';ib='<h1>Veterinary Cancer Research Centers</h1><p class="lead">Browse universities, teaching hospitals, specialty hospitals and research centers with current cancer treatment opportunities.</p><ul>'+''.join(f'<li><a href="{g.SITE}/{p}">{g.esc(n)}</a> — {c} current opportunities</li>' for n,p,c in items)+'</ul>'
    d=g.OUT/'centers';d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(g.page('Veterinary Cancer Research Centers','Veterinary cancer research centers and current treatment studies.',ib,iu),encoding='utf-8')
    sm=g.OUT/'sitemap.xml';s=sm.read_text();sm.write_text(s.replace('</urlset>',''.join(f'<url><loc>{g.esc(u)}</loc></url>\n' for u in [iu]+links)+'</urlset>'))
    print('CENTER_PAGES_OK',len(grouped))

def audit():
    pages=list(g.OUT.rglob('index.html'));assert pages
    for p in pages:
        s=p.read_text(errors='replace')
        for block in re.findall(r'<div class="study-locations">.*?</div>',s,re.S):
            for item in re.findall(r'<li>(.*?)</li>',block,re.S):
                text=html.unescape(re.sub(r'<.*?>','',item));assert full_address(text),(p,text)
    (g.OUT/'mapping-audit.json').write_text(json.dumps({'effective_treatment_records':len(g.load_effective())},indent=2))

def main():
    g.main();generate_centers();audit()
if __name__=='__main__':main()
