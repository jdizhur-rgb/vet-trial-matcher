#!/usr/bin/env python3
"""Generate a plain-language Help Center and add it to the sitemap."""
from __future__ import annotations
from pathlib import Path
import generate_seo as g
from site_config import SITE


def generate_help_center(root: Path) -> None:
    url=f'{SITE}/help/'
    body=f'''<style>
.help-center{{max-width:850px}}
.help-faq{{margin:28px 0}}
.help-faq details{{background:#fff;border:1px solid #d9e2ea;border-radius:12px;margin:0 0 10px;overflow:hidden}}
.help-faq summary{{position:relative;padding:16px 48px 16px 18px;color:#315f7d;font-size:1.08rem;font-weight:680;line-height:1.35;cursor:pointer;list-style:none}}
.help-faq summary::-webkit-details-marker{{display:none}}
.help-faq summary::after{{content:'+';position:absolute;right:18px;top:50%;transform:translateY(-50%);color:#6b8193;font-size:1.45rem;font-weight:400}}
.help-faq details[open] summary{{border-bottom:1px solid #e3e9ee}}
.help-faq details[open] summary::after{{content:'−'}}
.help-answer{{padding:15px 18px 17px}}
.help-answer p{{margin:0 0 13px}}
.help-answer p:last-child{{margin-bottom:0}}
.help-center .cta{{padding:8px 13px;border-radius:7px;font-size:.9rem;font-weight:650}}
@media(max-width:600px){{.help-faq{{margin-top:22px}}.help-faq summary{{padding:14px 42px 14px 15px;font-size:1rem}}.help-answer{{padding:13px 15px 15px}}.help-center .cta{{padding:7px 11px;font-size:.86rem}}}}
</style>
<div class="help-center"><h1>Help Center</h1>
<p class="lead">Clinical trials can be confusing, especially when you are trying to make decisions for a dog or cat with cancer. This page explains how to use the finder and what to expect if you find a study that may fit.</p>
<div class="help-faq">
<details><summary>How do I use the trial finder?</summary><div class="help-answer"><p>Enter your pet's diagnosis and the information you know. The finder compares it with the requirements listed for current studies. You do not need to know every answer. If something is unknown, leave it unknown rather than guessing.</p><p><a class="cta" href="{g.FINDER}">Search clinical trials</a></p></div></details>
<details><summary>Does a match mean my pet is eligible?</summary><div class="help-answer"><p>No. A match means the study looks worth checking based on the information available. The research team makes the final decision. They may need medical records, pathology, blood work, imaging or other tests before confirming eligibility.</p></div></details>
<details><summary>What should I have ready?</summary><div class="help-answer"><p>Start with the pathology or cytology report if you have one. It also helps to have recent blood work, imaging reports, surgery reports and a list of treatments your pet has already received. Exact dates can matter because some studies require a waiting period after chemotherapy, radiation or other treatment.</p></div></details>
<details><summary>Who do I contact?</summary><div class="help-answer"><p>Use the contact information or official study link shown with the trial. You can contact the study team yourself. Your regular veterinarian or oncologist can also send records or speak with the research team if needed.</p></div></details>
<details><summary>Are clinical trials free?</summary><div class="help-answer"><p>Sometimes, but not always. A study may cover the experimental treatment, some tests, or part of the visit costs. Other expenses may still be your responsibility. The amount covered is different for every study, so ask exactly what is paid for before making travel or treatment plans.</p></div></details>
<details><summary>Will I have to travel?</summary><div class="help-answer"><p>Possibly. Some studies require several visits to the same hospital. Others use multiple participating hospitals or need fewer visits. Check the location and visit schedule with the study team before enrolling.</p></div></details>
<details><summary>Do veterinary cancer trials use placebos?</summary><div class="help-answer"><p>Some do, many do not. The study information should explain the treatment groups. If a placebo or randomized group is possible, ask what standard treatment your pet can still receive and whether you can leave the study if you change your mind.</p></div></details>
<details><summary>Can I leave a study after enrolling?</summary><div class="help-answer"><p>In general, participation is voluntary. Before enrolling, read the consent form and ask the study team what happens if you decide to stop or if your pet's condition changes.</p></div></details>
<details><summary>What if the finder shows no matches?</summary><div class="help-answer"><p>It does not mean there are no treatment choices for your pet. It only means our current catalog did not find a study that matched the information entered. New studies open and old studies close. You can also check oncology centers and other treatment options on this site, and discuss standard treatment with your veterinarian or veterinary oncologist.</p></div></details>
<details><summary>Why can a trial disappear from the site?</summary><div class="help-answer"><p>Enrollment changes. A study can fill, pause, close or change its requirements. We update the catalog as we verify changes, but the research team is always the final source for current enrollment status.</p></div></details>
<details><summary>What does "last verified" mean?</summary><div class="help-answer"><p>It is the most recent date we checked the study information against a source we use for that listing. It is not a promise that a spot is still available today. Contact the study team before making plans.</p></div></details>
<details><summary>Do I need to pay to use this site?</summary><div class="help-answer"><p>No. The finder and the information on this site are free. There is no paid report and no fee to see the matches.</p></div></details>
<details><summary>Still not sure what to do?</summary><div class="help-answer"><p>If you find a study that looks close, contact the study team even if you are unsure about one requirement. They can tell you what records they need and whether your pet can be screened.</p></div></details>
</div></div>'''
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
