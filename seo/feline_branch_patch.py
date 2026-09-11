"""Apply feline-specific decision branches without mixing canine branch logic."""
import html
import practical_cancer_pages as guides
from cancer_owner_content import CONTENT
from feline_branch_content import FELINE_BRANCHES


def _feline_section(label,key,pet,practical):
    if pet != 'cat':
        return _ORIGINAL(label,key,pet,practical)
    about,treatment,factors=CONTENT[key]
    p=practical[key]
    branches=FELINE_BRANCHES.get(key,guides._generic_branches(pet))
    branch_html=''.join(
        f'<details><summary>{guides._p(title)}</summary><div class="guide-detail"><p>{guides._p(body)}</p></div></details>'
        for title,body in branches
    )
    return f'''<section class="disease owner-guide">
<h2>Understanding {html.escape(label)}</h2><p>{guides._p(about)}</p>
<div class="guide-reality"><h2>What does the prognosis look like?</h2><p>{guides._p(p['prognosis'])}</p><p><strong>No statistic can predict your cat.</strong> The useful question is what the published numbers mean for the decisions in front of you now.</p></div>
<h2>After a {html.escape(label)} diagnosis</h2><p>{guides._p(p['next'])}</p>
<h2>Where are you now?</h2><div class="guide-accordions">{branch_html}</div>
<div class="guide-waiting"><h2>If you are waiting for oncology</h2><p>If the appointment is far away, ask about a cancellation list or another oncology center. Complete useful staging that can be arranged safely and check trials before the next irreversible treatment decision.</p><p>Checking early does not commit you to a trial. It simply prevents an otherwise suitable option from disappearing because a required tumor was removed or an excluded drug was started first.</p></div>
<div class="guide-accordions guide-more"><details><summary>Questions to ask your oncologist</summary><div class="guide-detail"><ul class="guide-questions"><li>What exact subtype, grade and stage do we know?</li><li>Is anything important still missing before we choose treatment?</li><li>What is the goal of treatment: cure, long-term control, slowing spread, or symptom control?</li><li>What would make you change this plan?</li><li>Could treatment we start now affect clinical-trial eligibility later?</li></ul></div></details>
<details><summary>How it is usually treated</summary><div class="guide-detail"><p>{guides._p(treatment)}</p></div></details>
<details><summary>What can affect treatment choices</summary><div class="guide-detail"><p>{guides._p(factors)}</p></div></details>
<details><summary>Tests worth asking about</summary><div class="guide-detail"><p>{guides._p(p['tests'])}</p><p>Before paying for an additional cancer test, ask one practical question: <strong>will this result change treatment or trial eligibility now?</strong></p></div></details></div></section>'''


_ORIGINAL=guides.section
guides.section=_feline_section
