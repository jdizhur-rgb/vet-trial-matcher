from pathlib import Path
import ast,re,subprocess
p=Path('app.py'); s=p.read_text()
old=s
# Expand CANCERS safely.
m=re.search(r'^CANCERS = (\[.*\])$',s,re.M); cancers=ast.literal_eval(m.group(1))
new=['Gastric / stomach cancer','Gastrointestinal stromal tumor (GIST)','Colorectal / rectal cancer','Nasal tumor / nasal cancer','Salivary gland cancer','Esophageal cancer','Thymoma / thymic tumor','Multiple myeloma / plasma cell cancer','Peripheral nerve sheath tumor','Leiomyosarcoma','Chondrosarcoma','Fibrosarcoma','Liposarcoma','Rhabdomyosarcoma',"My cancer type isn't listed"]
for x in new:
    if x not in cancers: cancers.append(x)
s=s[:m.start()]+"CANCERS = "+repr(cancers)+s[m.end():]
# Explicit broad families; never inferred from free text.
marker="TREATMENT_OPTIONS = ['Chemotherapy','Radiation','Surgery','Immunotherapy','Targeted therapy','Experimental drug']"
block="""DIAGNOSIS_FAMILIES = {\n    'Gastric / stomach cancer': {'solid_tumor','carcinoma'},\n    'Colorectal / rectal cancer': {'solid_tumor','carcinoma'},\n    'Salivary gland cancer': {'solid_tumor','carcinoma'},\n    'Esophageal cancer': {'solid_tumor','carcinoma'},\n    'Thymoma / thymic tumor': {'solid_tumor'},\n    'Gastrointestinal stromal tumor (GIST)': {'solid_tumor','sarcoma'},\n    'Peripheral nerve sheath tumor': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},\n    'Leiomyosarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},\n    'Fibrosarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},\n    'Liposarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},\n    'Rhabdomyosarcoma': {'solid_tumor','sarcoma','soft_tissue_sarcoma'},\n    'Chondrosarcoma': {'solid_tumor','sarcoma'},\n    'Nasal tumor / nasal cancer': {'solid_tumor','nasal_tumor'},\n    'Multiple myeloma / plasma cell cancer': {'hematologic'},\n}\nUNLISTED_CANCER = \"My cancer type isn't listed\"\n"""
if 'DIAGNOSIS_FAMILIES =' not in s: s=s.replace(marker,block+marker)
# Helper after is_current_trial.
needle="def is_current_trial(tr):\n    return tr.get('status_confidence') in CURRENT_STATUS_CONFIDENCE\n"
helper="""\ndef trial_accepts_diagnosis(tr, diagnosis):\n    \"\"\"Return (accepted, broad) without fuzzy disease inference.\"\"\"\n    tc=set(tr.get('cancers', []))\n    exact={diagnosis, *CANCER_ALIASES.get(diagnosis, [])}\n    if diagnosis == 'Spindle cell sarcoma': exact.add('Soft tissue sarcoma')\n    if exact.intersection(tc): return True, False\n    broad=set(tr.get('broad_disease_families', []))\n    if 'all_tumors' in broad or 'Cancer — any type' in tc: return True, True\n    fam=DIAGNOSIS_FAMILIES.get(diagnosis,set())\n    if fam.intersection(broad): return True, True\n    return False, False\n"""
if 'def trial_accepts_diagnosis' not in s: s=s.replace(needle,needle+helper)
# Unlisted free-text UI.
needle="cancer = st.selectbox('Cancer type', CANCERS)"
rep=needle+"\nunlisted_mode = cancer == UNLISTED_CANCER\nunlisted_diagnosis = st.text_input('Enter the diagnosis as written in the pathology report, if known') if unlisted_mode else ''"
s=s.replace(needle,rep)
# Form candidate filter uses safe helper; unlisted only all-tumor.
oldcond="if cancer == 'Cancer — any type' or accepted_for_form.intersection(_tr.get('cancers', [])) or 'Cancer — any type' in _tr.get('cancers', []):\n        _form_trials.append(_tr)"
newcond="if cancer == 'Cancer — any type' or (unlisted_mode and ('all_tumors' in _tr.get('broad_disease_families', []) or 'Cancer — any type' in _tr.get('cancers', []))) or (not unlisted_mode and trial_accepts_diagnosis(_tr, cancer)[0]):\n        _form_trials.append(_tr)"
s=s.replace(oldcond,newcond)
# Unlisted behaves as no disease-specific form.
s=s.replace("any_cancer_browse = cancer == 'Cancer — any type'","any_cancer_browse = cancer == 'Cancer — any type'")
s=s.replace("if any_cancer_browse:\n    st.caption('Browse mode: disease-specific eligibility is not used until a cancer type is selected.')","if any_cancer_browse or unlisted_mode:\n    st.caption('Browse mode: disease-specific eligibility is not used until a cancer type is selected.' if any_cancer_browse else 'Unlisted diagnosis: only genuinely all-tumor treatment programs will be shown for investigator review.')")
s=s.replace('(not any_cancer_browse and ', '(not any_cancer_browse and not unlisted_mode and ')
s=s.replace('surgery_relevant = (not any_cancer_browse) and ', 'surgery_relevant = (not any_cancer_browse and not unlisted_mode) and ')
s=s.replace('chemo_relevant = (not any_cancer_browse) and ', 'chemo_relevant = (not any_cancer_browse and not unlisted_mode) and ')
s=s.replace('radiation_relevant = (not any_cancer_browse) and ', 'radiation_relevant = (not any_cancer_browse and not unlisted_mode) and ')
s=s.replace('immunotherapy_relevant = (not any_cancer_browse) and ', 'immunotherapy_relevant = (not any_cancer_browse and not unlisted_mode) and ')
s=s.replace('steroids_relevant = (not any_cancer_browse) and ', 'steroids_relevant = (not any_cancer_browse and not unlisted_mode) and ')
s=s.replace('immunosuppressive_relevant = (not any_cancer_browse) and ', 'immunosuppressive_relevant = (not any_cancer_browse and not unlisted_mode) and ')
# Matcher diagnosis gate.
oldgate="accepted_cancers = {cancer, *CANCER_ALIASES.get(cancer, [])}\n        if cancer == 'Spindle cell sarcoma':\n            accepted_cancers.add('Soft tissue sarcoma')\n        # Owner-side 'Cancer — any type' means ANY diagnosis, not a literal cancer label.\n        if cancer != 'Cancer — any type' and not accepted_cancers.intersection(tr['cancers']) and 'Cancer — any type' not in tr['cancers']:\n            continue"
newgate="broad_match = False\n        if unlisted_mode:\n            if 'all_tumors' not in tr.get('broad_disease_families', []) and 'Cancer — any type' not in tr.get('cancers', []):\n                continue\n            broad_match = True\n        elif cancer != 'Cancer — any type':\n            accepted, broad_match = trial_accepts_diagnosis(tr, cancer)\n            if not accepted:\n                continue"
if oldgate not in s: raise SystemExit('matcher gate not found')
s=s.replace(oldgate,newgate)
# Dedicated unlisted branch before any-cancer branch.
needle="        if cancer == 'Cancer — any type':\n            req = tr.get('requires', {})"
unlisted="""        if unlisted_mode:\n            req = tr.get('requires', {})\n            min_age=req.get('min_age_years'); max_age=req.get('max_age_years')\n            if min_age is not None and age_known and age < min_age: continue\n            if max_age is not None and age_known and age > max_age: continue\n            min_lb=req.get('min_weight_lb')\n            if min_lb is None and req.get('min_weight_kg') is not None: min_lb=req['min_weight_kg']*2.2046226218\n            if min_lb is not None and weight_known and weight_lb < min_lb: continue\n            shown = unlisted_diagnosis.strip() or 'unlisted diagnosis'\n            matches.append(('Trial to review — diagnosis requires prescreening', tr, [f'{shown} has not been mapped to a trial disease category'], ['investigator must confirm diagnosis-specific eligibility']))\n            continue\n\n"""
if unlisted not in s: s=s.replace(needle,unlisted+needle)
# Broad match presentation.
s=s.replace("reasons.append(f'{cancer} matches the study disease category')","reasons.append('broad disease-family eligibility supports investigator review' if broad_match else f'{cancer} matches the study disease category')")
s=s.replace("if cancer != 'Cancer — any type':\n                confidence = 'Possible match'","if cancer != 'Cancer — any type':\n                confidence = 'Potential broad-treatment trial — prescreening required' if broad_match else 'Possible match'")
# Existing broad records: explicit metadata.
def add_meta(id_, families):
    global s
    pat="'id': '"+id_+"',"
    if pat in s and "'id': '"+id_+"',\n  'broad_disease_families'" not in s:
        s=s.replace(pat,pat+"\n  'broad_disease_families': "+repr(families)+",",1)
add_meta('eu-ch-large-tumor-lattice-sbrt',['solid_tumor'])
add_meta('eu-ch-oral-vinorelbine-phase1',['all_tumors'])
add_meta('case-cosmyc-it',['all_tumors'])
# Existing Zurich nasal record becomes location-broad.
s=s.replace("'id': 'eu-ch-sinonasal-heterogeneous-rt',\n  'title'","'id': 'eu-ch-sinonasal-heterogeneous-rt',\n  'broad_disease_families': ['nasal_tumor'],\n  'title'",1)
# Mark all VROC compassionate records as all-tumor without duplicating them.
s=re.sub(r"('id': 'vroc-compassionate-advanced[^']*',)(?!\n\s*'broad_disease_families')",r"\1\n  'broad_disease_families': ['all_tumors'],",s)
# Add verified Tufts and Zurich PNST records if absent.
insert="""\n {'id':'tufts-z007-broad-solid-2026','title':'Evaluation of TLR agonist Z-007 in dogs with cancer','center':'Cummings School of Veterinary Medicine, Tufts University','country':'USA','species':'Dog','cancers':['Other solid tumor'],'broad_disease_families':['solid_tumor','carcinoma','sarcoma'],'status':'Recruiting','url':'https://vet.tufts.edu/clinical-trials/evaluation-tlr-agonist-z-007-dogs-cancer','contacts':'clinicaltrials@tufts.edu','funding':'Study covers Z-007 treatment through Day 63 and treatment of Z-007/biopsy-related side effects; confirm other owner costs with Tufts.','requires':{'confirmed':True,'min_weight_kg':7,'measurable':True},'excludes':{},'notes':'Dog study of IV or intratumoral Z-007 for solid tumors including carcinomas, sarcomas and melanoma. Public criteria include a generally 2–7 cm repeat-biopsy-accessible tumor plus medical/laboratory requirements; no prior immunotherapy or autoimmune disease. Investigator prescreening required.','verified':'2026-09-04','study_type':'treatment','available_for_matching':True,'status_confidence':'confirmed_current','owner_prescreen_required':True},\n {'id':'eu-ch-pnst-plexus-fluorescence-surgery','title':'Fluorescence-guided surgery for canine peripheral nerve sheath / plexus tumors','center':'Universitäres Tierspital Zürich / University of Zurich','country':'Switzerland','species':'Dog','cancers':['Peripheral nerve sheath tumor'],'status':'Studienteilnahme möglich','url':'https://www.tierspital.uzh.ch/forschungsprojekte/studie-plexustumore-hunde/','contacts':'University of Zurich study team — use official study page','funding':'Confirm study-covered and owner-paid costs with the University of Zurich study team.','requires':{'confirmed':True,'active_treatment_target':True},'excludes':{},'notes':'Therapeutic surgical study for peripheral nerve sheath/plexus tumors using fluorescence guidance to improve tumor visualization and potentially enable limb-preserving surgery. PNST-specific; other STS are not automatically eligible.','verified':'2026-09-04','study_type':'treatment','available_for_matching':True,'status_confidence':'confirmed_current','owner_prescreen_required':True},\n"""
anchor="\n])\n\n\n# 2026-09-03 regulatory / CRO / sponsor-development pass"
if 'tufts-z007-broad-solid-2026' not in s: s=s.replace(anchor,insert+anchor,1)
# Ensure nasal choice can exact-match existing Zurich record too.
s=s.replace("'cancers': ['Sinonasal carcinoma', 'Other solid tumor'],","'cancers': ['Sinonasal carcinoma', 'Nasal tumor / nasal cancer', 'Other solid tumor'],",1)
p.write_text(s)
# Static safety checks.
ast.parse(s)
ids=re.findall(r"['\"]id['\"]\s*:\s*['\"]([^'\"]+)",s)
if len(ids)!=len(set(ids)): raise SystemExit('duplicate trial ids')
if old==s: raise SystemExit('no changes')
subprocess.run(['python3','-m','py_compile','app.py'],check=True)
subprocess.run(['git','diff','--check'],check=True)
print('updated app.py; ids',len(ids),'unique',len(set(ids)))
