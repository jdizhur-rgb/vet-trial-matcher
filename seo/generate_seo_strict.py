#!/usr/bin/env python3
"""Single owner-facing SEO rendering layer with catalog-wide location preflight."""
from __future__ import annotations
import hashlib,html,json,re,shutil
import generate_seo as g
from cancer_page_enhancements import enhance_cancer_pages
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES
from center_directory import LOCATIONS, address_for, addresses_for, address_is_complete, canonical_name_for, normalize
PROFILES.update(EXTRA_PROFILES)
PROFILES["Aurelius Biotherapeutics"] = {
    "title": "About Aurelius Biotherapeutics",
    "about": (
        "Aurelius Biotherapeutics develops personalized immune-cell treatments for dogs with lymphoma "
        "in partnership with Bellingham Veterinary. Its current program uses a dog's own T cells as part "
        "of treatment for eligible canine patients."
    ),
    "image": "https://bhamvet.com/wp-content/uploads/2022/07/HalfCircle-Dog.png",
    "image_alt": "Dog featured by Bellingham Veterinary, clinical partner of Aurelius Biotherapeutics",
    "image_caption": "Photo: Bellingham Veterinary.",
    "links": [("Aurelius Biotherapeutics", "https://aureliusbio.com/")],
}
_PROTECT_IMAGE = "https://static.wixstatic.com/media/4821a9_49c524132f724ed58438736cd49db928~mv2.jpg/v1/fill/w_980,h_650,al_c,q_85/927d1999a28aba712c858eccbfe8e7dc95b3c504.jpg"
_PROTECT_LINK = "https://www.protectvac.com/news-18.html"
_ONCOWAF_IMAGE = "https://oncowaf.be/public/images/skin/default/contact.png"
_ONCOWAF_LINK = "https://oncowaf.be/en/ClinicalTrials/searchResults"
PROFILES.update({
    "Woke Animal Hospital": {"title":"About Woke Animal Hospital","about":"Woke Animal Hospital in Taichung is a participating site in Protect Animal Health's current PT001 field trial for dogs with stage II–III oral malignant melanoma.","image":_PROTECT_IMAGE,"image_alt":"Recruitment notice for the PT001 canine oral melanoma field trial","image_caption":"Trial image: Protect Animal Health.","links":[("Protect Animal Health trial",_PROTECT_LINK)]},
    "Evergreen Animal Hospital": {"title":"About Evergreen Animal Hospital","about":"Evergreen Animal Hospital in Taiwan is recruiting canine patients for oncology research, including current studies in oral melanoma and osteosarcoma.","image":"https://static.wixstatic.com/media/4821a9_49c524132f724ed58438736cd49db928~mv2.jpg/v1/fill/w_980,h_650,al_c,q_85/927d1999a28aba712c858eccbfe8e7dc95b3c504.jpg","image_alt":"Veterinary patient featured by Evergreen Animal Hospital","image_caption":"Photo: Evergreen Animal Hospital.","links":[("Evergreen clinical-trial notice","https://www.egah.com.tw/news/%E6%8B%9B%E5%8B%9F%E7%8A%AC%E9%BB%91%E8%89%B2%E7%B4%A0%E7%98%A4%E5%8F%8A%E9%AA%A8%E8%82%89%E7%98%A4%E8%87%A8%E5%BA%8A%E8%A9%A6%E9%A9%97")]},
    "Jimmy Harry Animal Hospital": {"title":"About Jimmy Harry Animal Hospital","about":"Jimmy Harry Animal Hospital in Taichung is one of the veterinary sites listed for Protect Animal Health's PT001 therapeutic-vaccine field trial for canine oral melanoma.","image":_PROTECT_IMAGE,"image_alt":"Recruitment notice for the PT001 canine oral melanoma field trial","image_caption":"Trial image: Protect Animal Health.","links":[("Protect Animal Health trial",_PROTECT_LINK)]},
    "National Chung Hsing University Veterinary Teaching Hospital": {"title":"About NCHU Veterinary Teaching Hospital","about":"National Chung Hsing University Veterinary Teaching Hospital is an academic referral hospital in Taichung and a participating site for the current PT001 canine oral-melanoma field trial.","image":_PROTECT_IMAGE,"image_alt":"Recruitment notice for the PT001 canine oral melanoma field trial","image_caption":"Trial image: Protect Animal Health.","links":[("Protect Animal Health trial",_PROTECT_LINK)]},
    "Bubble Animal Hospital": {"title":"About Bubble Animal Hospital","about":"Bubble Animal Hospital in Taichung is a participating veterinary site in the current PT001 therapeutic-vaccine field trial for dogs with oral malignant melanoma.","image":_PROTECT_IMAGE,"image_alt":"Recruitment notice for the PT001 canine oral melanoma field trial","image_caption":"Trial image: Protect Animal Health.","links":[("Protect Animal Health trial",_PROTECT_LINK)]},
    "National Taiwan University Veterinary Hospital": {"title":"About National Taiwan University Veterinary Hospital","about":"National Taiwan University Veterinary Hospital is an academic referral center participating in current canine cancer research, including the PT001 oral-melanoma vaccine field trial.","image":_PROTECT_IMAGE,"image_alt":"Recruitment notice for the PT001 canine oral melanoma field trial","image_caption":"Trial image: Protect Animal Health.","links":[("Protect Animal Health trial",_PROTECT_LINK)]},
    "Protect Animal Health (寶泰生醫) multicenter field trial": {"title":"About the Protect Animal Health field trial","about":"Protect Animal Health is coordinating a Taiwanese multicenter field trial of PT001, an investigational PD-L1/CTLA-4 recombinant-protein therapeutic vaccine for dogs with stage II–III oral malignant melanoma.","image":_PROTECT_IMAGE,"image_alt":"Recruitment notice for the PT001 canine oral melanoma field trial","image_caption":"Trial image: Protect Animal Health.","links":[("Official PT001 recruitment notice",_PROTECT_LINK)]},
    "University of Évora Veterinary Hospital": {"title":"About the University of Évora Veterinary Hospital","about":"The University of Évora Veterinary Hospital provides university-based veterinary care and participates in European clinical research; the current catalog listing is tied to an oncology study registered through OncoWAF.","image":"https://www.uevora.pt/var/uevora_responsive/storage/images/utilidades/destaques-banner/primeira-pagina-imagem/rececao-26/151524-2-por-PT/Rececao-26_frontpage_highlight_containerfluid.jpg","image_alt":"University of Évora campus","image_caption":"Photo: University of Évora.","links":[("OncoWAF clinical-trial listing",_ONCOWAF_LINK)]},
    "VetAgro Sup CHUVAC": {"title":"About VetAgro Sup CHUVAC","about":"VetAgro Sup's companion-animal university hospital near Lyon provides specialty care including oncology and participates in European veterinary clinical research.","image":"https://chuvac.vetagro-sup.fr/wp-content/uploads/2025/10/Vetagro_1094-1920x700.jpg","image_alt":"Companion-animal care at VetAgro Sup CHUVAC","image_caption":"Photo: VetAgro Sup CHUVAC.","links":[("VetAgro Sup CHUVAC","https://chuvac.vetagro-sup.fr/")]},
    "European multicenter study — Floryne Buishand": {"title":"About this European multicenter study","about":"This European veterinary oncology study is coordinated across participating hospitals by the research team led by veterinary surgical oncologist Floryne Buishand; the active locations are listed inside the opportunity.","image":_ONCOWAF_IMAGE,"image_alt":"OncoWAF veterinary clinical-trials contact image","image_caption":"Image: OncoWAF.","links":[("European trial registry",_ONCOWAF_LINK)]},
    "Duma Animal Hospital": {"title":"About Duma Animal Hospital","about":"Duma Animal Hospital is listed as a participating hospital in a current European veterinary oncology study; diagnosis-specific eligibility and the active visit site must be confirmed with the study team.","image":_ONCOWAF_IMAGE,"image_alt":"OncoWAF veterinary clinical-trials contact image","image_caption":"Image: OncoWAF.","links":[("OncoWAF clinical-trial listing",_ONCOWAF_LINK)]},
    "Hospital Veterinario Peña Jasso": {"title":"About Hospital Veterinario Peña Jasso","about":"Hospital Veterinario Peña Jasso in Ensenada is participating in translational nanomedicine research for dogs with cancer through a collaboration involving UNAM, UABC and UAG.","image":"https://zonanorte.mx/media/notas/8542/7555.jpg","image_alt":"Veterinary nanomedicine research team in Ensenada","image_caption":"Photo: Zona Norte.","links":[("Research collaboration news","https://zonanorte.mx/main/mozaico/nid/8542")]},
    "University of Milan Veterinary Teaching Hospital (Lodi)": {"title":"About the University of Milan Veterinary Teaching Hospital","about":"The University of Milan Veterinary Teaching Hospital in Lodi combines referral care with clinical research and is a participating site for a current veterinary oncology study.","image":"https://www.ospedaleveterinario.unimi.it/static/026a281f10ce96c6b02ba6c3b134e481/ec873/hero-veterinari.png","image_alt":"Veterinary clinicians at the University of Milan Veterinary Teaching Hospital","image_caption":"Photo: University of Milan Veterinary Teaching Hospital.","links":[("University of Milan research studies","https://www.ospedaleveterinario.unimi.it/collaborare-con-noi-studi-di-ricerca/")]},
    "Ghent University Faculty of Veterinary Medicine": {"title":"About Ghent University Veterinary Medicine","about":"Ghent University's Small Animal Clinic combines referral care with clinical research in dogs and cats; its current catalog listing evaluates fluorescence-lifetime imaging during cancer surgery.","image":"https://www.ugent.be/img/dcom/faciliteiten/techlaneghentscienceparkdrone.jpg/@@images/image/focus-small","image_alt":"Ghent University research campus","image_caption":"Photo: Ghent University.","links":[("Ghent veterinary imaging study","https://www.ugent.be/di/khd/nl/onderzoek/fluorescentie-levensduur-beeldvorming")]},
    "Anivive Lifesciences — multicenter": {"title":"About Anivive Lifesciences clinical trials","about":"Anivive Lifesciences coordinates multicenter veterinary drug studies; its current oncology listing evaluates verdinexor with carboplatin for dogs with osteosarcoma.","image":"https://bhamvet.com/wp-content/uploads/2022/07/HalfCircle-Dog.png","image_alt":"Dog receiving care through a veterinary cancer program","image_caption":"Canine patient photo: Bellingham Veterinary.","links":[("Anivive clinical trials","https://anivivelifesciences.com/trials")]},
    "Multicenter local T-cell-engager STS immunotherapy": {"title":"About the multicenter T-cell-engager study","about":"This U.S. study evaluates a locally injected hydrogel and T-cell engager before surgery for eligible dogs with accessible soft-tissue sarcoma; participating hospitals and study support are shown in the opportunity.","image":"https://wpcdn.web.wsu.edu/news/uploads/sites/2797/2020/12/Capecitabinephoto-1024x683.jpg","image_alt":"Canine oncology patient with a Washington State University veterinary clinician","image_caption":"Photo: Washington State University.","links":[("WSU study information","https://hospital.vetmed.wsu.edu/2025/11/03/feasibility-and-dose-escalation-clinical-trial-of-local-immunotherapy-for-solid-and-brain-tumors-in-canine-cancer-patient/")]},
    "PETcura (宝科雅) multicenter IIT": {"title":"About the PETcura multicenter study","about":"PETcura is coordinating an investigator-initiated study of personalized mRNA immunotherapy for dogs with cancer in China; treatment locations and diagnosis-specific requirements are listed inside the opportunity.","image":"https://www.petcura.cn/static/img/diagram_iit_8step.webp","image_alt":"PETcura personalized canine cancer immunotherapy study","image_caption":"Study image: PETcura.","links":[("PETcura study information","https://www.petcura.cn/zh/mrna-vaccine/study/")]},
    "Zhongnong Dongjun Laboratory": {"title":"About Zhongnong Dongjun Laboratory","about":"Zhongnong Dongjun Laboratory is associated with a current companion-animal oncology research listing in China; owners should confirm the treating hospital and enrollment details with the study team.","image":"https://www.petcura.cn/static/img/diagram_iit_8step.webp","image_alt":"Canine precision-oncology study diagram","image_caption":"Study image: PETcura.","links":[("Current study details","https://www.petcura.cn/zh/mrna-vaccine/study/")]},
    "University Hospital for Companion Animals, University of Copenhagen / Lund University": {"title":"About the Copenhagen–Lund research collaboration","about":"The University Hospital for Companion Animals in Copenhagen and Lund University collaborate on veterinary clinical research; the current listing identifies the participating hospital and study requirements below.","image":"https://ikv.ku.dk/om/fundraising/qimmeqhealth/Sl_dehund_til_fundraising_FB.jpg","image_alt":"Dog featured by the University of Copenhagen veterinary program","image_caption":"Photo: University of Copenhagen.","links":[("University Hospital research projects","https://dyrehospitalet.ku.dk/forskning/forskningsprojekter/")]},
})
for _name in (
    "Woke Animal Hospital", "Jimmy Harry Animal Hospital",
    "National Chung Hsing University Veterinary Teaching Hospital", "Bubble Animal Hospital",
    "National Taiwan University Veterinary Hospital",
    "Protect Animal Health (寶泰生醫) multicenter field trial",
):
    if _name in PROFILES:
        PROFILES[_name]["image_caption"] = "Trial-site photo: Evergreen Animal Hospital."
_IMAGE_REPLACEMENTS = {
    "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)": ("https://assets1.cbsnewsstatic.com/hub/i/r/2015/04/29/340c23e5-e5a3-40ef-bf68-dcc84ef47c4b/thumbnail/1200x630/6e2e666786e7a06c8786e0cd609401f5/restrictedimagesub.jpg", "Photo: Johns Hopkins CIGAT, published by CBS Baltimore."),
    "University of Pennsylvania School of Veterinary Medicine": ("https://www.vet.upenn.edu/wp-content/uploads/2026/05/vet-hospital.jpg", "Photo: Penn Vet."),
    "MedVet Clinical Studies Center": ("https://cdn.medvet.com/app/uploads/2025/07/Medical-Oncology_Cover-Photo-1024x819.jpg?strip=all&w=1080", "Photo: MedVet Medical Oncology."),
    "University of Georgia College of Veterinary Medicine": ("https://news.uga.edu/wp-content/uploads/2017/12/20140115-LinAc-Mallory-Nagata-6916-1024x683.jpg", "Photo: UGA Veterinary Teaching Hospital / UGA Today."),
    "UT Southwestern Veterinary Research and Oncology Clinic": ("https://www.utsouthwestern.edu/departments/radiation-oncology/assets/vroc-team-6.2026.JPG", "Photo: UT Southwestern VROC."),
    "UT Southwestern Veterinary Radiation Oncology Clinic (VROC)": ("https://www.utsouthwestern.edu/departments/radiation-oncology/assets/vroc-team-6.2026.JPG", "Photo: UT Southwestern VROC."),
}
for _name, (_image, _caption) in _IMAGE_REPLACEMENTS.items():
    if _name in PROFILES:
        PROFILES[_name]["image"] = _image
        PROFILES[_name]["image_caption"] = _caption
for _center, _label, _url in (
    ("AniCura Ospedale Veterinario I Portoni Rossi", "Current European trial listing", _ONCOWAF_LINK),
    ("CHV AniCura Armonia", "Current European trial listing", _ONCOWAF_LINK),
    ("AniCura AOI -Animal Oncology and Imaging Center", "AniCura AOI oncology", "https://www.anicura.ch/standorte/aoi/onkologie/weitere-therapien/"),
    ("AniCura AOI - Animal Oncology and Imaging Center", "AniCura AOI oncology", "https://www.anicura.ch/standorte/aoi/onkologie/weitere-therapien/"),
    ("North Downs Specialist Referrals", "NDSR canine cancer research", "https://www.ndsr.co.uk/insights/canine-mammary-cancer/"),
    ("UT Southwestern Veterinary Radiation Oncology Clinic (VROC)", "VROC study listings", "https://veterinaryclinicaltrials.org/investigator/e49205cb5a4046f8bb9e288a2ea04f48/"),
    ("Ontario Veterinary College / Hospital for Sick Children", "OVC clinical trial", "https://ovcclinicaltrials.uoguelph.ca/evaluating-a-non-invasive-heat-therapy-for-the-treatment-of-bone-cancer-in-dogs-2/"),
    ("Ontario Veterinary College — University of Guelph", "OVC oncology trials", "https://ovcclinicaltrials.uoguelph.ca/evaluating-palladia-for-the-treatment-of-canine-oral-melanoma/"),
    ("AniCura Atlântico Hospital Veterinário", "Current European trial listing", _ONCOWAF_LINK),
):
    if _center in PROFILES:
        PROFILES[_center]["links"] = [(_label, _url)]

# Canonical owner-facing description for each published center. Trial counts,
# diagnoses and enrollment details are rendered in the structured blocks below,
# so they are deliberately not repeated here.
CENTER_ABOUT = {
    "AniCura AOI - Animal Oncology and Imaging Center": "AniCura AOI in Switzerland is a referral center devoted to cancer care and advanced imaging. Its team uses chemotherapy, radiation therapy and treatments delivered directly into a tumor, with CT and MRI available in the same hospital.",
    "AniCura Atlântico Hospital Veterinário": "AniCura Atlântico is a referral hospital near Lisbon with medical oncology, cancer surgery and advanced imaging. The team also studies ways to destroy selected tumors with precisely directed heat when ordinary surgery may be difficult.",
    "AniCura Ospedale Veterinario I Portoni Rossi": "I Portoni Rossi is a large referral hospital near Bologna with medical oncology, cancer surgery and advanced imaging. Its oncology team also takes part in research on personalized treatments made from a dog's own tumor.",
    "Anivive Lifesciences — multicenter": "Anivive develops veterinary medicines and tests them through a network of participating hospitals. Its cancer program focuses on turning laboratory discoveries into treatments that can be given in ordinary veterinary oncology clinics.",
    "Auburn University College of Veterinary Medicine": "Auburn's Bailey Small Animal Teaching Hospital brings medical oncology, cancer surgery and radiation therapy together in one service. The university also studies new cancer drugs, immune treatments and more precise ways to deliver radiation.",
    "Aurelius Biotherapeutics": "Aurelius Biotherapeutics is developing personalized immune-cell treatment for dogs with lymphoma. The process uses a dog's own T cells, which are prepared outside the body and returned to help the immune system recognize the cancer.",
    "Bubble Animal Hospital": "Bubble Animal Hospital in Taichung provides companion-animal care and helps recruit dogs for veterinary cancer research in Taiwan. It is one of the community hospitals connecting eligible patients with studies run by specialist research teams.",
    "CHV AniCura Armonia": "CHV AniCura Armonia is a multidisciplinary referral hospital near Nice with oncology, surgery and advanced imaging. The hospital also studies focused ultrasound, which treats a selected area inside the body without a surgical incision.",
    "Colorado State University Flint Animal Cancer Center": "Colorado State's Flint Animal Cancer Center is one of the largest veterinary cancer programs in the world. For more than four decades it has combined treatment of pets with comparative cancer research, helping establish approaches now widely used in cancer surgery, chemotherapy and radiation care.",
    "Cornell University College of Veterinary Medicine": "Cornell's oncology service combines medical and radiation oncology with the Sprecher Institute for Comparative Cancer Research. Its teams study how cancers grow and spread, then test new drugs, imaging methods and treatments in dogs and cats receiving care at the teaching hospital.",
    "Duma Animal Hospital": "Duma Animal Hospital is a companion-animal hospital in Taiwan that helps bring university and biotechnology research into everyday veterinary practice. Its role is to examine patients, explain a study to owners and provide treatment and follow-up locally.",
    "Ethos Veterinary Health / Ethos Discovery": "Ethos Discovery runs veterinary research through a national network of specialty hospitals. Because the same organization includes oncologists, laboratories and participating clinics, a study can move from an idea to enrollment and follow-up without sending every pet to a university hospital.",
    "European multicenter study — Floryne Buishand": "This European research group is led by veterinary surgical oncologist Floryne Buishand and works through several participating hospitals. The group studies difficult cancers that need both surgery and drug treatment, allowing owners to use the nearest active study site.",
    "Evergreen Animal Hospital": "Evergreen Animal Hospital in Taiwan provides companion-animal care and has an active clinical-research program for dogs with cancer. The hospital works with outside research teams so screening, treatment and follow-up can be performed in a regular veterinary setting.",
    "Ghent University Faculty of Veterinary Medicine": "Ghent University's Small Animal Clinic is a teaching hospital with oncology, cancer surgery and advanced imaging. Its researchers are developing real-time optical tools that may help surgeons see the boundary between tumor and healthy tissue more clearly during an operation.",
    "Hospital Veterinario Peña Jasso": "Hospital Veterinario Peña Jasso in Ensenada combines clinical veterinary care with cancer research carried out with Mexican universities. The collaboration tests whether very small engineered particles can deliver treatment to tumors more selectively.",
    "Jimmy Harry Animal Hospital": "Jimmy Harry Animal Hospital in Taichung is one of the local clinics participating in Taiwan's veterinary cancer-research network. The hospital screens dogs, provides study treatment and follows patients while the research program is coordinated centrally.",
    "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)": "Johns Hopkins CIGAT treats animals inside a major human academic medical center. Its veterinarians and radiologists adapt MRI, CT, focused ultrasound and other image-guided procedures so tumors can be targeted through small or no incisions.",
    "Louisiana State University School of Veterinary Medicine": "LSU combines its veterinary cancer service with centers for clinical innovation and comparative oncology. Its teams study treatments given directly into tumors and use naturally occurring cancers in pets to answer questions relevant to both veterinary and human medicine.",
    "MedVet Clinical Studies Center": "MedVet coordinates clinical studies across its network of specialty hospitals. Board-certified oncologists test new cancer drugs, vaccines, diagnostic tests and devices while patients continue to receive care at a participating MedVet location.",
    "Michigan State University College of Veterinary Medicine": "Michigan State's oncology service treats dogs and cats while running a broad program of cancer research. Its teams study lymphoma, mast cell tumors, histiocytic sarcoma and other aggressive cancers, with laboratory scientists and hospital oncologists working together.",
    "Multicenter local T-cell-engager STS immunotherapy": "This research program brings together several US veterinary hospitals to test a treatment placed directly into a tumor before surgery. The goal is to draw the dog's own immune cells into the cancer while limiting treatment to the affected area.",
    "National Chung Hsing University Veterinary Teaching Hospital": "National Chung Hsing University Veterinary Teaching Hospital is an academic referral center in Taichung. It combines specialist care with university research and gives dogs in central Taiwan access to cancer studies that require hospital screening and follow-up.",
    "National Taiwan University Veterinary Hospital": "National Taiwan University Veterinary Hospital is a major academic referral center in Taipei. Its specialists combine cancer care with university research and collaborate with biotechnology teams developing immune-based treatments for dogs.",
    "NC State College of Veterinary Medicine": "NC State's Animal Cancer Care and Research Program brings medical oncology, surgery and radiation therapy together with laboratory research. The college is also known for its canine bone-marrow transplant program, developed as an option for selected dogs with lymphoma.",
    "North Downs Specialist Referrals": "North Downs Specialist Referrals is a multidisciplinary hospital in Surrey with medical oncology, radiation therapy, surgery and advanced imaging. Its cancer team also contributes patients and clinical expertise to research organized across UK and European hospitals.",
    "Ohio State University College of Veterinary Medicine": "Ohio State has a large comparative oncology program linking its veterinary hospital with the university's human cancer center. Work by its veterinary researchers helped develop toceranib, sold as Palladia, the first cancer drug approved by the FDA specifically for dogs.",
    "Ontario Veterinary College / Hospital for Sick Children": "The Ontario Veterinary College and Toronto's Hospital for Sick Children share imaging and cancer expertise across veterinary and human medicine. Their joint work applies MRI-guided focused ultrasound to tumors without making a surgical incision.",
    "Ontario Veterinary College — University of Guelph": "The Ontario Veterinary College is Canada's oldest veterinary school and runs a broad companion-animal cancer program. Its researchers work on drug treatment, radiation and light-activated therapies, including methods designed specifically for difficult oral tumors.",
    "PETcura (宝科雅) multicenter IIT": "PETcura develops personalized cancer vaccines for dogs using genetic information from an individual tumor. Its multicenter research program works with veterinary hospitals in China to prepare the treatment and monitor each patient.",
    "Protect Animal Health (寶泰生醫) multicenter field trial": "Protect Animal Health is a Taiwanese biotechnology company developing immune treatments for dogs with cancer. It coordinates a network of veterinary hospitals so a new treatment can be tested in patients under everyday clinical conditions.",
    "Purdue University College of Veterinary Medicine": "Purdue's Comparative Oncology Program connects the veterinary teaching hospital with cancer scientists across the university. Its teams have studied immune treatments, cancer vaccines and focused ultrasound while caring for dogs and cats with naturally occurring tumors.",
    "Schwarzman Animal Medical Center": "The Schwarzman Animal Medical Center in New York is one of the world's largest nonprofit animal hospitals. Its Cancer Institute combines medical oncology, surgery and radiation therapy and uses its large clinical caseload to support veterinary cancer research.",
    "Texas A&M School of Veterinary Medicine": "Texas A&M's veterinary teaching hospital combines specialist cancer care with a long-running comparative oncology program. Its researchers study lymphoma, bone cancer, cancer detection and new treatments with support from a dedicated clinical-investigation office.",
    "Tufts University Cummings School of Veterinary Medicine": "Tufts' Harrington Oncology Service combines medical oncology, radiation therapy and cancer surgery at Foster Hospital. Its Clinical Trials Office, led by veterinary oncologist Cheryl London, is especially active in immune treatments, targeted drugs and cancers that also occur in people.",
    "UC Davis Veterinary Center for Clinical Trials": "UC Davis created a dedicated center to coordinate clinical studies at its veterinary teaching hospital. Its cancer researchers are especially known for work on how tumors spread and for moving new drugs and diagnostic methods from the laboratory into studies with companion animals.",
    "University Hospital for Companion Animals, University of Copenhagen / Lund University": "The University of Copenhagen's animal hospital and Lund University combine veterinary cancer care with radiation research. Their shared program is studying very fast radiation delivery, called FLASH, in hopes of treating tumors while causing less damage to nearby healthy tissue.",
    "University of Florida College of Veterinary Medicine": "The University of Florida runs medical and radiation oncology studies through its veterinary hospitals. Its researchers work on cancer vaccines, immune treatments and targeted drugs, moving promising ideas from the laboratory into carefully monitored treatment studies.",
    "University of Georgia College of Veterinary Medicine": "The University of Georgia's teaching hospital provides medical, surgical and radiation oncology in one service. Its comparative cancer researchers are particularly active in lymphoma, bladder cancer and testing new treatments for companion animals.",
    "University of Illinois College of Veterinary Medicine": "Illinois combines its Cancer Care Clinic with a large comparative oncology research group. Its teams study cancer vaccines, immune and cell therapies, radiation combinations and ways to carry treatment directly to a tumor.",
    "University of Milan Veterinary Teaching Hospital (Lodi)": "The University of Milan's teaching hospital in Lodi combines referral oncology with drug-development research. Its teams test targeted treatments designed to carry a cancer-killing drug into the tissue that supports a tumor while reducing exposure elsewhere in the body.",
    "University of Minnesota College of Veterinary Medicine": "Minnesota's Animal Cancer Care and Research Program links its veterinary hospital with the Masonic Cancer Center. The Modiano laboratory and clinical teams are widely known for comparative research on lymphoma, bone cancer and hemangiosarcoma.",
    "University of Missouri College of Veterinary Medicine": "Missouri's veterinary hospital brings medical oncology, cancer surgery and radiation therapy into one program. Its clinicians work with university cancer scientists to test new treatments while also providing standard care for dogs and cats.",
    "University of Pennsylvania School of Veterinary Medicine": "Penn Vet links cancer care at Ryan Hospital with the Penn Vet Cancer Center and laboratories across the university. Nicola Mason's team is known for adapting CAR-T and other immune-cell treatments for dogs, helping connect veterinary trials with advances in human cancer medicine.",
    "University of Évora Veterinary Hospital": "The University of Évora Veterinary Hospital combines clinical care with veterinary teaching and research in Portugal. Its oncology work includes photodynamic therapy, which uses a light-activated medicine to damage tumor cells in a precisely illuminated area.",
    "University of Zurich Veterinary Hospital": "The University Animal Hospital Zurich provides medical oncology and modern image-guided radiation therapy for dogs and cats. Its clinical researchers study how to target tumors accurately while protecting nearby normal tissue.",
    "UT Southwestern Veterinary Radiation Oncology Clinic (VROC)": "UT Southwestern's veterinary clinic places dogs and cats inside the research environment of a major human cancer center. Its teams study radiation, focused ultrasound, tumor-destroying sound waves, immune treatments and drug combinations for naturally occurring cancers.",
    "UT Southwestern Veterinary Research and Oncology Clinic": "UT Southwestern's veterinary clinic places dogs and cats inside the research environment of a major human cancer center. Its teams study radiation, focused ultrasound, tumor-destroying sound waves, immune treatments and drug combinations for naturally occurring cancers.",
    "VetAgro Sup CHUVAC": "VetAgro Sup's companion-animal hospital near Lyon is a university referral center with specialist cancer care and clinical research. Its teams study treatments placed directly into oral tumors to produce a local effect and stimulate the immune system.",
    "Veterinary Referral Center of Central Oregon": "The Veterinary Referral Center of Central Oregon provides specialty oncology outside a university setting. Its oncologists join multicenter studies so pets in central Oregon can reach new cancer treatments without traveling to a distant academic hospital.",
    "Virginia-Maryland College of Veterinary Medicine / Virginia Tech": "Virginia Tech's veterinary teaching hospital runs cancer studies through a dedicated Clinical Research Office. The office connects pet owners, hospital specialists and laboratory researchers testing new ways to diagnose and treat naturally occurring disease.",
    "Washington State University College of Veterinary Medicine": "Washington State's teaching hospital combines chemotherapy, cancer surgery and radiation therapy with clinical research. Its current immunotherapy work uses treatment placed inside a tumor to attract the dog's own cancer-fighting immune cells before surgery.",
    "Woke Animal Hospital": "Woke Animal Hospital in Taichung helps bring veterinary cancer research to dogs treated in a community hospital. Its clinicians screen patients, administer study treatment and provide follow-up in cooperation with the team coordinating the research.",
    "Zhongnong Dongjun Laboratory": "Zhongnong Dongjun Laboratory develops experimental medicines for companion-animal cancers in China. It works with treating hospitals to test drug candidates in dogs while collecting the safety and response information needed for further development.",
}
for _name, _copy in CENTER_ABOUT.items():
    if _name in PROFILES:
        PROFILES[_name]["about"] = _copy
CURRENT={'current','confirmed_current'}

RESEARCH_ORGANIZATIONS = {
    "Anivive Lifesciences — multicenter",
    "Aurelius Biotherapeutics",
    "Protect Animal Health (寶泰生醫) multicenter field trial",
    "Zhongnong Dongjun Laboratory",
}
MULTICENTER_STUDIES = {
    "European multicenter study — Floryne Buishand",
    "Multicenter local T-cell-engager STS immunotherapy",
    "PETcura (宝科雅) multicenter IIT",
}


def center_type(center):
    if center in MULTICENTER_STUDIES:
        return "Multicenter Study"
    if center in RESEARCH_ORGANIZATIONS:
        return "Research Organization"
    if any(term in center for term in ("University", "College of Veterinary Medicine", "School of Veterinary Medicine")):
        return "University / Teaching Hospital"
    return "Specialty Hospital / Research Center"


def center_page_title(center):
    kind = center_type(center)
    if kind == "Multicenter Study":
        return f"{center} | Veterinary Cancer Study | Vet Trial Finder"
    if kind == "Research Organization":
        return f"{center} | Veterinary Cancer Research | Vet Trial Finder"
    return f"{center} | Veterinary Oncology & Clinical Trials | Vet Trial Finder"


def center_page_description(center):
    kind = center_type(center)
    if kind == "Multicenter Study":
        return f"Current veterinary cancer treatment study information, participating locations, eligibility details and official links for {center}."
    if kind == "Research Organization":
        return f"Current veterinary cancer research and treatment opportunities from {center}, with eligibility details, contacts and official links."
    return f"Veterinary oncology services, cancer clinical trials and current treatment opportunities at {center}."


def merge(old,patch):
    new=dict(old)
    for k,v in patch.items():
        if k in {'requires','excludes'} and isinstance(v,dict):
            x=dict(new.get(k,{}) if isinstance(new.get(k),dict) else {});x.update(v);new[k]=x
        else:new[k]=v
    return new


def load_effective():
    base=json.loads((g.ROOT/'data'/'trials_base.json').read_text());rows={r['id']:r for r in base}
    paths=[g.ROOT/'data'/'trial_updates.json']+sorted((g.ROOT/'data').glob('catalog_patch_*.json'))
    for path in paths:
        if not path.exists():continue
        doc=json.loads(path.read_text())
        for rid in doc.get('delete',[]):rows.pop(rid,None)
        for p in doc.get('upsert',[]):rows[p['id']]=merge(rows.get(p['id'],{}),p)
    return [r for r in rows.values() if r.get('study_type')=='treatment' and r.get('available_for_matching') is True and r.get('status_confidence') in CURRENT]
g.load_effective=load_effective


def phrase(needle,text):
    needle=g.norm(needle);text=g.norm(text);return bool(needle and re.search(r'(?<![a-z0-9])'+re.escape(needle)+r'(?![a-z0-9])',text))
def canonical_cancer(v):
    raw=g.norm(v)
    if not raw or any(phrase(x,raw) for x in g.GENERIC_WORDS):return None
    for key,aliases in g.CANONICAL_RULES:
        if any(phrase(a,raw) for a in aliases):return key
    return None
def cancer_values(r):
    v=r.get('cancers',[]);return [v] if isinstance(v,str) else list(v) if isinstance(v,(list,tuple,set)) else []
def row_cancers(r):return {x for x in (canonical_cancer(v) for v in cancer_values(r)) if x}
g.canonical_cancer=canonical_cancer;g.row_cancers=row_cancers


def site_active(s):
    return isinstance(s,dict) and s.get('available_for_matching') is not False and not any(x in g.norm(s.get('status','')) for x in ('not enrolling','enrollment closed','closed','paused'))


def site_is_coverage_placeholder(s):
    """True for coverage records that name a city/network but not a real hospital."""
    name=normalize(s.get('hospital') or s.get('name') or '')
    return 'partner hospital' in name or name in {'participating hospital','participating hospitals','partner site','partner sites'}


def embedded_address(obj,country=''):
    a=str(obj.get('address') or '').strip();city=str(obj.get('city') or '').strip();state=str(obj.get('state') or '').strip();z=str(obj.get('zip') or obj.get('zipcode') or obj.get('postal_code') or '').strip()
    candidates=[]
    if a:candidates.append(a)
    if a and city:
        tail=', '.join(x for x in (city,state) if x)
        if z:tail=(tail+' '+z).strip()
        candidates.append(f'{a}, {tail}')
    for detail in reversed(candidates):
        if address_is_complete(detail,country):return detail
    return ''


def site_labels(s,country=''):
    known=[x for x in addresses_for(s.get('hospital') or s.get('name') or '') if address_is_complete(x,country)]
    if known:return known
    detail=embedded_address(s,country)
    if not detail:return []
    name=str(s.get('hospital') or s.get('name') or '').strip()
    return [f'{name}, {detail}' if name and normalize(name) not in normalize(detail) else detail]


def row_locations(r):
    country=str(r.get('country') or '')
    vals=[]
    for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
        if site_active(s) and not site_is_coverage_placeholder(s):vals.extend(site_labels(s,country))
    if not vals:
        vals.extend(x for x in addresses_for(r.get('center','')) if address_is_complete(x,country))
    if not vals:
        own=embedded_address(r,country)
        if own:vals.append(own)
    out=[];seen=set()
    for x in vals:
        k=normalize(x)
        if k not in seen:seen.add(k);out.append(x)
    return out


def coverage_areas(r):
    out=[];seen=set();country=str(r.get('country') or '')
    for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
        if not (site_active(s) and site_is_coverage_placeholder(s)):continue
        pieces=[str(s.get(k) or '').strip() for k in ('city','state')]
        label=', '.join(x for x in pieces if x)
        if country and normalize(country) not in normalize(label):label=', '.join(x for x in (label,country) if x)
        if not label:label='Participating hospital assigned by the study team'
        key=normalize(label)
        if key not in seen:seen.add(key);out.append(label)
    return out


def region_for(country):
    c=normalize(country)
    if c in {'usa','united states','united states of america','canada','mexico'}:return 'North America'
    if c in {'uk','united kingdom','england','scotland','wales','ireland','france','germany','italy','spain','portugal','belgium','netherlands','switzerland','austria','poland','czechia','denmark','sweden','norway','finland','hungary','slovenia','cyprus'}:return 'UK / Europe'
    return str(country or 'Other')


def is_composite_center(name):
    raw=str(name or '').lower();n=normalize(name)
    return '/' in raw or '+' in raw or any(x in n for x in ('multicenter','multicentre','field trial','partner network','research network'))


def institution_like(name):
    if is_composite_center(name):return False
    n=normalize(name)
    return any(x in n for x in ('university','college','school of veterinary','teaching hospital','animal medical center'))


def preflight(rows):
    missing_sites=[];missing_centers=[];coverage=[];seen_sites=set();seen_centers=set();seen_coverage=set();covered_sites=0
    for r in rows:
        rid=str(r.get('id') or '?');country=str(r.get('country') or '');center=str(r.get('center') or '').strip()
        if center:
            ck=(normalize(center),normalize(country))
            if ck not in seen_centers:
                seen_centers.add(ck)
                addrs=addresses_for(center);own=embedded_address(r,country)
                if institution_like(center) and not (any(address_is_complete(a,country) for a in addrs) or address_is_complete(own,country)):
                    missing_centers.append({'name':center,'country':country,'region':region_for(country),'trial_id':rid})
        for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
            if not site_active(s):continue
            name=str(s.get('hospital') or s.get('name') or '').strip() or '(unnamed site)'
            if site_is_coverage_placeholder(s):
                key=(normalize(name),normalize(s.get('city')),normalize(country))
                if key not in seen_coverage:
                    seen_coverage.add(key);coverage.append({'name':name,'city':s.get('city'),'state':s.get('state'),'country':country,'trial_id':rid})
                continue
            sk=(normalize(name),normalize(country))
            if sk in seen_sites:continue
            seen_sites.add(sk)
            if site_labels(s,country):covered_sites+=1
            else:missing_sites.append({'name':name,'country':country,'region':region_for(country),'trial_id':rid})
    report={
        'effective_treatment_records':len(rows),'directory_locations':len(LOCATIONS),'unique_centers':len(seen_centers),
        'unique_active_physical_sites':len(seen_sites),'covered_active_physical_sites':covered_sites,
        'coverage_placeholders':coverage,'missing_center_addresses':missing_centers,'missing_participating_site_addresses':missing_sites,
    }
    print('ADDRESS_PREFLIGHT',json.dumps({'centers':len(seen_centers),'physical_sites':len(seen_sites),'coverage_placeholders':len(coverage),'missing_centers':len(missing_centers),'missing_sites':len(missing_sites)},sort_keys=True))
    if missing_centers or missing_sites:
        raise AssertionError('Address preflight failed: '+json.dumps({'centers':missing_centers,'sites':missing_sites},ensure_ascii=False,sort_keys=True))
    return report


def cards(rows):
    out=[]
    for r in rows:
        p=[f'<article class="card"><h3>{g.esc(r.get("title"))}</h3><p class="meta"><strong>{g.esc(r.get("center"))}</strong> · {g.esc(r.get("country"))}</p>']
        if r.get('status'):p.append(f'<p class="status">{g.esc(r["status"])}</p>')
        treatment=g.prose(r.get('intervention') or r.get('treatment') or r.get('notes'))
        if treatment:p.append(f'<p><b>What is being offered:</b> {g.esc(treatment)}</p>')
        req=g.prose(r.get('requires'));exc=g.prose(r.get('excludes'));fund=g.prose(r.get('funding'));contact=g.contact_text(r)
        if req:p.append(f'<p><b>Who may qualify:</b> {g.esc(req)}</p>')
        if exc:p.append(f'<p><b>May not qualify if:</b> {g.esc(exc)}</p>')
        if fund:p.append(f'<p><b>Costs / coverage:</b> {g.esc(fund)}</p>')
        if contact:p.append(f'<p><b>Contact:</b> {g.esc(contact)}</p>')
        locs=row_locations(r)
        if locs:p.append('<div class="study-locations"><p class="field-label">'+('Location' if len(locs)==1 else 'Participating locations')+'</p><ul>'+''.join(f'<li>{g.esc(x)}</li>' for x in locs)+'</ul></div>')
        areas=coverage_areas(r)
        if areas:p.append('<div class="enrollment-areas"><p class="field-label">Enrollment area</p><ul>'+''.join(f'<li>{g.esc(x)}</li>' for x in areas)+'</ul><p class="coverage-note">The public study listing names a partner-hospital network rather than a specific hospital. Confirm the assigned hospital with the study team.</p></div>')
        if r.get('last_verified'):p.append(f'<p class="verified">Last verified: {g.esc(r["last_verified"])}</p>')
        if r.get('url'):p.append(f'<p><a class="official" href="{g.esc(r["url"])}" rel="noopener">Official study / enrollment information →</a></p>')
        p.append('</article>');out.append(''.join(p))
    return ''.join(out)
g.cards=cards

base_page=g.page
def page(title,desc,body,canonical,lang='en',alts=None):
    rendered=base_page(title,desc,body,canonical,lang,alts)
    css='body{font-size:16px}.center-page{max-width:860px}.center-page h1{font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.06;margin:18px 0 8px}.center-page>h2{font-size:1.35rem;line-height:1.08;margin:22px 0 8px}.center-kicker{color:#607086;font-size:.95rem;font-weight:650;margin:0 0 20px}.center-overview{display:grid;grid-template-columns:minmax(0,1fr) minmax(240px,38%);grid-template-areas:"heading heading" "copy image";gap:10px 24px;align-items:start;margin:0 0 22px}.center-overview>h2{grid-area:heading;font-size:1.18rem;margin:0 0 4px}.center-overview-copy{grid-area:copy}.center-overview-copy p{margin:.55rem 0;line-height:1.55}.center-overview figure{grid-area:image;margin:0;width:100%}.center-overview figure img{width:100%!important;max-width:none!important;aspect-ratio:4/3;object-fit:cover;border-radius:12px;display:block}.center-overview figcaption{font-size:.78rem!important;line-height:1.3}.center-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0 22px}.center-fact{background:#fff;border:1px solid #d9e2ea;border-radius:10px;padding:12px 14px;font-size:.94rem;line-height:1.45}.center-fact strong{display:block;color:#356d89;margin-bottom:4px}.center-note{border-top:1px solid #d9e2ea;padding:10px 0 0;margin:18px 0 8px;color:#607086}.center-note summary{cursor:pointer;font-size:.82rem;font-weight:650;color:#607086}.center-note p{font-size:.8rem;line-height:1.45;margin:.45rem 0;max-width:720px}.opportunity-list{display:grid;gap:12px}.opportunity{background:#fff;border:1px solid #d9e2ea;border-radius:12px;overflow:hidden}.opportunity summary{cursor:pointer;list-style:none;padding:14px 16px;font-weight:700;color:#274f65}.opportunity summary::-webkit-details-marker{display:none}.opportunity summary:after{content:"+";float:right;font-size:1.25rem;font-weight:400}.opportunity[open] summary:after{content:"−"}.opportunity .card{border:0;border-top:1px solid #e2e9ee;border-radius:0;margin:0;box-shadow:none}.study-locations,.enrollment-areas{margin:14px 0 4px;padding:11px 13px;background:#f6f8fb;border-radius:9px}.study-locations ul,.enrollment-areas ul{margin:5px 0 0;padding-left:20px}.field-label{font-weight:750;margin:0}.coverage-note,.source-note{font-size:.84rem;color:#607086}.free-note{font-size:.8rem;color:#607086}.card p{margin:.65rem 0}.center-search-link{display:inline-block;margin-top:20px;font-weight:700}@media(max-width:700px){.center-page{font-size:16px}.center-page h1{font-size:1.5rem;line-height:1.06;margin-top:12px}.center-page>h2{font-size:1.28rem;line-height:1.08;margin-top:20px}.center-kicker{font-size:.95rem;margin-bottom:16px}.center-overview{display:flex;flex-direction:column;gap:0}.center-overview>h2{font-size:1.22rem;margin-bottom:10px}.center-overview figure{order:2;margin:0 0 10px}.center-overview-copy{order:3}.center-overview figure img{aspect-ratio:16/9;border-radius:10px}.center-overview-copy p{margin:.5rem 0;line-height:1.55;font-size:1rem}.center-facts{display:block;background:#fff;border:1px solid #d9e2ea;border-radius:11px;padding:2px 14px;margin:14px 0 20px}.center-fact{border:0;border-bottom:1px solid #e4eaee;border-radius:0;padding:11px 0;font-size:1rem}.center-fact:last-child{border-bottom:0}.center-fact strong{margin-bottom:2px}.center-note{margin:16px 0 6px}.opportunity summary{padding:14px;font-size:1rem}}'
    return rendered.replace('</style>',css+'</style>',1)
g.page=page

ETHOS_NETWORK = "Ethos Veterinary Health / Ethos Discovery"
ETHOS_HOSPITALS = {
    "Atlantic Veterinary Internal Medicine & Oncology", "CARE Center Cincinnati",
    "Colorado Animal Specialty & Emergency (CASE)", "First Coast Veterinary Specialists & Emergency",
    "Gulf Coast Veterinary Specialists", "Massachusetts Veterinary Referral Hospital",
    "Mission Veterinary Emergency & Specialty", "Peak Veterinary Referral Center",
    "Pet Emergency and Specialty Center of Marin", "SAGE Veterinary Centers",
    "Veterinary Specialty Hospital - North County", "Veterinary Specialty Hospital - Sorrento Valley",
    "WVRC Grafton", "WVRC Racine Kenosha", "WVRC Waukesha",
    "Metropolitan Veterinary Hospital", "Metropolitan Veterinary Hospital - Akron",
    "Summit Veterinary Referral Center", "Veterinary Specialty Hospital",
    "Veterinary Specialty Hospital – North County", "Veterinary Specialty Hospital – Sorrento Valley",
    "Overland Park Veterinary Emergency & Specialty",
    "Southeast Veterinary Oncology & Internal Medicine",
    "Veterinary Emergency + Referral Center",
    "WVRC – Grafton", "WVRC – Racine/Kenosha", "WVRC – Waukesha",
    "SAGE", "SAGE – San Francisco", "CASE",
}

CENTER_RULES=(
('Hospital Veterinario Peña Jasso',('hospital veterinario peña jasso','hospital veterinario pena jasso')),('Colorado State University Flint Animal Cancer Center',('colorado state university','flint animal cancer center')),('University of Florida College of Veterinary Medicine',('university of florida',)),('Michigan State University College of Veterinary Medicine',('michigan state university',)),('Auburn University College of Veterinary Medicine',('auburn university',)),('University of Pennsylvania School of Veterinary Medicine',('university of pennsylvania','penn vet')),('Tufts University Cummings School of Veterinary Medicine',('tufts university','tufts cummings')),('NC State College of Veterinary Medicine',('nc state','north carolina state university')),('University of Missouri College of Veterinary Medicine',('university of missouri',)),('University of Illinois College of Veterinary Medicine',('university of illinois',)),('Purdue University College of Veterinary Medicine',('purdue university',)),('Cornell University College of Veterinary Medicine',('cornell university',)),('University of Minnesota College of Veterinary Medicine',('university of minnesota',)),('Ohio State University College of Veterinary Medicine',('ohio state university','the ohio state university')),('Texas A&M School of Veterinary Medicine',('texas a&m','texas a and m')),('Louisiana State University School of Veterinary Medicine',('louisiana state university','lsu')),('University of Georgia College of Veterinary Medicine',('university of georgia',)),('Washington State University College of Veterinary Medicine',('washington state university',)),('UC Davis Veterinary Center for Clinical Trials',('uc davis veterinary center for clinical trials','uc davis veterinary medical teaching hospital','uc davis')),('Aurelius Biotherapeutics',('aurelius biotherapeutics',)),('Ethos Veterinary Health / Ethos Discovery',('ethos veterinary health','ethos discovery')),('Colorado Animal Specialty & Emergency (CASE)',('colorado animal specialty','case / ethos discovery')),('Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)',('johns hopkins center for image-guided animal therapy',)),('SAGE Veterinary Centers',('sage san francisco','sage veterinary')),
)
def canonical_center(v):
    raw=str(v or '').strip()
    if raw in ETHOS_HOSPITALS:return ETHOS_NETWORK
    known=canonical_name_for(raw)
    if known:return known
    text=normalize(raw)
    for name,aliases in CENTER_RULES:
        if any(normalize(a) in text for a in aliases):return name
    return re.sub(r'\s+',' ',raw) if raw else None


def profile(center):
    p=PROFILES.get(center)
    if p:return p
    if is_composite_center(center):
        about=(f'This page groups the current cancer studies in our catalog that are coordinated by {center}. '
            'A multicenter listing does not mean visits happen at one central address; the participating hospital or enrollment area is shown inside each option when it is publicly available.')
    else:
        about=(f'This page brings together current cancer studies and treatment options in our catalog that name {center} as the main center or a participating hospital. '
            'It is not a complete list of every oncology service the center may offer.')
    return {'title':'','about':about,'links':[]}


def overview(center):
    p=profile(center);fig=''
    if p.get('image'):fig=f'<figure><img src="{g.esc(p["image"])}" alt="{g.esc(p.get("image_alt") or center)}" loading="lazy">'+(f'<figcaption>{g.esc(p.get("image_caption"))}</figcaption>' if p.get('image_caption') else '')+'</figure>'
    # The overview is one self-contained paragraph. Trial counts, diagnoses and
    # current-study details already have their own structured sections below.
    primary_link=next(iter(p.get('links',[])),None)
    links=(f'<a href="{g.esc(primary_link[1])}" rel="noopener">{g.esc(primary_link[0])} →</a>'
        if primary_link else '')
    heading=f'<h2>{g.esc(p["title"])}</h2>' if p.get('title') else ''
    intro=str(p.get('about') or '').strip()
    copy=f'<div class="center-overview-copy"><p>{g.esc(intro)}</p>'+(f'<p class="center-source">{links}</p>' if links else '')+'</div>'
    return f'<div class="center-overview{" has-image" if fig else ""}">{heading}{fig}{copy}</div>'


def species_for(rows):
    found=[]
    for label in ('Dog','Cat'):
        if any(g.species_ok(r,label) for r in rows):found.append(label.lower()+'s')
    return found


def center_kind(center,rows):
    if is_composite_center(center) or any(coverage_areas(r) for r in rows):return 'Multicenter program or hospital network'
    n=normalize(center)
    if any(x in n for x in ('university','college','school','teaching hospital')):return 'University or teaching hospital'
    return 'Specialty hospital or research center'


def owner_summary(center,rows,cancers,addresses):
    species=species_for(rows)
    species_text=' and '.join(species) if species else 'companion animals'
    cancer_text=', '.join(g.display_name(c) for c in cancers) if cancers else 'Cancer diagnoses listed in the studies below'
    location_fact=(
        '<div class="center-fact"><strong>Where visits take place</strong>'
        + '<br>'.join(g.esc(x) for x in addresses)
        + '</div>'
        if addresses else ''
    )
    return ('<div class="center-facts">'
        f'<div class="center-fact"><strong>Who the current listings are for</strong>{g.esc(species_text.capitalize())}</div>'
        f'<div class="center-fact"><strong>Cancer types currently listed</strong>{g.esc(cancer_text)}</div>'
        f'{location_fact}'
        '</div>')


def center_cards(rows):
    rendered=[]
    for row in rows:
        title=g.esc(row.get('title') or 'Cancer treatment opportunity')
        card=cards([row])
        card=re.sub(r'(<article class="card">)<h3>.*?</h3>',r'\1',card,count=1,flags=re.S)
        rendered.append(f'<details class="opportunity"><summary>{title}</summary>{card}</details>')
    return '<div class="opportunity-list">'+''.join(rendered)+'</div>'


def add(grouped,name,row):
    name=canonical_center(name)
    if not name:return
    b=grouped.setdefault(name,[])
    if not any(x.get('id')==row.get('id') for x in b):b.append(row)


def center_page_addresses(center,hit):
    country=str(hit[0].get('country') or '') if hit else ''
    known=[x for x in addresses_for(center) if address_is_complete(x,country)]
    if known:return known
    for r in hit:
        if canonical_center(r.get('center'))==center:
            own=embedded_address(r,str(r.get('country') or ''))
            if own:return [own]
    return []


def safe_center_slug(center,used):
    base=g.slugify(center.replace('College of Veterinary Medicine','').replace('School of Veterinary Medicine',''))
    digest=hashlib.sha1(center.encode('utf-8')).hexdigest()[:8]
    if not base:base=f'center-{digest}'
    slug=base
    if slug in used and used[slug]!=center:slug=f'{base}-{digest}'
    return slug


def ethos_sections(hit):
    branches={}
    for r in hit:
        for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
            if not site_active(s) or site_is_coverage_placeholder(s):continue
            name=str(s.get('hospital') or s.get('name') or '').strip()
            if name not in ETHOS_HOSPITALS:continue
            entry=branches.setdefault(name,{'rows':[],'locations':[]})
            if not any(x.get('id')==r.get('id') for x in entry['rows']):entry['rows'].append(r)
            for loc in site_labels(s,str(r.get('country') or '')):
                if loc not in entry['locations']:entry['locations'].append(loc)
    out=['<div class="network-branches"><h2>Participating Ethos hospitals</h2><p class="source-note">Open a hospital to see its current options and location.</p>']
    for name,entry in sorted(branches.items()):
        out.append(f'<section class="network-branch" id="{g.slugify(name)}"><h3>{g.esc(name)}</h3>')
        if entry['locations']:out.append('<p class="branch-location">'+ '<br>'.join(g.esc(x) for x in entry['locations'])+'</p>')
        out.append(center_cards(entry['rows'])+'</section>')
    out.append('</div>')
    return ''.join(out)


def write_redirect(path,target,title):
    d=g.OUT/path;d.mkdir(parents=True,exist_ok=True)
    doc=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{g.esc(target)}"><meta http-equiv="refresh" content="0; url={g.esc(target)}"><title>{g.esc(title)}</title></head><body><p>This hospital is now listed on the <a href="{g.esc(target)}">Ethos Veterinary Health page</a>.</p></body></html>'
    (d/'index.html').write_text(doc,encoding='utf-8')


def generate_centers(rows):
    rows=[r for r in rows if str(r.get('center','')).strip()];grouped={}
    for r in rows:
        add(grouped,r.get('center'),r)
        for s in r.get('sites',[]) if isinstance(r.get('sites'),list) else []:
            if site_active(s) and not site_is_coverage_placeholder(s) and (s.get('hospital') or s.get('name')):add(grouped,s.get('hospital') or s.get('name'),r)
    links=[];items=[];used={}
    for center,hit in sorted(grouped.items()):
        slug=safe_center_slug(center,used);used[slug]=center;path=f'centers/{slug}/';url=f'{g.SITE}/{path}'
        cancers=sorted({c for r in hit for c in row_cancers(r)});ct=', '.join(g.display_name(c) for c in cancers) or 'multiple cancer types'
        addrs=center_page_addresses(center,hit)
        count=len(hit);noun='opportunity' if count==1 else 'opportunities'
        body=('<div class="center-page">'
            f'<h1>{g.esc(center)}</h1><p class="center-type">{g.esc(center_type(center))}</p><p class="center-kicker">{count} current cancer treatment or research {noun}</p>'
            +overview(center)+owner_summary(center,hit,cancers,addrs)
            +(ethos_sections(hit) if center==ETHOS_NETWORK else f'<h2>Current options at {g.esc(center)}</h2><p class="source-note">Open an option to see who may qualify, locations, costs or coverage, contact details and the official source.</p>'+center_cards(hit))
            +'<details class="center-note"><summary>Before you contact the center</summary>'
            +'<p>A listing here does not mean every pet will qualify. Enrollment can change, and the study team makes the final decision after reviewing your pet’s diagnosis, records and previous treatment.</p>'
            +'<p>Have the pathology report, recent imaging and treatment history ready. Ask whether a referral is required, which visits must happen in person and what the study pays for before making travel plans.</p></details>'
            +f'<p><a class="center-search-link" href="{g.FINDER}">Check all options for your pet →</a></p><p class="free-note">Free to use. No registration or paid report.</p></div>')
        title=center_page_title(center);desc=center_page_description(center)
        d=g.OUT/path;d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(g.page(title,desc,body,url),encoding='utf-8');links.append(url);items.append((center,path,len(hit),center_type(center)))
        if center==ETHOS_NETWORK:
            for hospital in ETHOS_HOSPITALS:
                write_redirect(f'centers/{safe_center_slug(hospital,{})}/',url+'#'+g.slugify(hospital),hospital)
    assert len(used)==len(grouped),(len(used),len(grouped))
    iu=f'{g.SITE}/centers/';ib='<h1>Oncology Centers &amp; Research Programs</h1><p class="lead">Browse universities, teaching hospitals, specialty hospitals, research organizations and multicenter studies with current cancer treatment opportunities.</p><ul>'+''.join(f'<li><a href="{g.SITE}/{p}">{g.esc(n)}</a> <span class="entity-type">{g.esc(kind)}</span> — {c} current opportunities</li>' for n,p,c,kind in items)+'</ul>'
    d=g.OUT/'centers';d.mkdir(parents=True,exist_ok=True);(d/'index.html').write_text(g.page('Veterinary Oncology Centers & Research Programs | Vet Trial Finder','Veterinary oncology centers, research organizations, multicenter studies and current cancer treatment opportunities.',ib,iu),encoding='utf-8')
    sm=g.OUT/'sitemap.xml';s=sm.read_text();sm.write_text(s.replace('</urlset>',''.join(f'<url><loc>{g.esc(u)}</loc></url>\n' for u in [iu]+links)+'</urlset>'))
    print('CENTER_PAGES_OK',len(grouped))


def audit(report):
    pages=list(g.OUT.rglob('index.html'));assert pages
    invalid=[]
    for p in pages:
        s=p.read_text(errors='replace')
        for block in re.findall(r'<div class="study-locations">.*?</div>',s,re.S):
            for item in re.findall(r'<li>(.*?)</li>',block,re.S):
                text=html.unescape(re.sub(r'<.*?>','',item))
                if not address_is_complete(text,''):invalid.append({'page':str(p.relative_to(g.OUT)),'location':text})
    report['invalid_rendered_locations']=invalid
    center_pages=list((g.OUT/'centers').glob('*/index.html'))
    malformed=[]
    for p in center_pages:
        s=p.read_text(errors='replace')
        if 'noindex,follow' in s and 'http-equiv="refresh"' in s:continue
        required=('class="center-kicker"','class="center-facts"','Before you contact the center','class="opportunity-list"')
        if any(marker not in s for marker in required) or s.count('<details class="opportunity">')!=s.count('<article class="card">'):
            malformed.append(str(p.relative_to(g.OUT)))
    report['owner_friendly_center_pages']=len(center_pages)-len(malformed)
    report['malformed_center_pages']=malformed
    (g.OUT/'mapping-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    assert not invalid,invalid[:10]
    assert center_pages and not malformed,malformed[:10]
    print('CENTER_OWNER_PAGES_OK',len(center_pages))


def main():
    rows=g.load_effective();report=preflight(rows)
    g.main();enhance_cancer_pages(g.OUT)
    # The base generator writes center pages from raw catalog names. Rebuild the
    # directory from scratch after canonicalization so obsolete aliases cannot
    # survive as malformed, indexable pages in a clean production build.
    shutil.rmtree(g.OUT/'centers',ignore_errors=True)
    generate_centers(rows);audit(report)
if __name__=='__main__':main()
