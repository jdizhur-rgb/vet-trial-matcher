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
'en':('Clinical Trials and Cancer Treatment Studies','Current treatment-focused opportunities','Search current treatment opportunities'),
'de':('Klinische Studien und Krebsbehandlungsstudien','Aktuelle behandlungsorientierte Möglichkeiten','Aktuelle Behandlungsmöglichkeiten suchen'),
'fr':('Essais cliniques et études de traitement du cancer','Options thérapeutiques actuellement disponibles','Rechercher les options de traitement actuelles'),
'es':('Ensayos clínicos y estudios de tratamiento del cáncer','Opciones terapéuticas disponibles actualmente','Buscar opciones de tratamiento actuales'),
'it':('Studi clinici e studi sul trattamento del cancro','Opportunità terapeutiche attualmente disponibili','Cerca le opzioni terapeutiche attuali'),
'nl':('Klinische onderzoeken en kankerbehandelingsstudies','Huidige behandelingsgerichte mogelijkheden','Zoek actuele behandelingsmogelijkheden'),
}
EU_LANGS=('en','de','fr','es','it','nl')
GENERIC={'all cancers','solid tumors','solid tumor','other','multiple cancers','other cancer','cancer any type','advanced unresectable tumor','other solid tumor','carcinoma other','sarcoma other','other sarcoma','oral tumor','oral tumor other','other bone tumor','other liver tumor','melanoma other','lymphoma other','mammary tumor other'}
ALIASES={
 'urothelial/transitional cell carcinoma':'urothelial carcinoma','transitional cell carcinoma':'urothelial carcinoma','bladder cancer':'urothelial carcinoma',
 'brain tumor (glioma)':'glioma','brain tumor glioma':'glioma',
 'feline oral scc':'oral squamous cell carcinoma','squamous cell carcinoma other':'squamous cell carcinoma',
 'hepatic carcinoma':'hepatocellular carcinoma','prostatic carcinoma':'prostate cancer','thyroid tumor/carcinoma':'thyroid carcinoma','thyroid tumor':'thyroid carcinoma',
 'primary bone tumor':'osteosarcoma','pulmonary carcinoma':'primary lung tumor'
}

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
def norm_cancer(c):
 k=str(c).strip().lower()
 if not k or k in GENERIC: return None
 return ALIASES.get(k,k)
def display_name(k): return ' '.join(w.upper() if w in {'scc','aml'} else w.capitalize() for w in k.split())
def row_cancers(r): return {x for x in (norm_cancer(c) for c in r.get('cancers',[])) if x}

def page(title,desc,body,canonical,lang='en',alternates=None):
 alts=''.join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k,v in (alternates or {}).items())
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">{alts}<style>body{{font-family:system-ui,sans-serif;max-width:920px;margin:auto;padding:28px;line-height:1.55;color:#17243b}}a{{color:#175b8c}}article{{border-top:1px solid #d9e2ea;padding:12px 0}}.cta{{display:inline-block;padding:12px 18px;background:#17243b;color:white;text-decoration:none;border-radius:8px}}</style></head><body><header><a href="{SITE}/"><strong>Cancer Trial Finder For Dogs And Cats</strong></a><p>Free. No registration, email or paywall.</p></header><main>{body}<p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p><p><small>Listings change. Final eligibility and enrollment decisions are made by each research team.</small></p></main></body></html>'''
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
     h1=f'{label}: {LANGS[lang][0]} for {sname}s in {region_label}'; body=f'<h1>{esc(h1)}</h1><p>{esc(LANGS[lang][1])}: <strong>{len(hit)}</strong>.</p>{cards(hit)}'
     dest=OUT/path; dest.mkdir(parents=True,exist_ok=True); (dest/'index.html').write_text(page(h1,f'Current {label} cancer treatment trials for {sname.lower()}s in {region_label}.',body,url,lang,alternates),encoding='utf-8')
     links.append(url)
     if lang=='en': index.append((h1,path))
 body='<h1>Veterinary Cancer Clinical Trials for Dogs and Cats</h1><p>Browse only cancer and region combinations that currently have treatment opportunities in the live catalog.</p><ul>'+''.join(f'<li><a href="{SITE}/{p}">{esc(n)}</a></li>' for n,p in sorted(index))+'</ul>'
 (OUT/'index.html').write_text(page('Cancer Trial Finder For Dogs And Cats','Free current veterinary cancer treatment trial finder for dogs and cats.',body,SITE+'/'),encoding='utf-8')
 links.insert(0,SITE+'/'); sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{esc(u)}</loc></url>\n' for u in links)+'</urlset>\n'; (OUT/'sitemap.xml').write_text(sm,encoding='utf-8'); (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n',encoding='utf-8'); (OUT/'.nojekyll').write_text('')
 print(f'Generated {len(links)} indexable pages from {len(rows)} current treatment opportunities; generic and duplicate cancer labels omitted')
if __name__=='__main__': main()
