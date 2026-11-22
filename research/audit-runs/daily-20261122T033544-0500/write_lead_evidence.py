#!/usr/bin/env python3
import json
from pathlib import Path

here = Path(__file__).resolve().parent

def write(name, rows):
    (here / name).write_text(json.dumps({"run_id": here.name, "routes": rows}, ensure_ascii=False, indent=2) + "\n")

write("lead-open-a.json", [
    {"url":"https://vrcvet.com/clinical-trials/","reference":"turn584456385view0","crawled":"today","result":"success","facts":["Clinical Trials Now Enrolling","canine cutaneous soft tissue sarcoma >1.7 cm","weight >=5 kg","intratumoral T-cell engagers followed by surgery one week later","no placebo"]},
    {"url":"https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/olaparib","reference":"turn584456385view1","crawled":"today","result":"success","facts":["Open and enrolling","feline mammary carcinoma","olaparib plus meloxicam","measurable mammary tumor >=1 cm"]},
    {"url":"https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/trike-new","reference":"turn584456385view2","result":"web_error_403"},
    {"url":"https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/","reference":"turn584456385view3","crawled":"today","result":"success","facts":["Current Clinical Trials roster retrieved"]},
    {"url":"https://www.paccalvet.com/cat-cancer-study","reference":"turn584456385view4","result":"web_error_401"},
    {"url":"https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/","reference":"turn584456385view5","crawled":"today","result":"success","facts":["Page says currently recruiting","same page says Enrollment Paused","cats with oral carcinoma","oral LSD1 inhibitor after radiation"]},
    {"url":"https://vet.tufts.edu/clinical-trials/bg34-200-plus-immunotherapy-canine-malignant-melanoma","reference":"turn584456385view6","crawled":"yesterday","result":"success","facts":["Suspended","canine oral malignant melanoma","BG34-200 immune therapy"]},
    {"url":"https://assets.ctfassets.net/rt5zmd3ipxai/4cqVogdVNGzvFz2o047tYy/063d8492a098faf1aa7aeddf44e0135e/Metro_Vet_Hospital_-_Carcinoma_Study_flyer__Cleveland_East_.pdf","reference":"turn584456385view7","crawled":"2 months ago","result":"success","facts":["Canine transitional/urothelial carcinoma immunotherapy","Metropolitan Veterinary Hospital Cleveland East","fully funded","histologic confirmation and measurable intravesicular tumor"]},
])

write("lead-open-b.json", [
    {"url":"https://research.vetmed.ufl.edu/determine-how-lsd1-inhibitors-alone-attenuate-feline-oral-carcinomas/","reference":"turn586591508view0","crawled":"today","result":"success","facts":["current recruiting statement","Enrollment Criteria: Enrollment Paused","LSD1 inhibitor after radiation","study covers biopsies, study drug, related visits and up to $1,000 for drug adverse events"]},
    {"url":"https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/","reference":"turn586591508view1","crawled":"today","result":"success","facts":["COTC033 Vaccine Peptide Library","dogs 15-60 kg","confirmed solid tumor 2-8 cm","study covers all treatment and recheck costs plus $1,000 post-study treatment gift"]},
    {"url":"https://assets.ctfassets.net/rt5zmd3ipxai/4cqVogdVNGzvFz2o047tYy/063d8492a098faf1aa7aeddf44e0135e/Metro_Vet_Hospital_-_Carcinoma_Study_flyer__Cleveland_East_.pdf","reference":"turn586591508view2","crawled":"today","result":"success","facts":["older canine urothelial carcinoma immunotherapy flyer","fully funded"]},
    {"url":"https://www.gamgee.io/trial/","reference":"turn586591508view3","crawled":"today","result":"success","facts":["Trial now recruiting in Australia","dogs with mast cell cancer","personalized mRNA vaccine"]},
    {"url":"https://www.vm.a.u-tokyo.ac.jp/vmc/wp2/wp-content/uploads/2025/11/poster12.pdf","reference":"turn586591508view4","crawled":"today","result":"success","facts":["dog/cat refractory solid tumors","organoid screening identifies targeted drug","screening and first five weeks of targeted drug are free"]},
    {"url":"https://www.egah.com.tw/news/%E6%8B%9B%E5%8B%9F%E7%8A%AC%E9%BB%91%E8%89%B2%E7%B4%A0%E7%98%A4%E5%8F%8A%E9%AA%A8%E8%82%89%E7%98%A4%E8%87%A8%E5%BA%8A%E8%A9%A6%E9%A9%97","reference":"turn586591508view5","crawled":"today","result":"success","facts":["recruiting dogs with melanoma or osteosarcoma","IL-15 therapy","lung metastasis >1 cm","weekly visits for 10-12 weeks"]},
    {"url":"https://site.unibo.it/ospedale-veterinario/it/piccoli-animali/trials-clinici-in-oncologia-veterinaria","reference":"turn586591508view6","crawled":"today","result":"success","facts":["current oncology-trials index","canine appendicular osteosarcoma concluded","canine malignant melanoma concluded"]},
    {"url":"https://www.jvcog.jp/clinical/03rinsho.html","reference":"turn586591508view7","crawled":"last week","result":"success","facts":["page labels study ongoing","unnamed anticancer drug","canine unresectable/recurrent mast cell tumor or poorly differentiated lymphoma","tumor scope note dated June 8, 2016"]},
])

write("lead-open-c.json", [
    {"url":"https://bluepearlvet.com/current-clinical-studies/","reference":"turn189572454view0","crawled":"today","result":"success","facts":["page says complete list of studies currently happening","one canine oncology treatment study: splenic hemangiosarcoma chemotherapy","locations Kirkland and Tacoma"]},
    {"url":"https://vcahospitals.com/clinical-studies","reference":"turn189572454view1","result":"tool_inaccessible_exact_url"},
    {"url":"https://www.ethosvet.com/clinical-study/canine-oncology-sample-study/","reference":"turn189572454view2","crawled":"2 days ago","result":"success","facts":["Now Enrolling Patients","diagnostic sample collection only","single visit","no anticancer treatment"]},
    {"url":"https://vetigenics.com/technology-pipeline/pipeline-and-clinical-trials/","reference":"turn189572454view3","crawled":"today","result":"success","facts":["VGS-001 canine oral melanoma sites closed","VGS-002 canine urothelial carcinoma Ethos and BARC sites closed","CHECKMATE-K9 fully enrolled and all listed sites closed"]},
])
