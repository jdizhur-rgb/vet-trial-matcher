#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import generate_seo as g
from site_config import SITE

def generate_trial_directions_article(root: Path) -> None:
    url=f"{SITE}/articles/where-veterinary-cancer-trials-are-heading/"
    m=f"{SITE}/matcher/?cancer=Cancer%20%E2%80%94%20any%20type&autostart=1"
    links={
      "immune":m+"&approach=immunotherapy","vaccines":m+"&approach=cancer_vaccine",
      "cells":m+"&approach=engineered_immune_cells","targeted":m+"&approach=targeted_therapy",
      "microbes":m+"&approach=oncolytic_microbe","ultrasound":m+"&approach=focused_ultrasound",
      "radiation":m+"&approach=radiation_innovation"}
    body=f'''<article class="article-page"><h1>Where veterinary cancer trials are heading</h1>
<p class="article-deck">Many current cancer trials in dogs are testing ways to make treatment more selective: helping the immune system recognize cancer, targeting a weakness inside the cancer cell, or destroying a tumor in ways that may also trigger an immune response.</p>
<nav class="article-jumps" aria-label="On this page"><strong>Quick links:</strong> <a href="#immune">Helping the immune system attack cancer</a> · <a href="#vaccines">Cancer vaccines</a> · <a href="#cells">Giving immune cells a cancer target</a> · <a href="#targeted">Targeted drugs</a> · <a href="#microbes">Viruses and bacteria</a> · <a href="#ultrasound">Focused ultrasound</a> · <a href="#radiation">New radiation approaches</a> · <a href="#combinations">Combination treatment</a></nav>
<h2 id="immune">Helping the immune system attack cancer</h2>
<p>Cancer can survive partly because it learns to suppress the immune response against it. One way involves a protein called <strong>PD-1</strong> on immune cells. When the corresponding signal is switched on, the immune cell is told not to attack.</p>
<p>PD-1 inhibitors block that signal. They do not kill cancer directly in the way chemotherapy does. The aim is to remove one of the ways a tumor protects itself and allow the dog's own immune system to attack it.</p>
<p>This approach has changed treatment for several human cancers. In dogs it is much less established. Responses have been reported in some canine tumors, but researchers are still working out which cancers respond, how long responses last and why some dogs respond while others do not.</p>
<p>Current veterinary studies include PD-1 treatment for <a href="{SITE}/north-america/dogs/urothelial-carcinoma/">urothelial carcinoma (bladder cancer)</a> and combinations of immune treatment with vaccines, radiation or local tumor treatment.</p>
<p><a href="{links["immune"]}">Browse current immunotherapy trials →</a></p>
<h2 id="vaccines">Cancer vaccines</h2>
<p>Most cancer vaccines in veterinary trials are treatment vaccines, not vaccines given to healthy dogs to prevent cancer. They expose the immune system to something associated with the tumor, with the aim of helping it recognize cancer cells that remain after surgery, chemotherapy or radiation.</p>
<p>The history of canine <a href="{SITE}/north-america/dogs/osteosarcoma/">osteosarcoma</a> shows why early results need caution. A small early study of a Listeria-based HER2 vaccine produced striking results. A later multicenter study of 118 dogs found an immune response but did <strong>not</strong> find a statistically significant improvement in disease-free interval or overall survival compared with a historical standard-treatment group.</p>
<p>Other vaccine approaches have produced encouraging preliminary signals. In a small study of dogs with aggressive <a href="{SITE}/north-america/dogs/hemangiosarcoma/">hemangiosarcoma</a>, dogs receiving a peptide vaccine after surgery and doxorubicin had longer median survival than a retrospective comparison group. Because the study was small and not randomized, that result still needs confirmation.</p>
<p>Current studies include vaccines for osteosarcoma, hemangiosarcoma, melanoma, bladder cancer and feline oral squamous cell carcinoma, including mRNA and personalized vaccine approaches.</p>
<p><a href="{SITE}/articles/cancer-vaccines/">Read the cancer vaccine guide</a> · <a href="{links["vaccines"]}">Browse current vaccine trials →</a></p>
<h2 id="cells">Giving immune cells a cancer target</h2>
<p>Another approach modifies immune cells so that they can recognize a selected marker on cancer cells. This is where names such as <strong>CAR-T</strong> and <strong>CAR-iNKT</strong> appear. The technical difference is the type of immune cell being used. For an owner, the important point is that these are living immune cells modified to recognize a particular cancer target.</p>
<p>This has produced major results in some human blood cancers. Solid tumors are harder: the modified cells must reach the tumor, survive there and keep working in an environment that suppresses immune responses.</p>
<p>Veterinary trials are testing these approaches in osteosarcoma, B-cell lymphoma/leukemia and soft tissue sarcoma. These are still experimental treatments; current studies are answering basic questions about safety, persistence of the modified cells and tumor response.</p>
<p><a href="{links["cells"]}">Browse current engineered immune-cell trials →</a></p>
<h2 id="targeted">Targeting a weakness in the cancer cell</h2>
<p>Some trials look for a molecular pathway that a cancer depends on and try to block it. Trametinib and histiocytic sarcoma are a useful example. Research found abnormal activity in the MAPK pathway in some canine histiocytic sarcomas. Trametinib blocks MEK, one part of that pathway, and canine histiocytic sarcoma cells were sensitive to it in laboratory studies.</p>
<p>A phase I study in dogs established a dose for further study. It did not establish that trametinib improves survival in histiocytic sarcoma. That question is now being tested directly in a phase II study at the University of Florida.</p>
<p>Current targeted-drug studies also include other cancers and molecular targets. Finding a target gives researchers a specific reason to test a drug; it does not guarantee that blocking the target will control cancer in a living dog.</p>
<p><a href="{links["targeted"]}">Browse current targeted-therapy trials →</a></p>
<h2 id="microbes">Viruses and bacteria used against cancer</h2>
<p>Some viruses are engineered to infect or damage cancer cells. Bacteria can also be modified to carry tumor targets and provoke an immune response. The Listeria-HER2 osteosarcoma vaccine is one example; oncolytic viruses are another.</p>
<p>Destroying tumor cells this way may release tumor material that the immune system can recognize. The difficult question is whether that biological effect produces meaningful control of metastatic disease. Canine studies have shown immune activity and occasional long survivors, but that is not the same as a proven general survival benefit.</p>
<p><a href="{links["microbes"]}">Browse current virus/bacteria-based trials →</a></p>
<h2 id="ultrasound">Destroying tumors with ultrasound</h2>
<p><strong>Focused ultrasound</strong> concentrates acoustic energy inside a tumor without a surgical incision. <strong>Histotripsy</strong> uses very short ultrasound pulses to mechanically break tumor tissue apart. Other ultrasound-based techniques use heat or electrical effects to ablate tissue.</p>
<p>The immediate goal is local tumor destruction. Researchers are also studying whether the resulting release of tumor material changes the immune response elsewhere in the body.</p>
<p>Recent canine osteosarcoma research found local and systemic immune changes after histotripsy. That provides a reason for larger studies, but it does not yet prove that histotripsy extends survival. Current trials include osteosarcoma, lymphoma, thyroid tumors, melanoma, bladder cancer and liver tumors.</p>
<p><a href="{links["ultrasound"]}">Browse current focused-ultrasound and ablation trials →</a></p>
<h2 id="radiation">New ways to use radiation</h2>
<p>One direction is <strong>FLASH radiation</strong>, in which radiation is delivered at an extremely high dose rate. Current veterinary studies are testing FLASH in osteosarcoma, soft tissue sarcoma and feline oral squamous cell carcinoma.</p>
<p>Other studies use stereotactic or lattice radiation, or combine radiation with immune treatment. Radiation can damage cancer cells and release tumor material, so researchers are asking whether local treatment can also help produce a broader immune response.</p>
<p>A small 2026 study combining palliative radiation with Listeria-HER2 immunotherapy in 15 dogs with osteosarcoma found a subgroup with delayed progression and longer survival. With 15 dogs, that is a reason for further study, not proof that the combination improves survival.</p>
<p><a href="{links["radiation"]}">Browse current radiation-innovation trials →</a></p>
<h2 id="combinations">Why combinations matter</h2>
<p>Many current trials combine these ideas. Radiation or ultrasound may destroy tumor cells and expose cancer antigens. A vaccine may help the immune system recognize them. PD-1 treatment may make it harder for the tumor to suppress that response. A targeted drug may interfere with a pathway the cancer needs.</p>
<p>For owners, this makes trial descriptions harder to interpret. A study may include chemotherapy, radiation or surgery even when the experimental part is an immune treatment. The conventional treatment may still be doing much of the work.</p>
<h2>What “promising” actually means</h2>
<p>A phase I trial usually tells us mainly whether a treatment can be given safely and what dose should be studied next. Tumor shrinkage does not necessarily mean longer survival. An immune response proves that the immune system noticed something; it does not prove that the response controlled the cancer.</p>
<p>The canine HER2 osteosarcoma vaccine is a useful example. The early study was exciting. The larger trial still found biological activity, but the apparent survival advantage did not hold up. That is exactly why larger clinical trials are necessary.</p>
<p>For an owner considering a trial, the useful questions are simple: <strong>What is the experimental treatment supposed to do? What has actually been shown in dogs? What is still unknown? And what treatment would my dog receive if we did not enter this trial?</strong></p>
<div class="article-cta"><a href="{SITE}/matcher/">Search current cancer trials for your dog or cat</a></div>
<h2>References</h2><ol class="article-sources">
<li><a href="https://pubmed.ncbi.nlm.nih.gov/39955616/" rel="noopener">Mason NJ, et al. Immunological responses and clinical outcomes in dogs with osteosarcoma receiving standard therapy and a Listeria vaccine expressing HER2. Molecular Therapy. 2025.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/26994144/" rel="noopener">Mason NJ, et al. HER2-targeting Listeria immunotherapy in canine osteosarcoma. Clinical Cancer Research. 2016.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/37686485/" rel="noopener">Phase 2 peptide-based vaccination in dogs with aggressive hemangiosarcoma. 2023.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/30135215/" rel="noopener">Gardner HL, et al. Targeting MEK in a translational model of histiocytic sarcoma. 2018.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/38889903/" rel="noopener">Phase I trametinib pharmacokinetics, pharmacodynamics and safety in dogs with cancer. 2024.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/42588726/" rel="noopener">Histotripsy ablation in spontaneously occurring canine osteosarcoma. 2026.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/42291138/" rel="noopener">Radiation plus Listeria immunotherapy in canine osteosarcoma. 2026.</a></li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/37792729/" rel="noopener">Anti-PD-L1 antibody c4G12 in dogs with advanced malignant tumors. 2023.</a></li>
</ol>
<p class="article-note"><strong>Current-trial links:</strong> trial status changes faster than published literature. The links above open the live Vet Trial Finder catalog filtered by research approach. Final eligibility and enrollment are determined by each study team.</p>
<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 26, 2026</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed above and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div></article>'''
    dest=root/"articles"/"where-veterinary-cancer-trials-are-heading";dest.mkdir(parents=True,exist_ok=True)
    rendered=g.page("Where Veterinary Cancer Trials Are Heading | Vet Trial Finder","An owner-friendly guide to current directions in veterinary cancer research: immunotherapy, vaccines, targeted drugs, engineered immune cells, ultrasound and new radiation approaches.",body,url)
    (dest/"index.html").write_text(rendered,encoding="utf-8")
    index=root/"articles"/"index.html"
    if index.exists():
        text=index.read_text(encoding="utf-8")
        card=f'<a class="directory-card" href="{url}"><strong>Where veterinary cancer trials are heading</strong><span>Immunotherapy, vaccines, targeted drugs, engineered immune cells, focused ultrasound and new radiation approaches — what is being tested and what the results mean.</span></a>'
        if url not in text:
            pos=text.find("</div>",text.find('<div class="directory-grid">'))
            if pos>=0:index.write_text(text[:pos]+card+text[pos:],encoding="utf-8")
    sm=root/"sitemap.xml"
    if sm.exists():
        text=sm.read_text(encoding="utf-8")
        if url not in text:sm.write_text(text.replace("</urlset>",f"<url><loc>{g.esc(url)}</loc></url>\n</urlset>"),encoding="utf-8")
