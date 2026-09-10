#!/usr/bin/env python3
"""Generate a plain-language Help Center and add it to the sitemap."""
from __future__ import annotations
from pathlib import Path
import generate_seo as g
from site_config import SITE


def generate_help_center(root: Path) -> None:
    url=f'{SITE}/help/'
    body=f'''<h1>Help Center</h1>
<p class="lead">Clinical trials can be confusing, especially when you are trying to make decisions for a dog or cat with cancer. This page explains how to use the finder and what to expect if you find a study that may fit.</p>

<h2>How do I use the trial finder?</h2>
<p>Enter your pet's diagnosis and the information you know. The finder compares it with the requirements listed for current studies. You do not need to know every answer. If something is unknown, leave it unknown rather than guessing.</p>
<p><a class="cta" href="{g.FINDER}">Search clinical trials</a></p>

<h2>Does a match mean my pet is eligible?</h2>
<p>No. A match means the study looks worth checking based on the information available. The research team makes the final decision. They may need medical records, pathology, blood work, imaging or other tests before confirming eligibility.</p>

<h2>What should I have ready?</h2>
<p>Start with the pathology or cytology report if you have one. It also helps to have recent blood work, imaging reports, surgery reports and a list of treatments your pet has already received. Exact dates can matter because some studies require a waiting period after chemotherapy, radiation or other treatment.</p>

<h2>Who do I contact?</h2>
<p>Use the contact information or official study link shown with the trial. You can contact the study team yourself. Your regular veterinarian or oncologist can also send records or speak with the research team if needed.</p>

<h2>Are clinical trials free?</h2>
<p>Sometimes, but not always. A study may cover the experimental treatment, some tests, or part of the visit costs. Other expenses may still be your responsibility. The amount covered is different for every study, so ask exactly what is paid for before making travel or treatment plans.</p>

<h2>Will I have to travel?</h2>
<p>Possibly. Some studies require several visits to the same hospital. Others use multiple participating hospitals or need fewer visits. Check the location and visit schedule with the study team before enrolling.</p>

<h2>Do veterinary cancer trials use placebos?</h2>
<p>Some do, many do not. The study information should explain the treatment groups. If a placebo or randomized group is possible, ask what standard treatment your pet can still receive and whether you can leave the study if you change your mind.</p>

<h2>Can I leave a study after enrolling?</h2>
<p>In general, participation is voluntary. Before enrolling, read the consent form and ask the study team what happens if you decide to stop or if your pet's condition changes.</p>

<h2>What if the finder shows no matches?</h2>
<p>It does not mean there are no treatment choices for your pet. It only means our current catalog did not find a study that matched the information entered. New studies open and old studies close. You can also check oncology centers and other treatment options on this site, and discuss standard treatment with your veterinarian or veterinary oncologist.</p>

<h2>Why can a trial disappear from the site?</h2>
<p>Enrollment changes. A study can fill, pause, close or change its requirements. We update the catalog as we verify changes, but the research team is always the final source for current enrollment status.</p>

<h2>What does "last verified" mean?</h2>
<p>It is the most recent date we checked the study information against a source we use for that listing. It is not a promise that a spot is still available today. Contact the study team before making plans.</p>

<h2>Do I need to pay to use this site?</h2>
<p>No. The finder and the information on this site are free. There is no paid report and no fee to see the matches.</p>

<h2>Still not sure what to do?</h2>
<p>If you find a study that looks close, contact the study team even if you are unsure about one requirement. They can tell you what records they need and whether your pet can be screened.</p>'''
    dest=root/'help'; dest.mkdir(parents=True,exist_ok=True)
    html=g.page('Veterinary Cancer Clinical Trials Help Center','Plain-language answers about finding veterinary cancer clinical trials, eligibility, costs, records, travel and contacting study teams.',body,url)
    # FAQ structured data mirrors the visible questions and answers.
    import json
    faqs=[
      ('Does a match mean my pet is eligible?','No. A match means the study looks worth checking based on the information available. The research team makes the final eligibility decision.'),
      ('Are veterinary cancer clinical trials free?','Sometimes. A study may cover treatment, tests or part of the visit costs, but coverage is different for every study.'),
      ('Will I have to travel for a veterinary clinical trial?','Possibly. Some studies require several visits to one hospital, while others use multiple participating hospitals or require fewer visits.'),
      ('Do veterinary cancer trials use placebos?','Some do and many do not. The study information and consent process should explain the treatment groups.'),
      ('What if the trial finder shows no matches?','It means the current catalog did not find a study matching the information entered. It does not mean there are no treatment choices for your pet.'),
    ]
    schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}
    html=html.replace('</head>',f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head>',1)
    (dest/'index.html').write_text(html,encoding='utf-8')
    sm=root/'sitemap.xml'
    if sm.exists():
        text=sm.read_text(encoding='utf-8')
        entry=f'<url><loc>{g.esc(url)}</loc></url>\n'
        if url not in text:
            text=text.replace('</urlset>',entry+'</urlset>')
            sm.write_text(text,encoding='utf-8')
    print('HELP_CENTER_OK',url)
