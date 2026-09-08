#!/usr/bin/env python3
"""Generate crawlable owner-facing SEO pages from the effective treatment catalog."""
from __future__ import annotations
import html,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'seo'/'site'
FINDER='https://vet-cancer-trial-finder.streamlit.app/'; SITE='https://jdizhur-rgb.github.io/vet-trial-matcher'
EUROPE={'Belgium','Denmark','France','Germany','Italy','Netherlands','Portugal','Spain','Sweden','Switzerland','UK','Ireland','Austria','Czechia','Poland','Finland','Norway','Hungary','Slovenia','Cyprus'}
REGIONS={'north-america':{'USA','Canada'},'uk-europe':EUROPE}; SPECIES={'dogs':'Dog','cats':'Cat'}
LANGS={'en':('Clinical Trials and Cancer Treatment Studies','current treatment opportunities','Check your pet against these options'),'de':('Klinische Studien und Krebsbehandlungsstudien','aktuelle Behandlungsmöglichkeiten','Behandlungsoptionen prüfen'),'fr':('Essais cliniques et études de traitement du cancer','options thérapeutiques actuelles','Vérifier les options de traitement'),'es':('Ensayos clínicos y estudios de tratamiento del cáncer','opciones terapéuticas actuales','Consultar opciones de tratamiento'),'it':('Studi clinici e studi sul trattamento del cancro','opzioni terapeutiche attuali','Controlla le opzioni di trattamento'),'nl':('Klinische onderzoeken en kankerbehandelingsstudies','huidige behandelingsmogelijkheden','Bekijk behandelingsopties')}; EU_LANGS=('en','de','fr','es','it','nl')
CANONICAL_RULES=(('oral squamous cell carcinoma',('oral squamous cell carcinoma','oral scc','feline oral scc')),('squamous cell carcinoma',('squamous cell carcinoma','scc')),('oral melanoma',('oral melanoma','mucosal melanoma')),('melanoma',('melanoma',)),('mast cell tumor',('mast cell tumor','mast cell tumour','mct')),('soft tissue sarcoma',('soft tissue sarcoma','soft-tissue sarcoma','sts')),('histiocytic sarcoma',('histiocytic sarcoma',)),('hemangiosarcoma',('hemangiosarcoma','haemangiosarcoma','hsa')),('osteosarcoma',('osteosarcoma','bone cancer')),('urothelial carcinoma',('urothelial','transitional cell carcinoma','bladder cancer','tcc')),('hepatocellular carcinoma',('hepatocellular carcinoma','hepatic carcinoma')),('mammary carcinoma',('mammary carcinoma','mammary cancer','mammary tumor','mammary tumour')),('thyroid carcinoma',('thyroid carcinoma','thyroid cancer','thyroid tumor','thyroid tumour')),('prostate cancer',('prostate cancer','prostatic carcinoma')),('primary lung tumor',('primary lung tumor','primary lung tumour','pulmonary carcinoma','lung cancer')),('glioma',('glioma','brain tumor (glioma)','brain tumour (glioma)')),('meningioma',('meningioma',)),('nasal tumor',('nasal tumor','nasal tumour','nasal cancer','nasal carcinoma')),('lymphoma',('lymphoma','lymphosarcoma')),('leukemia',('leukemia','leukaemia')),('multiple myeloma',('multiple myeloma',)),('chemodectoma',('chemodectoma',)))
GENERIC_WORDS=('any type','other','multiple cancers','solid tumor','solid tumour','advanced unresectable')
LABELS={'active_treatment_target':'active tumor required','measurable_disease':'measurable disease required','measurable_tumor':'measurable tumor required','prior_treatment_allowed':'prior treatment allowed','progressive_disease':'progressive disease required','chemo_washout_days':'chemotherapy washout','radiation_washout_days':'radiation washout','radiation_washout_weeks':'radiation washout','no_concurrent_anticancer':'no concurrent anticancer treatment','no_concurrent_anticancer_therapy':'no concurrent anticancer therapy','no_pregnant_household_members':'household pregnancy restriction'}
def load_effective():
 base=json.loads((ROOT/'data'/'trials_base.json').read_text()); upd=json.loads((ROOT/'data'/'trial_updates.json').read_text()); rows={r['id']:r for r in base}
 for p in upd.get('upsert',[]): rows[p['id']]={**rows.get(p['id'],{}),**p}
 for rid in upd.get('delete',[]): rows.pop(rid,None)
 return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True]
def esc(x): return html.escape(str(x or ''))
def slugify(x): return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',x.lower())).strip('-')
def norm(x): return re.sub(r'[^a-z0-9]+',' ',str(x).lower()).strip()
def species_ok(r,s):
 v=r.get('species',''); vals=v if isinstance(v,list) else re.split(r'[/,;]',str(v)); vals={norm(x) for x in vals}; return norm(s) in vals or ('dog' in vals and 'cat' in vals)
def canonical_cancer(c):
 raw=norm(c)
 if not raw or any(norm(g) in raw for g in GENERIC_WORDS): return None
 for key,aliases in CANONICAL_RULES:
  if any(norm(a) in raw for a in aliases): return key
 return None
def row_cancers(r): return {x for x in (canonical_cancer(c) for c in r.get('cancers',[])) if x}
def display_name(k): return ' '.join({'scc':'SCC','aml':'AML'}.get(w,w.capitalize()) for w in k.split())
def prose(v):
 if v is None or v is False or v=='': return ''
 if isinstance(v,str): return v.strip()
 if isinstance(v,list): return '; '.join(filter(None,(prose(x) for x in v)))
 if isinstance(v,dict):
  out=[]
  for k,x in v.items():
   if x is False or x is None or x=='': continue
   label=LABELS.get(k,k.replace('_',' '))
   if x is True: out.append(label.capitalize())
   elif k.endswith('_days'): out.append(f'{label}: {x} days')
   elif k.endswith('_weeks'): out.append(f'{label}: {x} weeks')
   else: out.append(f'{label.capitalize()}: {prose(x)}')
  return '; '.join(out)
 return str(v)
def contact_text(r):
 v=r.get('contacts') or r.get('contact')
 if not v: return ''
 if isinstance(v,list): return '; '.join(filter(None,(prose(x) for x in v)))
 return prose(v)
def cards(rows):
 out=[]
 for r in rows:
  p=[f'<article class="card"><h3>{esc(r.get("title"))}</h3><p class="meta"><strong>{esc(r.get("center"))}</strong> · {esc(r.get("country"))}</p>']
  if r.get('status'): p.append(f'<p class="status">{esc(r["status"])}</p>')
  treatment=prose(r.get('intervention') or r.get('treatment') or r.get('notes'))
  if treatment: p.append(f'<p><b>Treatment:</b> {esc(treatment)}</p>')
  req=prose(r.get('requires')); exc=prose(r.get('excludes')); funding=prose(r.get('funding')); contact=contact_text(r)
  if req: p.append(f'<p><b>Key eligibility:</b> {esc(req)}</p>')
  if exc: p.append(f'<p><b>Important exclusions:</b> {esc(exc)}</p>')
  if funding: p.append(f'<p><b>Costs:</b> {esc(funding)}</p>')
  if contact: p.append(f'<p><b>Contact:</b> {esc(contact)}</p>')
  if r.get('last_verified'): p.append(f'<p class="verified">Last verified: {esc(r["last_verified"])}</p>')
  if r.get('url'): p.append(f'<p><a class="official" href="{esc(r["url"])}" rel="noopener">Official study / enrollment information →</a></p>')
  p.append('</article>'); out.append(''.join(p))
 return ''.join(out)
def page(title,desc,body,canonical,lang='en',alts=None):
 alternate=''.join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k,v in (alts or {}).items())
 css='*{box-sizing:border-box}body{margin:0;background:#f6f8fb;color:#17243b;font:16px/1.55 system-ui,-apple-system,sans-serif}.wrap{max-width:900px;margin:auto;padding:24px 20px 48px}header{padding:6px 0 22px;border-bottom:1px solid #dce4ec}header a{font-weight:750;text-decoration:none}h1{font-size:clamp(2rem,5vw,3rem);line-height:1.12;margin:30px 0 12px}h2{margin-top:28px}.lead{font-size:1.08rem;color:#42536a}.free{background:#eaf3fb;border-radius:12px;padding:14px 16px;margin:22px 0}.cta{display:inline-block;background:#175b8c;color:#fff!important;text-decoration:none;font-weight:750;padding:12px 18px;border-radius:9px}.card{background:#fff;border:1px solid #d9e2ea;border-radius:14px;padding:20px;margin:18px 0;box-shadow:0 1px 2px rgba(23,36,59,.04)}.card h3{font-size:1.28rem;line-height:1.3;margin:0 0 8px}.meta,.verified{color:#5a697c}.status{font-weight:700}.official{font-weight:650}a{color:#175b8c}@media(max-width:600px){.wrap{padding:18px 15px 36px}.card{padding:16px}h1{font-size:2rem}.cta{width:auto;max-width:100%}}'
 return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">{alternate}<style>{css}</style></head><body><div class="wrap"><header><a href="{SITE}/">← Cancer Trial Finder For Dogs And Cats</a><p>Find cancer treatment options and clinical trials for dogs and cats.</p></header><main>{body}</main><footer><p><small>Listings change. Final eligibility and enrollment decisions are made by each research or treatment team.</small></p></footer></div></body></html>'
def main():
 rows=load_effective(); shutil.rmtree(OUT,ignore_errors=True); OUT.mkdir(parents=True); links=[]; index=[]; cancers=sorted({c for r in rows for c in row_cancers(r)})
 for region,countries in REGIONS.items():
  rrows=[r for r in rows if r.get('country') in countries]; langs=EU_LANGS if region=='uk-europe' else ('en',); region_label='USA & Canada' if region=='north-america' else 'UK & Europe'
  for skey,sname in SPECIES.items():
   srows=[r for r in rrows if species_ok(r,sname)]
   for key in cancers:
    hit=[r for r in srows if key in row_cancers(r)]
    if not hit: continue
    label=display_name(key); slug=slugify(key)
    for lang in langs:
     prefix='' if lang=='en' else lang+'/'; path=f'{prefix}{region}/{skey}/{slug}/'; url=f'{SITE}/{path}'; alts={l:f'{SITE}/{"" if l=="en" else l+"/"}{region}/{skey}/{slug}/' for l in langs}; alts['x-default']=f'{SITE}/{region}/{skey}/{slug}/'
     h1=f'{label}: Clinical Trials and Cancer Treatment Studies for {sname}s in {region_label}' if lang=='en' else f'{label}: {LANGS[lang][0]} for {sname}s in {region_label}'
     intro=(f'<h1>{esc(h1)}</h1><p class="lead">{len(hit)} {LANGS[lang][1]} in our catalog. Trial names, locations and official source links are shown below.</p>')
     if lang=='en': intro+=f'<h2>About {esc(label)}</h2><p>This page collects treatment-focused research and advanced oncology options currently represented in our live catalog for {sname.lower()}s with {esc(label)}.</p><h2>Treatment &amp; research</h2>'
     intro+=f'<div class="free"><strong>100% FREE</strong> — view matching options, details, contacts and official enrollment links.<br><small>No registration, email or paid report.</small></div><p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p>'+cards(hit)
     dest=OUT/path; dest.mkdir(parents=True,exist_ok=True); (dest/'index.html').write_text(page(h1,f'Current {label} treatment trials and cancer treatment studies for {sname.lower()}s in {region_label}.',intro,url,lang,alts),encoding='utf-8'); links.append(url)
     if lang=='en': index.append((h1,path))
 body='<h1>Cancer Treatment Options and Clinical Trials for Dogs and Cats</h1><p class="lead">Browse current treatment-focused opportunities by diagnosis and region, or use the free matcher.</p><p><a class="cta" href="'+FINDER+'">Search treatment options</a></p><h2>Current treatment pages</h2><ul>'+''.join(f'<li><a href="{SITE}/{p}">{esc(n)}</a></li>' for n,p in sorted(index))+'</ul>'
 (OUT/'index.html').write_text(page('Cancer Trial Finder For Dogs And Cats | Treatment Options & Clinical Trials','Free finder for current dog and cat cancer treatment options and clinical trials.',body,SITE+'/'),encoding='utf-8'); links.insert(0,SITE+'/')
 sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{esc(u)}</loc></url>\n' for u in links)+'</urlset>\n'; (OUT/'sitemap.xml').write_text(sm,encoding='utf-8'); (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n',encoding='utf-8'); (OUT/'.nojekyll').write_text(''); print(f'Generated {len(links)} pages from {len(rows)} treatment opportunities')
if __name__=='__main__': main()
