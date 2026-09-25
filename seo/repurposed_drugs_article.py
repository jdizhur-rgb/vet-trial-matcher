#!/usr/bin/env python3
"""Generate the owner-facing article about repurposed drugs for canine cancer."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html


def generate_repurposed_drugs_article(root: Path) -> None:
    url = f"{SITE}/articles/fenbendazole-ivermectin-dogs-with-cancer/"
    body = f'''<article class="article-page">
<h1>Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer</h1>

<p>When a dog is diagnosed with cancer, searching for another option is a natural response. Owners read PubMed, learn the vocabulary, compare protocols, and look closely at every good day. Fenbendazole and ivermectin did not appear in these discussions from nowhere. Both have attracted real scientific interest. The difficult part is deciding what that interest means for one particular dog.</p>

<h2>Why the conversation changed in 2025 and 2026</h2>

<p>The recent attention is not simply recycled social-media speculation. In 2025 and 2026, new laboratory studies appeared, an early human trial tested ivermectin together with immunotherapy, and the U.S. National Cancer Institute confirmed that it had examined ivermectin in a more rigorous preclinical study. The American Cancer Society published patient guides on both drugs, and the American Society of Clinical Oncology issued a formal clinical notice after oncologists reported seeing growing interest among patients.</p>

<p>The public response moved even faster. A celebrity claim on a major podcast was followed by a measurable rise in ivermectin and benzimidazole prescribing among people with cancer. A widely shared three-patient fenbendazole case series was published in 2025 and retracted in 2026 because of an undisclosed conflict of interest. BBC reporting then documented unproven products being sold directly to cancer patients.</p>

<p>All of this shows that the scientific question is active and the demand is real. It does not establish a safe or effective cancer protocol for dogs. Human studies of a specific drug, cancer, dose, and combination cannot supply the missing canine evidence, but they do explain why owners are encountering more research headlines and more confident claims than they did only a few years ago.</p>

<h2>One drug and many different cancers</h2>

<p>Cancer is not one disease. Lymphoma, osteosarcoma, melanoma, and mammary carcinoma involve different cells, mutations, behavior, and treatment responses. We would not treat pneumonia with an asthma medicine simply because both diseases affect the lungs. In the same way, a substance that affects one cancer model cannot automatically be expected to treat every tumor.</p>

<p>Repurposing existing drugs is a legitimate area of research. It starts with a plausible mechanism, then asks quantitative questions: can a useful concentration reach the tumor, is it safe, which cancer might respond, and does it improve outcomes in living patients? A mechanism is the beginning of that process, not the finished protocol.</p>

<h2>Fenbendazole</h2>

<p>Fenbendazole is an antiparasitic drug. Laboratory studies and animal models suggest several possible anticancer effects, including interference with cell division and tumor metabolism. That is enough to justify further study. It does not yet establish an effective cancer dose, schedule, or target diagnosis in dogs.</p>

<p>A 2024 scientific review described the experimental findings as promising and called for clinical trials to determine anticancer effects, dosing, treatment schedules, and tolerability. In other words, the question is being studied; the practical answers needed for routine cancer treatment are still missing.</p>

<h2>What owners have reported</h2>

<p>In 2026, researchers published a survey of 87 owners who had given fenbendazole to dogs with cancer for at least three months. About four in ten said their dog lived longer than the prognosis they had been given, and many perceived an improvement in quality of life.</p>

<p>Those experiences matter, and the study authors concluded that they justify a systematic evaluation of fenbendazole. The survey cannot tell us whether fenbendazole caused the reported outcomes. Owners were recruited through social media, the diagnoses and outcomes were self-reported, most dogs also received supplements, many had diet changes, and some received standard cancer treatment. Twenty-one percent of owners did not know the exact cancer diagnosis, and more than a third had not been given a prognosis to compare against. As the authors wrote, the benefit in companion animals “has yet to be established.”</p>

<p>The same distinction applies to safety. Most owners in this small survey reported no serious problem, while gastrointestinal signs were reported in about one dog in ten. Separately, the U.S. Food and Drug Administration has received reports of bone-marrow suppression and pancytopenia in dogs given fenbendazole for longer than its labeled three-day course. Reports do not reveal how often this happens, but they show why an over-the-counter dewormer should not be treated as risk-free when used repeatedly or off label.</p>

<h2>Why a home protocol can always appear to work</h2>

<p>A dog has a good day: the protocol is working. The dog is stable: it is holding the cancer back. The tumor grows: toxins are leaving, the dose was too low, or the treatment needs more time. The dog deteriorates: it was started too late.</p>

<p>This does not mean owners are foolish. It means an uncontrolled personal experiment has no neutral result. Almost any change can be fitted into the story after it happens. Steroids may improve appetite and energy within days. Pain relief can restore walks and sleep. Surgery, chemotherapy, radiation, diet changes, supplements, and the natural rise and fall of symptoms may all occur at the same time. A good day is real and valuable. By itself, it cannot identify which part of a ten-item protocol produced it or whether the tumor changed.</p>

<h2>Ivermectin</h2>

<p>Ivermectin also has genuine laboratory research behind it. It has affected canine mammary-tumor cells in culture and slowed tumors grown from those cells in mice. Researchers have also explored whether it might alter drug resistance. These are useful leads, not evidence that ivermectin treats cancer in dogs at a safe home dose.</p>

<p>Asked about ivermectin for dogs with lymphoma, veterinary oncologist Dr. Brooke Britton put the clinical gap plainly: “We don’t have any data to support using it in dogs with lymphoma.” That sentence does not dismiss the laboratory work. It says that a mechanism found in one model cannot supply the missing dose, safety, and outcome data for a different cancer in a living dog.</p>

<p>Ivermectin has an additional complication: dogs with certain variants of the <em>ABCB1</em> gene, often called MDR1, can be unusually sensitive to neurological toxicity. A negative genetic test does not prove that an untested anticancer dose or drug combination is safe.</p>

<h2>When one extra chance becomes ten drugs</h2>

<p>Internet protocols rarely remain one-drug experiments. Fenbendazole may be combined with ivermectin, CBD, turmeric or curcumin, mushroom extracts, vitamins, antioxidants, and several other products. Each addition has its own absorption, metabolism, and adverse effects. The combination usually has not been studied at all.</p>

<p>If the dog feels better, there is no way to know what helped. If vomiting, weakness, poor appetite, liver abnormalities, or falling blood-cell counts appear, there is no way to know what caused them. Adding more components may feel like increasing the chance of success. It also removes the ability to read the experiment.</p>

<h2>If you decide to try anyway</h2>

<p>Some owners will choose an experimental add-on after understanding the uncertainty. In that situation, the most useful goal is not to reproduce a social-media protocol perfectly. It is to preserve enough information and enough safety margin to stop before the experiment takes away good days.</p>

<p>Do not begin several new drugs or supplements at once. Make a complete list of everything the dog receives, including nonprescription products, and show it to the treating veterinarian or pharmacist. Record the confirmed diagnosis, current tumor measurements, medications, appetite, weight, activity, symptoms, and laboratory results before the change. Agree in advance which adverse signs or objective changes mean stop and seek care.</p>

<p>For ivermectin, discuss <em>ABCB1/MDR1</em> testing and all interacting medicines. For prolonged or repeated off-label fenbendazole use, ask whether blood counts and liver-related bloodwork should be monitored. Normal tests can help detect some toxicity; they do not demonstrate that the treatment is controlling cancer.</p>

<p>Repeated vomiting, refusal to eat, marked weakness, unusual sleepiness, tremors, loss of coordination, seizures, or major changes in bloodwork are not signs that the body is “detoxing.” Stop a self-administered product and contact a veterinarian urgently.</p>

<h2>What a veterinarian can and cannot do</h2>

<p>A veterinarian may not be able to endorse an untested cancer protocol or calculate a proven anticancer dose when no such dose exists. That is not the same as refusing to help. A clinician can check the diagnosis, look for interactions, establish baseline measurements, monitor for toxicity, treat pain and nausea, and define what would count as progression.</p>

<p>Bring the actual paper and the actual product, not only a screenshot of the protocol. A useful question is: “If we add this, what can we measure, what could it interact with, and what would make us stop?”</p>

<h2>What remains true</h2>

<p>Searching is not the mistake. Hope is not the mistake. The danger is a system in which every good day proves success and every bad day creates a reason to add another drug.</p>

<p>If you go down this path, keep the hypothesis narrow, the record honest, and the exit clearly marked. A protocol should have to earn your confidence with measurements. Your dog should not have to earn the right to stop it by becoming desperately ill.</p>

<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 20, 2026</p><p><strong>Last updated:</strong> September 20, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and a dog owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance and information from veterinary hospitals and research teams.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>

<h2>Sources</h2>
<ul class="article-sources">
<li><a href="https://pubmed.ncbi.nlm.nih.gov/39197912/" rel="noopener">Nguyen J, et al. Oral Fenbendazole for Cancer Therapy in Humans and Animals</a>. Anticancer Research. 2024.</li>
<li><a href="https://www.ahvma.org/journal/kmeb8015/" rel="noopener">Kim J, et al. Potential of Fenbendazole in Canine Cancer: Pet Owner Experiences</a>. Journal of the American Holistic Veterinary Medical Association. 2026.</li>
<li><a href="https://www.fda.gov/animal-veterinary/product-safety-information/dear-veterinarian-letter-regarding-adverse-events-associated-extra-label-use-fenbendazole-dogs" rel="noopener">U.S. FDA. Dear Veterinarian Letter regarding adverse events associated with extra-label use of fenbendazole in dogs</a>. 2023.</li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/31375107/" rel="noopener">Diao H, et al. Ivermectin inhibits canine mammary tumor growth by regulating cell cycle progression and WNT signaling</a>. BMC Veterinary Research. 2019.</li>
<li><a href="https://www.dogcancer.com/podcast/supplements/ivermectin-for-dogs-with-lymphoma-dr-brooke-britton-qa/" rel="noopener">Britton B. Ivermectin for Dogs with Lymphoma</a>. Dog Cancer Answers.</li>
<li><a href="https://prime.vetmed.wsu.edu/2022/03/01/problem-medications-for-dogs/" rel="noopener">Washington State University College of Veterinary Medicine. Problem medications for dogs</a>. 2022.</li>
<li><a href="https://www.uclahealth.org/news/release/ivermectin-prescriptions-more-doubled-after-celebrity" rel="noopener">UCLA Health. Ivermectin prescriptions more than doubled after a celebrity endorsed it as a cancer treatment</a>. 2026.</li>
<li><a href="https://kffhealthnews.org/health-industry/ivermectin-cancer-treatment-nih-study-dewormer-offlabel-drug/" rel="noopener">KFF Health News. US Cancer Institute Studying Ivermectin’s “Ability To Kill Cancer Cells”</a>. 2026.</li>
<li><a href="https://connection.asco.org/do/asco-clinical-notice-recommending-against-ivermectin-and-fenbendazole-cancer-treatment" rel="noopener">American Society of Clinical Oncology. Clinical Notice on ivermectin and fenbendazole for cancer treatment</a>. 2026.</li>
<li><a href="https://karger.com/cro/article/19/1/169/941881/Retraction-StatementPaper-by-William-Makis-Ilyes" rel="noopener">Karger. Retraction statement for the 2025 fenbendazole case series</a>. 2026.</li>
</ul>
</article>'''

    directory = root / 'articles' / 'fenbendazole-ivermectin-dogs-with-cancer'
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(
        'Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer | Vet Trial Finder',
        'What the evidence does and does not show about fenbendazole, ivermectin, and home cancer protocols for dogs, including practical safety considerations.',
        body,
        url,
    )
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer"><meta property="og:description" content="What the evidence shows, why personal protocols are hard to interpret, and how to reduce avoidable risk."><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer"><meta name="twitter:description" content="What the evidence shows, why personal protocols are hard to interpret, and how to reduce avoidable risk.">'''
    rendered = rendered.replace('</head>', social + '</head>', 1)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': 'Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer',
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
        raise AssertionError('Articles index is required before adding the repurposed-drugs article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = f'''<a class="directory-card" href="{url}"><strong>Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer</strong><span>What the evidence shows, why personal protocols are hard to interpret, and how to reduce avoidable risk.</span></a>'''
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
        '<h1 class="page-title">Fenbendazole, ivermectin, and repurposed drugs for dogs with cancer</h1>',
        'About four in ten',
        'Why the conversation changed in 2025 and 2026',
        'has yet to be established',
        'Why a home protocol can always appear to work',
        'We don’t have any data to support using it in dogs with lymphoma',
        'Reviewed and edited by:',
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in required if marker not in article]
    if missing:
        raise AssertionError(f'Repurposed-drugs article validation failed: {missing}')


def main() -> None:
    generate_repurposed_drugs_article(Path(__file__).resolve().parent / 'site')


if __name__ == '__main__':
    main()
