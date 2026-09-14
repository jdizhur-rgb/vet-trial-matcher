#!/usr/bin/env python3
"""Generate the owner-facing guide to clinical trials for dogs with cancer."""
from pathlib import Path
import generate_seo as g
from site_config import SITE


def generate_dog_cancer_trials_article(root: Path) -> None:
    url = f"{SITE}/articles/clinical-trials-for-dogs-with-cancer/"
    finder = g.FINDER.rstrip('/') + '/'
    body = f'''
<article class="article-page">
<h1>Clinical Trials for Dogs with Cancer</h1>
<p class="article-deck">Clinical trials can give some dogs access to treatments that are not yet widely available. They are not a shortcut around standard care, and a trial match is not the same as being accepted into a study.</p>
<p>The useful question is whether a specific study fits your dog's diagnosis, stage, previous treatment, current health, and location.</p>

<h2>When should you look for a clinical trial?</h2>
<p>You do not have to wait until every standard option has failed. Some studies are designed for newly diagnosed dogs, some require surgery or chemotherapy first, and others are intended for recurrent, metastatic, or treatment-resistant cancer.</p>
<p>Timing matters because previous treatment can change eligibility. If you are interested in trials, it is reasonable to check before starting the next treatment and ask your oncologist whether any study should be considered first.</p>

<h2>What information do you usually need?</h2>
<p>Most study teams will need the exact diagnosis and pathology report. Depending on the cancer, they may also ask for tumor grade or subtype, stage, imaging results, treatment history, dates of chemotherapy or radiation, current medications, bloodwork, and information about other medical conditions.</p>
<p>Some studies require measurable disease. Others require that the visible tumor has already been removed. A study may exclude dogs with metastasis, while another may specifically be for metastatic disease.</p>

<h2>What does a match mean?</h2>
<p>Vet Trial Finder compares the information you enter with the eligibility rules that are publicly available. A match means the study is worth checking. It does not mean your dog has been accepted.</p>
<p>The research team makes the final decision after reviewing the medical record and may use eligibility details that are not fully published online.</p>

<h2>Does a clinical trial mean placebo?</h2>
<p>Not necessarily. Veterinary oncology trials use many designs. Some compare a new treatment with standard care, some add an investigational treatment to standard care, some are single-arm studies in which every enrolled dog receives the investigational treatment, and some may include a placebo or control group.</p>
<p>If a control group is possible, the study team should be able to explain exactly what each group receives and whether rescue treatment or crossover is available.</p>

<h2>Who pays for treatment?</h2>
<p>Funding varies widely. A study may cover the investigational drug but not the initial oncology exam, staging, travel, standard chemotherapy, or treatment of unrelated medical problems. Other studies may cover most trial-related care.</p>
<p>Do not assume that “clinical trial” means free treatment. Check the official study information and ask the study coordinator what is covered before making travel plans.</p>

<h2>Where are veterinary cancer trials run?</h2>
<p>Many are based at veterinary teaching hospitals, but private specialty hospitals, multicenter research networks, biotechnology companies, and referral oncology practices also participate. Some studies are available at several hospitals under one protocol.</p>
<p>For that reason, searching by cancer type is often more useful than searching only the nearest university.</p>

<h2>Common cancer types with active or recurring research</h2>
<ul>
<li><a href="{SITE}/north-america/dogs/osteosarcoma/">Osteosarcoma</a></li>
<li><a href="{SITE}/north-america/dogs/lymphoma/">Lymphoma</a></li>
<li><a href="{SITE}/north-america/dogs/hemangiosarcoma/">Hemangiosarcoma</a></li>
<li><a href="{SITE}/north-america/dogs/mast-cell-tumor/">Mast cell tumor</a></li>
<li><a href="{SITE}/north-america/dogs/oral-melanoma/">Oral melanoma</a></li>
<li><a href="{SITE}/north-america/dogs/soft-tissue-sarcoma/">Soft tissue sarcoma</a></li>
<li><a href="{SITE}/north-america/dogs/histiocytic-sarcoma/">Histiocytic sarcoma</a></li>
<li><a href="{SITE}/north-america/dogs/urothelial-carcinoma/">Urothelial / bladder carcinoma</a></li>
</ul>
<p>Research availability changes. A cancer type with no active listing today may have a study open later.</p>

<h2>Before you contact a study</h2>
<ul>
<li>Have the pathology report and recent oncology records ready.</li>
<li>Know what treatments your dog has already received and the dates.</li>
<li>Ask whether a referral from your veterinarian or oncologist is required.</li>
<li>Confirm travel requirements and how often visits are needed.</li>
<li>Ask what costs are covered.</li>
<li>Ask what happens if your dog does not respond or has side effects.</li>
<li>Do not stop or delay current treatment without discussing it with the treating oncologist.</li>
</ul>

<div class="article-cta"><a href="{finder}">Search current cancer clinical trials for your dog</a></div>

<h2>The bottom line</h2>
<p>A clinical trial is one treatment option, not automatically a better treatment. The value of a study depends on the individual dog and the quality of the evidence behind the approach.</p>
<p>The best use of a trial finder is to identify realistic possibilities quickly, then take those possibilities to the oncology team and the study investigators for a medical decision.</p>
<p class="article-byline">Vet Trial Finder is independent and free to use. Trial status can change, and final eligibility is always determined by the research team.</p>
</article>
'''
    dest = root / 'articles' / 'clinical-trials-for-dogs-with-cancer'
    dest.mkdir(parents=True, exist_ok=True)
    html = g.page(
        'Clinical Trials for Dogs with Cancer | Vet Trial Finder',
        'How to find cancer clinical trials for dogs, understand eligibility, costs, study design and what a trial match really means.',
        body,
        url,
    )
    (dest / 'index.html').write_text(html, encoding='utf-8')
