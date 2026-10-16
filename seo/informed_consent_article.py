#!/usr/bin/env python3
"""Generate the owner-focused article on informed consent in cancer trials."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

SLUG = "informed-consent-veterinary-cancer-trials"
URL = f"{SITE}/articles/{SLUG}/"
IMAGE = f"{SITE}/assets/social/clinical-trial-consent.jpg"


def generate_informed_consent_article(root: Path) -> None:
    title = "Consent to a cancer clinical trial: what owners should understand"
    description = "An owner-focused look at public veterinary cancer trial consent forms: risks, complication costs, withdrawal, restrictions on public accounts and new safety information."
    assets = root / "assets" / "social"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(__file__).resolve().parent / "assets" / "social" / "clinical-trial-consent.jpg", assets / "clinical-trial-consent.jpg")
    body = f'''<article class="article-page">
<h1>{title}</h1>
<figure style="margin:18px 0 24px"><img src="{IMAGE}" alt="Illustration of a fictional unsigned clinical trial consent form with sections for possible benefits, risks, costs and withdrawal" width="1536" height="1024" style="display:block;width:100%;height:auto;border-radius:12px"></figure>
<p>The starting point for this article was a cancer study reporting that two of its 17 dogs had died. I could not stop thinking about their owners. Were they prepared for that outcome? Did they understand, before enrolling, that they might lose their dog during the study?</p>
<p>That is how this analysis began: I wanted to look at how publicly available consent forms explain the risks and conditions of participation, and what someone looking for a chance to help their animal can understand from those documents.</p>
<p>An owner considering a clinical trial for a dog or cat with cancer is looking for a way to help their animal. The research team is testing a treatment whose outcome has not yet been established. These goals may align, but participation does not guarantee a benefit for an individual patient. Before signing, owners need to understand the possible outcome, risks, costs and conditions for leaving the study.</p>
<p>We read several publicly available consent forms for veterinary cancer studies. They include a document from a program currently accepting applications and earlier forms whose use in current recruitment has not been confirmed. This is a small sample for examining how information is presented. The documents cannot establish how the conversation with the veterinarian went or what each owner ultimately understood. Even in this sample, however, there are noticeable differences in how participation is explained.</p>
<p>The public consent form for the EGFR/HER2 vaccine study, developed by Yale researchers and offered through Veterinary Cancer Concierge Services (VCCS), explicitly states that safety and effectiveness are not fully known. It mentions possible severe reactions and death, and says that an individual dog may receive no medical benefit.</p>
<p>At the same time, the introduction describes longer survival in some dogs with little to no side effects. The risk section begins by saying that adverse side effects are not anticipated. A sterile abscess at the injection site, reported in about 20% of patients, is described as an encouraging sign of an immune response. The warning about unknown severe complications comes later. In my view, that sequence may leave a more reassuring impression than the uncertainty of the treatment warrants. The risk is stated, but how it is presented matters too.</p>
<p>Another example is Wisconsin's consent form for a study combining Laverdia and lomustine. Its specificity is useful: it lists side effects and gives the days for blood tests and temperature checks, including one week after each lomustine dose. Owners can use that information to plan their animal's care.</p>
<p>But the terms neutropenia and thrombocytopenia appear without definitions. Owners need their ordinary meaning: a reduction in neutrophils, cells that help protect against infection, and a reduction in platelets, which help blood clot. A list of medical terms is more useful when the document explains what those changes mean for the animal and what action will be needed.</p>
<p>Wisconsin's COTC031 consent form, dated April 11, 2024, describes the uncertainty of experimental 45H1 immunotherapy more directly. It separately lists the consequences of cancer progression, drug toxicity and complications of research procedures. Sepsis and death are among the drug risks. The benefit to the dog is described as unknown, and owners are instructed to report even one episode of vomiting, diarrhea, decreased appetite or lethargy immediately.</p>
<p>The same form contains conditions that may materially affect a family's decision. Treatment of complications, including unanticipated hospitalization, is covered up to $2,000 per event. Leaving early means foregoing further financial support. An unexpected death while the animal is on study requires a post-mortem examination.</p>
<p>The statement that an owner can leave at any time does not, by itself, explain every consequence of leaving. Coverage for complications may also have a limit.</p>
<p>The consequences of participation ending can be seen in Rufio's story, posted by his owner Kristie on the Tripawds forum in February 2017. After amputation and six rounds of chemotherapy, her dog with osteosarcoma developed lung metastases. Kristie wrote that she could not afford Palladia herself, so a study combining Palladia and losartan at Colorado State University gave them a way to continue treatment.</p>
<p>According to her account, she was told at the January examination that his disease was stable. In February, she learned that the previous assessment had been wrong: the metastases were continuing to grow, and Rufio no longer met the conditions for continuing in the study. Kristie described anger and helplessness. Her dog remained active and appeared well, but the treatment opportunity she had relied on had ended. She later wrote that she had discussed the situation and another chemotherapy option with the oncologist.</p>
<p>This is an owner's account of cancer progression and participation ending, rather than an established case of death caused by experimental treatment. It illustrates another aspect of informed consent: before enrollment, a family needs to understand when treatment will stop, how examination results will be explained and what care plan will remain afterward.</p>
<p>A different public Wisconsin form, for a separate verdinexor lymphoma study, contains a restriction on public accounts. Owners acknowledge that they will not mention the trial, sponsor or drug name in media or on social media, including Facebook. The clause itself gives no duration, explanation or exception for describing complications. Its use in current recruitment has not been confirmed.</p>
<p>One document cannot establish how widespread such restrictions are. But the clause deserves attention. Protecting unpublished research data and restricting an owner's account of their dog's condition have different consequences. In my view, if a study includes such a condition, owners should receive a clear explanation of its boundaries, including whether they can describe a severe complication or their animal's death.</p>
<p>Another question arises after signing: how will owners be notified if new risk information emerges? In the four treatment-study forms we read, we did not find a separate promise of such notification. A 2024 review by a Cornell clinical trials specialist recommends timely disclosure of significant new findings to owners, including unexpected complications, an increased frequency of adverse events or evidence of a lack of effectiveness.</p>
<p>Clinical trials are needed. They help advance veterinary oncology and sometimes give an animal access to treatment that would otherwise be unavailable. Standard treatment carries risks too, and some risks of experimental treatment are still unknown. A serious outcome does not, by itself, mean that a study should not have taken place.</p>
<p>But my position is clear: owners should understand exactly what they are agreeing to. Possible benefits, uncertainty, the risk of severe complications and death, financial obligations and the consequences of participation ending should be explained in plain language before consent is signed. If significant new information emerges, families should be told and have an opportunity to reconsider their decision.</p>
<p>And owners should have the right to speak about what they have been through, including disappointment, complications and the death of their animal. They have the right to grieve in public too. Consent to participate in research should not become consent to stay silent about their loss.</p>
<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> October 3, 2026</p><p><strong>Last updated:</strong> October 3, 2026</p></div>
<h2>Sources</h2>
<ul class="article-sources">
<li><a href="https://vetcancerconcierge.com/client-consent-form/" target="_blank" rel="noopener">VCCS: public EGFR/HER2 vaccine consent form</a>; <a href="https://vetcancerconcierge.com/clinical-trials/" target="_blank" rel="noopener">enrollment information</a>.</li>
<li><a href="https://uwveterinarycare.wisc.edu/wp-content/uploads/2024/08/Naive-Laverdia-CCNU-Consent.pdf" target="_blank" rel="noopener">UW Veterinary Care: Laverdia and lomustine owner consent form</a>.</li>
<li><a href="https://uwveterinarycare.wisc.edu/wp-content/uploads/2024/05/COTC031-Consent-Form.pdf" target="_blank" rel="noopener">UW Veterinary Care: COTC031 owner consent form, April 11, 2024</a>.</li>
<li><a href="https://tripawds.com/forums/treatment-and-recovery/when-chemo-palladia-dont-work/" target="_blank" rel="noopener">Tripawds: Kristie's account of Rufio's treatment, February 2017</a>.</li>
<li><a href="https://uwveterinarycare.wisc.edu/wp-content/uploads/2022/07/Verdinexor-consent-form.pdf" target="_blank" rel="noopener">UW Veterinary Care: separate verdinexor study consent form</a>.</li>
<li><a href="https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2024.1426014/full" target="_blank" rel="noopener">Frederick CE (2024): Obtaining informed consent in veterinary clinical trials mini review</a>.</li>
</ul>
</article>'''
    directory = root / "articles" / SLUG
    directory.mkdir(parents=True, exist_ok=True)
    rendered = g.page(f"{title} | Vet Trial Finder", description, body, URL)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="{g.esc(title)}"><meta property="og:description" content="{g.esc(description)}"><meta property="og:url" content="{URL}"><meta property="og:image" content="{IMAGE}"><meta property="og:image:secure_url" content="{IMAGE}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:alt" content="Illustration of a fictional unsigned clinical trial consent form"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{g.esc(title)}"><meta name="twitter:description" content="{g.esc(description)}"><meta name="twitter:image" content="{IMAGE}">'''
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": title, "image": [IMAGE], "datePublished": "2026-10-03", "dateModified": "2026-10-03", "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"}, "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"}, "mainEntityOfPage": URL}
    rendered = rendered.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (directory / "index.html").write_text(wrap_html(rendered), encoding="utf-8")
    index = root / "articles" / "index.html"
    index_text = index.read_text(encoding="utf-8")
    if URL not in index_text:
        card = f'<a class="directory-card" href="{URL}"><strong>{title}</strong><span>How trial consent forms explain risks, complication costs, withdrawal and restrictions on public accounts.</span></a>'
        index.write_text(index_text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1), encoding="utf-8")
    sitemap = root / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    if URL not in text:
        sitemap.write_text(text.replace("</urlset>", f"<url><loc>{URL}</loc></url>\n</urlset>"), encoding="utf-8")


if __name__ == "__main__":
    generate_informed_consent_article(Path(__file__).resolve().parent / "site")
