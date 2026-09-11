#!/usr/bin/env python3
"""Single owner-facing SEO rendering layer with catalog-wide location preflight."""
from __future__ import annotations
import hashlib,html,json,re
import generate_seo as g
from cancer_page_enhancements import enhance_cancer_pages
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES
from center_directory import LOCATIONS, address_for, addresses_for, address_is_complete, canonical_name_for, normalize
PROFILES.update(EXTRA_PROFILES)
CURRENT={'current','confirmed_current'}

# NOTE: Core strict rendering helpers are intentionally imported from the existing
# production module state below. This file is kept complete by GitHub contents API.

def merge(old,patch):
    new=dict(old)
    for k,v in patch.items():
        if k in {'requires','excludes'} and isinstance(v,dict):
            x=dict(new.get(k,{}) if isinstance(new.get(k),dict) else {});x.update(v);new[k]=x
        else:new[k]=v
    return new

def load_effective():
    base=json.loads((g.ROOT/'data'/'trials_base.json').read_text());rows={r['id']:r for r in base}
    # Only the canonical production update file belongs in the public catalog.
    # catalog_patch_* files are staging inputs and must not leak into a deploy.
    path=g.ROOT/'data'/'trial_updates.json'
    doc=json.loads(path.read_text()) if path.exists() else {}
    for p in doc.get('upsert',[]):rows[p['id']]=merge(rows.get(p['id'],{}),p)
    # Deletes have final precedence so an upsert cannot resurrect a removed row.
    for rid in doc.get('delete',[]):rows.pop(rid,None)
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

def site_active(s):return isinstance(s,dict) and s.get('available_for_matching') is not False and not any(x in g.norm(s.get('status','')) for x in ('not enrolling','enrollment closed','closed','paused'))
def site_is_coverage_placeholder(s):
    name=normalize(s.get('hospital') or s.get('name') or '');return 'partner hospital' in name or name in {'participating hospital','participating hospitals','partner site','partner sites'}
def embedded_address(obj,country=''):
    a=str(obj.get('address') or '').strip();city=str(obj.get('city') or '').strip();state=str(obj.get('state') or '').strip();z=str(obj.get('zip') or obj.get('zipcode') or obj.get('postal_code') or '').strip();candidates=[]
    if a:candidates.append(a)
    if a and city:
        tail=', '.join(x for x in (city,state) if x)
        if z:tail=(tail+' '+z).strip()
        candidates.append(f'{a}, {tail}')
    for detail in reversed(candidates):
        if address_is_complete(detail,country):return detail
    return ''
def site_labels(s,country=''):
    known=[x for x in addresses_for(s.get('hospital') or s.get('name') or '') if address_is_complete(x,country)]
    if known:return known
    detail=embedded_address(s,country)
    if not detail:return []
    name=str(s.get('hospital') or s.get('name') or '').strip();return [f'{name}, {detail}' if name and normalize(name) not in normalize(detail) else detail]
def row_locations(r):
    country=str(r.get('country') or '');vals=[]
    for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
        if site_active(s) and not site_is_coverage_placeholder(s):vals.extend(site_labels(s,country))
    if not vals:vals.extend(x for x in addresses_for(r.get('center','')) if address_is_complete(x,country))
    if not vals:
        own=embedded_address(r,country)
        if own:vals.append(own)
    out=[];seen=set()
    for x in vals:
        k=normalize(x)
        if k not in seen:seen.add(k);out.append(x)
    return out
def coverage_areas(r):
    out=[];seen=set();country=str(r.get('country') or '')
    for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
        if not(site_active(s) and site_is_coverage_placeholder(s)):continue
        pieces=[str(s.get(k) or '').strip() for k in ('city','state')];label=', '.join(x for x in pieces if x)
        if country and normalize(country) not in normalize(label):label=', '.join(x for x in (label,country) if x)
        if not label:label='Participating hospital assigned by the study team'
        key=normalize(label)
        if key not in seen:seen.add(key);out.append(label)
    return out
def region_for(country):
    c=normalize(country)
    if c in {'usa','united states','united states of america','canada','mexico'}:return 'North America'
    if c in {'uk','united kingdom','england','scotland','wales','ireland','france','germany','italy','spain','portugal','belgium','netherlands','switzerland','austria','poland','czechia','denmark','sweden','norway','finland','hungary','slovenia','cyprus'}:return 'UK / Europe'
    return str(country or 'Other')
def is_composite_center(name):
    raw=str(name or '').lower();n=normalize(name);return '/' in raw or '+' in raw or any(x in n for x in ('multicenter','multicentre','field trial','partner network','research network'))
def institution_like(name):
    if is_composite_center(name):return False
    n=normalize(name);return any(x in n for x in ('university','college','school of veterinary','teaching hospital','animal medical center'))
def preflight(rows):
    missing_sites=[];missing_centers=[];coverage=[];seen_sites=set();seen_centers=set();seen_coverage=set();covered_sites=0
    for r in rows:
        rid=str(r.get('id') or '?');country=str(r.get('country') or '');center=str(r.get('center') or '').strip()
        if center:
            ck=(normalize(center),normalize(country))
            if ck not in seen_centers:
                seen_centers.add(ck);addrs=addresses_for(center);own=embedded_address(r,country)
                if institution_like(center) and not(any(address_is_complete(a,country) for a in addrs) or address_is_complete(own,country)):missing_centers.append({'name':center,'country':country,'region':region_for(country),'trial_id':rid})
        for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
            if not site_active(s):continue
            name=str(s.get('hospital') or s.get('name') or '').strip() or '(unnamed site)'
            if site_is_coverage_placeholder(s):
                key=(normalize(name),normalize(s.get('city')),normalize(country))
                if key not in seen_coverage:seen_coverage.add(key);coverage.append({'name':name,'city':s.get('city'),'state':s.get('state'),'country':country,'trial_id':rid})
                continue
            sk=(normalize(name),normalize(country))
            if sk in seen_sites:continue
            seen_sites.add(sk)
            if site_labels(s,country):covered_sites+=1
            else:missing_sites.append({'name':name,'country':country,'region':region_for(country),'trial_id':rid})
    report={'effective_treatment_records':len(rows),'directory_locations':len(LOCATIONS),'unique_centers':len(seen_centers),'unique_active_physical_sites':len(seen_sites),'covered_active_physical_sites':covered_sites,'coverage_placeholders':coverage,'missing_center_addresses':missing_centers,'missing_participating_site_addresses':missing_sites}
    print('ADDRESS_PREFLIGHT',json.dumps({'centers':len(seen_centers),'physical_sites':len(seen_sites),'coverage_placeholders':len(coverage),'missing_centers':len(missing_centers),'missing_sites':len(missing_sites)},sort_keys=True))
    if missing_centers or missing_sites:raise AssertionError('Address preflight failed: '+json.dumps({'centers':missing_centers,'sites':missing_sites},ensure_ascii=False,sort_keys=True))
    return report

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
        areas=coverage_areas(r)
        if areas:p.append('<div class="enrollment-areas"><p class="field-label">Enrollment area</p><ul>'+''.join(f'<li>{g.esc(x)}</li>' for x in areas)+'</ul><p class="coverage-note">The public study listing names a partner-hospital network rather than a specific hospital. Confirm the assigned hospital with the study team.</p></div>')
        if r.get('last_verified'):p.append(f'<p class="verified">Last verified: {g.esc(r["last_verified"])}</p>')
        if r.get('url'):p.append(f'<p><a class="official" href="{g.esc(r["url"])}" rel="noopener">Official study / enrollment information →</a></p>')
        p.append('</article>');out.append(''.join(p))
    return ''.join(out)
g.cards=cards

base_page=g.page
def page(title,desc,body,canonical,lang='en',alts=None):
    rendered=base_page(title,desc,body,canonical,lang,alts)
    css='body{font-size:16px}.center-page h1{font-size:clamp(1.45rem,3.2vw,2rem);line-height:1.12;margin:20px 0 14px}.center-page .center-overview h2{font-size:1.18rem;margin-top:14px}.center-page .center-overview p{max-width:760px}.center-page .center-overview figure{margin:16px 0 14px;width:100%;max-width:760px}.center-page .center-overview figure img{width:100%!important;max-width:none!important;max-height:390px!important;object-fit:cover;border-radius:14px;display:block}.study-locations,.enrollment-areas{margin:15px 0 4px;padding:12px 14px;background:#f6f8fb;border-radius:10px}.study-locations ul,.enrollment-areas ul{margin:5px 0 0;padding-left:20px}.field-label{font-weight:750;margin:0}.coverage-note{font-size:.86rem;color:#607086}.center-address{background:#fff;border:1px solid #d9e2ea;border-radius:12px;padding:12px 15px;margin:14px 0 22px}.free-note{font-size:.8rem;color:#607086}.card p{margin:.7rem 0}@media(max-width:600px){.center-page h1{font-size:1.42rem}.center-page .center-overview h2{font-size:1.08rem}.center-page .center-overview figure{max-width:none}}'
    return rendered.replace('</style>',css+'</style>',1)
g.page=page

CENTER_RULES=(('Colorado State University Flint Animal Cancer Center',('colorado state university','flint animal cancer center')),('University of Florida College of Veterinary Medicine',('university of florida',)),('Michigan State University College of Veterinary Medicine',('michigan state university',)),('Auburn University College of Veterinary Medicine',('auburn university',)),('University of Pennsylvania School of Veterinary Medicine',('university of pennsylvania','penn vet')),('Tufts University Cummings School of Veterinary Medicine',('tufts university','tufts cummings')),('NC State College of Veterinary Medicine',('nc state','north carolina state university')),('University of Missouri College of Veterinary Medicine',('university of missouri',)),('University of Illinois College of Veterinary Medicine',('university of illinois',)),('Purdue University College of Veterinary Medicine',('purdue university',)),('Cornell University College of Veterinary Medicine',('cornell university',)),('University of Minnesota College of Veterinary Medicine',('university of minnesota',)),('Ohio State University College of Veterinary Medicine',('ohio state university','the ohio state university')),('Texas A&M School of Veterinary Medicine',('texas a&m','texas a and m')),('Louisiana State University School of Veterinary Medicine',('louisiana state university','lsu')),('University of Georgia College of Veterinary Medicine',('university of georgia',)),('Washington State University College of Veterinary Medicine',('washington state university',)),('UC Davis Veterinary Center for Clinical Trials',('uc davis veterinary center for clinical trials','uc davis veterinary medical teaching hospital','uc davis')),('Aurelius Biotherapeutics',('aurelius biotherapeutics',)),('Ethos Veterinary Health / Ethos Discovery',('ethos veterinary health','ethos discovery')),('Colorado Animal Specialty & Emergency (CASE)',('colorado animal specialty','case / ethos discovery')),('Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)',('johns hopkins center for image-guided animal therapy',)),('SAGE Veterinary Centers',('sage san francisco','sage veterinary')))
def canonical_center(v):
    raw=str(v or '').strip();known=canonical_name_for(raw)
    if known:return known
    text=normalize(raw)
    for name,aliases in CENTER_RULES:
        if any(normalize(a) in text for a in aliases):return name
    return re.sub(r'\s+',' ',raw) if raw else None

def profile(center):
    p=PROFILES.get(center)
    if p:return p
    return {'title':f'About {center}','about':f'{center} is involved in companion-animal cancer treatment or clinical research. Current opportunities are listed below with study-specific eligibility, contacts and participating locations.','links':[]}
def overview(center):
    p=profile(center);fig=''
    if p.get('image'):fig=f'<figure><img src="{g.esc(p["image"])}" alt="{g.esc(p.get("image_alt") or center)}" loading="lazy">'+(f'<figcaption style="font-size:.86rem;color:#607086;margin-top:7px">{g.esc(p.get("image_caption"))}</figcaption>' if p.get('image_caption') else '')+'</figure>'
    links=' · '.join(f'<a href="{g.esc(u)}" rel="noopener">{g.esc(l)}</a>' for l,u in p.get('links',[]));research=f'<p>{g.esc(p["research"])}</p>' if p.get('research') else ''
    return f'<div class="center-overview"><h2>{g.esc(p.get("title") or ("About "+center))}</h2>{fig}<p>{g.esc(p.get("about") or "")}</p>{research}'+(f'<p>{links}</p>' if links else '')+'</div>'

def center_slug(center):return g.slugify(center)
def generate_centers(rows):
    grouped={}
    for r in rows:
        center=canonical_center(r.get('center'))
        if center:grouped.setdefault(center,[]).append(r)
    links=[];items=[];used=set()
    for center,hit in sorted(grouped.items()):
        path='centers/'+center_slug(center);url=f'{g.SITE}/{path}/';used.add(center)
        cancers=sorted({c for r in hit for c in row_cancers(r)});ct=', '.join(g.display_name(c) for c in cancers) if cancers else 'multiple cancer types'
        addrs=[]
        for r in hit:addrs.extend(row_locations(r))
        addrs=list(dict.fromkeys(addrs));address_html='<div class="center-address"><strong>Location</strong><br>'+('<br>'.join(g.esc(a) for a in addrs) if addrs else 'Contact the center for the current study location.')+'</div>'
        body='<div class="center-page">'+f'<h1>{g.esc(center)}</h1>'+overview(center)+address_html+f'<p>Current opportunities here include research or treatment options for <strong>{g.esc(ct)}</strong>.</p><p><a class="cta" href="{g.FINDER}">Find cancer treatment options near you</a></p><p class="free-note">100% free. No registration, hidden results or paid report.</p><h2>Cancer treatment &amp; research options</h2>'+g.cards(hit)+'</div>'
        desc=f'Dog and cat cancer treatment options, research studies and clinical trials at {center}.';d=g.OUT/path;d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(g.page(center,desc,body,url),encoding='utf-8');links.append(url);items.append((center,path,len(hit),addrs))
    assert len(used)==len(grouped),(len(used),len(grouped))
    iu=f'{g.SITE}/centers/'
    cards_html=''.join(f'<a class="directory-card" href="{g.SITE}/{p}"><strong>{g.esc(n)}</strong><span>{c} current '+('opportunity' if c==1 else 'opportunities')+((' · '+g.esc(a[0])) if a else '')+'</span></a>' for n,p,c,a in items)
    ib='<h1>Veterinary Oncology Centers</h1><p class="lead catalog-intro"><strong>Find hospitals and research centers that may have options beyond your local clinic.</strong> This directory includes universities, teaching hospitals, specialty oncology hospitals and other research programs with current cancer treatment opportunities. Search by hospital, city or state.</p><input class="catalog-search" type="search" placeholder="Search hospital, city or state" aria-label="Search oncology centers" oninput="filterCenters(this.value)"><div class="directory-grid">'+cards_html+'</div><script>function filterCenters(q){q=q.toLowerCase().trim();document.querySelectorAll(".directory-card").forEach(function(x){x.style.display=!q||x.textContent.toLowerCase().includes(q)?"":"none";});}</script>'
    d=g.OUT/'centers';d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(g.page('Veterinary Oncology Centers','Veterinary oncology centers, research hospitals and current treatment studies.',ib,iu),encoding='utf-8')
    sm=g.OUT/'sitemap.xml';s=sm.read_text();sm.write_text(s.replace('</urlset>',''.join(f'<url><loc>{g.esc(u)}</loc></url>\n' for u in [iu]+links)+'</urlset>'));print('CENTER_PAGES_OK',len(grouped))

def audit(report):
    pages=list(g.OUT.rglob('index.html'));assert pages;invalid=[]
    for p in pages:
        s=p.read_text(errors='replace')
        for block in re.findall(r'<div class="study-locations">.*?</div>',s,re.S):
            for item in re.findall(r'<li>(.*?)</li>',block,re.S):
                text=html.unescape(re.sub(r'<.*?>','',item))
                if not address_is_complete(text,''):invalid.append({'page':str(p.relative_to(g.OUT)),'location':text})
    report['invalid_rendered_locations']=invalid;(g.OUT/'mapping-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8');assert not invalid,invalid[:10]
def main():
    rows=g.load_effective();report=preflight(rows);g.main();enhance_cancer_pages(g.OUT);generate_centers(rows);audit(report)
if __name__=='__main__':main()
