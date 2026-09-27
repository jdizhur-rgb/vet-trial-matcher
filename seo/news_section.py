#!/usr/bin/env python3
"""Generate the Vet Trial Finder news index and current trial updates."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

NEWS_URL = f"{SITE}/news/"
MATCHER_URL = f"{SITE}/matcher/"
CORNELL_URL = f"{NEWS_URL}cornell-smart-start-b-cell-lymphoma/"
NC_STATE_URL = f"{NEWS_URL}nc-state-il12-bladder-cancer-deadline/"
WISCONSIN_URL = f"{NEWS_URL}wisconsin-ptcl-radiopharmaceutical-trial/"
PURDUE_URL = f"{NEWS_URL}purdue-three-cancer-treatment-trials/"
TAIWAN_IL15_URL = f"{NEWS_URL}taiwan-inhaled-il15-lung-metastases/"
BARC_TRIALS_URL = f"{NEWS_URL}barc-dog-cat-cancer-trials/"
CORNELL_OFFICIAL = "https://www.vet.cornell.edu/hospitals/clinical-trials/smart-start-therapy-canine-b-cell-lymphoma"
NC_STATE_OFFICIAL = "https://cvm.ncsu.edu/clinical-trial/now-enrolling-dogs-with-invasive-bladder-cancer/"
WISCONSIN_OFFICIAL = "https://uwveterinarycare.wisc.edu/veterinary-clinical-studies/oncology/"
PURDUE_ABLATION_OFFICIAL = "https://vet.purdue.edu/wcorc/clinical-trials/tumor-ablation.php"
TAIWAN_IL15_OFFICIAL = "https://www.egah.com.tw/news/%E6%8B%9B%E5%8B%9F%E7%8A%AC%E9%BB%91%E8%89%B2%E7%B4%A0%E7%98%A4%E5%8F%8A%E9%AA%A8%E8%82%89%E7%98%A4%E8%87%A8%E5%BA%8A%E8%A9%A6%E9%A9%97"
TAIWAN_IL15_PHASE1 = "https://jitc.bmj.com/content/10/6/e004493"
TAIWAN_IL15_PHASE2 = "https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2025.1672790/full"
BARC_TRIALS_OFFICIAL = "https://www.barcseattle.com/clinical-trials-index"
PURDUE_SOCIAL_IMAGE = f"{SITE}/assets/social/purdue-ablation-1200x630.jpg"
BARC_ARTICLE_IMAGE = f"{SITE}/assets/social/barc-dog-cat-cancer-trials.jpg"
BARC_SOCIAL_IMAGE = f"{SITE}/assets/social/barc-dog-cat-cancer-trials-square-safe.jpg"


def add_to_sitemap(root: Path, urls: tuple[str, ...]) -> None:
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        raise AssertionError("Sitemap is required before generating news")
    text = sitemap.read_text(encoding="utf-8")
    for url in urls:
        if url not in text:
            text = text.replace("</urlset>", f"<url><loc>{g.esc(url)}</loc></url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def write_article(root: Path, slug: str, title: str, description: str, body: str, source_name: str, published: str = "September 17, 2026", published_iso: str = "2026-09-17", social_image: str | None = None, social_image_size: tuple[int, int] = (1200, 630)) -> None:
    url = f"{NEWS_URL}{slug}/"
    article_dir = root / "news" / slug
    article_dir.mkdir(parents=True, exist_ok=True)
    byline = f'''<div class="article-byline"><p><strong>Published:</strong> {published}</p><p><strong>Recruitment status checked:</strong> {published}</p><p><strong>Source:</strong> {source_name}.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance and reviewed by Yuliia Dizhur. Trial eligibility and enrollment decisions are made by the study team.</p></div>'''
    page = g.page(f"{title} | Vet Trial Finder", description, f'<article class="article-page news-article">{body}{byline}</article>', url)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="{g.esc(title)}"><meta property="og:description" content="{g.esc(description)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="{'summary_large_image' if social_image else 'summary'}"><meta name="twitter:title" content="{g.esc(title)}"><meta name="twitter:description" content="{g.esc(description)}">'''
    if social_image:
        social += f'<meta property="og:image" content="{g.esc(social_image)}"><meta property="og:image:width" content="{social_image_size[0]}"><meta property="og:image:height" content="{social_image_size[1]}"><meta property="og:image:alt" content="Vet Trial Finder news cover"><meta name="twitter:image" content="{g.esc(social_image)}">'
    schema = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": title, "datePublished": published_iso, "dateModified": published_iso, "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"}, "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"}, "mainEntityOfPage": url}
    page = page.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (article_dir / "index.html").write_text(wrap_html(page), encoding="utf-8")


def generate_news_section(root: Path) -> None:
    source_assets = Path(__file__).resolve().parent / "assets" / "social"
    built_assets = root / "assets" / "social"
    built_assets.mkdir(parents=True, exist_ok=True)
    for name in ("purdue-ablation-1200x630.jpg", "purdue-ablation-story-1080x1920.jpg", "barc-dog-cat-cancer-trials.jpg", "barc-dog-cat-cancer-trials-square-safe.jpg"):
        shutil.copy2(source_assets / name, built_assets / name)
    index_body = f'''<div class="registry-page news-index">
<h1>Veterinary oncology news</h1>
<p class="lead">Newly opened treatment trials, meaningful recruitment changes and other developments that may matter to owners looking for cancer treatment options.</p>
<div class="directory-grid">
<a class="directory-card" href="{BARC_TRIALS_URL}"><strong>BARC is recruiting dogs and cats for cancer treatment trials</strong><span>September 27, 2026. Gold nanoparticle treatment includes selected dog and cat tumors; two other recruiting studies are for dogs.</span></a>
<a class="directory-card" href="{TAIWAN_IL15_URL}"><strong>Taiwan trial tests inhaled IL-15 for canine lung metastases</strong><span>September 25, 2026. A rare non-US study builds on mixed published evidence in dogs with melanoma or osteosarcoma.</span></a>
<a class="directory-card" href="{PURDUE_URL}"><strong>Purdue adds experimental tumor ablation to standard cancer treatment in three trials</strong><span>September 20, 2026. Standard treatment remains in place and part of the care is study-funded; additional clinical benefit from HIFU or H-FIRE has not been established.</span></a>
<a class="directory-card" href="{NC_STATE_URL}"><strong>NC State bladder cancer immunotherapy trial closes enrollment September 30</strong><span>September 17, 2026. The fully funded eight-day IL-12 treatment study has no placebo group.</span></a>
<a class="directory-card" href="{WISCONSIN_URL}"><strong>Wisconsin recruits dogs with peripheral T-cell lymphoma for 90Y-NM600 therapy</strong><span>September 17, 2026. All enrolled dogs receive targeted radiopharmaceutical therapy; most study costs are covered after screening.</span></a>
<a class="directory-card" href="{CORNELL_URL}"><strong>Cornell opens Smart-Start trial for dogs with B-cell lymphoma</strong><span>September 17, 2026. A biology-guided pre-treatment is followed by standard CHOP chemotherapy; there is no placebo.</span></a>
</div></div>'''
    index_dir = root / "news"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_page = g.page("Veterinary Oncology News | Vet Trial Finder", "New veterinary cancer treatment trials, recruitment changes and other oncology developments for dogs and cats.", index_body, NEWS_URL)
    (index_dir / "index.html").write_text(wrap_html(index_page), encoding="utf-8")

    cornell_body = f'''<p class="eyebrow">Trial opening · September 17, 2026</p>
<h1>Cornell opens Smart-Start trial for dogs with B-cell lymphoma</h1>
<p>Cornell University Hospital for Animals has opened enrollment in a new treatment study for dogs with B-cell lymphoma. Smart-Start is not a sample-collection or observational study. Every enrolled dog receives an anticancer pre-treatment selected according to the biology of that dog’s tumor, followed by standard CHOP chemotherapy.</p>
<p>The pre-treatment is either an oral drug given four times over a 14-day period or an injectable drug given at Cornell on five consecutive days. There is no placebo. After the pre-treatment period, dogs return for routine CHOP chemotherapy visits.</p>
<h2>Who may qualify</h2><p>The study is for dogs diagnosed with B-cell lymphoma that are seen by Cornell’s oncology service in Ithaca, New York. Dogs must not have received previous lymphoma treatment other than prednisolone, and owners must be willing to proceed with standard-of-care CHOP chemotherapy.</p>
<h2>What the study covers</h2><p>Tests and procedures performed specifically for the study are covered. Owners remain responsible for ordinary clinical care, but Cornell provides a 10% discount on standard-of-care chemotherapy visits and an additional $1,000 toward chemotherapy costs.</p>
<p>Owners can contact Cornell Oncology or the Clinical Trials Coordinator at 607-253-3060 or <a href="mailto:vet-research@cornell.edu">vet-research@cornell.edu</a>.</p>
<div class="article-cta"><a href="{CORNELL_OFFICIAL}" target="_blank" rel="noopener">Read the official Cornell trial page</a></div><p><a href="{MATCHER_URL}">Check this and other current cancer treatment trials in Vet Trial Finder</a></p>'''
    write_article(root, "cornell-smart-start-b-cell-lymphoma", "Cornell opens Smart-Start trial for dogs with B-cell lymphoma", "Cornell has opened enrollment in a treatment trial for dogs with B-cell lymphoma using a biology-guided pre-treatment followed by CHOP chemotherapy.", cornell_body, "Cornell University College of Veterinary Medicine")

    nc_state_body = f'''<p class="eyebrow">Enrollment deadline · September 30, 2026</p>
<h1>NC State bladder cancer immunotherapy trial closes enrollment September 30</h1>
<p>NC State is still recruiting dogs with invasive urothelial carcinoma, also called transitional cell carcinoma, for an experimental IL-12 immunotherapy study. The official enrollment window ends September 30, 2026, so owners interested in screening have little time left to contact the study team.</p>
<p>The study lasts eight days, from Monday through the following Monday. Dogs receive the bladder immunotherapy under general anesthesia on day 1, remain hospitalized through day 3, and return for outpatient checks on days 4 and 8. There is no placebo group. Every enrolled dog receives the immunotherapy, and some dogs may be able to enroll again for additional doses.</p>
<h2>Who may qualify</h2><p>Dogs must weigh at least 8 kg (17.6 lb) and have muscle-invasive bladder urothelial carcinoma confirmed by cytology with a BRAF test or by biopsy. Metastatic disease is allowed. Dogs may be untreated or previously treated, but at least one month must have passed since radiation or chemotherapy. Other immunotherapy and prednisone are not allowed during enrollment.</p>
<h2>What the study covers</h2><p>Pre-staging, IL-12 treatment and study monitoring are provided at no cost. Coverage includes specified blood and urine testing, focused urinary-tract ultrasound, hospitalization, anesthesia and repeat bloodwork.</p>
<div class="article-cta"><a href="{NC_STATE_OFFICIAL}" target="_blank" rel="noopener">Read the official NC State trial page</a></div><p><a href="{MATCHER_URL}">Check current bladder cancer trials in Vet Trial Finder</a></p>'''
    write_article(root, "nc-state-il12-bladder-cancer-deadline", "NC State bladder cancer immunotherapy trial closes enrollment September 30", "NC State's fully funded IL-12 immunotherapy study for dogs with invasive bladder cancer is scheduled to close enrollment September 30, 2026.", nc_state_body, "NC State College of Veterinary Medicine")

    wisconsin_body = f'''<p class="eyebrow">New treatment trial · September 17, 2026</p>
<h1>Wisconsin recruits dogs with peripheral T-cell lymphoma for 90Y-NM600 therapy</h1>
<p>UW Veterinary Care is recruiting dogs with peripheral T-cell lymphoma for a dose-finding study of 90Y-NM600 targeted radiopharmaceutical therapy. NM600 is designed to carry radiation to cancer throughout the body. All enrolled dogs receive the treatment; this is not a placebo-controlled or masked trial.</p>
<p>Dogs with a response or stable disease at the day 21 assessment may qualify for another dose. Standard chemotherapy is not part of the study, and owners should discuss that distinction with the oncology team before deciding whether the protocol fits their dog.</p>
<h2>Who may qualify</h2><p>Dogs need peripheral T-cell lymphoma confirmed by flow cytometry or immunohistochemistry, a measurable tumor that can be biopsied, body weight of at least 10 kg (22 lb), and age over one year. Significant health problems that would make completion unlikely may exclude a dog.</p>
<h2>What the study covers</h2><p>The initial screening visit and initial laboratory work are owner-paid. After enrollment, the study covers required examination visits, laboratory work, tumor biopsy, PET-CT scans, hospitalization and all costs related to 90Y-NM600 treatment. Up to $1,000 is also available for treatment-related side effects.</p>
<p>Owners or veterinarians can contact UW Veterinary Care Oncology at 608-890-0422 or <a href="mailto:oncclinicaltrials@vetmed.wisc.edu">oncclinicaltrials@vetmed.wisc.edu</a>.</p>
<div class="article-cta"><a href="{WISCONSIN_OFFICIAL}" target="_blank" rel="noopener">Read the official Wisconsin trial listing</a></div><p><a href="{MATCHER_URL}">Check current lymphoma trials in Vet Trial Finder</a></p>'''
    write_article(root, "wisconsin-ptcl-radiopharmaceutical-trial", "Wisconsin recruits dogs with peripheral T-cell lymphoma for 90Y-NM600 therapy", "UW Veterinary Care is recruiting dogs with peripheral T-cell lymphoma for a funded study of targeted 90Y-NM600 radiopharmaceutical therapy.", wisconsin_body, "UW Veterinary Care")

    purdue_body = f'''<p class="eyebrow">Three recruiting treatment trials · September 20, 2026</p>
<h1>Purdue adds experimental tumor ablation to standard cancer treatment in three trials</h1>
<p>Purdue University Veterinary Hospital in West Lafayette, Indiana, is recruiting dogs for three treatment studies: focused ultrasound plus CHOP for lymphoma, H-FIRE before liver-tumor surgery, and focused ultrasound before amputation and carboplatin for osteosarcoma. In each protocol, the experimental procedure is added to an established treatment plan rather than offered as an unsupported substitute.</p>
<p>The experimental ablation itself has not been shown to improve remission, disease control or survival. The practical benefit for enrolled dogs is that standard treatment remains in place and part of the care is study-funded.</p>

<h2>Lymphoma: HIFU followed by CHOP</h2>
<p><strong>Who may qualify:</strong> Dogs at least 1 year old and over 8 kg (18 lb) with newly diagnosed, untreated intermediate- or large-cell multicentric B- or T-cell lymphoma. Small-cell, extranodal and stage V lymphoma are excluded. Dogs must be able to undergo sedation or anesthesia and must not have had recent chemotherapy, anticancer treatment or corticosteroids.</p>
<p><strong>How it differs from standard treatment:</strong> Standard UW-25 CHOP chemotherapy still begins after the study procedure and continues for 25 weeks. Before CHOP, Purdue partially treats one enlarged lymph node with HIFU and samples treated and untreated nodes to look for an immune response. The experimental procedure is an addition to CHOP, not a replacement for it, and there is no placebo.</p>
<p><strong>Study support:</strong> HIFU, sedation or anesthesia, study biopsies and laboratory work are covered. The study provides a $2,000 CHOP credit and up to $2,000 more for HIFU-related side effects or CHOP. Initial diagnostics and unrelated care remain owner-paid.</p>

<h2>Liver cancer: H-FIRE before surgery</h2>
<p><strong>Who may qualify:</strong> Dogs with one or more liver tumors that Purdue considers surgically removable. The dog must be able to undergo anesthesia, H-FIRE and the planned surgery. Coagulation disorders, severe systemic illness or declining tumor removal after H-FIRE exclude participation.</p>
<p><strong>How it differs from standard treatment:</strong> Surgery remains the definitive treatment. The trial adds one image-guided H-FIRE procedure under general anesthesia, then repeats CT and removes the tumor about 5–7 days later. H-FIRE uses short electrical pulses to damage tumor cells and is experimental; it is not standard veterinary care.</p>
<p><strong>Study support:</strong> H-FIRE, the post-treatment CT and study rechecks are covered, with a $2,000 credit toward surgery. Owners pay the remaining surgical cost and unrelated care.</p>

<h2>Osteosarcoma: HIFU before amputation and carboplatin</h2>
<p><strong>Who may qualify:</strong> Dogs at least 1 year old and over 8 kg (18 lb) with newly diagnosed appendicular osteosarcoma, no detected metastases and a tumor position that provides a safe ultrasound path. Dogs must be candidates for anesthesia, limb amputation and carboplatin.</p>
<p><strong>How it differs from standard treatment:</strong> The standard plan of amputation followed by carboplatin remains in place. Purdue adds functional imaging and partial HIFU ablation, then performs amputation about 5–7 days later. The study is examining safety and biological effects; direct benefit from HIFU is not guaranteed.</p>
<p><strong>Study support:</strong> HIFU and functional imaging are covered, up to $2,600 is provided toward amputation, and chemotherapy recheck visits are covered. Owners pay initial staging, remaining surgery costs and carboplatin administration.</p>

<p>Owners and veterinarians can contact <a href="mailto:TumorAblation@purdue.edu">TumorAblation@purdue.edu</a>. Purdue requires a veterinary referral for the lymphoma evaluation.</p>
<div class="article-cta"><a href="{PURDUE_ABLATION_OFFICIAL}" target="_blank" rel="noopener">Read Purdue’s three tumor-ablation protocols</a></div>
<p><a href="{MATCHER_URL}">Check these and other current cancer treatment trials in Vet Trial Finder</a></p>'''
    write_article(root, "purdue-three-cancer-treatment-trials", "Purdue adds experimental tumor ablation to standard cancer treatment in three trials", "Three Purdue studies add experimental ablation to standard treatment for lymphoma, liver cancer and osteosarcoma, with part of the care funded.", purdue_body, "Purdue University College of Veterinary Medicine", "September 20, 2026", "2026-09-20", PURDUE_SOCIAL_IMAGE)

    taiwan_il15_body = f'''<p class="eyebrow">Recruiting in Taiwan · September 25, 2026</p>
<h1>Taiwan trial tests inhaled IL-15 for canine lung metastases</h1>
<p>Evergreen Animal Hospital in Taipei is recruiting dogs with melanoma or osteosarcoma and measurable lung metastases for an IL-15 immunotherapy study.</p>
<p>IL-15, or interleukin-15, is an immune-signaling protein. It does not attack cancer directly like chemotherapy. It stimulates natural killer cells and certain T cells that can recognize and destroy tumor cells.</p>
<p>Dogs with pulmonary metastases receive IL-15 as an aerosol through a breathing mask while awake. The treatment is intended to deliver the immune-stimulating cytokine directly to the lungs, where these cancers commonly spread. The protocol also describes subcutaneous administration.</p>
<p>This approach has published canine evidence, but the results are mixed. In a Phase I study of dogs with visible lung metastases from melanoma or osteosarcoma, the objective response rate was 11% and the clinical benefit rate was 39% among 18 evaluable dogs. A small number had durable responses, including one complete response lasting more than a year.</p>
<p>A later Phase II study tested inhaled IL-15 in a different setting: dogs with localized osteosarcoma received it after amputation and before chemotherapy, when no visible metastases were present. That study was stopped for futility after outcomes were worse than the historical comparison group. These results do not directly answer whether IL-15 may help some dogs with established lung metastases, but they show that timing and treatment context matter.</p>
<p>The Taiwanese study is closer to the original metastatic-disease trial, although its dosing schedule is different. Its phase, enrollment target and interim results have not been published, so the earlier response rates should not be assumed to apply to this protocol.</p>
<h2>Who may qualify</h2>
<p>Dogs must have confirmed melanoma or osteosarcoma, lung lesions larger than 1 cm, no life-threatening tumor-related symptoms, and no current steroid or other immunosuppressive treatment. The hospital describes weekly treatment for eight weeks, followed by reassessment.</p>
<h2>What the study covers</h2>
<p>IL-15 is provided at no charge. Owners are responsible for diagnostic testing, supportive medications and other veterinary expenses.</p>
<p>IL-15 is also being studied in human cancer care, and an IL-15 receptor agonist has been approved for one form of bladder cancer. Inhaled IL-15, however, remains an experimental veterinary approach. This is an unusual example of dogs participating at the front edge of immunotherapy research rather than receiving a veterinary adaptation of an established human treatment.</p>
<div class="article-cta"><a href="{TAIWAN_IL15_OFFICIAL}" target="_blank" rel="noopener">Read the official Evergreen recruitment page</a></div>
<p><a href="{TAIWAN_IL15_PHASE1}" target="_blank" rel="noopener">Read the published Phase I study</a> · <a href="{TAIWAN_IL15_PHASE2}" target="_blank" rel="noopener">Read the published Phase II study</a></p>
<p><a href="{MATCHER_URL}">Check this and other current cancer treatment trials in Vet Trial Finder</a></p>'''
    write_article(root, "taiwan-inhaled-il15-lung-metastases", "Taiwan trial tests inhaled IL-15 for canine lung metastases", "A recruiting study in Taipei is testing inhaled IL-15 in dogs with melanoma or osteosarcoma and measurable lung metastases.", taiwan_il15_body, "Evergreen Animal Hospital and linked peer-reviewed studies", "September 25, 2026", "2026-09-25")

    barc_trials_body = f'''<p class="eyebrow">Recruiting in Washington · September 27, 2026</p>
<h1>BARC is recruiting dogs and cats for cancer treatment trials</h1>
<figure style="margin:18px 0 24px"><img src="{BARC_ARTICLE_IMAGE}" alt="Illustrative cover showing a dog and a cat beside the BARC cancer trials headline and Edmonds clinic address" width="1733" height="908" style="display:block;width:100%;height:auto;border-radius:12px"></figure>
<p>Bridge Animal Referral Center (BARC) in Edmonds, Washington, lists three current cancer treatment studies. One accepts selected dogs and cats; the other two are for dogs. The diagnosis alone does not establish eligibility: tumor location, size, stage and previous treatment can matter.</p>
<h2>Gold nanoparticles and laser heating: dogs and cats</h2>
<p>In this study, gold nanoparticles are given intravenously, then the superficial tumor is heated with a near-infrared laser. BARC lists dogs with mast cell tumors, soft tissue sarcomas or selected melanomas, with different size limits for each. Eligible cats may have oral squamous cell carcinoma that does not involve bone, or certain other superficial skin tumors, including mast cell tumors, sarcomas and carcinomas. BARC has not published current funding terms for this study. Its clinical benefit has not been established.</p>
<h2>Intratumoral carboplatin: dogs with superficial SCC</h2>
<p>BARC is also enrolling dogs with non-metastatic superficial squamous cell carcinoma (SCC) to test a new carboplatin formulation injected directly into the tumor. It is designed for longer local activity, but whether it improves tumor control has not yet been established.</p>
<p>Dogs need a confirmed SCC diagnosis and at least one measurable lesion 1 cm or larger. BARC requires chest imaging and lymph-node assessment to check for spread. Previous chemotherapy, immunotherapy or radiation for cancer excludes participation; significant illness or abnormal blood counts may also rule a dog out. BARC says study treatments and associated procedures are fully funded. The team can clarify any costs outside the study.</p>
<h2>EGFR/HER2 vaccine: selected dog cancers</h2>
<p>BARC also lists active enrollment for an experimental EGFR/HER2 peptide vaccine. The clinic names osteosarcoma, hemangiosarcoma and transitional cell carcinoma among the dog cancers it considers; some other tumor types require a records review. This is a participating site in a broader vaccine study already listed in Vet Trial Finder, not a second copy of that trial. Ask BARC about eligibility and costs for this site.</p>
<p><strong>Location and contact:</strong> Bridge Animal Referral Center, Edmonds, Washington · 425-697-2272</p>
<div class="article-cta"><a href="{BARC_TRIALS_OFFICIAL}" target="_blank" rel="noopener">Read the official BARC study information</a></div>
<p><a href="{MATCHER_URL}">Check these and other current cancer treatment trials in Vet Trial Finder</a></p>'''
    write_article(root, "barc-dog-cat-cancer-trials", "BARC is recruiting dogs and cats for cancer treatment trials", "BARC in Edmonds is recruiting dogs and cats for selected gold nanoparticle treatment and dogs for intratumoral carboplatin and an EGFR/HER2 vaccine.", barc_trials_body, "Bridge Animal Referral Center", "September 27, 2026", "2026-09-27", BARC_SOCIAL_IMAGE, (1733, 907))

    add_to_sitemap(root, (NEWS_URL, CORNELL_URL, NC_STATE_URL, WISCONSIN_URL, PURDUE_URL, TAIWAN_IL15_URL, BARC_TRIALS_URL))
    rendered = "\n".join((root / "news" / slug / "index.html").read_text(encoding="utf-8") for slug in ("cornell-smart-start-b-cell-lymphoma", "nc-state-il12-bladder-cancer-deadline", "wisconsin-ptcl-radiopharmaceutical-trial", "purdue-three-cancer-treatment-trials", "taiwan-inhaled-il15-lung-metastases", "barc-dog-cat-cancer-trials"))
    required = ("There is no placebo.", "$1,000 toward chemotherapy costs", "September 30, 2026", "There is no placebo group.", "90Y-NM600", "initial screening visit and initial laboratory work are owner-paid", "HIFU followed by CHOP", "H-FIRE before surgery", "Osteosarcoma: HIFU", "has not been shown to improve remission, disease control or survival", "objective response rate was 11%", "phase, enrollment target and interim results have not been published", "whether it improves tumor control has not yet been established", "study treatments and associated procedures are fully funded", "Eligible cats may have oral squamous cell carcinoma that does not involve bone", BARC_TRIALS_OFFICIAL, BARC_SOCIAL_IMAGE, PURDUE_SOCIAL_IMAGE, 'summary_large_image', PURDUE_ABLATION_OFFICIAL, TAIWAN_IL15_OFFICIAL, TAIWAN_IL15_PHASE1, TAIWAN_IL15_PHASE2, CORNELL_OFFICIAL, NC_STATE_OFFICIAL, WISCONSIN_OFFICIAL, '"@type": "NewsArticle"')
    missing = [marker for marker in required if marker not in rendered]
    if missing:
        raise AssertionError(f"News validation failed: {missing}")


if __name__ == "__main__":
    generate_news_section(Path(__file__).resolve().parent / "site")
