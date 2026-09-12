"""Catalog loading and conservative diagnosis taxonomy helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CANCER_ALIASES = {
    "B-cell lymphoma": ["Lymphoma", "Lymphoma — other"],
    "T-cell lymphoma": ["Lymphoma", "Lymphoma — other", "Enteropathy-associated T-cell lymphoma"],
    "Lymphoma — other": ["Lymphoma", "Gastrointestinal lymphoma", "Large cell lymphoma"],
    "Brain tumor / glioma": ["Brain tumor", "Glioma"],
    "Feline mammary carcinoma": ["Mammary carcinoma", "Mammary tumor"],
    "Mammary carcinoma": ["Mammary tumor"],
    "Mammary tumor — other": ["Mammary tumor"],
    "Urothelial / transitional cell carcinoma": ["Urothelial carcinoma", "Transitional cell carcinoma"],
    "Urothelial carcinoma": ["Urothelial / transitional cell carcinoma", "Transitional cell carcinoma", "Bladder cancer"],
    "Thyroid tumor / carcinoma": ["Thyroid carcinoma"],
    "Thyroid carcinoma": ["Thyroid tumor / carcinoma"],
    "Hepatocellular carcinoma": ["Hepatic carcinoma"],
    "Primary lung tumor": ["Pulmonary carcinoma"],
    "Oral squamous cell carcinoma": ["Feline oral SCC"],
    "Squamous cell carcinoma — other": ["Squamous cell carcinoma"],
    "Oral tumor — other": ["Oral tumor"],
    "Ocular melanoma / iris melanocytic tumor": ["Ocular melanoma", "Iris melanocytic tumor"],
    "Chemodectoma": ["Aortic body tumor", "Aortic body tumors", "Heart-base tumor", "Heart base tumor", "Paraganglioma", "Non-chromaffin paraganglioma"],
}

DIAGNOSIS_FAMILIES = {
    "Gastric / stomach cancer": {"solid_tumor", "carcinoma"},
    "Colorectal / rectal cancer": {"solid_tumor", "carcinoma"},
    "Salivary gland cancer": {"solid_tumor", "carcinoma"},
    "Esophageal cancer": {"solid_tumor", "carcinoma"},
    "Thymoma / thymic tumor": {"solid_tumor"},
    "Gastrointestinal stromal tumor (GIST)": {"solid_tumor", "sarcoma"},
    "Peripheral nerve sheath tumor": {"solid_tumor", "sarcoma", "soft_tissue_sarcoma"},
    "Leiomyosarcoma": {"solid_tumor", "sarcoma", "soft_tissue_sarcoma"},
    "Fibrosarcoma": {"solid_tumor", "sarcoma", "soft_tissue_sarcoma"},
    "Liposarcoma": {"solid_tumor", "sarcoma", "soft_tissue_sarcoma"},
    "Rhabdomyosarcoma": {"solid_tumor", "sarcoma", "soft_tissue_sarcoma"},
    "Chondrosarcoma": {"solid_tumor", "sarcoma"},
    "Nasal tumor / nasal cancer": {"solid_tumor", "nasal_tumor"},
    "Multiple myeloma / plasma cell cancer": {"hematologic"},
}

CANCERS = [
    "Acute myeloid leukemia", "Adrenal tumor", "Anal sac adenocarcinoma (AGASACA)",
    "B-cell lymphoma", "Brain tumor / glioma", "Chemodectoma", "Chondrosarcoma",
    "Colorectal / rectal cancer", "Cutaneous epitheliotropic lymphoma", "Esophageal cancer",
    "Feline injection-site sarcoma", "Feline mammary carcinoma", "Fibrosarcoma",
    "Gallbladder carcinoma", "Gastric / stomach cancer", "Gastrointestinal stromal tumor (GIST)",
    "Hemangiosarcoma", "Hepatocellular carcinoma", "Histiocytic sarcoma", "Insulinoma",
    "Intestinal carcinoma", "Leiomyosarcoma", "Liposarcoma", "Lymphoma — other",
    "Mammary carcinoma", "Mammary tumor — other", "Mast cell tumor", "Melanoma — other",
    "Multiple myeloma / plasma cell cancer", "Nasal tumor / nasal cancer",
    "Ocular melanoma / iris melanocytic tumor", "Oral melanoma", "Oral squamous cell carcinoma",
    "Oral tumor — other", "Osteosarcoma", "Other bone tumor", "Other liver tumor",
    "Other sarcoma", "Other solid tumor", "Pancreatic carcinoma",
    "Peripheral nerve sheath tumor", "Primary lung tumor", "Prostate cancer", "Renal tumor",
    "Rhabdomyosarcoma", "Salivary gland cancer", "Sinonasal carcinoma", "Soft tissue sarcoma",
    "Spindle cell sarcoma", "Squamous cell carcinoma", "Squamous cell carcinoma — other",
    "T-cell lymphoma", "Thymoma / thymic tumor", "Thyroid carcinoma",
    "Thyroid tumor / carcinoma", "Urothelial / transitional cell carcinoma",
    "Urothelial carcinoma", "Cancer — any type", "Other / not sure",
    "My cancer type isn't listed",
]

CURRENT_STATUS_CONFIDENCE = {"current", "confirmed_current"}


def load_trials(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or Path(__file__).resolve().parent
    with (root / "data" / "trials_base.json").open(encoding="utf-8") as handle:
        by_id = {trial["id"]: trial for trial in json.load(handle)}
    paths = [root / "data" / "trial_updates.json"]
    paths.extend(sorted((root / "data").glob("catalog_patch_*.json")))
    for path in paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as handle:
            document = json.load(handle)
        for trial_id in document.get("delete", []):
            by_id.pop(trial_id, None)
        for patch in document.get("upsert", []):
            trial_id = patch["id"]
            merged = dict(by_id.get(trial_id, {}))
            for key, value in patch.items():
                if key in {"requires", "excludes"} and isinstance(value, dict):
                    nested = dict(merged.get(key, {}))
                    nested.update(value)
                    merged[key] = nested
                else:
                    merged[key] = value
            by_id[trial_id] = merged
    return list(by_id.values())


def species_matches(trial_species: Any, selected_species: str) -> bool:
    """Normalize legacy string and newer list species fields."""
    if isinstance(trial_species, (list, tuple, set)):
        values = {str(value).strip() for value in trial_species}
    else:
        values = {
            value.strip()
            for value in str(trial_species or "").split("/")
            if value.strip()
        }
    return selected_species in values


def is_current_trial(trial: dict[str, Any]) -> bool:
    return trial.get("status_confidence") in CURRENT_STATUS_CONFIDENCE


def trial_accepts_diagnosis(trial: dict[str, Any], diagnosis: str) -> tuple[bool, bool]:
    trial_cancers = set(trial.get("cancers", []))
    exact = {diagnosis, *CANCER_ALIASES.get(diagnosis, [])}
    if diagnosis == "Spindle cell sarcoma":
        exact.add("Soft tissue sarcoma")
    if exact.intersection(trial_cancers):
        return True, False
    family = DIAGNOSIS_FAMILIES.get(diagnosis)
    if not family:
        return False, False
    broad = set(trial.get("broad_disease_families", []))
    if "all_tumors" in broad or "Cancer — any type" in trial_cancers:
        return True, True
    return bool(family.intersection(broad)), bool(family.intersection(broad))


def trial_modalities(trial: dict[str, Any]) -> set[str]:
    text = " ".join(str(trial.get(key, "")) for key in ("title", "intervention", "notes")).lower()
    req = trial.get("requires", {})
    modalities: set[str] = set()
    if req.get("planned_surgery") or req.get("planned_amputation") or req.get("planned_amputation_and_chemo") or any(word in text for word in ("surgery", "surgical", "mastectom", "amputation")):
        modalities.add("Surgery")
    if req.get("planned_radiation") or any(word in text for word in ("radiotherapy", "radiation", "sbrt", "flash", "lattice", "radiosensiti", "proton")):
        modalities.add("Radiation")
    if req.get("planned_doxorubicin") or req.get("planned_amputation_and_chemo") or any(word in text for word in ("chemotherapy", "doxorubicin", "carboplatin", "lomustine", "vinorelbine", "toceranib", "tigilanol", "chemoembol")):
        modalities.add("Chemotherapy")
    if any(word in text for word in ("immunotherap", "vaccine", "car-t", "car t", "interleukin", "il-2", "checkpoint", "pd-1", "pd-l1", "oncolytic", "tlr agonist", "bcg")):
        modalities.add("Immunotherapy")
    if any(word in text for word in ("targeted", "toceranib", "kinase inhibitor", "adam-12", "versican", "antibody", "radioimmunotherap", "nanobody")):
        modalities.add("Targeted therapy")
    if any(word in text for word in ("phase i", "phase 1", "phase ii", "phase 2", "experimental", "investigational", "tigilanol", "oxc-101", "rimcazole", "gcn2", "oncofap", "nebumet", "cantrixil")):
        modalities.add("Experimental drug")
    return modalities
