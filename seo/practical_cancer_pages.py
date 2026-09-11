"""Turn reviewed diagnosis landing pages into concise practical owner guides."""
from __future__ import annotations
import html,re
from pathlib import Path
from cancer_owner_content import CONTENT
from cancer_practical_content import PRACTICAL
from canine_branch_content import ADDITIONAL_BRANCHES
from feline_practical_content import FELINE_PRACTICAL
from species_owner_content_overrides import FELINE_OWNER_CONTENT
from cancer_content_audit_overrides import CANINE_PRACTICAL_OVERRIDES,FELINE_PRACTICAL_OVERRIDES

CSS=r'''.owner-guide,.owner-guide p,.owner-guide li{color:#263238!important}.owner-guide strong{color:#1f2d38!important}.owner-guide h2{margin-top:25px;color:#477ca8!important;font-size:1.2rem;font-weight:700}.guide-reality{margin:19px 0;padding:16px 18px;border:1px solid #dbe7f0;border-radius:14px;background:#f8fbfd}.guide-reality h2{margin-top:0;color:#477ca8!important}.guide-accordions{display:grid;gap:9px;margin:12px 0 20px}.guide-accordions details{border:1px solid #dbe7f0;border-radius:12px;background:#fff;overflow:hidden}.guide-accordions summary{position:relative;cursor:pointer;list-style:none;padding:13px 42px 13px 15px;color:#4d7da3!important;font-weight:650;line-height:1.35}.guide-accordions summary::-webkit-details-marker{display:none}.guide-accordions summary:after{content:'+';position:absolute;right:15px;top:50%;transform:translateY(-50%);color:#9aabba;font-size:1.25rem;font-weight:400}.guide-accordions details[open] summary:after{content:'−'}.guide-accordions details[open] summary{background:#f8fbfd}.guide-detail{padding:2px 15px 13px}.guide-detail p{margin:.45rem 0}.guide-more{margin-top:22px}@media(max-width:600px){.owner-guide h2{font-size:1.08rem;margin-top:20px}.guide-reality{padding:13px 14px;margin:15px 0}.guide-accordions summary{padding:11px 38px 11px 13px;font-size:.96rem}}'''.strip()

BRANCHES={}
BRANCHES.update(ADDITIONAL_BRANCHES)

SKIP_FIRST_CANINE={
 'prostate cancer','primary lung tumor','glioma','meningioma','nasal tumor',
 'leukemia','multiple myeloma','chemodectoma'
}
SKIP_FIRST_FELINE={
 'lymphoma','primary lung tumor','meningioma','nasal tumor','melanoma',
 'urothelial carcinoma','hepatocellular carcinoma','thyroid carcinoma',
 'prostate cancer','glioma','leukemia','multiple myeloma','chemodectoma'
}

def _p(s):return html.escape(s)

def _owner_content(key,pet):
 if pet=='cat' and key in FELINE_OWNER_CONTENT:return FELINE_OWNER_CONTENT[key]
 return CONTENT[key]

def _practical_content(key,pet,practical):
 base=dict(practical[key])
 overrides=FELINE_PRACTICAL_OVERRIDES if pet=='cat' else CANINE_PRACTICAL_OVERRIDES
 base.update(overrides.get(key,{}))
 return base

def _useful_branches(key,pet):
 branches=list(BRANCHES.get(key,[]))
 skip=SKIP_FIRST_FELINE if pet=='cat' else SKIP_FIRST_CANINE
 if key in skip and branches:branches=branches[1:]
 return branches

def section(label,key,pet,practical):
 about,treatment,_factors=_owner_content(key,pet);p=_practical_content(key,pet,practical)
 branches=_useful_branches(key,pet)
 branch_block=''
 if branches:
  items=''.join(f'<details><summary>{_p(a)}</summary><div class="guide-detail"><p>{_p(b)}</p></div></details>' for a,b in branches)
  branch_block=f'<h2>Where are you now?</h2><div class="guide-accordions">{items}</div>'
 tests=p.get('tests','').strip()
 tests_block=f'<details><summary>Tests that may matter</summary><div class="guide-detail"><p>{_p(tests)}</p></div></details>' if tests else ''
 return f'''<section class="disease owner-guide">
<h2>Understanding {html.escape(label)}</h2><p>{_p(about)}</p>
<div class="guide-reality"><h2>What does the prognosis look like?</h2><p>{_p(p['prognosis'])}</p></div>
<h2>What matters next</h2><p>{_p(p['next'])}</p>
{branch_block}
<div class="guide-accordions guide-more"><details><summary>How it is usually treated</summary><div class="guide-detail"><p>{_p(treatment)}</p></div></details>{tests_block}</div></section>'''

def _apply(root,species,pet,practical,skip_hs=False):
 root=Path(root);changed=0
 for path in root.rglob('index.html'):
  rel=path.relative_to(root).parts
  if len(rel)!=4 or rel[0] not in {'north-america','uk-europe'} or rel[1]!=species or rel[3]!='index.html':continue
  key=rel[2].replace('-',' ')
  if skip_hs and key=='histiocytic sarcoma':continue
  if key not in practical or key not in CONTENT:continue
  text=path.read_text(encoding='utf-8');h=re.search(r'<h1>(.*?)</h1>',text,re.S);label=html.unescape(re.sub(r'<.*?>','',h.group(1))) if h else key.title()
  new,n=re.subn(r'<section class="disease(?: owner-guide)?">.*?</section>',section(label,key,pet,practical),text,count=1,flags=re.S)
  if n!=1:raise AssertionError(f'Could not replace practical guide in {path}')
  if CSS not in new:new=new.replace('</style>',CSS+'</style>',1)
  if new!=text:path.write_text(new,encoding='utf-8');changed+=1
 return changed

def apply_practical_cancer_guides(root:Path)->int:
 changed=_apply(root,'dogs','dog',PRACTICAL,True)
 if not changed:raise AssertionError('Practical cancer guide matched no canine pages')
 print('PRACTICAL_CANINE_CANCER_GUIDES_APPLIED',changed);return changed

def apply_feline_practical_guides(root:Path)->int:
 changed=_apply(root,'cats','cat',FELINE_PRACTICAL)
 if not changed:raise AssertionError('Reviewed feline practical guide matched no pages')
 print('PRACTICAL_FELINE_CANCER_GUIDES_APPLIED',changed);return changed