#!/usr/bin/env python3
"""Generate crawlable SEO pages from current treatment opportunities only."""
from __future__ import annotations
import html, json, re, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'seo'/'site'
FINDER='https://vet-cancer-trial-finder.streamlit.app/'
SITE='https://jdizhur-rgb.github.io/vet-trial-matcher'
EUROPE={'Belgium','Denmark','France','Germany','Italy','Netherlands','Portugal','Spain','Sweden','Switzerland','UK','Ireland','Austria','Czechia','Poland','Finland','Norway','Hungary','Slovenia','Cyprus'}
REGIONS={'north-america':{'USA','Canada'},'uk-europe':EUROPE}
SPECIES={'dogs':'Dog','cats':'Cat'}
LANGS={
'en':('Clinical Trials and Cancer Treatment Studies','Current treatment-focused opportunities','Search the Vet Cancer Trial Finder'),
'de':('Klinische Studien und Krebsbehandlungsstudien','Aktuelle behandlungsorientierte Möglichkeiten','Aktuelle Behandlungsmöglichkeiten suchen'),
'fr':('Essais cliniques et études de traitement du cancer','Options thérapeutiques actuellement disponibles','Rechercher les options de traitement actuelles'),
'es':('Ensayos clínicos y estudios de tratamiento del cáncer','Opciones terapéuticas disponibles actualmente','Buscar opciones de tratamiento actuales'),
'it':('Studi clinici e studi sul trattamento del cancro','Opportunità terapeutiche attualmente disponibili','Cerca le opzioni terapeutiche attuali'),
'nl':('Klinische onderzoeken en kankerbehandelingsstudies','Huidige behandelingsgerichte mogelijkheden','Zoek actuele behandelingsmogelijkheden'),
}
EU_LANGS=('en','de','fr','es','it','nl')

# SEO taxonomy is deliberately smaller than the matching taxonomy. Raw catalog labels,
# catch-alls and pathology variants must not become doorway/thin pages.
CANONICAL_RULES=(
 ('oral squamous cell carcinoma', ('oral squamous cell carcinoma','oral scc','feline oral scc')),
 ('squamous cell carcinoma', ('squamous cell carcinoma','scc')),
 ('oral melanoma', ('oral melanoma','mucosal melanoma')),
 ('melanoma', ('melanoma',)),
 ('mast cell tumor', ('mast cell tumor','mast cell tumour','mct')),
 ('soft tissue sarcoma', ('soft tissue sarcoma','soft-tissue sarcoma','sts')),
 ('histiocytic sarcoma', ('histiocytic sarcoma',)),
 ('hemangiosarcoma', ('hemangiosarcoma','haemangiosarcoma','hsa')),
 ('osteosarcoma', ('osteosarcoma','bone cancer')),
 ('urothelial carcinoma', ('urothelial','transitional cell carcinoma','bladder cancer','tcc')),
 ('hepatocellular carcinoma', ('hepatocellular carcinoma','hepatic carcinoma')),
 ('mammary carcinoma', ('mammary carcinoma','mammary cancer','mammary tumor','mammary tumour')),
 ('thyroid carcinoma', ('thyroid carcinoma','thyroid cancer','thyroid tumor','thyroid tumour')),
 ('prostate cancer', ('prostate cancer','prostatic carcinoma')),
 ('primary lung tumor', ('primary lung tumor','primary lung tumour','pulmonary carcinoma','lung cancer')),
 ('glioma', ('glioma','brain tumor (glioma)','brain tumour (glioma)')),
 ('meningioma', ('meningioma',)),
 ('nasal tumor', ('nasal tumor','nasal tumour','nasal cancer','nasal carcinoma')),
 ('lymphoma', ('lymphoma','lymphosarcoma')),
 ('leukemia', ('leukemia','leukaemia')),
 ('multiple myeloma', ('multiple myeloma',)),
 ('chemodectoma', ('chemodectoma',)),
)
GENERIC_WORDS=('any type','other','multiple cancers','solid tumor','solid tumour','advanced unresectable')

def load_effective():
 base=json.loads((ROOT/'data'/'trials_base.json').read_text())
 upd=json.loads((ROOT/'data'/'trial_updates.json').read_text())
 rows={r['id']:r for r in base}
 for rid in upd.get('delete',[]): rows.pop(rid,None)
 for p in upd.get('upsert',[]): rows[p['id']]={**rows.get(p['id'],{}),**p}
 return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True]

def esc(x): return html.escape(str(x or ''))
def slugify(x): return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',x.lower())).strip('-')
def species_ok(r,s):
 v=str(r.get('species','')).lower(); return s.lower() in v or ('dog' in v and 'cat' in v)
def norm_text(x):
 return re.sub(r'[^a-z0-9]+',' ',str(x).lower()).strip()
def canonical_cancer(c):
 raw=norm_text(c)
 if not raw or any(norm_text(g) in raw for g in GENERIC_WORDS): return None
 # More specific rules are intentionally ordered before broad parent diagnoses.
 for canonical, aliases in CANONICAL_RULES:
  if any(norm_text(a) in raw for a in aliases): return canonical
 return None
def display_name(k):
 special={'scc':'SCC','aml':'AML'}
 return ' '.join(special.get(w,w.capitalize()) for w in k.split())
def row_cancers(r): return {x for x in (canonical_cancer(c) for c in r.get('cancers',[])) if x}

def page(title,desc,body,canonical,lang='en',alternates=None):
 alts=''.join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k,v in (alternates or {}).items())
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">{alts}<style>body{{font-family:system-ui,sans-serif;max-width:920px;margin:auto;padding:28px;line-height:1.55;color:#17243b}}a{{color:#175b8c}}article{{border-top:1px solid #d9e2ea;padding:12px 0}}.cta{{display:inline-block;padding:12px 18px;background:#17243b;color:white;text-decoration:none;border-radius:8px}}</style></head><body><header><a href="{SITE}/"><strong>Vet Cancer Trial Finder</strong></a><p>Free. No registration, email or paywall.</p></header><main>{body}<p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p><p>Answer a few questions about your pet to find potentially matching clinical trials and other cancer treatment options.</p><p><small>Listings change. Final eligibility and enrollment decisions are made by each research team.</small></p></main></body></html>'''
def cards(rows):
 return ''.join(f'<article><h3>{esc(r.get("title"))}</h3><p><strong>{esc(r.get("center"))}</strong> · {esc(r.get("country"))}</p><p>{esc(r.get("status"))}</p></article>' for r in rows)

def main():
 rows=load_effective()
 if OUT.exists(): shutil.rmtree(OUT)
 OUT.mkdir(parents=True)
 links=[]; index=[]
 cancers=sorted({c for r in rows for c in row_cancers(r)})
 for region,countries in REGIONS.items():
  rrows=[r for r in rows if r.get('country') in countries]; langs=EU_LANGS if region=='uk-europe' else ('en',); region_label='USA & Canada' if region=='north-america' else 'UK & Europe'
  for skey,sname in SPECIES.items():
   srows=[r for r in rrows if species_ok(r,sname)]
   for key in cancers:
    hit=[r for r in srows if key in row_cancers(r)]
    if not hit: continue
    label=display_name(key); cslug=slugify(key)
    for lang in langs:
     prefix='' if lang=='en' else f'{lang}/'; path=f'{prefix}{region}/{skey}/{cslug}/'; url=f'{SITE}/{path}'
     alternates={l:f'{SITE}/{"" if l=="en" else l+"/"}{region}/{skey}/{cslug}/' for l in langs}; alternates['x-default']=f'{SITE}/{region}/{skey}/{cslug}/'
     h1=f'{label}: Treatment Options and Clinical Trials for {sname}s in {region_label}' if lang=='en' else f'{label}: {LANGS[lang][0]} for {sname}s in {region_label}'; body=f'<h1>{esc(h1)}</h1><p>{esc(LANGS[lang][1])}: <strong>{len(hit)}</strong>.</p>'+((f'<p>This page brings together current treatment-focused options for {label} in {sname.lower()}s, including clinical trials and investigational or advanced treatment programs represented in our live catalog. Use the finder to review location and eligibility details.</p>' if lang=='en' else ''))+cards(hit)
     dest=OUT/path; dest.mkdir(parents=True,exist_ok=True); (dest/'index.html').write_text(page(h1,(f'Current {label} treatment options, clinical trials, advanced and experimental cancer treatments for {sname.lower()}s in {region_label}.' if lang=='en' else f'Current {label} cancer treatment trials for {sname.lower()}s in {region_label}.'),body,url,lang,alternates),encoding='utf-8')
     links.append(url)
     if lang=='en': index.append((h1,path))
 body='''<h1>Cancer Treatment Options and Clinical Trials for Dogs and Cats</h1>
<p>Find current canine and feline cancer treatment options, clinical trials, advanced treatments and experimental therapies by diagnosis and region.</p>
<h2>Find Cancer Treatment Options</h2><p>Start with your pet's cancer type and location. The live finder screens current treatment-focused opportunities and links to the treating or research program.</p>
<h2>Clinical Trials</h2><p>We track treatment trials for client-owned dogs and cats and remove observational, sample-only and diagnostic studies from treatment matching.</p>
<h2>More Treatment Options</h2><p>Beyond clinical trials, the finder also highlights selected advanced or less-common oncology treatments when a real patient access route can be verified.</p>
<h2>Electrochemotherapy</h2><p>Search veterinary centers offering electrochemotherapy, a local cancer treatment used for selected tumors in dogs and cats.</p>
<h2>Cancer Types</h2><p>Browse current treatment opportunities by diagnosis, including lymphoma, osteosarcoma, mast cell tumor, melanoma, soft tissue sarcoma, squamous cell carcinoma and other cancers represented in the live catalog.</p>
<h2>How It Works</h2><p>The catalog is built from current university, veterinary hospital, research-center and treatment-program sources. Listings are checked regularly, but the treating team always makes the final eligibility and enrollment decision.</p>
<h2>Current Treatment Pages</h2><ul>'''+''.join(f'<li><a href="{SITE}/{p}">{esc(n)}</a></li>' for n,p in sorted(index))+'</ul>'
 (OUT/'index.html').write_text(page('Vet Cancer Trial Finder | Treatment Options & Clinical Trials for Dogs and Cats','Free finder for current dog and cat cancer treatment options, clinical trials, advanced treatments and experimental therapies.',body,SITE+'/'),encoding='utf-8')
 links.insert(0,SITE+'/'); sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{esc(u)}</loc></url>\n' for u in links)+'</urlset>\n'; (OUT/'sitemap.xml').write_text(sm,encoding='utf-8'); (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n',encoding='utf-8'); (OUT/'.nojekyll').write_text('')
 print(f'Generated {len(links)} indexable pages from {len(rows)} current treatment opportunities using {len(cancers)} canonical cancer types')
if __name__=='__main__': main()
