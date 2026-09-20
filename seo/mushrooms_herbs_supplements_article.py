#!/usr/bin/env python3
"""Generate the owner-facing article about mushrooms, herbs, and supplements in canine cancer care."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html


def generate_mushrooms_herbs_supplements_article(root: Path) -> None:
    url = f"{SITE}/articles/mushrooms-herbs-supplements-dogs-with-cancer/"
    body = f'''<article class="article-page">
<h1>Mushrooms, herbs, and supplements for dogs with cancer</h1>

<blockquote><p>“The systemic and individualized nature of each cancer diagnosis will prevent us from creating disease-based recommendations.”</p></blockquote>

<p>That observation comes from Dr. Kendra Pope, a board-certified veterinary oncologist whose practice focuses on integrative oncology, including herbal medicine and Traditional Chinese Veterinary Medicine. In her chapter on <a href="https://onlinelibrary.wiley.com/doi/10.1002/9781119823551.ch22" rel="noopener">integrative oncology</a>, she reviews herbs, supplements, medicinal mushrooms, nutrition, and other complementary approaches while emphasizing individualized, evidence-informed decisions.</p>

<p>This is the central point when considering turkey tail, reishi, Chinese herbal formulas, curcumin, CBD, omega-3 fatty acids, or vitamins. These products can have a place in supportive care. The useful question is not whether one ingredient is “good for cancer.” It is what this particular dog needs, what the supplement is meant to do, and how it fits with the rest of the treatment plan.</p>

<h2>Traditional Chinese medicine begins with the patient</h2>

<p>Traditional Chinese herbal practice is not usually built around one herb for one disease. Practitioners combine several ingredients and choose or modify the formula according to the individual patient. Appetite, digestion, pain, weakness, sleep, concurrent illness, and other signs may all influence that choice.</p>

<p>A contemporary veterinarian also considers the confirmed diagnosis, laboratory results, current medications, and the goals of care. The formula may change as the dog’s condition changes.</p>

<p>Centuries of use provide history and practical experience. They do not prove that a product controls a particular tumor. The two ideas can coexist: traditional practice can contribute to supportive care while modern evidence and monitoring help determine safety, interactions, and whether the intended goal is being met.</p>

<p>The <a href="https://www.msdvetmanual.com/therapeutics/integrative-complementary-and-alternative-veterinary-medicine/herbal-medicine-in-veterinary-patients" rel="noopener">MSD Veterinary Manual</a> notes that botanical products can contain biologically active compounds and may alter the blood concentrations of other medications. That is one reason an herbal formula deserves the same attention to ingredients, dose, and interactions as any other part of a dog’s care.</p>

<h2>Medicinal mushrooms</h2>

<p>Turkey tail (<em>Trametes versicolor</em>), reishi, maitake, and shiitake are among the mushrooms most often discussed in canine cancer care. Their polysaccharides, beta-glucans, and other compounds can affect immune activity, which is why some integrative veterinarians include selected mushroom products in supportive plans.</p>

<p>Turkey tail has the best-known canine cancer study. A small <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3440946/" rel="noopener">2012 trial</a> included 15 dogs with splenic hemangiosarcoma after splenectomy. The findings were encouraging and supported further research.</p>

<p>A later randomized study tested a polysaccharopeptide extract, alone or with doxorubicin. The authors reported:</p>

<blockquote><p>“The addition of PSP to doxorubicin post-splenectomy did not improve survival in dogs with splenic HSA.”</p></blockquote>

<p>The study was published in <a href="https://pubmed.ncbi.nlm.nih.gov/35442554/" rel="noopener"><em>Veterinary and Comparative Oncology</em></a>.</p>

<p>Together, these studies do not make medicinal mushrooms either a proven cancer treatment or a useless product. They show why the exact preparation matters. Whole mushroom powder, a hot-water extract, purified PSP, and a blend of several mushrooms are not interchangeable, even when their labels use the same mushroom name.</p>

<p>A specialist may still recommend a mushroom supplement, but the recommendation should identify the product, the intended purpose, and how the dog’s response will be assessed.</p>

<h2>Curcumin and other botanical supplements</h2>

<p>Curcumin is studied for anti-inflammatory, immune-modulating, and antiproliferative effects. These are legitimate areas of research. The practical uncertainty is whether a particular oral product is absorbed well enough to produce a meaningful effect in a dog.</p>

<p>Turmeric used in food, turmeric powder, a standardized curcumin extract, and formulations designed to increase absorption are different products. Curcumin can also cause gastrointestinal signs, affect clotting, and potentially interact with medications.</p>

<p>The same principle applies to milk thistle, ginger, boswellia, antioxidants, vitamins, and omega-3 fatty acids. Each may have a role, but supporting liver function, correcting a deficiency, improving nutrition, easing a symptom, and treating a tumor are different goals. The product and dose should be chosen for the goal.</p>

<h2>CBD</h2>

<p>In canine cancer care, CBD is more appropriately discussed as a possible part of symptom and quality-of-life support than as a treatment for the tumor itself. It may be considered for pain, anxiety, or other specific problems, depending on the patient.</p>

<p>Dr. Trina Hazzah, a veterinary oncologist and co-founder of the Veterinary Cannabis Society, described the distinction this way:</p>

<blockquote><p>“I don’t think anyone can say that right now, but perhaps use it at this dose so you don’t hurt your pet.”</p></blockquote>

<p>In the full <a href="https://www.dogcancer.com/podcast/supplements/cannabis-to-help-dogs-with-cancer-a-veterinary-oncologist-perspective-dr-trina-hazzah-deep-dive/" rel="noopener">discussion of cannabis in canine cancer care</a>, she frames veterinary guidance as a harm-reduction strategy. Owners can already obtain these products, so professional input can help them assess the contents, choose a dose, and recognize adverse effects.</p>

<p>CBD products vary in concentration, additional ingredients, and THC content. THC can be toxic to dogs. CBD may cause sedation, gastrointestinal signs, reduced appetite, or changes in liver enzymes, and it may interact with other drugs. A few drops is not a complete plan unless the concentration, dose, purpose, and monitoring are known.</p>

<h2>What individualized support looks like</h2>

<p>A supplement becomes part of a coordinated plan when the clinician knows the diagnosis, the dog’s current condition, and everything else the dog receives. The recommendation should answer:</p>

<ul>
<li>What specific goal does this supplement have?</li>
<li>Which preparation, extract, and active-ingredient amount are being used?</li>
<li>Could it interact with medication or affect surgery, bleeding, or laboratory results?</li>
<li>How will benefit be recognized?</li>
<li>What adverse sign or test result would mean changing or stopping it?</li>
</ul>

<p>Introducing one new supplement at a time makes changes in appetite, stool, energy, comfort, or laboratory results easier to interpret. When several products begin together, neither a better day nor a worse day can identify which one made the difference.</p>

<p>Mushrooms, herbs, CBD, and nutritional supplements can be reasonable parts of supportive cancer care. The distinction is between a self-assembled collection and supplements selected by a qualified professional for one dog, one purpose, and one coordinated treatment plan. What matters is the formulation, dose, compatibility, and follow-up.</p>

<h2>Finding an integrative veterinary professional</h2>

<p>Availability, telemedicine rules, and the ability to recommend a specific product vary by location. These resources are starting points for owners seeking a veterinarian trained in both oncology and integrative care, or a professional who can collaborate with the treating oncology team:</p>

<ul>
<li><a href="https://www.prismvethealth.com/doctors/dr-kendra-pope" rel="noopener">Dr. Kendra Pope, Prism Integrative Veterinary Health</a></li>
<li><a href="https://drtrinahazzah.com/" rel="noopener">Dr. Trina Hazzah</a></li>
<li><a href="https://www.ahvma.org/find-a-holistic-veterinarian/" rel="noopener">American Holistic Veterinary Medical Association veterinarian directory</a></li>
<li><a href="https://veterinarycannabissociety.org/" rel="noopener">Veterinary Cannabis Society</a></li>
</ul>

<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 20, 2026</p><p><strong>Last updated:</strong> September 20, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and a dog owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance and information from veterinary hospitals and research teams.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>

<h2>Sources</h2>
<ul class="article-sources">
<li><a href="https://onlinelibrary.wiley.com/doi/10.1002/9781119823551.ch22" rel="noopener">Pope K. Integrative Oncology</a>. In: <em>Integrative Veterinary Medicine</em>. 2023.</li>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3440946/" rel="noopener">Brown DC, Reetz J. Single Agent Polysaccharopeptide Delays Metastases and Improves Survival in Naturally Occurring Hemangiosarcoma</a>. 2012.</li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/35442554/" rel="noopener">Evaluation of Coriolus versicolor polysaccharopeptide alone or with doxorubicin for canine splenic hemangiosarcoma</a>. 2022.</li>
<li><a href="https://www.msdvetmanual.com/therapeutics/integrative-complementary-and-alternative-veterinary-medicine/herbal-medicine-in-veterinary-patients" rel="noopener">MSD Veterinary Manual. Herbal Medicine in Veterinary Patients</a>.</li>
<li><a href="https://www.dogcancer.com/podcast/supplements/cannabis-to-help-dogs-with-cancer-a-veterinary-oncologist-perspective-dr-trina-hazzah-deep-dive/" rel="noopener">Hazzah T. Cannabis to Help Dogs with Cancer: A Veterinary Oncologist Perspective</a>.</li>
</ul>
</article>'''

    directory = root / 'articles' / 'mushrooms-herbs-supplements-dogs-with-cancer'
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(
        'Mushrooms, herbs, and supplements for dogs with cancer | Vet Trial Finder',
        'How medicinal mushrooms, Chinese herbal formulas, curcumin, CBD, and other supplements can be selected as individualized supportive care for dogs with cancer.',
        body,
        url,
    )
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="Mushrooms, herbs, and supplements for dogs with cancer"><meta property="og:description" content="Why supportive supplements should be selected for the individual dog, purpose, and treatment plan."><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="Mushrooms, herbs, and supplements for dogs with cancer"><meta name="twitter:description" content="Why supportive supplements should be selected for the individual dog, purpose, and treatment plan.">'''
    rendered = rendered.replace('</head>', social + '</head>', 1)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': 'Mushrooms, herbs, and supplements for dogs with cancer',
        'datePublished': '2026-09-20',
        'dateModified': '2026-09-20',
        'author': {'@type': 'Person', 'name': 'Yuliia Dizhur', 'url': f'{SITE}/about/', 'jobTitle': 'Founder of Vet Trial Finder'},
        'publisher': {'@type': 'Organization', 'name': 'Vet Trial Finder', 'url': f'{SITE}/'},
        'mainEntityOfPage': url,
    }
    rendered = rendered.replace('</head>', f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (directory / 'index.html').write_text(wrap_html(rendered), encoding='utf-8')

    index = root / 'articles' / 'index.html'
    if not index.exists():
        raise AssertionError('Articles index is required before adding the supplements article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = f'''<a class="directory-card" href="{url}"><strong>Mushrooms, herbs, and supplements for dogs with cancer</strong><span>Why supportive supplements should be selected for the individual dog, purpose, and treatment plan.</span></a>'''
        if '<div class="directory-grid">' not in text:
            raise AssertionError('Articles index is missing the directory-grid container')
        text = text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1)
        index.write_text(text, encoding='utf-8')

    sitemap = root / 'sitemap.xml'
    if sitemap.exists():
        text = sitemap.read_text(encoding='utf-8')
        if url not in text:
            text = text.replace('</urlset>', f'<url><loc>{url}</loc></url></urlset>')
            sitemap.write_text(text, encoding='utf-8')

    article = (directory / 'index.html').read_text(encoding='utf-8')
    required = (
        '<h1>Mushrooms, herbs, and supplements for dogs with cancer</h1>',
        'individualized nature of each cancer diagnosis',
        'Traditional Chinese medicine begins with the patient',
        'The addition of PSP to doxorubicin',
        'What individualized support looks like',
        'Finding an integrative veterinary professional',
        'Reviewed and edited by:',
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in required if marker not in article]
    if missing:
        raise AssertionError(f'Supplements article validation failed: {missing}')


def main() -> None:
    generate_mushrooms_herbs_supplements_article(Path(__file__).resolve().parent / 'site')


if __name__ == '__main__':
    main()
