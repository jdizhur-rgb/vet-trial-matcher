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
CORNELL_OFFICIAL = "https://www.vet.cornell.edu/hospitals/clinical-trials/smart-start-therapy-canine-b-cell-lymphoma"
NC_STATE_OFFICIAL = "https://cvm.ncsu.edu/clinical-trial/now-enrolling-dogs-with-invasive-bladder-cancer/"
WISCONSIN_OFFICIAL = "https://uwveterinarycare.wisc.edu/veterinary-clinical-studies/oncology/"
PURDUE_ABLATION_OFFICIAL = "https://vet.purdue.edu/wcorc/clinical-trials/tumor-ablation.php"
TAIWAN_IL15_OFFICIAL = "https://www.egah.com.tw/news/%E6%8B%9B%E5%8B%9F%E7%8A%AC%E9%BB%91%E8%89%B2%E7%B4%A0%E7%98%A4%E5%8F%8A%E9%AA%A8%E8%82%89%E7%98%A4%E8%87%A8%E5%BA%8A%E8%A9%A6%E9%A9%97"
TAIWAN_IL15_PHASE1 = "https://jitc.bmj.com/content/10/6/e004493"
TAIWAN_IL15_PHASE2 = "https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2025.1672790/full"
PURDUE_SOCIAL_IMAGE = f"{SITE}/assets/social/purdue-ablation-1200x630.jpg"


def add_to_sitemap(root: Path, urls: tuple[str, ...]) -> None:
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        raise AssertionError("Sitemap is required before generating news")
    text = sitemap.read_text(encoding="utf-8")
    for url in urls:
        if url not in text:
            text = text.replace("</urlset>", f"<url><loc>{g.esc(url)}</loc></url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def write_article(root: Path, slug: str, title: str, description: str, body: str, source_name: str, published: str = "September 17, 2026", published_iso: str = "2026-09-17", social_image: str | None = None) -> None:
    url = f"{NEWS_URL}{slug}/"
    article_dir = root / "news" / slug
    article_dir.mkdir(parents=True, exist_ok=True)
    byline = f'''<div class="article-byline"><p><strong>Published:</strong> {published}</p><p><strong>Recruitment status checked:</strong> {published}</p><p><strong>Source:</strong> {source_name}.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance and reviewed by Yuliia Dizhur. Trial eligibility and enrollment decisions are made by the study team.</p></div>'''
    page = g.page(f"{title} | Vet Trial Finder", description, f'<article class="article-page news-article">{body}{byline}</article>', url)
    social = f'''<meta property="og:type" content="article"><meta property="og:site_name" content="Vet Trial Finder"><meta property="og:title" content="{g.esc(title)}"><meta property="og:description" content="{g.esc(description)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="{'summary_large_image' if social_image else 'summary'}"><meta name="twitter:title" content="{g.esc(title)}"><meta name="twitter:description" content="{g.esc(description)}">'''
    if social_image:
        social += f'<meta property="og:image" content="{g.esc(social_image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Vet Trial Finder news cover"><meta name="twitter:image" content="{g.esc(social_image)}">'
    schema = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": title, "datePublished": published_iso, "dateModified": published_iso, "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"}, "publisher": {"@type": "Organization", "name": "Vet Trial Finder", "url": f"{SITE}/"}, "mainEntityOfPage": url}
    page = page.replace("</head>", social + f'<script type="application/ld+json">{json.dumps(schema)}</script></head>', 1)
    (article_dir / "index.html").write_text(wrap_html(page), encoding="utf-8")


def generate_news_section(root: Path) -> None:
    source_assets = Path(__file__).resolve().parent / "assets" / "social"
    built_assets = root / "assets" / "social"
    built_assets.mkdir(parents=True, exist_ok=True)
    for name in ("purdue-ablation-1200x630.jpg", "purdue-ablation-story-1080x1920.jpg"):
        shutil.copy2(source_assets / name, built_assets / name)
    index_body = f'''<div class="registry-page news-index">
<h1>Veterinary oncology news</h1>
<p class="lead">Newly opened treatment trials, meaningful recruitment changes and other developments that may matter to owners looking for cancer treatment options.</p>
<div class="directory-grid">
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

    add_to_sitemap(root, (NEWS_URL, CORNELL_URL, NC_STATE_URL, WISCONSIN_URL, PURDUE_URL, TAIWAN_IL15_URL))
    rendered = "\n".join((root / "news" / slug / "index.html").read_text(encoding="utf-8") for slug in ("cornell-smart-start-b-cell-lymphoma", "nc-state-il12-bladder-cancer-deadline", "wisconsin-ptcl-radiopharmaceutical-trial", "purdue-three-cancer-treatment-trials", "taiwan-inhaled-il15-lung-metastases"))
    required = ("There is no placebo.", "$1,000 toward chemotherapy costs", "September 30, 2026", "There is no placebo group.", "90Y-NM600", "initial screening visit and initial laboratory work are owner-paid", "HIFU followed by CHOP", "H-FIRE before surgery", "Osteosarcoma: HIFU", "has not been shown to improve remission, disease control or survival", "objective response rate was 11%", "phase, enrollment target and interim results have not been published", PURDUE_SOCIAL_IMAGE, 'summary_large_image', PURDUE_ABLATION_OFFICIAL, TAIWAN_IL15_OFFICIAL, TAIWAN_IL15_PHASE1, TAIWAN_IL15_PHASE2, CORNELL_OFFICIAL, NC_STATE_OFFICIAL, WISCONSIN_OFFICIAL, '"@type": "NewsArticle"')
    missing = [marker for marker in required if marker not in rendered]
    if missing:
        raise AssertionError(f"News validation failed: {missing}")


if __name__ == "__main__":
    generate_news_section(Path(__file__).resolve().parent / "site")
