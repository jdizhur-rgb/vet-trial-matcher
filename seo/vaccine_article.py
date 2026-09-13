#!/usr/bin/env python3
"""Generate the owner-facing canine cancer vaccine article and add it to Articles."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE

FINDER = g.FINDER.rstrip('/')

VACCINE_CSS = r'''
.vaccine-accordions{margin:24px 0 28px}
.vaccine-accordion{border:1px solid #d6e1e9;border-radius:10px;background:#fff;margin:10px 0;overflow:hidden}
.vaccine-accordion summary{cursor:pointer;list-style:none;padding:15px 17px;font-weight:700;color:#315f7d;line-height:1.35;position:relative;padding-right:42px}
.vaccine-accordion summary::-webkit-details-marker{display:none}
.vaccine-accordion summary:after{content:'+';position:absolute;right:17px;top:11px;font-size:24px;font-weight:400;color:#6b8293}
.vaccine-accordion[open] summary:after{content:'−'}
.vaccine-accordion[open] summary{border-bottom:1px solid #e2e8ed;background:#f8fbfd}
.vaccine-accordion .accordion-body{padding:4px 17px 16px}
.vaccine-accordion .accordion-body p{margin:12px 0}
.vaccine-status{font-size:.9rem;color:#52677b}
.vaccine-status strong{color:#315f7d}
.article-note{padding:14px 16px;border-left:3px solid #91b6cc;background:#f3f8fb;border-radius:6px;margin:18px 0}
@media(max-width:560px){.vaccine-accordion summary{padding:13px 14px;padding-right:38px}.vaccine-accordion summary:after{right:14px}.vaccine-accordion .accordion-body{padding:3px 14px 14px}}
'''

HERO = "https://www.vet.upenn.edu/wp-content/uploads/2025/01/mason-res-header.jpg"


def _accordion(title: str, body: str) -> str:
    return f'''<details class="vaccine-accordion"><summary>{title}</summary><div class="accordion-body">{body}</div></details>'''


def generate_cancer_vaccine_article(root: Path) -> None:
    """Create the article, link it from the Articles index, and add it to sitemap."""
    url = f'{SITE}/articles/cancer-vaccines/'
    trial_finder = f'{FINDER}/'
    options_finder = f'{FINDER}/Additional_Oncology_Options'

    accordions = ''.join([
        _accordion(
            'ONCEPT | Oral melanoma',
            '''<p>ONCEPT is a USDA-licensed DNA vaccine used as an <strong>adjunct treatment</strong> for dogs with stage II or III oral melanoma after local control of the primary disease has been achieved. Local control usually means surgery and, in some cases, radiation.</p>
<p>Each dose contains DNA encoding human tyrosinase. Tyrosinase is expressed by melanoma cells. The human version is different enough to attract the dog's immune system but similar enough that the resulting immune response can also recognize canine melanoma cells.</p>
<p>The initial course is four doses given two weeks apart, followed by boosters every six months.</p>
<p>The licensing evidence suggested longer survival than a historical control group, but this was not a modern randomized trial with a concurrent control arm. The published numbers should not be read as a promise of a specific survival gain for an individual dog.</p>
<p class="vaccine-status"><strong>Status:</strong> licensed veterinary cancer vaccine. It complements local treatment rather than replacing it.</p>
<p><a href="https://animalhealth.boehringer-ingelheim.com/pets/canine/products/therapeutics/oncept" rel="noopener">Official ONCEPT information</a></p>'''
        ),
        _accordion(
            'Yale / TheraJan EGFR-HER2 vaccine | Osteosarcoma, hemangiosarcoma, TCC',
            '''<p>This peptide vaccine was developed by the Yale group led by Mark Mamula and is being evaluated through TheraJan in a USDA-regulated study. It targets the EGFR/HER2 family of tumor proteins and is intended to stimulate antibodies and T cells against cancer cells carrying these targets.</p>
<p>As of September 2026, the study is open to dogs with confirmed <strong>osteosarcoma, hemangiosarcoma, or transitional cell carcinoma (urothelial/bladder cancer)</strong>. Eligibility is decided by the individual clinical site, not by Yale and not by a preliminary online match.</p>
<p>The vaccine itself is currently supplied without charge to participating sites and owners. The owner remains responsible for evaluation, testing, and vaccine administration costs because the study is not fully funded.</p>
<p>More than 600 dogs have reportedly received the vaccine, and early reports include some striking long-term responders. Those individual cases are not proof that another dog will have the same result. The current program is still collecting efficacy data, and USDA has not established full safety and efficacy for this investigational product.</p>
<p class="vaccine-status"><strong>Status:</strong> experimental vaccine in an active USDA-regulated clinical study.</p>
<p><a href="https://therajan.com/joomla/" rel="noopener">TheraJan study information</a><br><a href="https://www.ccralliance.org/yale-status" rel="noopener">Current study locations and updates</a></p>'''
        ),
        _accordion(
            'University of Minnesota AAV vaccine | Oral melanoma',
            '''<p>The University of Minnesota is enrolling dogs in a study of a new adeno-associated virus (AAV) cancer vaccine for malignant oral melanoma.</p>
<p>Dogs must have biopsy-confirmed oral malignant melanoma, at least stage I, be at least one year old, weigh at least 5 kg (11 lb), and meet additional health criteria. Dogs that have already received ONCEPT are excluded. The study also tests for pre-existing neutralizing antibodies to the AAV delivery system.</p>
<p>The protocol includes staging, local treatment of the melanoma with surgery or radiation as clinically appropriate, vaccination, and scheduled follow-up. The study covers trial-related visits and provides up to a $4,000 credit toward local therapy performed at the University of Minnesota Veterinary Medical Center. Costs beyond that credit remain the owner's responsibility.</p>
<p class="vaccine-status"><strong>Status:</strong> active clinical trial, open and enrolling as of September 2026.</p>
<p><a href="https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/new-vaccine" rel="noopener">University of Minnesota trial page</a></p>'''
        ),
        _accordion(
            'ELIAS Cancer Immunotherapy (ECI) | Osteosarcoma',
            '''<p>ELIAS Cancer Immunotherapy is not simply a vaccine. It is a <strong>vaccine-enhanced adoptive T-cell therapy</strong>. Tumor tissue from the dog is used to make a personalized series of cancer-cell vaccines. The dog's immune cells are then collected, activated outside the body, and returned by infusion.</p>
<p>ECI is distributed under a USDA Autologous Prescription Product license for canine osteosarcoma. It is available through trained oncology centers in the United States, so a dog does not have to enter a trial to receive the licensed product. The full protocol is required. ELIAS specifically states that the vaccine step is not offered by itself.</p>
<p>There are also active studies of ECI combinations. In September 2026, ELIAS lists an enrolling study at the University of Missouri combining ECI with a novel adjuvant after surgery, and a prospective study combining ECI with chemotherapy.</p>
<p>Because the vaccine is manufactured from the dog's tumor, planning must happen before amputation or other treatment that would make usable tumor tissue unavailable.</p>
<p class="vaccine-status"><strong>Status:</strong> USDA-licensed autologous prescription product for canine osteosarcoma, plus active clinical studies of combination protocols.</p>
<p><a href="https://eliasanimalhealth.com/elias-cancer-immunotherapy/" rel="noopener">Official ECI treatment information</a><br><a href="https://eliasanimalhealth.com/available-locations/" rel="noopener">Authorized ECI treatment centers</a><br><a href="https://eliasanimalhealth.com/clinical-studies/" rel="noopener">Current ELIAS clinical studies</a></p>'''
        ),
        _accordion(
            'Autologous tumor vaccines | Personalized vaccines from the dog\'s own tumor',
            '''<p>An autologous vaccine is made from the patient's own tumor. Fresh tumor or lymph-node tissue is collected, processed, and used to expose the immune system to antigens from that individual cancer.</p>
<p>The idea is biologically attractive, but the word <em>personalized</em> does not mean the treatment has been proven better. A small K9-ACV study found an increased tumor-directed immune response in 17 of 20 dogs that completed vaccination. An immune response in a laboratory test is not the same outcome as longer survival.</p>
<p>A 2026 systematic review evaluated 24 studies of autologous tumor vaccines in dogs. The treatments were generally well tolerated. The most encouraging clinical evidence was in lymphoma, while evidence for many solid tumors remained limited and heterogeneous.</p>
<p>One example is APAVAC/Vaxkit, an autologous vaccine platform used with chemotherapy in canine B-cell lymphoma. Availability and regulatory status differ by product and country, so owners should ask exactly which product is being proposed and what evidence exists for that diagnosis.</p>
<p class="vaccine-status"><strong>Status:</strong> varies by product. Some are veterinarian-directed products; others remain investigational.</p>
<p><a href="https://vaxkit.com/" rel="noopener">APAVAC / Vaxkit information</a></p>'''
        ),
        _accordion(
            'Listeria-HER2 vaccine | Osteosarcoma research',
            '''<p>This experimental platform uses modified <em>Listeria monocytogenes</em> to stimulate an immune response against HER2.</p>
<p>The first Phase I study included only 18 dogs with appendicular osteosarcoma after surgery and chemotherapy. Fifteen of 18 developed a HER2-specific immune response, and comparison with historical controls suggested fewer metastases and longer survival.</p>
<p>A much larger prospective multicenter study then treated 118 dogs. It did <strong>not</strong> show a statistically significant improvement in disease-free interval or overall survival compared with the historical standard-treatment group.</p>
<p>A 2026 pilot study combined palliative radiation with Listeria-HER2 immunotherapy in 15 dogs. Five had notably longer local control and survival associated with certain immune characteristics. That result is interesting, but 15 dogs are not enough to establish a new standard of care.</p>
<p class="vaccine-status"><strong>Status:</strong> experimental research platform, not standard osteosarcoma treatment.</p>'''
        ),
        _accordion(
            'Peptide vaccine | Hemangiosarcoma research',
            '''<p>A Phase II study evaluated a peptide cancer vaccine in 28 dogs with aggressive hemangiosarcoma after standard surgery and doxorubicin chemotherapy.</p>
<p>The investigators documented tumor-specific immune responses and did not observe serious vaccine-related toxicity. Outcomes were compared with a retrospective group of 32 dogs rather than a randomized concurrent control group.</p>
<p>This is useful evidence that the vaccine can generate an immune response and appears feasible, but it is not enough to treat the approach as established therapy.</p>
<p class="vaccine-status"><strong>Status:</strong> research evidence; not a standard commercially available hemangiosarcoma vaccine.</p>'''
        ),
        _accordion(
            'Preventive cancer vaccines | VACCS and prevention research',
            '''<p>Most cancer vaccines are therapeutic. They are given after cancer has already been diagnosed. Researchers have also tested whether vaccination could prevent cancer from developing in healthy dogs.</p>
<p>The Vaccination Against Canine Cancer Study (VACCS) enrolled 804 healthy dogs in a randomized, placebo-controlled study. Its purpose was to test a multivalent vaccine before cancer appeared and then follow the dogs for cancer development over time.</p>
<p>This is fundamentally different from ONCEPT, the Yale vaccine, or an autologous tumor vaccine. There is currently no universal preventive cancer vaccine available for dogs in routine veterinary practice.</p>
<p class="vaccine-status"><strong>Status:</strong> prevention research, not an available routine vaccine.</p>'''
        ),
    ])

    body = f'''<article class="article-page"><h1>Cancer Vaccines for Dogs</h1>
<p class="article-deck">Cancer vaccines are already part of veterinary oncology, but the word <em>vaccine</em> covers very different treatments. One is licensed for oral melanoma. Some are personalized from a dog's own tumor. Others are available only through clinical trials.</p>
<figure class="article-hero"><img src="{HERO}" alt="Researchers working in a canine cancer immunotherapy laboratory" width="1600" height="891"><figcaption>Canine cancer immunotherapy research in the Mason Immunotherapy Research Laboratory. Photo: University of Pennsylvania School of Veterinary Medicine.</figcaption></figure>
<p>Unlike routine vaccines against infectious disease, most cancer vaccines are not given to prevent cancer. They are used after a tumor has been diagnosed. Their goal is to help the immune system recognize tumor-associated targets and attack cancer cells more effectively.</p>
<p>That does not make every cancer vaccine interchangeable. The diagnosis, stage, previous treatment, available tumor tissue, and the exact vaccine all matter.</p>
<div class="article-note"><strong>One useful question before anything else:</strong> Is this a licensed treatment, a veterinarian-directed product, or an experimental vaccine available only through a clinical study?</div>
<div class="vaccine-accordions">{accordions}</div>
<h2>Can a cancer vaccine replace surgery, chemotherapy, or radiation?</h2>
<p>Usually not. Most therapeutic vaccines have been studied as an addition to local treatment or systemic therapy, or after the visible tumor has been removed. ONCEPT, for example, is used after local control of oral melanoma. The Minnesota melanoma trial also includes local treatment. ELIAS ECI is a multi-step treatment built around tumor removal and immune-cell therapy.</p>
<p>If a vaccine is being proposed <em>instead of</em> standard treatment, ask whether that exact strategy has been studied for the same cancer and stage.</p>
<h2>What to ask the veterinary oncologist</h2>
<ul><li>What is the exact name of the vaccine or immunotherapy?</li><li>Is it licensed, used under a veterinary prescription product pathway, off-label, or experimental?</li><li>Is there published evidence for this cancer type and stage?</li><li>How many dogs were included, and was there a concurrent control group?</li><li>Did the study measure survival or tumor control, or only an immune response?</li><li>Does the vaccine supplement standard treatment or replace any part of it?</li><li>Does fresh tumor tissue need to be saved before surgery?</li><li>Is there an active clinical trial my dog may qualify for?</li><li>Which costs are covered by the study and which remain the owner's responsibility?</li><li>What adverse effects have been reported?</li></ul>
<h2>Find a vaccine, study, or treatment center</h2>
<p>Trial status and participating hospitals change. A study that is open today may close, and new vaccine studies may appear.</p>
<div class="article-cta"><a href="{trial_finder}">Search current veterinary cancer trials in Vet Trial Finder</a></div>
<p>For treatments that can be offered outside a conventional clinical trial, including selected advanced immunotherapies, use the treatment-options section as a starting point and confirm current availability directly with the oncology center.</p>
<div class="article-cta"><a href="{options_finder}">Search other oncology treatment options and centers</a></div>
<p>A preliminary match in Vet Trial Finder is not final eligibility. The treating or research team makes that decision after reviewing the medical record.</p>
<h2>The bottom line</h2>
<p>There is no single "cancer vaccine." ONCEPT is a licensed melanoma vaccine. ELIAS ECI includes a personalized vaccine as part of a licensed multi-step cell therapy. Yale/TheraJan and the University of Minnesota are testing different vaccine strategies in active studies. Other platforms remain research tools whose early results still need confirmation.</p>
<p>The useful question is not whether cancer vaccines work in general. It is whether a particular vaccine has meaningful evidence for a particular dog, cancer, stage, and treatment plan.</p>
<div class="article-byline"><p><strong>Author:</strong> Yuliia Dizhur</p><p><strong>Published:</strong> September 13, 2026</p><p><strong>Last updated:</strong> September 13, 2026</p><p>This article is educational and does not replace consultation with a veterinary oncologist.</p></div>
<h2>Sources</h2>
<ul class="article-sources">
<li><a href="https://animalhealth.boehringer-ingelheim.com/pets/canine/products/therapeutics/oncept" rel="noopener">Boehringer Ingelheim: ONCEPT Canine Melanoma Vaccine, DNA</a></li>
<li><a href="https://therajan.com/joomla/" rel="noopener">TheraJan: Canine EGFR/HER2 Peptide Cancer Immunotherapeutic</a></li>
<li><a href="https://www.ccralliance.org/yale-status" rel="noopener">Canine Cancer Alliance: EGFR/HER2 Vaccine Study Status</a></li>
<li><a href="https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/new-vaccine" rel="noopener">University of Minnesota: AAV vaccine trial for oral melanoma</a></li>
<li><a href="https://www.aphis.usda.gov/veterinary-biologics/product-summaries/691-95a750" rel="noopener">USDA APHIS: ELIAS Autologous Prescription Product</a></li>
<li><a href="https://eliasanimalhealth.com/elias-cancer-immunotherapy/" rel="noopener">ELIAS Cancer Immunotherapy: treatment information</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/27863558/" rel="noopener">Autologous cancer vaccine pilot study</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/42284812/" rel="noopener">2026 systematic review of autologous tumor vaccines in dogs</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/26994144/" rel="noopener">Phase I Listeria-HER2 osteosarcoma study</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/39955616/" rel="noopener">Multicenter Listeria-HER2 osteosarcoma study</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/42291138/" rel="noopener">2026 radiation plus Listeria-HER2 pilot study</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/37686485/" rel="noopener">Hemangiosarcoma peptide vaccine Phase II study</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/38056066/" rel="noopener">Vaccination Against Canine Cancer Study (VACCS)</a></li>
<li><a href="https://www.vet.upenn.edu/research/research-laboratories/mason-immunotherapy-research-laboratory/our-research/" rel="noopener">University of Pennsylvania School of Veterinary Medicine: Mason Immunotherapy Research Laboratory</a></li>
</ul></article>'''

    dest = root / 'articles' / 'cancer-vaccines'
    dest.mkdir(parents=True, exist_ok=True)
    rendered = g.page(
        'Cancer Vaccines for Dogs | Vet Trial Finder',
        'A practical guide to licensed and experimental cancer vaccines for dogs, including ONCEPT, Yale EGFR/HER2, ELIAS ECI and active vaccine trials.',
        body,
        url,
    )
    rendered = rendered.replace('</style>', VACCINE_CSS + '</style>', 1)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': 'Cancer Vaccines for Dogs',
        'image': [HERO],
        'datePublished': '2026-09-13',
        'dateModified': '2026-09-13',
        'author': {'@type': 'Person', 'name': 'Yuliia Dizhur'},
        'publisher': {'@type': 'Organization', 'name': 'Vet Trial Finder', 'url': f'{SITE}/'},
        'mainEntityOfPage': url,
    }
    rendered = rendered.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (dest / 'index.html').write_text(rendered, encoding='utf-8')

    article_index = root / 'articles' / 'index.html'
    if article_index.exists():
        text = article_index.read_text(encoding='utf-8')
        card = f'''<a class="directory-card" href="{url}"><strong>Cancer Vaccines for Dogs</strong><span>ONCEPT, Yale EGFR/HER2, personalized vaccines, active trials and what the evidence actually shows.</span></a>'''
        if url not in text:
            marker = '</div>'
            grid_start = text.find('<div class="directory-grid">')
            if grid_start >= 0:
                grid_end = text.find(marker, grid_start)
                if grid_end >= 0:
                    text = text[:grid_end] + card + text[grid_end:]
                    article_index.write_text(text, encoding='utf-8')

    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        text = sitemap.read_text(encoding='utf-8')
        if url not in text:
            text = text.replace('</urlset>', f'<url><loc>{g.esc(url)}</loc></url>\n</urlset>')
            sitemap.write_text(text, encoding='utf-8')