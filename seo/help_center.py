#!/usr/bin/env python3
"""Generate Help content aligned with the current site and matcher."""
from __future__ import annotations

import json
import re
from pathlib import Path

import generate_seo as g
from site_config import SITE


def _item(question: str, answer: str) -> str:
    return f'<details><summary>{question}</summary><div class="help-answer">{answer}</div></details>'


def generate_help_center(root: Path) -> None:
    url = f'{SITE}/help/'
    finder = g.FINDER
    sections = [
        ('Using Vet Trial Finder', [
            ('Where should I start?',
             f'<p>Use <a href="{finder}">Find trials</a> to compare one pet’s diagnosis and treatment history with current studies. Use <a href="{SITE}/matcher/centers/">Find an oncologist</a> to search veterinary oncology locations by service or US ZIP code, including centers offering electrochemotherapy. Use <a href="{SITE}/cancer-types/">Cancer types</a> to read about a diagnosis and see current listings. <a href="{SITE}/centers/">Trial centers</a> lists institutions connected to treatment opportunities in our catalog. <a href="{SITE}/other-treatments/">Other treatments</a> covers selected newer treatments and expanded-access programs.</p>'),
            ('How do I use the trial finder?',
             f'<p>Open <a href="{finder}">Find Trials</a> and complete the five sections:</p><ol><li><strong>Your pet:</strong> choose dog or cat and the country or region. Add age, weight and sex if known.</li><li><strong>Diagnosis:</strong> say whether it is confirmed by pathology or cytology, suspected, or unknown, then choose the cancer type.</li><li><strong>Current disease:</strong> enter whether the tumor is still present, removed, recurrent or not currently visible. Add what you know about margins, metastases and whether the disease is localized.</li><li><strong>Treatment:</strong> record surgery, chemotherapy, immunotherapy and radiation. Medication questions appear only when they matter to possible studies.</li><li><strong>Treatment options:</strong> leave selected only the kinds of treatment you would consider, then press <em>Find potential trials</em>.</li></ol><p>The form changes with the diagnosis. Lymphoma, mast cell tumor, osteosarcoma, hemangiosarcoma and some other cancers have additional questions because those details can change eligibility.</p>'),
            ('What if I do not know an answer?',
             '<p>Choose <em>I don’t know</em>. Unknown information does not automatically disqualify a pet, but it may keep a result in the “Possible match” category until the study team checks the missing detail. Do not guess at margins, metastases, grade or treatment history.</p>'),
            ('What if the cancer type is not listed?',
             '<p>Select <em>My cancer type isn’t listed</em> and enter the diagnosis exactly as it appears in the pathology report, if known. The matcher then shows only genuinely broad programs that may review multiple tumor types. It will not treat an unrelated cancer trial as a match.</p>'),
            ('How does the country or region choice work?',
             '<p>Choose one country to see studies there, or choose <em>Europe — all countries</em> to search across the European listings. A result in another country does not mean that the center accepts international patients. Confirm that directly before making travel plans.</p>'),
            ('What does “Select all that you would consider” do?',
             '<p>This is a preference filter, not a treatment recommendation. Selected choices are alternatives: choosing chemotherapy and immunotherapy means “show either,” not “the study must include both.” Removing a treatment type can hide otherwise relevant studies, so leave everything selected if you are still exploring.</p>'),
        ]),
        ('Understanding results', [
            ('What do the result labels mean?',
             '<p><strong>Likely match</strong> means the information entered agrees with the key criteria recorded for that study and no required answer is missing. <strong>Possible match</strong> means the study may fit but at least one point still needs confirmation. <strong>Prescreening required</strong> is used when eligibility cannot be decided from the short form. <strong>Other treatment-access opportunity</strong> is a real access pathway, but not a conventional experimental-treatment trial. None of these labels is final eligibility.</p>'),
            ('What information is shown in a result?',
             '<p>Each result shows the study center and title, why it may fit, facts that still need confirmation, contact details, participating sites when available, and a direct link to the official study page. Open <em>Study information</em> for the intervention, funding, recruitment status and the date we last checked the listing.</p>'),
            ('Can I save or share the results?',
             '<p>Yes. Use <em>Copy results</em> for a text summary. <em>Save / print PDF</em> opens your browser’s print dialog, where you can choose to save a PDF or print the results. A saved result is a snapshot; recruitment and eligibility requirements can change later.</p>'),
            ('What if the finder shows no matches?',
             f'<p>It means the currently verified catalog did not find a plausible study for the information entered. It does not mean that your pet has no treatment choices. Check the country, diagnosis and treatment preferences, then look at <a href="{SITE}/centers/">Trial Centers</a> and <a href="{SITE}/other-treatments/">Other Treatments</a>. A clear “no matches” is more useful than showing a study that does not fit.</p>'),
            ('Why can a trial disappear from the site?',
             '<p>A study can fill, pause, close or change its criteria. We remove it from patient-facing matching when current enrollment cannot be confirmed. It may return if the study reopens or its status is verified again.</p>'),
            ('What does “last verified” mean?',
             '<p>It is the most recent date we checked the listing against a source used for that record. It does not guarantee that a place is available today. The study team is always the final source for current enrollment.</p>'),
        ]),
        ('Oncology centers and trial centers', [
            ('How do I find an oncologist or ECT center?',
             f'<p>Open <a href="{SITE}/matcher/centers/">Find an oncologist</a> to search veterinary oncology locations by hospital, city or state, or enter a five-digit US ZIP code to see nearby US locations first. Use the service filter and choose <em>Electrochemotherapy</em> for ECT centers. This broader directory also includes local cancer-care clinics; a listing does not mean a board-certified oncologist or ECT is available at every location. Confirm services with the hospital.</p>'),
            ('What are Trial Centers?',
             f'<p>These are universities, veterinary teaching hospitals, specialty hospitals, research organizations and multicenter programs connected to at least one current treatment opportunity in our catalog. A center page shows the cancer types currently listed there, where visits take place when that information is available, and the active studies or treatment programs linked to that institution. It is not a directory of every veterinary oncology clinic.</p>'),
            ('How do I find the nearest trial centers?',
             f'<p>Open <a href="{SITE}/centers/">Trial Centers</a>. Enter a five-digit US ZIP code to sort listed US centers by approximate straight-line distance. The mileage is not driving distance. You can also search by hospital, city, state or country. This is a directory of centers connected to current opportunities in our catalog, not every veterinary oncology hospital near you.</p>'),
        ]),
        ('Other Treatments', [
            ('What is included under Other Treatments?',
             f'<p><a href="{SITE}/other-treatments/">Other treatments</a> links to <a href="{SITE}/matcher/centers/?service=electrochemotherapy">oncology centers offering electrochemotherapy</a>, selected <strong>advanced treatments</strong> you can filter by species, region and cancer type, and <strong>expanded access</strong> programs that may review patients outside ordinary trial enrollment. These listings do not decide whether a treatment is medically appropriate.</p>'),
        ]),
        ('Contacting a study', [
            ('Does a match mean my pet is eligible?',
             '<p>No. The matcher is a prescreening tool. Final eligibility is decided by the research or treatment team after reviewing the diagnosis, records, previous treatment, current health and any tests required by the protocol.</p>'),
            ('What should I have ready?',
             '<p>Useful records include the pathology or cytology report, surgery report, recent imaging or staging, bloodwork, medication list, and the names and dates of cancer treatments. Exact dates can matter because some protocols require a waiting period after chemotherapy, radiation or another treatment.</p>'),
            ('Who should contact the study?',
             '<p>Use the contact shown in the result or the official study link. Owners can usually make the first inquiry. The team may then ask the regular veterinarian or oncologist to send records or discuss the case.</p>'),
            ('Are clinical trials free?',
             '<p>Sometimes, but not always. A study may cover the experimental treatment, selected tests or part of the visits while the owner pays for other care. Ask exactly what is covered, what is not, and whether costs change if the pet leaves the study.</p>'),
            ('Will I have to travel?',
             '<p>Possibly. Some protocols require repeated visits to one hospital; others have several participating sites. Confirm the exact hospital, number of visits and which visits must be in person before making plans. Distances shown on the site are estimates, not travel instructions.</p>'),
            ('Do trials use placebos, and can I leave after enrolling?',
             '<p>Some trials use randomization or a placebo group and many do not. The consent documents should explain the groups, what standard care remains available and what happens if the disease progresses. Participation is generally voluntary; ask how withdrawal works before enrolling.</p>'),
            ('Is Vet Trial Finder free, and how do I contact you?',
             '<p>The site, matcher and saved results are free. There is no paid report and no fee to reveal matches. For a correction, broken link or question about using the site, email <a href="mailto:info@vettrialfinder.com">info@vettrialfinder.com</a>. For eligibility or medical advice, contact the study team or your veterinarian.</p>'),
        ]),
    ]

    section_html = ''.join(
        f'<section class="help-section"><h2>{title}</h2>{"".join(_item(q, a) for q, a in items)}</section>'
        for title, items in sections
    )
    body = f'''<style>
.help-center{{max-width:900px;font-family:inherit;font-size:1rem;line-height:1.58}}
.help-intro{{max-width:800px}}
.help-section{{margin:30px 0}}
.help-section h2{{margin:0 0 12px;font-family:inherit;font-size:1.45rem;line-height:1.2;font-weight:700}}
.help-section details{{background:#fff;border:1px solid #d9e2ea;border-radius:10px;margin:0 0 9px;overflow:hidden}}
.help-section summary{{position:relative;padding:14px 46px 14px 16px;color:#315f7d;font-family:inherit;font-size:1rem;font-weight:700;line-height:1.4;cursor:pointer;list-style:none}}
.help-section summary::-webkit-details-marker{{display:none}}
.help-section summary::after{{content:'+';position:absolute;right:16px;top:50%;transform:translateY(-50%);color:#6b8193;font-size:1.35rem;font-weight:400}}
.help-section details[open] summary{{border-bottom:1px solid #e3e9ee}}
.help-section details[open] summary::after{{content:'−'}}
.help-answer{{padding:14px 17px 16px;font-family:inherit;font-size:1rem;line-height:1.58}}
.help-answer p{{margin:0 0 11px}}
.help-answer p:last-child{{margin-bottom:0}}
.help-answer ol{{margin:0 0 12px;padding-left:22px}}
.help-answer li{{margin:0 0 7px}}
.help-urgent{{border-left:4px solid #8aaec4;background:#edf4f8;padding:13px 15px;margin:30px 0 0}}
@media(max-width:600px){{.help-center{{font-size:1rem}}.help-section{{margin:25px 0}}.help-section h2{{font-size:1.28rem}}.help-section summary{{padding:13px 41px 13px 14px;font-size:1rem}}.help-answer{{padding:13px 14px 15px;font-size:1rem}}}}
</style>
<div class="help-center"><h1>Help Center</h1>
<p class="lead help-intro">Use this page to choose the right part of Vet Trial Finder, complete the matcher without guessing, understand the results and contact a study with the right records.</p>
{section_html}
<p class="help-urgent"><strong>Urgent symptoms come first.</strong> Difficulty breathing, collapse, uncontrolled bleeding, severe pain or another emergency should be assessed by a veterinarian immediately rather than delayed for a trial search.</p>
</div>'''

    html = g.page(
        'How to Use Vet Trial Finder | Help Center',
        'How to use the veterinary cancer trial matcher, understand results, search trial centers and contact study teams.',
        body,
        url,
    )
    schema_items = [item for _, items in sections for item in items]
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': question,
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': re.sub(r'<[^>]+>', ' ', answer).replace('&amp;', '&'),
                },
            }
            for question, answer in schema_items
        ],
    }
    html = html.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>', 1)
    dest = root / 'help'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'index.html').write_text(html, encoding='utf-8')

    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        text = sitemap.read_text(encoding='utf-8')
        if url not in text:
            text = text.replace('</urlset>', f'<url><loc>{g.esc(url)}</loc></url>\n</urlset>')
            sitemap.write_text(text, encoding='utf-8')
    print('HELP_CENTER_OK', url)
