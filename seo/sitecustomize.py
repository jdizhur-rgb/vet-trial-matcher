"""Render study-specific participating sites and treatment-focused local SEO."""
import re
import generate_seo as g

_original_cards = g.cards
_original_page = g.page

MULTI_CENTER_MARKERS = (
    'ethos', 'medvet', 'sage veterinary', 'veterinary specialty hospital',
    'multicenter', 'multi-center', 'hospital network'
)

_RAW_TITLE_SITE_FALLBACKS = {
    'canine b-cell lymphoma study': [
        'Colorado Animal Specialty & Emergency (CASE) — Boulder, CO',
        'Overland Park Veterinary & Specialty (OPVES) — Overland Park, KS',
        'Veterinary Specialty Hospital — Sorrento Valley, CA',
    ],
    'canine epitheliotropic lymphosarcoma sample collection study': [
        'Overland Park Veterinary Emergency and Specialty — Overland Park, KS',
        'Nashville Veterinary Specialists — Nashville, TN',
        'Gulf Coast Veterinary Specialists (GCVS) — Houston, TX',
        'Peak Veterinary Referral Center — Williston, VT',
    ],
    'canine oncology sample study': [
        'Charleston Veterinary Referral Center (CVRC) — Charleston, SC',
        'Boston West Veterinary Emergency and Specialty — Natick, MA',
        'Massachusetts Veterinary Referral Hospital (MVRH) — Woburn, MA',
        'Metropolitan Veterinary Hospital — Cleveland, OH',
        'Metropolitan Veterinary Hospital — Akron, OH',
        'Pacific Northwest Pet ER & Specialty Center (PACWVETS) — Vancouver, WA',
        'SAGE — San Francisco, CA',
        'Southeast Veterinary Oncology & Internal Medicine — Jacksonville, FL',
        'Upstate Vet Emergency + Specialty Care — Greenville, SC',
        'Veterinary Specialty Hospital – North County — San Marcos, CA',
        'Animal Medical Center of Plainfield — Plainfield, IL',
        'Eastern Carolina Veterinary Medical Center — Wilmington, NC',
        'Spanaway Veterinary Clinic — Spanaway, WA',
    ],
    'fine needle aspirate sample study wave 2': [
        'Animal Emergency Hospital (AEH) — Bel Air, MD',
        'Metropolitan Veterinary Hospital — Cleveland, OH',
        'Boston West Veterinary Emergency & Specialty — Natick, MA',
        'Metropolitan Veterinary Hospital — Akron, OH',
        'Pacific Northwest Pet Emergency & Specialty Center (PACWVETS) — Vancouver, WA',
        'Premier Vet Group — Orland Park, IL',
        'SAGE San Francisco — San Francisco, CA',
        'McAbee Veterinary Hospital — Winter Park, FL',
        'Sumner Veterinary Hospital — Sumner, WA',
    ],
    'experimental egfr/her2 tumor vaccine': [
        'MedVet Salt Lake City — Salt Lake City, UT',
        'MedVet Cincinnati — Cincinnati, OH (established patients)',
        'MedVet Cleveland — Cleveland, OH (established patients)',
        'MedVet Pittsburgh — Pittsburgh, PA (Pennsylvania residents)',
    ],
}
TITLE_SITE_FALLBACKS = {g.norm(k): v for k, v in _RAW_TITLE_SITE_FALLBACKS.items()}


def _active(site):
    if not isinstance(site, dict) or site.get('available_for_matching') is False:
        return False
    status = g.norm(site.get('status', ''))
    return not any(x in status for x in ('not enrolling', 'enrollment closed', 'closed', 'paused'))


def _site_label(site):
    name = str(site.get('hospital') or site.get('name') or '').strip()
    address = str(site.get('address') or '').strip()
    city = str(site.get('city') or '').strip()
    state = str(site.get('state') or '').strip()
    zipcode = str(site.get('zip') or site.get('zipcode') or '').strip()
    location = str(site.get('location') or '').strip()
    geo = ', '.join(x for x in (city, state) if x)
    if zipcode: geo = (geo + ' ' + zipcode).strip()
    detail = address
    if geo and g.norm(geo) not in g.norm(detail): detail = ', '.join(x for x in (detail, geo) if x)
    if location and g.norm(location) not in g.norm(detail): detail = ', '.join(x for x in (detail, location) if x)
    return f'{name} — {detail}' if name and detail else name or detail


def _row_sites(row):
    vals=[]
    for site in row.get('sites',[]) if isinstance(row.get('sites'),list) else []:
        if _active(site):
            label=_site_label(site)
            if label: vals.append(label)
    if not vals: vals.extend(TITLE_SITE_FALLBACKS.get(g.norm(row.get('title','')),[]))
    if not vals:
        address=str(row.get('address') or '').strip(); city=str(row.get('city') or '').strip(); state=str(row.get('state') or '').strip(); zipcode=str(row.get('zip') or row.get('zipcode') or '').strip(); location=str(row.get('location') or '').strip()
        geo=', '.join(x for x in (city,state) if x)
        if zipcode: geo=(geo+' '+zipcode).strip()
        direct=', '.join(x for x in (address,geo) if x) or location
        if direct and g.norm(direct) not in ('multiple','usa','united states'): vals.append(direct)
    out=[]; seen=set()
    for value in vals:
        value=re.sub(r'\s+',' ',str(value)).strip(' ,'); key=g.norm(value)
        if not key or key in ('multiple','co') or key in seen: continue
        seen.add(key); out.append(value)
    return out


def _locations_html(row):
    sites=_row_sites(row)
    if not sites:return ''
    label='Treatment / study location' if len(sites)==1 else 'Treatment / study locations near you'
    return f'<div class="study-locations"><p><b>{label}:</b></p><ul>'+''.join(f'<li>{g.esc(x)}</li>' for x in sites)+'</ul></div>'


def cards_with_study_locations(rows):
    rows=list(rows); rendered_html=_original_cards(rows)
    cards=re.findall(r'<article class="card">.*?</article>',rendered_html,flags=re.S)
    if len(cards)!=len(rows):return rendered_html
    rendered=[]; hide_center_rollup=False
    for row,card in zip(rows,cards):
        loc=_locations_html(row)
        if loc: card=card.replace('</article>',loc+'</article>')
        center=g.norm(row.get('center',''))
        if len(_row_sites(row))>1 or any(g.norm(x) in center for x in MULTI_CENTER_MARKERS): hide_center_rollup=True
        rendered.append(card)
    prefix='<style>.center-locations{display:none}.study-locations{margin:14px 0}.study-locations p{margin-bottom:4px}.study-locations ul{margin-top:4px;padding-left:22px}</style>' if hide_center_rollup else ''
    return prefix+''.join(rendered)


def treatment_focused_page(title,desc,body,canonical,lang='en',alts=None):
    # Keep clinical-trial terminology, but add the phrases ordinary owners actually search.
    if lang=='en':
        if '/centers/' in canonical:
            body=body.replace('</h1>','</h1><p class="lead treatment-search">Looking for dog or cat cancer treatment near you? Browse current treatment options, advanced cancer treatments, research studies and clinical trials available through this center.</p>',1)
            desc=desc.replace('Current veterinary cancer clinical trials and treatment studies','Dog and cat cancer treatment options, advanced treatments, research studies and clinical trials')
        else:
            body=body.replace('<h2>Treatment &amp; research</h2>','<h2>Treatment options, advanced treatments &amp; research</h2>')
            desc=desc.replace('Current ', 'Current treatment options, advanced treatments and ')
    return _original_page(title,desc,body,canonical,lang,alts)

g.cards=cards_with_study_locations
g.page=treatment_focused_page
