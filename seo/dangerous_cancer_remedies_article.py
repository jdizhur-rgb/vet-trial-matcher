#!/usr/bin/env python3
"""Generate the owner-facing article about directly harmful cancer remedies."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html


def generate_dangerous_cancer_remedies_article(root: Path) -> None:
    url = f"{SITE}/articles/when-cancer-remedies-cause-harm/"
    body = f'''<article class="article-page">
<h1>When a cancer remedy causes visible harm</h1>

<p>Some cancer remedies look convincing precisely because something visible happens. A mass turns black and appears to come away with a piece of tissue. A liquid foams. A dog or cat vomits or develops diarrhea, followed by a better day. The reaction is presented as evidence that the remedy found the cancer or removed toxins.</p>

<p>Chemical burns, tissue death, and poisoning are visible too.</p>

<p>This is not a discussion of supplements with uncertain evidence or treatments built around a research hypothesis. Black salve, chlorine dioxide products, and swallowed hydrogen peroxide can cause direct physical injury. They can produce painful inflammation, vomiting, diarrhea, open wounds, and destruction of normal tissue. Pain does not become treatment because it was inflicted with the hope of helping an animal.</p>

<p>Many of the best-described cases involve people. That does not make these products safe for animals. Human reports tell us what a dog or cat cannot put into words: a chemical burn burns, an injured esophagus hurts with every swallow, an inflamed stomach causes nausea, cramping, and pain, and a necrotic wound can remain painful after the black tissue separates.</p>

<h2>Black salve and the tumor that “came out”</h2>

<p>Black salve is sold under names including bloodroot salve, drawing salve, and escharotic. It commonly contains bloodroot extract and zinc chloride. Its legend draws credibility from older corrosive pastes once used to destroy abnormal tissue, while photographs of blackened masses appear to show the result.</p>

<p>After the paste is applied, the area becomes inflamed and painful. Cells die and a dark, dry layer called an eschar forms. Days or weeks later, the dead tissue may separate, leaving a deep open wound. It can look exactly as if the salve recognized the tumor, killed it, and pulled it out by the roots.</p>

<p>What came away was chemically destroyed tissue. It may contain cancer cells, normal skin, fat, muscle, and blood vessels. The paste cannot see a microscopic tumor margin or stop when it reaches healthy tissue.</p>

<p>Australia's Therapeutic Goods Administration warns that black salve can destroy healthy skin and cause severe pain, scarring, and disfigurement. It also describes cases in which cancer remained after the apparent removal. The detached piece cannot show what remains beneath or around it, and it says nothing about cancer elsewhere in the body.</p>

<p>Black salve does not draw out cancer. It burns and kills the part of the body it touches. A mass turning black and falling away proves tissue necrosis, not successful cancer treatment.</p>

<h2>MMS and chlorine dioxide</h2>

<p>MMS, Miracle Mineral Solution, and similar products generate chlorine dioxide when their components are mixed. Chlorine dioxide is an oxidizing disinfectant. The legend begins with a true observation: outside the body, it can damage microorganisms and other organic material. That is why it has controlled industrial and water-treatment uses.</p>

<p>Inside an animal, it does not acquire the ability to identify malignant cells. The lining of the mouth, esophagus, stomach, and intestine is organic material too.</p>

<p>After ingestion, chlorine dioxide products can cause painful irritation, vomiting, diarrhea, and dehydration. Severe human poisonings have included dangerously low blood pressure, red-blood-cell injury, and acute liver failure. The US Food and Drug Administration states: “Drinking any of these chlorine dioxide products can cause nausea, vomiting, diarrhea, and symptoms of severe dehydration.”</p>

<p>Vomiting and diarrhea after MMS are not evidence of detoxification. They are the body's response to an irritating toxic substance. Calling that response a cleanse changes the word, not what the animal experiences.</p>

<p>A good day afterward does not establish that the product worked. Cancer symptoms fluctuate, supportive medication may begin working, and an animal may simply recover from the dose. The sequence “product, illness, improvement” can feel like a treatment response when an equally direct explanation is that the animal was injured and then partly recovered.</p>

<h2>Hydrogen peroxide and “oxygenating” cancer</h2>

<p>The peroxide story is built around an appealing idea: cancer cells supposedly dislike oxygen, so delivering more oxygen should kill them. Hydrogen peroxide does release oxygen as it breaks down. That does not mean swallowing it safely transports oxygen into a tumor.</p>

<p>Peroxide first contacts the mouth, esophagus, and stomach. It irritates those tissues and can cause painful gastritis, inflammation of the esophagus, repeated vomiting, erosions, ulcers, and bleeding. Concentrated peroxide causes corrosive chemical burns. Released gas can distend the stomach, and vomit entering the airways can injure the lungs.</p>

<p>In a narrow set of poisoning emergencies, a veterinarian may instruct an owner to give a measured amount of 3% hydrogen peroxide to make a dog vomit when safer options are not available. The <a href="https://www.merckvetmanual.com/toxicology/toxicology-introduction/principles-of-toxicosis-treatment-in-animals" rel="noopener">Merck Veterinary Manual</a> identifies it as a gastric irritant. That is how it causes vomiting. This exception does not apply to cats: hydrogen peroxide is not an acceptable home method for inducing vomiting in a cat.</p>

<p>Peroxide does not feel like extra oxygen to the animal. It feels like an irritating chemical. Foam, bubbles, and vomiting show that a chemical reaction occurred. They do not show that oxygen reached the tumor or damaged it selectively.</p>

<h2>Colloidal silver</h2>

<p>Silver is more confusing because it has legitimate medical uses. Silver-containing dressings and some topical veterinary products can help control microorganisms at a wound surface. Researchers also study defined silver compounds and nanoparticles for specific applications.</p>

<p>A manufactured dressing with a defined form, concentration, and purpose is not the same intervention as drinking colloidal silver. Silver is not an essential nutrient. With repeated exposure it can accumulate in tissues. Human medicine has documented argyria, a permanent blue-gray discoloration, and silver deposition in internal organs.</p>

<p>Veterinary evidence for oral colloidal silver is sparse. There is no established anticancer dose, demonstrated survival benefit, or reliable boundary between an ineffective exposure and toxicity in dogs or cats. The <a href="https://www.nccih.nih.gov/health/colloidal-silver-what-do-we-know" rel="noopener">National Center for Complementary and Integrative Health</a> says evidence supporting its health claims is lacking and notes that it can interfere with the absorption of some medicines.</p>

<p>The existence of medical silver dressings does not validate bottled silver as a systemic cancer treatment, just as the use of chlorine dioxide in water treatment does not make a disinfectant safe to drink.</p>

<h2>Baking soda and the alkaline cancer story</h2>

<p>The baking-soda story also begins with a real observation: many tumors have an acidic local microenvironment. From this comes the claim that alkalizing the body will make cancer unable to survive.</p>

<p>The environment immediately surrounding a tumor is not the same as the pH of the whole animal. Blood pH is held within a narrow range by the lungs and kidneys. Urine may become more alkaline after baking soda, but urine pH does not measure the pH inside a tumor.</p>

<p>If enough sodium bicarbonate is given to alter blood chemistry substantially, that is not a nutritional adjustment. It is a medical disturbance. Excessive intake can cause vomiting, weakness, intense thirst, high blood sodium, metabolic alkalosis, and neurologic abnormalities. The additional sodium load is also a concern in animals with heart or kidney disease.</p>

<p>Researchers study tumor acidity and ways of changing the tumor microenvironment. Dosing an animal with kitchen baking soda is not the same intervention.</p>

<h2>Why a better day proves so little</h2>

<p>Owners do not imagine every improvement. A dog or cat may genuinely eat, move, or interact better after something new was started. The mistake is not noticing the change. It is assigning its cause from timing alone.</p>

<p>Cancer symptoms fluctuate. Pain medication, steroids, fluids, changes in food, recovery from a procedure, and the natural course of disease may all be operating at the same time. Even a harmful product can happen to be followed by a good day.</p>

<p>The strongest illusion comes from a dramatic physical event. A black mass fell off, so the cancer came out. The animal vomited, so toxins left. A liquid foamed, so oxygen reached the tumor. These explanations match what an owner can see, but the visible event is usually the known effect of the chemical on ordinary tissue.</p>

<h2>This is direct harm</h2>

<p>Cancer treatment can also have serious adverse effects. The difference is that a known risk is accepted for a measurable chance of benefit, monitored with examinations and tests, and treated with efforts to prevent or relieve pain and toxicity. With black salve, chlorine dioxide products, and swallowed peroxide, injury can occur immediately, while no anticancer benefit has been demonstrated in dogs or cats.</p>

<p>A dog or cat does not understand the theory used to explain the procedure. The animal feels the chemical burn, the open wound, the inflamed lining of the digestive tract, the abdominal cramping, nausea, and vomiting. The animal cannot refuse and cannot say, “Stop.”</p>

<p>An owner can make a mistake while desperately trying to save an animal. Once it is clear that a product burns tissue or poisons the body, continuing to use it cannot be defended as one more chance.</p>

<p><strong>If the evidence that a remedy is “working” is a burn, necrosis, vomiting, or diarrhea, it is not treating cancer. It is causing direct harm to the animal.</strong></p>

<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 20, 2026</p><p><strong>Last updated:</strong> September 20, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and an owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance, and information from veterinary hospitals and public health agencies.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>

<h2>Sources</h2>
<ul class="article-sources">
<li><a href="https://www.tga.gov.au/news/safety-alerts/black-salve-red-salve-and-cansemma" rel="noopener">Therapeutic Goods Administration. Black salve, red salve and Cansema</a>.</li>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC5299188/" rel="noopener">Croaker A, et al. A review of black salve: cancer specificity, cure, and cosmesis</a>. 2017.</li>
<li><a href="https://www.fda.gov/consumers/consumer-updates/danger-dont-drink-miracle-mineral-solution-or-similar-products" rel="noopener">US Food and Drug Administration. Danger: Don’t Drink Miracle Mineral Solution or Similar Products</a>.</li>
<li><a href="https://www.merckvetmanual.com/toxicology/toxicology-introduction/principles-of-toxicosis-treatment-in-animals" rel="noopener">Merck Veterinary Manual. Principles of Toxicosis Treatment in Animals</a>.</li>
<li><a href="https://www.nccih.nih.gov/health/colloidal-silver-what-do-we-know" rel="noopener">National Center for Complementary and Integrative Health. Colloidal Silver: What Do We Know?</a>.</li>
<li><a href="https://vcahospitals.com/know-your-pet/colloidal-silver" rel="noopener">VCA Animal Hospitals. Colloidal Silver</a>.</li>
</ul>
</article>'''

    directory = root / 'articles' / 'when-cancer-remedies-cause-harm'
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(
        'When a cancer remedy causes visible harm | Vet Trial Finder',
        'How black salve, chlorine dioxide, swallowed peroxide, colloidal silver, and baking soda can injure dogs and cats while creating the appearance of cancer treatment.',
        body,
        url,
    )
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="When a cancer remedy causes visible harm"><meta property="og:description" content="Why burns, necrosis, vomiting, and diarrhea are evidence of injury, not proof that cancer is being treated."><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="When a cancer remedy causes visible harm"><meta name="twitter:description" content="Why visible tissue damage is not proof of cancer treatment.">'''
    rendered = rendered.replace('</head>', social + '</head>', 1)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': 'When a cancer remedy causes visible harm',
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
        raise AssertionError('Articles index is required before adding the harmful-remedies article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = f'''<a class="directory-card" href="{url}"><strong>When a cancer remedy causes visible harm</strong><span>Why burns, necrosis, vomiting, and diarrhea are evidence of injury, not proof that cancer is being treated.</span></a>'''
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
        '<h1>When a cancer remedy causes visible harm</h1>',
        'Black salve does not draw out cancer',
        'This exception does not apply to cats',
        'This is direct harm',
        'causing direct harm to the animal',
        'Reviewed and edited by:',
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in required if marker not in article]
    if missing:
        raise AssertionError(f'Harmful-remedies article validation failed: {missing}')


def main() -> None:
    generate_dangerous_cancer_remedies_article(Path(__file__).resolve().parent / 'site')


if __name__ == '__main__':
    main()
