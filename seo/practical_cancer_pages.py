"""Turn canine diagnosis landing pages into short practical owner guides.

Feline pages intentionally remain on the conservative base copy until feline-specific
prognosis and decision guidance has been independently reviewed. Never reuse canine
survival statistics on a cat page.
"""
from __future__ import annotations
import html, re
from pathlib import Path
from cancer_owner_content import CONTENT
from cancer_practical_content import PRACTICAL

CSS=r'''.owner-guide,.owner-guide p,.owner-guide li{color:#263238!important}.owner-guide strong{color:#1f2d38!important}.owner-guide h2{margin-top:25px;color:#477ca8!important;font-size:1.2rem;font-weight:700}.guide-reality,.guide-waiting{margin:19px 0;padding:16px 18px;border:1px solid #dbe7f0;border-radius:14px;background:#f8fbfd}.guide-reality h2,.guide-waiting h2{margin-top:0;color:#477ca8!important}.guide-accordions{display:grid;gap:9px;margin:12px 0 20px}.guide-accordions details{border:1px solid #dbe7f0;border-radius:12px;background:#fff;overflow:hidden}.guide-accordions summary{position:relative;cursor:pointer;list-style:none;padding:13px 42px 13px 15px;color:#4d7da3!important;font-weight:650;line-height:1.35}.guide-accordions summary::-webkit-details-marker{display:none}.guide-accordions summary:after{content:'+';position:absolute;right:15px;top:50%;transform:translateY(-50%);color:#9aabba;font-size:1.25rem;font-weight:400}.guide-accordions details[open] summary:after{content:'−'}.guide-accordions details[open] summary{background:#f8fbfd}.guide-detail{padding:2px 15px 13px;color:#263238!important}.guide-detail p{margin:.45rem 0}.guide-more{margin-top:22px}.guide-questions{padding-left:20px;margin:.35rem 0}.guide-questions li{margin:.45rem 0}@media(max-width:600px){.owner-guide h2{font-size:1.08rem;margin-top:20px}.owner-guide p{font-size:.96rem;line-height:1.5}.guide-reality,.guide-waiting{padding:13px 14px;margin:15px 0}.guide-accordions{gap:7px;margin:10px 0 17px}.guide-accordions summary{padding:11px 38px 11px 13px;font-size:.96rem}.guide-accordions summary:after{right:13px}.guide-detail{padding:1px 13px 11px}.guide-questions{padding-left:18px}}'''.strip()

def _p(s): return html.escape(s)

def section(label,key):
 about,treatment,factors=CONTENT[key]; p=PRACTICAL[key]
 return f'''<section class="disease owner-guide">
<h2>Understanding {html.escape(label)}</h2><p>{_p(about)}</p>
<div class="guide-reality"><h2>What does the prognosis look like?</h2><p>{_p(p['prognosis'])}</p><p><strong>No statistic can predict your dog.</strong> The useful question is what the published numbers mean for the decisions in front of you now.</p></div>
<h2>After a {html.escape(label)} diagnosis</h2><p>{_p(p['next'])}</p>
<h2>Where are you now?</h2><div class="guide-accordions">
<details><summary>The tumor is still there</summary><div class="guide-detail"><p>Before the first major treatment, make sure the diagnosis and extent of disease are clear enough to plan it well. If surgery or another local treatment is appropriate, the goal is not to delay it — it is to avoid losing information or options that matter.</p><p>Check clinical trials before treatment when there is time to do so safely. Some studies require measurable disease, untreated tumor, a biopsy, or direct access to the tumor.</p></div></details>
<details><summary>The tumor was already removed</summary><div class="guide-detail"><p>Get the complete pathology report. Margin status, grade or subtype and other tumor-specific findings can change what comes next. Ask whether staging is complete and whether additional local or systemic treatment is actually indicated.</p></div></details>
<details><summary>The cancer has spread or cannot be removed</summary><div class="guide-detail"><p>Local treatment may still help with pain, bleeding, obstruction or another specific problem, but systemic treatment and trials often become more important. The realistic choices depend on the site, stage and your dog's condition.</p></div></details>
<details><summary>My dog is already in treatment</summary><div class="guide-detail"><p>Trials may still be possible. Look for studies that allow the treatments already given, and check eligibility before changing therapy if the current treatment stops working.</p></div></details></div>
<div class="guide-waiting"><h2>If you are waiting for oncology</h2><p>If the appointment is far away, ask about a cancellation list or another oncology center. Complete useful staging that can be arranged safely and check trials before the next irreversible treatment decision.</p><p>Checking early does not commit you to a trial. It simply prevents an otherwise suitable option from disappearing because a required tumor was removed or an excluded drug was started first.</p></div>
<div class="guide-accordions guide-more"><details><summary>Questions to ask your oncologist</summary><div class="guide-detail"><ul class="guide-questions"><li>What exact subtype, grade and stage do we know?</li><li>Is anything important still missing before we choose treatment?</li><li>What is the goal of treatment: cure, long-term control, slowing spread, or symptom control?</li><li>What would make you change this plan?</li><li>Could treatment we start now affect clinical-trial eligibility later?</li></ul></div></details>
<details><summary>How it is usually treated</summary><div class="guide-detail"><p>{_p(treatment)}</p></div></details>
<details><summary>What can affect treatment choices</summary><div class="guide-detail"><p>{_p(factors)}</p></div></details>
<details><summary>Tests worth asking about</summary><div class="guide-detail"><p>{_p(p['tests'])}</p><p>Before paying for an additional cancer test, ask one practical question: <strong>will this result change treatment or trial eligibility now?</strong></p></div></details></div></section>'''

def apply_practical_cancer_guides(root:Path)->int:
 root=Path(root); changed=0
 for path in root.rglob('index.html'):
  rel=path.relative_to(root).parts
  if len(rel)!=4 or rel[0] not in {'north-america','uk-europe'} or rel[1]!='dogs' or rel[3]!='index.html': continue
  key=rel[2].replace('-',' ')
  if key=='histiocytic sarcoma': continue
  if key not in PRACTICAL or key not in CONTENT: continue
  text=path.read_text(encoding='utf-8')
  h=re.search(r'<h1>(.*?)</h1>',text,re.S); label=html.unescape(re.sub(r'<.*?>','',h.group(1))) if h else key.title()
  new,n=re.subn(r'<section class="disease(?: owner-guide)?">.*?</section>',section(label,key),text,count=1,flags=re.S)
  if n!=1: raise AssertionError(f'Could not replace practical guide in {path}')
  if CSS not in new: new=new.replace('</style>',CSS+'</style>',1)
  if new!=text: path.write_text(new,encoding='utf-8'); changed+=1
 if not changed: raise AssertionError('Practical cancer guide matched no canine pages')
 print('PRACTICAL_CANINE_CANCER_GUIDES_APPLIED',changed); return changed
