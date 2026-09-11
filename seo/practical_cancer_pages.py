"""Turn reviewed diagnosis landing pages into short practical owner guides.

Canine and feline prognosis data are kept separate. Feline pages are upgraded only
when a diagnosis has feline-specific reviewed guidance.
"""
from __future__ import annotations
import html, re
from pathlib import Path
from cancer_owner_content import CONTENT
from cancer_practical_content import PRACTICAL
from feline_practical_content import FELINE_PRACTICAL

CSS=r'''.owner-guide,.owner-guide p,.owner-guide li{color:#263238!important}.owner-guide strong{color:#1f2d38!important}.owner-guide h2{margin-top:25px;color:#477ca8!important;font-size:1.2rem;font-weight:700}.guide-reality,.guide-waiting{margin:19px 0;padding:16px 18px;border:1px solid #dbe7f0;border-radius:14px;background:#f8fbfd}.guide-reality h2,.guide-waiting h2{margin-top:0;color:#477ca8!important}.guide-accordions{display:grid;gap:9px;margin:12px 0 20px}.guide-accordions details{border:1px solid #dbe7f0;border-radius:12px;background:#fff;overflow:hidden}.guide-accordions summary{position:relative;cursor:pointer;list-style:none;padding:13px 42px 13px 15px;color:#4d7da3!important;font-weight:650;line-height:1.35}.guide-accordions summary::-webkit-details-marker{display:none}.guide-accordions summary:after{content:'+';position:absolute;right:15px;top:50%;transform:translateY(-50%);color:#9aabba;font-size:1.25rem;font-weight:400}.guide-accordions details[open] summary:after{content:'−'}.guide-accordions details[open] summary{background:#f8fbfd}.guide-detail{padding:2px 15px 13px;color:#263238!important}.guide-detail p{margin:.45rem 0}.guide-more{margin-top:22px}.guide-questions{padding-left:20px;margin:.35rem 0}.guide-questions li{margin:.45rem 0}@media(max-width:600px){.owner-guide h2{font-size:1.08rem;margin-top:20px}.owner-guide p{font-size:.96rem;line-height:1.5}.guide-reality,.guide-waiting{padding:13px 14px;margin:15px 0}.guide-accordions{gap:7px;margin:10px 0 17px}.guide-accordions summary{padding:11px 38px 11px 13px;font-size:.96rem}.guide-accordions summary:after{right:13px}.guide-detail{padding:1px 13px 11px}.guide-questions{padding-left:18px}}'''.strip()

# Diagnosis-specific decision branches. These deliberately override the generic
# mass/surgery scaffold where that scaffold would give an owner the wrong next step.
BRANCHES={
'lymphoma':[
 ('Diagnosis confirmed, treatment not started','Lymphoma is usually a systemic disease, so removing one enlarged lymph node is not the treatment. Confirm the lymphoma type and discuss systemic therapy. If a trial is possible, check it before prednisone or chemotherapy because prior drugs can affect eligibility.'),
 ('Prednisone has already been started','Tell the oncologist the exact dose and start date. Do not stop it abruptly without instructions. Prednisone can change lymphoma cells and may affect later diagnostics, drug response, or trial eligibility, but treatment options still remain.'),
 ('Chemotherapy has already started','Keep the protocol, doses, dates and response in one place. If remission is incomplete or lymphoma returns, the previous drugs and length of remission help determine rescue therapy and trial eligibility.'),
 ('My dog is getting sick while we wait','Poor appetite, weakness, vomiting, breathing difficulty, fever, or rapidly enlarging nodes can justify earlier assessment. Lymphoma treatment planning should not be parked for months simply because the first oncology slot is far away.')],
'mast cell tumor':[
 ('The tumor is still there','Before surgery, know where the regional lymph node is and whether sampling it would change the plan. For a difficult location or suspected high-risk tumor, biopsy or staging before the first surgery can help avoid an inadequate operation. Do not delay medically necessary removal just to preserve a trial option.'),
 ('The tumor was already removed','Read the pathology for Kiupel grade, mitotic count and measured margins. A “dirty margin” does not automatically mean the same next step for every MCT: re-excision, radiation, monitoring and systemic treatment depend on grade, site and nodal status.'),
 ('The lymph node or another site is positive','Nodal spread changes risk but is not the same as hopeless widespread disease. Ask whether the involved node can be treated locally and whether systemic therapy is recommended based on grade, stage and other risk factors.'),
 ('My dog is already in treatment','Keep the pathology and staging results together with drug names and dates. If a targeted drug or chemotherapy stops working, trials may still be possible, but prior-treatment rules vary.')],
'soft tissue sarcoma':[
 ('The mass is still there','The first surgery is the best chance to plan adequate margins. If the location makes wide removal difficult, ask whether biopsy and imaging should come before surgery and whether a surgeon, radiation oncologist, ECT center, or trial should be considered before the mass is altered.'),
 ('It was removed with clean margins','Grade still matters. For many low- or intermediate-grade STS, complete excision can provide long local control. Ask whether the grade or other pathology features justify chest staging or additional treatment rather than assuming chemotherapy is automatically needed.'),
 ('It was removed with incomplete margins','Do not wait for a visible recurrence before discussing local control. Re-excision is often considered when feasible; radiation or ECT may be alternatives in selected locations. The best choice depends on grade, measured margin, anatomy and expected morbidity.'),
 ('It has recurred, spread, or cannot be widely removed','A recurrent or high-grade STS deserves restaging and a new local-control discussion. Radiation, ECT, systemic therapy, or trials may be useful depending on site and measurable disease; preserve pathology material for review if needed.')],
'hemangiosarcoma':[
 ('A splenic or abdominal mass is still present','The immediate issue is bleeding risk and whether the dog is stable. Pale gums, collapse, marked weakness, a distended abdomen, or breathing trouble can be urgent. When stable, staging and surgical planning can proceed without pretending that a suspected splenic mass is already a confirmed HSA.'),
 ('The spleen or tumor was already removed','Confirm the pathology diagnosis and stage, and note whether rupture or abdominal bleeding occurred. Oncology discussion about adjuvant chemotherapy is time-sensitive enough that a months-long wait is not ideal.'),
 ('A heart-base/right-atrial lesion is suspected','Echocardiography helps define the mass and whether pericardial fluid is present. Collapse or breathing difficulty with fluid around the heart can become an emergency; treatment planning differs from splenic HSA.'),
 ('Metastases are visible','Systemic treatment and symptom control become central. Ask what treatment is realistically expected to accomplish and whether an active trial accepts previously treated or metastatic HSA.')],
'osteosarcoma':[
 ('The painful bone tumor is still there','Pain control starts now. Ask about fracture risk and staging, then discuss amputation, limb-sparing approaches, radiation, or another local plan. Trial screening can happen quickly, but a painful unstable bone should not be left untreated solely to keep a study option open.'),
 ('Amputation or local surgery is already done','Review pathology and chest staging, then discuss adjuvant chemotherapy and trials. Microscopic metastatic disease is common even when lung imaging is clear, which is why local control alone and systemic treatment are separate decisions.'),
 ('Amputation is not an option','Palliative or stereotactic radiation and other local approaches may reduce pain in selected dogs; systemic therapy and trials can still be discussed. The plan should explicitly include pain control and fracture risk, not only cancer drugs.'),
 ('Metastases are already visible','Treatment becomes individualized around pain, breathing, mobility and sites of spread. Metastatic disease can change trial eligibility but does not automatically eliminate every treatment or research option.')],
'oral melanoma':[
 ('The oral tumor is still there','Measure the tumor, assess local invasion, sample the appropriate regional lymph node when indicated, and stage the lungs. Surgery or radiation should not be needlessly delayed, but checking trials first can matter because some require measurable accessible tumor.'),
 ('The tumor was already removed','Get the pathology, measured margins and original tumor size, and complete staging if it was not done. A visually clean mouth does not answer the metastatic-risk question; stage and nodal status still matter.'),
 ('The lymph node is positive','A positive regional node changes stage and prognosis. Ask whether nodal local treatment is appropriate and how systemic options fit with control of the primary tumor.'),
 ('There is distant metastatic disease','The goal usually shifts toward systemic control and maintaining comfort while treating local mouth problems when useful. Trial criteria can differ sharply by stage, so use the actual staging results rather than the diagnosis name alone.')],
}

def _p(s): return html.escape(s)

def _generic_branches(pet):
 return [('The tumor is still there','Before the first major treatment, make sure the diagnosis and extent of disease are clear enough to plan it well. Check clinical trials before treatment when there is time to do so safely; some require measurable or untreated disease.'),('The tumor was already removed','Get the complete pathology report. Margin status, grade or subtype and other tumor-specific findings can change what comes next. Ask whether staging is complete and whether additional local or systemic treatment is actually indicated.'),('The cancer has spread or cannot be removed',f'Local treatment may still help a specific problem, while systemic treatment and trials may become more important. The realistic choices depend on the site, stage and your {pet}\'s condition.'),(f'My {pet} is already in treatment','Trials may still be possible. Check which studies allow the treatments already given before changing therapy if the current treatment stops working.')]

def section(label,key,pet,practical):
 about,treatment,factors=CONTENT[key]; p=practical[key]
 branches=BRANCHES.get(key,_generic_branches(pet)) if pet=='dog' else _generic_branches(pet)
 branch_html=''.join(f'<details><summary>{_p(title)}</summary><div class="guide-detail"><p>{_p(body)}</p></div></details>' for title,body in branches)
 return f'''<section class="disease owner-guide">
<h2>Understanding {html.escape(label)}</h2><p>{_p(about)}</p>
<div class="guide-reality"><h2>What does the prognosis look like?</h2><p>{_p(p['prognosis'])}</p><p><strong>No statistic can predict your {pet}.</strong> The useful question is what the published numbers mean for the decisions in front of you now.</p></div>
<h2>After a {html.escape(label)} diagnosis</h2><p>{_p(p['next'])}</p>
<h2>Where are you now?</h2><div class="guide-accordions">{branch_html}</div>
<div class="guide-waiting"><h2>If you are waiting for oncology</h2><p>If the appointment is far away, ask about a cancellation list or another oncology center. Complete useful staging that can be arranged safely and check trials before the next irreversible treatment decision.</p><p>Checking early does not commit you to a trial. It simply prevents an otherwise suitable option from disappearing because a required tumor was removed or an excluded drug was started first.</p></div>
<div class="guide-accordions guide-more"><details><summary>Questions to ask your oncologist</summary><div class="guide-detail"><ul class="guide-questions"><li>What exact subtype, grade and stage do we know?</li><li>Is anything important still missing before we choose treatment?</li><li>What is the goal of treatment: cure, long-term control, slowing spread, or symptom control?</li><li>What would make you change this plan?</li><li>Could treatment we start now affect clinical-trial eligibility later?</li></ul></div></details>
<details><summary>How it is usually treated</summary><div class="guide-detail"><p>{_p(treatment)}</p></div></details>
<details><summary>What can affect treatment choices</summary><div class="guide-detail"><p>{_p(factors)}</p></div></details>
<details><summary>Tests worth asking about</summary><div class="guide-detail"><p>{_p(p['tests'])}</p><p>Before paying for an additional cancer test, ask one practical question: <strong>will this result change treatment or trial eligibility now?</strong></p></div></details></div></section>'''

def _apply(root,species,pet,practical,skip_hs=False):
 root=Path(root); changed=0
 for path in root.rglob('index.html'):
  rel=path.relative_to(root).parts
  if len(rel)!=4 or rel[0] not in {'north-america','uk-europe'} or rel[1]!=species or rel[3]!='index.html': continue
  key=rel[2].replace('-',' ')
  if skip_hs and key=='histiocytic sarcoma': continue
  if key not in practical or key not in CONTENT: continue
  text=path.read_text(encoding='utf-8')
  h=re.search(r'<h1>(.*?)</h1>',text,re.S); label=html.unescape(re.sub(r'<.*?>','',h.group(1))) if h else key.title()
  new,n=re.subn(r'<section class="disease(?: owner-guide)?">.*?</section>',section(label,key,pet,practical),text,count=1,flags=re.S)
  if n!=1: raise AssertionError(f'Could not replace practical guide in {path}')
  if CSS not in new: new=new.replace('</style>',CSS+'</style>',1)
  if new!=text: path.write_text(new,encoding='utf-8'); changed+=1
 return changed

def apply_practical_cancer_guides(root:Path)->int:
 changed=_apply(root,'dogs','dog',PRACTICAL,True)
 if not changed: raise AssertionError('Practical cancer guide matched no canine pages')
 print('PRACTICAL_CANINE_CANCER_GUIDES_APPLIED',changed); return changed

def apply_feline_practical_guides(root:Path)->int:
 changed=_apply(root,'cats','cat',FELINE_PRACTICAL)
 if not changed: raise AssertionError('Reviewed feline practical guide matched no pages')
 print('PRACTICAL_FELINE_CANCER_GUIDES_APPLIED',changed); return changed
