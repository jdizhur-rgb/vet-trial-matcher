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
LANGS={'en':('Clinical Trials and Cancer Treatment Studies','Current treatment-focused opportunities','Check your pet against these trials'),'de':('Klinische Studien und Krebsbehandlungsstudien','Aktuelle behandlungsorientierte Möglichkeiten','Behandlungsmöglichkeiten prüfen'),'fr':('Essais cliniques et études de traitement du cancer','Options thérapeutiques actuellement disponibles','Vérifier les options de traitement'),'es':('Ensayos clínicos y estudios de tratamiento del cáncer','Opciones terapéutiques disponibles actualmente','Comprobar opciones de tratamiento'),'it':('Studi clinici e studi sul trattamento del cancro','Opportunità terapeutiche attualmente disponibili','Verifica le opzioni di trattamento'),'nl':('Klinische onderzoeken en kankerbehandelingsstudies','Huidige behandelingsgerichte mogelijkheden','Bekijk behandelingsmogelijkheden')}
EU_LANGS=('en','de','fr','es','it','nl')
CANONICAL_RULES=(('oral squamous cell carcinoma',('oral squamous cell carcinoma','oral scc','feline oral scc')),('squamous cell carcinoma',('squamous cell carcinoma','scc')),('oral melanoma',('oral melanoma','mucosal melanoma')),('melanoma',('melanoma',)),('mast cell tumor',('mast cell tumor','mast cell tumour','mct')),('soft tissue sarcoma',('soft tissue sarcoma','soft-tissue sarcoma','sts')),('histiocytic sarcoma',('histiocytic sarcoma',)),('hemangiosarcoma',('hemangiosarcoma','haemangiosarcoma','hsa')),('osteosarcoma',('osteosarcoma','bone cancer')),('urothelial carcinoma',('urothelial','transitional cell carcinoma','bladder cancer','tcc')),('hepatocellular carcinoma',('hepatocellular carcinoma','hepatic carcinoma')),('mammary carcinoma',('mammary carcinoma','mammary cancer','mammary tumor','mammary tumour')),('thyroid carcinoma',('thyroid carcinoma','thyroid cancer','thyroid tumor','thyroid tumour')),('prostate cancer',('prostate cancer','prostatic carcinoma')),('primary lung tumor',('primary lung tumor','primary lung tumour','pulmonary carcinoma','lung cancer')),('glioma',('glioma','brain tumor (glioma)','brain tumour (glioma)')),('meningioma',('meningioma',)),('nasal tumor',('nasal tumor','nasal tumour','nasal cancer','nasal carcinoma')),('lymphoma',('lymphoma','lymphosarcoma')),('leukemia',('leukemia','leukaemia')),('multiple myeloma',('multiple myeloma',)),('chemodectoma',('chemodectoma',)))
GENERIC_WORDS=('any type','other','multiple cancers','solid tumor','solid tumour','advanced unresectable')

CANCER_INFO={
'lymphoma':('Lymphoma is a cancer of lymphocytes, a type of white blood cell. In dogs it commonly causes enlarged lymph nodes, while in cats gastrointestinal lymphoma is especially common; behavior and treatment vary substantially by subtype and grade.','Systemic chemotherapy is the main treatment for many forms of lymphoma. Current research includes new drug combinations, targeted agents, immunotherapies and cellular therapies intended to improve remission duration or provide options after relapse.'),
'osteosarcoma':('Osteosarcoma is an aggressive bone cancer seen most often in dogs, particularly large and giant breeds. It commonly affects the long bones of the limbs, causes pain and lameness, and has a strong tendency to spread to the lungs.','Treatment often combines control of the primary bone tumor through surgery or radiation with systemic chemotherapy. Research is exploring immunotherapy, targeted treatments and other strategies aimed at delaying or treating metastatic disease.'),
'hemangiosarcoma':('Hemangiosarcoma is an aggressive cancer arising from cells associated with blood vessels. In dogs it often develops in the spleen, heart, liver or other tissues and may be discovered after internal bleeding or sudden collapse.','When possible, treatment may include surgery followed by systemic chemotherapy. Research is focused on better control of microscopic metastatic disease, including targeted drugs, immunotherapy and novel drug combinations.'),
'mast cell tumor':('Mast cell tumors are among the most common malignant skin tumors in dogs and can range from relatively localized disease to aggressive cancer with metastatic potential. Tumor grade, location, margins and lymph-node involvement help guide treatment decisions.','Surgery is often the primary treatment for localized tumors, with radiation, chemotherapy or targeted therapy used in selected cases. Research continues into kinase inhibitors, immune-based treatments and approaches for recurrent or high-risk disease.'),
'histiocytic sarcoma':('Histiocytic sarcoma is a rare, aggressive cancer arising from histiocytic cells of the immune system. It may occur as a localized tumor or as disseminated disease involving multiple organs, and metastatic spread can occur early.','Localized disease may be treated with surgery or radiation when feasible, while systemic therapy is commonly considered because of metastatic risk. Research is investigating chemotherapy combinations, molecular targets and immune-based approaches for this difficult cancer.'),
'soft tissue sarcoma':('Soft tissue sarcomas are a diverse group of tumors arising from connective and supporting tissues. Their behavior varies by subtype and grade, but local invasion and the ability to recur after incomplete removal are important treatment considerations.','Wide surgical removal is commonly preferred for localized disease, with radiation used when adequate margins cannot be achieved and systemic therapy considered for higher-risk tumors. Research includes targeted, local and immune-based treatments.'),
'oral melanoma':('Oral melanoma is an aggressive tumor of pigment-producing cells and is an important oral cancer in dogs. These tumors can invade surrounding tissues and may spread to regional lymph nodes, lungs and other organs.','Local control may involve surgery and/or radiation, while systemic treatment can be considered because of metastatic risk. Research includes immunotherapy, vaccines, targeted agents and combinations intended to improve control beyond standard local treatment.'),
'melanoma':('Melanoma arises from melanocytes, the cells that produce pigment. Its behavior depends strongly on location: some cutaneous melanomas can behave relatively benignly, while oral and certain other forms may be highly invasive and metastatic.','Treatment is tailored to tumor site and stage and may include surgery, radiation and systemic therapy. Research is evaluating immune-based therapies, vaccines and targeted approaches for tumors with a higher risk of recurrence or spread.'),
'oral squamous cell carcinoma':('Oral squamous cell carcinoma is a locally invasive cancer arising from the lining of the mouth. It is especially important in cats, where it can invade the jaw and surrounding tissues and is often difficult to remove completely.','Treatment depends on location and extent and may involve surgery, radiation or systemic/local drug therapy. Research is exploring targeted treatments, immunotherapy and novel local-delivery approaches to improve tumor control while preserving quality of life.'),
'squamous cell carcinoma':('Squamous cell carcinoma is a cancer of squamous epithelial cells and can arise in the skin, mouth, nasal tissues, digits and other sites. Its metastatic potential and response to treatment vary considerably with location and stage.','Surgery and radiation are important local treatments when feasible. Current research includes targeted drugs, immunotherapy and local treatment strategies designed to improve control in tumors that are difficult to remove or have spread.'),
'urothelial carcinoma':('Urothelial carcinoma, also called transitional cell carcinoma, most often affects the urinary bladder or urethra in dogs. Its location can make complete surgical removal difficult, and spread to lymph nodes or distant organs may occur.','Medical treatment commonly uses anti-inflammatory and anticancer drugs, with surgery or radiation appropriate in selected cases. Research is investigating targeted agents, drug combinations and molecularly guided therapies.'),
'hepatocellular carcinoma':('Hepatocellular carcinoma is a primary cancer of liver cells. Some tumors occur as a single large mass that may be amenable to surgery, while nodular or diffuse forms can be more difficult to treat.','Surgical removal can provide strong local control when a solitary tumor is resectable. For unresectable or metastatic disease, research is evaluating systemic, targeted and image-guided local therapies.'),
'mammary carcinoma':('Mammary carcinoma is a malignant tumor of mammary tissue and occurs most often in female dogs and cats. Biological behavior varies by species, tumor type, size and stage, and some tumors can spread to lymph nodes or lungs.','Surgery is the main local treatment when disease is operable, with systemic therapy considered for higher-risk cases. Research includes molecularly targeted drugs, immunotherapy and treatment strategies for metastatic mammary cancer.'),
'thyroid carcinoma':('Thyroid carcinoma arises from thyroid tissue in the neck. Some tumors remain locally confined, while invasive or metastatic tumors can involve nearby structures or spread to the lungs and other sites.','Surgery can be effective for mobile, resectable tumors; radiation and systemic treatments may be considered when surgery is not possible or disease has spread. Research includes targeted therapies and other systemic approaches.'),
'prostate cancer':('Prostate cancer in dogs is uncommon but often biologically aggressive. Tumors can obstruct the urinary tract, invade nearby tissues and metastasize to lymph nodes, lungs or bone.','Treatment is individualized and may include anti-inflammatory drugs, radiation, chemotherapy or other local/systemic approaches. Research is evaluating targeted agents and new combinations for a cancer in which complete surgical removal is often not feasible.'),
'primary lung tumor':('Primary lung tumors begin in the lung rather than spreading there from another cancer. They are uncommon in dogs and cats and may be found incidentally or after coughing, breathing changes or other respiratory signs.','Surgery is often considered for a solitary resectable lung tumor. For advanced, metastatic or unresectable disease, systemic therapy and newer targeted approaches may be considered or studied.'),
'glioma':('Gliomas are brain tumors arising from glial cells, the cells that support the nervous system. Their effects depend on tumor location and can include seizures, behavior changes, weakness or other neurologic signs.','Treatment may include surgery, radiation and medical management of neurologic symptoms. Research is exploring improved radiation techniques, targeted drugs, immunotherapy and methods of delivering treatment more effectively across the brain.'),
'meningioma':('Meningioma arises from the membranes surrounding the brain or spinal cord. It is one of the more common primary brain tumors in dogs and cats and can cause neurologic signs by compressing nearby nervous tissue.','Surgery and radiation are important treatments depending on tumor location and patient factors. Research includes advanced radiation, local therapies and systemic approaches for tumors that cannot be fully removed or that recur.'),
'nasal tumor':('Nasal tumors develop within the nasal cavity or sinuses and can cause nasal discharge, bleeding, facial changes or breathing difficulty. They are usually locally invasive, and some types can eventually spread beyond the primary site.','Radiation therapy is a major treatment for many nasal cancers, with surgery or systemic therapy used selectively. Research includes precision radiation, targeted agents and combinations intended to improve local control and limit recurrence.'),
'leukemia':('Leukemia is a cancer of blood-forming cells that involves the bone marrow and circulating blood. Acute and chronic leukemias behave very differently, so precise classification is important when considering treatment and prognosis.','Systemic drug therapy is the main treatment and depends on the leukemia subtype. Research includes new chemotherapy combinations, targeted agents and molecular approaches intended to treat resistant or relapsed disease more selectively.'),
'multiple myeloma':('Multiple myeloma is a cancer of plasma cells, immune cells that normally produce antibodies. It can affect bone marrow and bones and may cause abnormal blood proteins, anemia, kidney problems or bone lesions.','Systemic drug therapy is the main treatment, often producing meaningful disease control in responsive patients. Research is evaluating newer drug classes and combinations adapted from advances in plasma-cell cancer treatment.'),
'chemodectoma':('Chemodectoma is a tumor arising from chemoreceptor tissue, most often near the base of the heart. Many grow slowly, but larger tumors can compress nearby structures, cause fluid around the heart or chest, or occasionally metastasize.','Management depends on tumor size, symptoms and spread and may include surgery in selected cases, radiation or medical therapy. Research and clinical use increasingly include targeted drugs and advanced radiation approaches for tumors that cannot be safely removed.')
}

def load_effective():
 base=json.loads((ROOT/'data'/'trials_base.json').read_text()); upd=json.loads((ROOT/'data'/'trial_updates.json').read_text()); rows={r['id']:r for r in base}
 for rid in upd.get('delete',[]): rows.pop(rid,None)
 for p in upd.get('upsert',[]): rows[p['id']]={**rows.get(p['id'],{}),**p}
 return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True]
def esc(x): return html.escape(str(x or ''))
def slugify(x): return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',x.lower())).strip('-')
def species_ok(r,s):
 v=str(r.get('species','')).lower(); return s.lower() in v or ('dog' in v and 'cat' in v)
def norm_text(x): return re.sub(r'[^a-z0-9]+',' ',str(x).lower()).strip()
def canonical_cancer(c):
 raw=norm_text(c)
 if not raw or any(norm_text(g) in raw for g in GENERIC_WORDS): return None
 for canonical,aliases in CANONICAL_RULES:
  if any(norm_text(a) in raw for a in aliases): return canonical
 return None
def display_name(k): return ' '.join({'scc':'SCC','aml':'AML'}.get(w,w.capitalize()) for w in k.split())
def row_cancers(r): return {x for x in (canonical_cancer(c) for c in r.get('cancers',[])) if x}
def cancer_intro(key,label):
 info=CANCER_INFO.get(key)
 if not info: return ''
 about,research=info
 return f'<section class="cancer-info"><h2>About {esc(label)}</h2><p>{esc(about)}</p><h2>Treatment &amp; research</h2><p>{esc(research)}</p></section>'

def page(title,desc,body,canonical,lang='en',alternates=None):
 alts=''.join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k,v in (alternates or {}).items())
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">{alts}<style>body{{font-family:system-ui,sans-serif;max-width:920px;margin:auto;padding:28px;line-height:1.55;color:#17243b}}a{{color:#175b8c}}article{{border-top:1px solid #d9e2ea;padding:18px 0}}article h3{{margin-bottom:5px}}.count{{font-size:1.12rem}}.status{{font-weight:600}}.cancer-info{{margin:18px 0 22px;padding:2px 0}}.cancer-info h2{{font-size:1.18rem;margin:16px 0 4px}}.cancer-info p{{margin:4px 0 10px}}.free-note{{font-size:1.05rem;background:#eef7fc;border-left:4px solid #287fb8;padding:10px 14px;border-radius:6px}}.cta,.trial-link{{display:inline-block;padding:10px 15px;background:#287fb8;color:white;text-decoration:none;border-radius:8px}}.trial-link{{padding:7px 11px;font-size:.92rem;background:#3b8fc4}}.meta{{color:#4d5967}}small{{color:#596674}}</style></head><body><header><a href="{SITE}/"><strong>Cancer Trial Finder For Dogs And Cats</strong></a><p><strong>100% FREE.</strong> No registration, email or paywall.</p></header><main>{body}<p><small>General cancer information is educational and is not a substitute for veterinary oncology advice. Listings change. Final eligibility and enrollment decisions are made by each research team. Always confirm current recruiting status with the study team.</small></p></main></body></html>'''

def cards(rows):
 out=[]
 for r in rows:
  notes=r.get('notes') or ''; funding=r.get('funding') or ''; verified=r.get('verified') or ''; contact=r.get('contacts') or r.get('contact') or ''; url=r.get('url') or ''
  bits=[f'<article><h3>{esc(r.get("title"))}</h3>',f'<p class="meta"><strong>{esc(r.get("center"))}</strong> · {esc(r.get("country"))}</p>',f'<p class="status">{esc(r.get("status"))}</p>']
  if notes: bits.append(f'<p>{esc(notes)}</p>')
  if funding: bits.append(f'<p><strong>Costs:</strong> {esc(funding)}</p>')
  if contact: bits.append(f'<p><strong>Contact:</strong> {esc(contact)}</p>')
  if verified: bits.append(f'<p><small>Last verified: {esc(verified)}</small></p>')
  if url: bits.append(f'<p><a class="trial-link" href="{esc(url)}" rel="nofollow noopener">Official study / enrollment information</a></p>')
  bits.append('</article>'); out.append(''.join(bits))
 return ''.join(out)

def main():
 rows=load_effective()
 if OUT.exists(): shutil.rmtree(OUT)
 OUT.mkdir(parents=True); links=[]; index=[]; cancers=sorted({c for r in rows for c in row_cancers(r)})
 for region,countries in REGIONS.items():
  rrows=[r for r in rows if r.get('country') in countries]; langs=EU_LANGS if region=='uk-europe' else ('en',); region_label='USA & Canada' if region=='north-america' else 'UK & Europe'
  for skey,sname in SPECIES.items():
   srows=[r for r in rrows if species_ok(r,sname)]
   for key in cancers:
    hit=[r for r in srows if key in row_cancers(r)]
    if not hit: continue
    label=display_name(key); cslug=slugify(key)
    for lang in langs:
     prefix='' if lang=='en' else f'{lang}/'; path=f'{prefix}{region}/{skey}/{cslug}/'; url=f'{SITE}/{path}'; alternates={l:f'{SITE}/{"" if l=="en" else l+"/"}{region}/{skey}/{cslug}/' for l in langs}; alternates['x-default']=f'{SITE}/{region}/{skey}/{cslug}/'
     h1=f'{label}: {LANGS[lang][0]} for {sname}s in {region_label}'
     noun='trial' if len(hit)==1 else 'trials'; body=f'<h1>{esc(h1)}</h1>{cancer_intro(key,label)}<p class="count"><strong>{len(hit)} current treatment {noun}</strong> in our catalog. Trial names, locations and source links are shown below.</p><p class="free-note"><strong>100% FREE — view all matching trials, details, contacts and official enrollment links.</strong><br>Free means free. No hidden trial results. No paid report.</p><p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p>{cards(hit)}'
     dest=OUT/path; dest.mkdir(parents=True,exist_ok=True); (dest/'index.html').write_text(page(h1,f'{len(hit)} current {label} cancer treatment {noun} for {sname.lower()}s in {region_label}. Free trial names, locations and enrollment links.',body,url,lang,alternates),encoding='utf-8'); links.append(url)
     if lang=='en': index.append((h1,path,len(hit)))
 body='<h1>Veterinary Cancer Clinical Trials for Dogs and Cats</h1><p>Browse cancer and region combinations that currently have treatment opportunities in the live catalog.</p><p class="free-note"><strong>100% FREE — view all matching trials, details, contacts and official enrollment links.</strong><br>Free means free. No hidden trial results. No paid report.</p><p><a class="cta" href="'+FINDER+'">Check your pet against these trials</a></p><ul>'+''.join(f'<li><a href="{SITE}/{p}">{esc(n)}</a> — {count} current treatment {"trial" if count==1 else "trials"}</li>' for n,p,count in sorted(index))+'</ul>'
 (OUT/'index.html').write_text(page('Cancer Trial Finder For Dogs And Cats','Free current veterinary cancer treatment trial finder for dogs and cats.',body,SITE+'/'),encoding='utf-8'); links.insert(0,SITE+'/'); sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{esc(u)}</loc></url>\n' for u in links)+'</urlset>\n'; (OUT/'sitemap.xml').write_text(sm,encoding='utf-8'); (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n',encoding='utf-8'); (OUT/'.nojekyll').write_text('')
 print(f'Generated {len(links)} indexable pages from {len(rows)} current treatment opportunities using {len(cancers)} canonical cancer types')
if __name__=='__main__': main()
