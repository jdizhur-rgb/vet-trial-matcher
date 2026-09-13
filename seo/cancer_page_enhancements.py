#!/usr/bin/env python3
"""Owner-facing polish for generated English cancer landing pages."""
from __future__ import annotations
import html, json, re
from pathlib import Path
from cancer_owner_content import CONTENT

H1_RE=re.compile(r'<h1>(?P<label>.+?): Clinical Trials and Cancer Treatment Studies for (?P<species>Dogs|Cats) in (?P<region>USA &amp; Canada|UK &amp; Europe)</h1>')
LEAD_RE=re.compile(r'<p class="lead">(?P<count>\d+) current treatment opportunities in our catalog\. Trial names, locations and official source links are shown below\.</p>')
DISEASE_RE=re.compile(r'<section class="disease">.*?</section>',re.S)
CANONICAL_RE=re.compile(r'<link rel="canonical" href="([^"]+)">')
FREE_RE=re.compile(r'<div class="free">.*?</div>\s*<p><a class="cta" href="([^"]+)">.*?</a></p>',re.S)
CARD_RE=re.compile(r'<article class="card"><h3>(.*?)</h3><p class="meta">(.*?)</p>(.*?)</article>',re.S)
LOCATION_RE=re.compile(r'(<div class="study-locations">.*?</div>)',re.S)

CSS=r'''.cancer-page{max-width:860px}.cancer-page p,.cancer-page li{color:#263238}.cancer-page h1{font-size:clamp(1.55rem,3.4vw,2.05rem);line-height:1.18;max-width:780px;margin:4px 0 5px;color:#477ca8!important;font-weight:700}.cancer-page .eyebrow{margin:0 0 18px;color:#8a98a8!important;font-size:.82rem;font-weight:500;letter-spacing:.01em}.cancer-page .disease{margin-top:24px}.cancer-page .disease h2{font-size:1.24rem;margin-top:20px}.options-transition{margin:28px 0 16px}.options-transition h2{margin:0 0 6px;color:#477ca8!important;font-size:1.28rem}.options-transition p{margin:.3rem 0;color:#263238}.options-transition .option-count{font-weight:700;color:#334e68}.options-transition .free-inline{font-size:.88rem;color:#526b80}.eligibility-cta{display:block;width:100%;box-sizing:border-box;text-align:center;margin-top:10px;padding:9px 15px;border-radius:9px;background:#eee9ff!important;border:1px solid #d8cff4;color:#43385f!important;text-decoration:none;font-size:.94rem;font-weight:400;line-height:1.2}.eligibility-cta:hover{background:#e5defb!important;color:#43385f!important}.cancer-page .card{padding:15px 16px;margin:12px 0}.cancer-page .card h3{font-size:1rem;line-height:1.4;color:#274f70;margin:0 0 5px}.cancer-page .card .meta{font-size:.95rem;margin:.2rem 0 .6rem}.cancer-page .card .study-locations{margin:10px 0 8px;padding:10px 12px}.cancer-page .card .study-locations .field-label{font-size:.92rem}.cancer-page .card .study-locations li{font-size:.92rem;line-height:1.45}.trial-details{border-top:1px solid #e2e8ee;margin-top:10px;padding-top:3px}.trial-details summary{cursor:pointer;list-style:none;position:relative;padding:10px 30px 8px 0;color:#477ca8;font-size:.96rem;font-weight:650}.trial-details summary::-webkit-details-marker{display:none}.trial-details summary:after{content:'+';position:absolute;right:2px;top:50%;transform:translateY(-50%);color:#91a3b3;font-size:1.15rem}.trial-details[open] summary:after{content:'−'}.trial-detail-body{padding:0 0 2px}.trial-detail-body p,.trial-detail-body li{font-size:1rem;line-height:1.55}.trial-detail-body .enrollment-areas{font-size:1rem}@media(max-width:600px){.cancer-page h1{font-size:1.5rem;line-height:1.2;margin-top:2px}.cancer-page .eyebrow{font-size:.78rem;margin-bottom:15px;color:#95a2b0!important}.cancer-page .disease h2{font-size:1.15rem}.options-transition{margin:23px 0 13px}.options-transition h2{font-size:1.12rem}.options-transition p{font-size:.94rem}.eligibility-cta{font-size:.92rem;padding:9px 14px}.cancer-page .card{padding:13px 14px}.cancer-page .card h3{font-size:.98rem}.cancer-page .card .meta,.cancer-page .card .study-locations li,.trial-details summary{font-size:.94rem}.trial-detail-body p,.trial-detail-body li{font-size:.96rem}}'''.strip()

def _is_english_cancer_page(path,root):
 rel=path.relative_to(root).parts;return len(rel)==4 and rel[0] in {'north-america','uk-europe'} and rel[1] in {'dogs','cats'} and rel[3]=='index.html'
def _json_ld(title,desc,canonical,label,species,region):
 root=canonical.split('/north-america/',1)[0] if '/north-america/' in canonical else canonical.split('/uk-europe/',1)[0];rp='north-america' if 'USA' in region else 'uk-europe';sp=species.lower();graph={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'about':{'@type':'Thing','name':label},'isPartOf':{'@type':'WebSite','@id':root+'/#website','url':root+'/','name':'Vet Trial Finder'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Vet Trial Finder','item':root+'/'},{'@type':'ListItem','position':2,'name':region,'item':f'{root}/{rp}/'},{'@type':'ListItem','position':3,'name':species,'item':f'{root}/{rp}/{sp}/'},{'@type':'ListItem','position':4,'name':label,'item':canonical}]}]};return '<script type="application/ld+json">'+json.dumps(graph,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'

def _collapse_card(match):
 title,meta,body=match.groups();locations=''.join(LOCATION_RE.findall(body));body=LOCATION_RE.sub('',body)
 return f'<article class="card"><h3>{title}</h3><p class="meta">{meta}</p>{locations}<details class="trial-details"><summary>Study details</summary><div class="trial-detail-body">{body}</div></details></article>'

def _enhance(text):
 m=H1_RE.search(text)
 if not m:return text,False
 label_html=m.group('label');label=html.unescape(re.sub(r'<.*?>','',label_html));key=label.strip().lower();species=m.group('species');region_html=m.group('region');region=html.unescape(region_html);lead=LEAD_RE.search(text);cm=CANONICAL_RE.search(text)
 if not lead or not cm:return text,False
 count=lead.group('count');canonical=html.unescape(cm.group(1));text=text.replace(m.group(0),f'<div class="cancer-page"><h1>{label_html}</h1><p class="eyebrow">{species} · {region_html}</p>',1);text=LEAD_RE.sub('',text,count=1)
 info=CONTENT.get(key)
 if not info:raise AssertionError(f'Missing owner-facing cancer content for {label}')
 about,treatment,factors=info;disease=f'<section class="disease"><h2>Understanding {label_html}</h2><p>{html.escape(about)}</p><h2>How it is usually treated</h2><p>{html.escape(treatment)}</p><h2>What can affect treatment choices</h2><p>{html.escape(factors)}</p></section>';text,n=DISEASE_RE.subn(disease,text,count=1)
 if n!=1:raise AssertionError(f'Could not replace disease section for {label}')
 finder='https://vet-cancer-trial-finder.streamlit.app/';fm=FREE_RE.search(text)
 if fm:finder=html.unescape(fm.group(1));text=FREE_RE.sub('',text,count=1)
 old_intro='<h2>Treatment &amp; research</h2><p>Below are treatment-focused clinical trials and advanced oncology options currently represented in our live catalog.</p>'
 transition=(f'<section class="options-transition"><h2>Treatment options available now</h2><p class="option-count">{count} option'+('' if count=='1' else 's')+' currently in our catalog.</p><p class="free-inline">Free to use · No registration · Official enrollment links</p><p><a class="eligibility-cta" href="'+html.escape(finder,quote=True)+'">Check eligibility</a></p></section>') if count!='0' else '<section class="options-transition"><h2>Treatment options available now</h2><p class="option-count">No active listings in our catalog right now.</p><p class="free-inline">Vet Trial Finder is free to use. New studies are added when enrollment opens.</p></section>'
 text=text.replace(old_intro,transition,1);text=re.sub(r'<h2>Current clinical trials &amp; treatment options</h2><p class="section-intro">.*?</p>',transition,text,count=1,flags=re.S)
 dm=DISEASE_RE.search(text);tm=text.find('<section class="options-transition">')
 if dm and tm>=0 and dm.start()>tm:block=dm.group(0);text=text[:dm.start()]+text[dm.end():];tm=text.find('<section class="options-transition">');text=text[:tm]+block+text[tm:]
 text=CARD_RE.sub(_collapse_card,text);text=text.replace('</main>','</div></main>',1)
 title=f'{label} Clinical Trials for {species} | Vet Trial Finder';desc=f'Learn about {label} in {species.lower()}, common treatment approaches and factors that affect care. Check Vet Trial Finder for new clinical trials and treatment studies.' if count=='0' else f'Find {count} current {label} clinical trial and treatment {"option" if count=="1" else "options"} for {species.lower()} in {region}. Free eligibility details, locations, contacts and official links.';text=re.sub(r'<title>.*?</title>',f'<title>{html.escape(title)}</title>',text,count=1,flags=re.S);text=re.sub(r'<meta name="description" content=".*?">',f'<meta name="description" content="{html.escape(desc,quote=True)}">',text,count=1,flags=re.S);text=text.replace('</head>',_json_ld(title,desc,canonical,label,species,region)+'</head>',1)
 if CSS not in text:text=text.replace('</style>',CSS+'</style>',1)
 return text,True

def enhance_cancer_pages(root):
 root=Path(root);changed=0
 for path in root.rglob('index.html'):
  if not _is_english_cancer_page(path,root):continue
  old=path.read_text(encoding='utf-8');new,ok=_enhance(old)
  if ok and new!=old:path.write_text(new,encoding='utf-8');changed+=1
 if not changed:raise AssertionError('Cancer page enhancement matched no English diagnosis pages')
 print('CANCER_PAGES_ENHANCED',changed);return changed
