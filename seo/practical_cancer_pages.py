"""Reviewed diagnosis-specific owner guides. Optional blocks appear only when useful."""
from __future__ import annotations
import html,re
from pathlib import Path
from cancer_owner_content import CONTENT
from cancer_practical_content import PRACTICAL
from canine_branch_content import ADDITIONAL_BRANCHES
from feline_practical_content import FELINE_PRACTICAL
from species_owner_content_overrides import CANINE_OWNER_CONTENT,FELINE_OWNER_CONTENT
from cancer_content_audit_overrides import CANINE_PRACTICAL_OVERRIDES,FELINE_PRACTICAL_OVERRIDES
from cancer_benchmark_content import CANINE_PRACTICAL as BENCHMARK,CANINE_BRANCHES as BENCHMARK_BRANCHES
from cancer_owner_depth import DOG_DEPTH,CAT_DEPTH
from cancer_treatment_factors import DOG_FACTORS,CAT_FACTORS

CSS=r'''.owner-guide,.owner-guide p,.owner-guide li{color:#263238!important}.owner-guide h2{margin-top:25px;color:#477ca8!important;font-size:1.2rem}.guide-reality,.guide-waiting{margin:19px 0;padding:16px 18px;border:1px solid #dbe7f0;border-radius:14px;background:#f8fbfd}.guide-reality h2,.guide-waiting h2{margin-top:0}.guide-accordions{display:grid;gap:9px;margin:12px 0 20px}.guide-accordions details{border:1px solid #dbe7f0;border-radius:12px;background:#fff;overflow:hidden}.guide-accordions summary{cursor:pointer;padding:13px 15px;color:#4d7da3!important;font-weight:650}.guide-detail{padding:2px 15px 13px}.guide-questions li{margin:.45rem 0}@media(max-width:600px){.owner-guide h2{font-size:1.08rem}.guide-reality,.guide-waiting{padding:13px 14px}}'''.strip()
BRANCHES=dict(ADDITIONAL_BRANCHES);BRANCHES.update(BENCHMARK_BRANCHES)

def _e(x):return html.escape(x)
def _owner(key,pet):return (FELINE_OWNER_CONTENT if pet=='cat' else CANINE_OWNER_CONTENT).get(key,CONTENT[key])
def _practical(key,pet,source):
 p=dict(source.get(key,{}));p.update((FELINE_PRACTICAL_OVERRIDES if pet=='cat' else CANINE_PRACTICAL_OVERRIDES).get(key,{}))
 if pet=='dog':p.update(BENCHMARK.get(key,{}))
 p.update((CAT_DEPTH if pet=='cat' else DOG_DEPTH).get(key,{}))
 return p

def _details(title,text):
 return f'<details><summary>{_e(title)}</summary><div class="guide-detail"><p>{_e(text)}</p></div></details>' if text else ''

def section(label,key,pet,source):
 about,treatment,legacy_factors=_owner(key,pet);p=_practical(key,pet,source)
 factors=(CAT_FACTORS if pet=='cat' else DOG_FACTORS).get(key,legacy_factors).strip()
 branches=BRANCHES.get(key,[])
 branch=''
 if branches:
  branch='<h2>Where are you now?</h2><div class="guide-accordions">'+''.join(_details(a,b) for a,b in branches)+'</div>'
 waiting=p.get('waiting','').strip();waiting=f'<div class="guide-waiting"><h2>If you are waiting for oncology</h2><p>{_e(waiting)}</p></div>' if waiting else ''
 questions=p.get('questions',[]);q=''
 if questions:q='<details><summary>Questions to ask your oncologist</summary><div class="guide-detail"><ul class="guide-questions">'+''.join(f'<li>{_e(x)}</li>' for x in questions)+'</ul></div></details>'
 more=q+_details('How it is usually treated',treatment.strip())+_details('What can affect treatment choices',factors)+_details('Tests that may matter',p.get('tests','').strip())
 more=f'<div class="guide-accordions">{more}</div>' if more else ''
 return f'''<section class="disease owner-guide"><h2>Understanding {_e(label)}</h2><p>{_e(about)}</p><div class="guide-reality"><h2>What does the prognosis look like?</h2><p>{_e(p['prognosis'])}</p></div><h2>What matters next</h2><p>{_e(p['next'])}</p>{branch}{waiting}{more}</section>'''

def _apply(root,species,pet,source):
 root=Path(root);changed=0;keys=set(source)|(set(BENCHMARK) if pet=='dog' else set())
 for path in root.rglob('index.html'):
  rel=path.relative_to(root).parts
  if len(rel)!=4 or rel[0] not in {'north-america','uk-europe'} or rel[1]!=species or rel[3]!='index.html':continue
  key=rel[2].replace('-',' ')
  if key not in keys or key not in CONTENT:continue
  text=path.read_text(encoding='utf-8');h=re.search(r'<h1>(.*?)</h1>',text,re.S);label=html.unescape(re.sub(r'<.*?>','',h.group(1))) if h else key.title()
  new,n=re.subn(r'<section class="disease(?: owner-guide| hs-guide)?">.*?</section>',section(label,key,pet,source),text,count=1,flags=re.S)
  if n!=1:raise AssertionError(f'Could not replace guide in {path}')
  if CSS not in new:new.replace('</style>',CSS+'</style>',1)
  if CSS not in new:new=new.replace('</style>',CSS+'</style>',1)
  if new!=text:path.write_text(new,encoding='utf-8');changed+=1
 return changed

def apply_practical_cancer_guides(root:Path)->int:
 changed=_apply(root,'dogs','dog',PRACTICAL)
 if not changed:raise AssertionError('Practical cancer guide matched no canine pages')
 return changed

def apply_feline_practical_guides(root:Path)->int:
 changed=_apply(root,'cats','cat',FELINE_PRACTICAL)
 if not changed:raise AssertionError('Reviewed feline practical guide matched no pages')
 return changed
