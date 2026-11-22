#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

here = Path(__file__).resolve().parent
run_id = here.name
run_ref = f"research/audit-runs/{run_id}"
reviewed_at = datetime.now(ZoneInfo("America/New_York")).replace(microsecond=0).isoformat()

def read(name):
    return json.loads((here / name).read_text())

def write(name, value):
    (here / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

queries = []
for path in sorted(here.glob("discovery-search-*.json")):
    batch = read(path.name)
    for region, pass_name, country, language, query in batch["specs"]:
        queries.append({
            "region": region,
            "pass": pass_name,
            "country": country,
            "language": language,
            "query": query,
            "performed_at": reviewed_at,
            "evidence_refs": [f"{run_ref}/{path.name}"],
        })

def lead(url, disposition, reason, ids=None, evidence=None, **extra):
    row = {
        "url": url,
        "primary_url": extra.pop("primary_url", url),
        "disposition": disposition,
        "canonical_ids": ids or [],
        "reason": reason,
        "evidence_refs": evidence or [],
    }
    row.update(extra)
    if disposition == "VERIFIED_EXISTING" and "identity_comparison" not in row:
        row["identity_comparison"] = reason
    return row

s = lambda n: f"{run_ref}/discovery-search-{n:02d}.json"
a = f"{run_ref}/lead-open-a.json"
b = f"{run_ref}/lead-open-b.json"
c = f"{run_ref}/lead-open-c.json"
leads = [
    lead("https://vrcvet.com/clinical-trials/", "VERIFIED_EXISTING",
         "Fresh official roster says now enrolling and describes the same intratumoral T-cell-engager soft-tissue-sarcoma cohort, no placebo, surgery one week later.",
         ["wsu-sts-local-immunotherapy"], [s(1), a],
         identity_comparison="Same AVMA 534230 cohort already represented by wsu-sts-local-immunotherapy; castr-vrcco-sts-tcell-engager remains its hidden duplicate."),
    lead("https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/olaparib", "VERIFIED_EXISTING",
         "Fresh official protocol says Open and enrolling and matches the canonical feline mammary carcinoma olaparib-plus-meloxicam pilot.",
         ["umn-feline-mammary-olaparib-meloxicam"], [s(1), a]),
    lead("https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/trike-new", "VERIFIED_EXISTING",
         "The exact URL is canonical as umn-trike-sarcoma-2026; today's direct fallback returned 403 and therefore did not justify re-enabling the inactive record.",
         ["umn-trike-sarcoma-2026"], [s(9), a]),
    lead("https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/", "VERIFIED_EXISTING",
         "Fresh official page lists COTC033 Vaccine Peptide Library with the same 15–60 kg, 2–8 cm solid-tumor cohort already canonicalized as the multicenter COTC033 protocol.",
         ["csu-cotc033-vaccine-immunity"], [s(1), b]),
    lead("https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/", "PENDING_EVIDENCE",
         "This is a distinct UF treatment protocol, but the current official page simultaneously says currently recruiting and Enrollment Paused. It cannot be safely enabled or assigned the CSU protocol ID.",
         [], [s(6), a, b],
         missing_primary_reason="The protocol-level primary source contains contradictory current recruitment labels; keep unresolved pending a clarified official status."),
    lead("https://www.paccalvet.com/cat-cancer-study", "PENDING_EVIDENCE",
         "The exact official feline-treatment page was discovered but returned 401. Search text does not establish exact tumor cohort, sites, current intake, or relation to the sponsor's completed cohorts.",
         [], [s(6), a],
         missing_primary_reason="Exact current protocol identity and recruitment are unavailable from the inaccessible primary page."),
    lead("https://www.gamgee.io/trial/", "VERIFIED_EXISTING",
         "Fresh official page says the Australian personalized mRNA vaccine trial for dogs with mast-cell cancer is recruiting and maps exactly to the existing identity.",
         ["au-gamgee-personalized-mrna-vaccine"], [s(4), s(9), b]),
    lead("https://www.vm.a.u-tokyo.ac.jp/vmc/wp2/wp-content/uploads/2025/11/poster12.pdf", "VERIFIED_EXISTING",
         "Fresh Japanese protocol poster describes organoid-guided targeted therapy for measurable refractory solid tumors in dogs and cats and maps exactly to the existing Tokyo record.",
         ["jp-tokyo-organoid-guided-targeted-therapy-2026"], [s(6), b]),
    lead("https://www.egah.com.tw/news/%E6%8B%9B%E5%8B%9F%E7%8A%AC%E9%BB%91%E8%89%B2%E7%B4%A0%E7%98%A4%E5%8F%8A%E9%AA%A8%E8%82%89%E7%98%A4%E8%87%A8%E5%BA%8A%E8%A9%A6%E9%A9%97", "VERIFIED_EXISTING",
         "Fresh Chinese-language hospital protocol names IL-15 treatment for dogs with melanoma or osteosarcoma and lung metastases, matching the existing Evergreen identity.",
         ["taiwan-evergreen-il15-melanoma-osa"], [s(5), b]),
    lead("https://vet.tufts.edu/clinical-trials/bg34-200-plus-immunotherapy-canine-malignant-melanoma", "VERIFIED_EXISTING",
         "Fresh official individual protocol is labeled Suspended, matching the existing disabled BG34-200 record.",
         ["tufts-bg34-melanoma"], [s(7), a]),
    lead("https://assets.ctfassets.net/rt5zmd3ipxai/4cqVogdVNGzvFz2o047tYy/063d8492a098faf1aa7aeddf44e0135e/Metro_Vet_Hospital_-_Carcinoma_Study_flyer__Cleveland_East_.pdf", "VERIFIED_EXISTING",
         "The older Ethos/NVA flyer is the VGS-002 anti-PD-1 canine urothelial-carcinoma cohort. Fresh sponsor pipeline evidence labels the Ethos and BARC sites Closed, consistent with the existing completed canonical record.",
         ["penn-anti-pd1-urothelial-carcinoma"], [s(8), a, b, c]),
    lead("https://bluepearlvet.com/current-clinical-studies/", "SOURCE_INDEX_REVIEWED",
         "Fresh BluePearl page explicitly calls its list complete and shows one canine oncology treatment study, splenic hemangiosarcoma chemotherapy at Kirkland and Tacoma. It maps to bluepearl-hsa-paccal; sponsor completion evidence remains controlling for matching status.",
         ["bluepearl-hsa-paccal"], [c],
         protocol_links_examined=["Treatment for Canine Hemangiosarcoma (HSA) of the Spleen -> bluepearl-hsa-paccal"]),
    lead("https://www.ethosvet.com/clinical-study/canine-oncology-sample-study/", "NOT_TREATMENT",
         "Fresh official page is an enrolling one-visit diagnostic sample-collection study and does not administer anticancer treatment.",
         ["ethos-oncology-sample"], [c]),
    lead("https://site.unibo.it/ospedale-veterinario/it/piccoli-animali/trials-clinici-in-oncologia-veterinaria", "SOURCE_INDEX_REVIEWED",
         "Fresh Italian-language official index shows both named treatment trials as CONCLUSO and no current enrolling protocol names.",
         [], [s(3), b],
         protocol_links_examined=["Canine appendicular osteosarcoma — CONCLUSO", "Canine malignant melanoma — CONCLUSO"]),
    lead("https://www.jvcog.jp/clinical/03rinsho.html", "PENDING_EVIDENCE",
         "The Japanese page calls the trial ongoing but names only an unidentified anticancer drug and carries a tumor-scope note dated 2016. No exact protocol or canonical identity can be established.",
         [], [s(5), b],
         missing_primary_reason="Drug/protocol identifier and current site-level intake are not published; leave unresolved rather than create a guessed record."),
    lead("https://chuv.oniris-nantes.fr/animaux-de-compagnie/chirurgie/osteosarcomes-appendiculaires-chez-le-chien/", "VERIFIED_EXISTING",
         "Same Oniris/TheraVet BIOCERA-VET cement cohort; the intervention remains palliative/supportive and outside tumor-directed matching.",
         ["fr-oniris-osa-biocera-vet-cement"], [s(3)]),
    lead("https://uqvets.com.au/about/clinical-research-trials", "VERIFIED_EXISTING",
         "Same UQ postoperative appendicular-osteosarcoma vaccine protocol; no second identity established.",
         ["au-uq-appendicular-osteosarcoma-vaccine"], [s(1), s(4)]),
    lead("https://www.vet.upenn.edu/ryan-hospital/clinical-trials/", "SOURCE_INDEX_REVIEWED",
         "Fresh index results reconcile to existing Penn FLASH glioma, metastatic osteosarcoma FLASH, oral-SCC NIR margin, prostate theranostic, and feline oral-SCC records; no unmatched identity was established.",
         [], [s(1)],
         protocol_links_examined=["penn-glioma-flash-gilvetmab-2026", "penn-flash-metastatic-osa-gilvetmab-2026", "penn-oral-scc-nir-margin-2026", "penn-psma-theranostic-prostate", "penn-feline-oscc"]),
    lead("https://research.vetmed.ufl.edu/research-programs/clinical-trials/oncology/", "SOURCE_INDEX_REVIEWED",
         "Fresh UF oncology index reconciles trametinib histiocytic sarcoma and other named protocols to existing IDs; Biocera is marked closed. The contradictory LSD1 detail page remains separately unresolved.",
         [], [s(1), s(9)],
         protocol_links_examined=["uf-hs-trametinib", "uf-osa-vaccine", "uf-osa-mrna", "uf-hsa-vaccine", "uf-melanoma", "Biocera-Vet — closed enrollment"]),
    lead("https://www.veterinarystudiesregistry.co.uk/studies", "SOURCE_INDEX_REVIEWED",
         "Fresh complete four-entry roster has no genuine dog/cat anticancer-treatment protocol; its canine lymphoma item is explicitly an AI-generated sample.",
         [], [f"{run_ref}/current-source-web-summary.json"],
         protocol_links_examined=["UK-VCSR-2026-00013", "UK-VCSR-2026-00006 — AI sample", "UK-VCSR-2026-00003 — AI sample", "UK-VCSR-2026-00001 — AI sample"]),
    lead("https://vetcancercare.com/clinical-trials/", "CLOSED_CONFIRMED",
         "Fresh official result says there are no trials currently enrolling and keeps Immunocidin studies under past trials.",
         [], [s(1)]),
    lead("https://www.tierspital.uzh.ch/wp-content/uploads/2025/12/Studie_Orale-Chemotherapie-mit-Vinorelbin.pdf", "VERIFIED_EXISTING",
         "Same inactive Zurich single-dose oral vinorelbine Phase I identity.",
         ["ch-zurich-oral-vinorelbine-phase1-2026"], [s(3)]),
    lead("https://assets.ctfassets.net/f18j4npi43lu/5qE2eAtbFbyZKYWKJgPxXn/90f325d565134ced751567da21bfcad1/Terapia_a_base_di_piccole_molecole_organiche_aventi_come_target_la_Proteina_di_Attivazione_dei_Fibroblasti__PAF__per_il_trat.pdf", "VERIFIED_EXISTING",
         "Same University of Milan OncoFAP-MMAE/FAP-positive solid-tumor protocol.",
         ["eu-it-unimi-oncofap-mmae"], [s(3)]),
]

coverage = {}
for q in queries:
    coverage.setdefault(q["region"], {"languages": set(), "passes": set(), "queries": 0})
    coverage[q["region"]]["languages"].add(q["language"])
    coverage[q["region"]]["passes"].add(q["pass"])
    coverage[q["region"]]["queries"] += 1
coverage = {k: {"languages": sorted(v["languages"]), "passes": sorted(v["passes"]), "queries": v["queries"]} for k, v in coverage.items()}

write("lead-protocol-current-findings.json", {
    "run_id": run_id,
    "reviewed_at": reviewed_at,
    "leads": leads,
    "summary": {
        "reviewed": len(leads),
        "verified_existing": sum(x["disposition"] == "VERIFIED_EXISTING" for x in leads),
        "pending_evidence": sum(x["disposition"] == "PENDING_EVIDENCE" for x in leads),
        "new_catalog_additions": 0,
    },
})
write("global-discovery-evidence.json", {
    "run_id": run_id,
    "reviewed_at": reviewed_at,
    "query_count": len(queries),
    "coverage": coverage,
    "candidate_count": read("discovery-candidates-raw.json")["count"],
    "selected_leads": len(leads),
    "queries": queries,
    "lead_review_ref": f"{run_ref}/lead-protocol-current-findings.json",
})
print(json.dumps({"queries": len(queries), "regions": len(coverage), "leads": len(leads)}, indent=2))
