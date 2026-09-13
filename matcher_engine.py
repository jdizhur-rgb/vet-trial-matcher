"""Pure, UI-independent matching logic for the clinical-trial finder.

The Streamlit page owns questions and rendering.  This module owns trial
screening so it can be tested without starting the web application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


UNKNOWN = "I don't know"
CURRENT_STATUS_CONFIDENCE = {"current", "confirmed_current"}
BLOCKED_STATUS_PHRASES = (
    "on hold", "completed", "closed enrollment", "enrollment closed",
    "closed for data review", "suspended", "past clinical study",
    "not accepting", "paused", "not on current", "do not match",
    "coming soon", "not yet independently confirmed",
    "enrollment not confirmed", "reconfirm before matching",
    "previously active recruitment", "sponsor page still lists study",
    "current oncology archive listing",
    "recent active trial; enrollment must be reconfirmed",
    "patients needed; current enrollment should be reconfirmed",
    "funded active-study evidence", "current funded translational research",
)

# These protocol details are intentionally not added to the owner questionnaire.
# If present, they cap the result at prescreening rather than silently counting as
# satisfied.  The study team decides them.
PRESCREEN_REQUIREMENTS = {
    "visible_tumor": "visible tumor requirement",
    "max_vcog_performance_status": "performance-status requirement",
    "anticipated_survival_over_3_months": "minimum expected-survival requirement",
    "life_expectancy_weeks_min": "minimum expected-survival requirement",
    "measurable_lung_metastases": "measurable lung-metastasis requirement",
    "primary_removed": "primary-tumor removal requirement",
    "suspected_or_confirmed_glioma": "brain-tumor diagnostic requirement",
    "brain_tumor_biopsy": "brain-tumor biopsy requirement",
    "muscle_invasive_bladder_mass": "muscle-invasive bladder-mass requirement",
    "oral_mass": "oral-mass requirement",
    "distal_radius_location": "distal-radius tumor-location requirement",
    "giant_breed": "breed/size requirement",
    "primary_bone_tumor": "primary bone-tumor requirement",
    "weight_bearing": "weight-bearing requirement",
    "serum_creatinine_lt_2": "kidney-function requirement",
    "cystoscopy_accessible_mass": "cystoscopy-accessible tumor requirement",
    "cutaneous_sts": "cutaneous tumor-location requirement",
    "extremity_sts": "extremity tumor-location requirement",
    "prostatic_cancer": "prostatic primary-tumor requirement",
    "thyroid_tumor": "thyroid primary-tumor requirement",
    "newly_diagnosed_brain_tumor": "newly diagnosed brain-tumor requirement",
    "metastatic_or_recurrent": "metastatic or recurrent disease requirement",
    "anesthesia_fit": "fitness-for-anesthesia requirement",
    "surgery_planned": "planned-surgery requirement",
    "radiation_therapy": "radiation-treatment requirement",
    "previously_untreated": "previously untreated requirement",
    "brain_tumor_present": "current brain-tumor requirement",
    "current_chemo": "current-chemotherapy requirement",
    "newly_diagnosed": "newly diagnosed disease requirement",
    "standard_of_care_therapy": "standard-of-care treatment requirement",
    "osteosarcoma": "osteosarcoma protocol requirement",
}

PRESCREEN_EXCLUSIONS = {
    "prior_osteosarcoma_treatment": "prior osteosarcoma treatment",
    "active_wounds": "active wounds",
    "immunodeficiency": "immunodeficiency",
    "immune_mediated_disease": "immune-mediated disease",
    "recent_systemic_antibiotics_14d": "recent systemic antibiotics",
    "recent_immunosuppressants_14d": "recent immunosuppressive medication",
    "recent_prednisone_7d": "recent prednisone",
    "recent_chemotherapy_14d": "recent chemotherapy",
    "recent_radiation_30d": "recent radiation",
    "metastases_outside_lungs": "metastases outside the lungs",
    "concurrent_immunomodulatory_drugs": "concurrent immunomodulatory drugs",
    "corticosteroids": "corticosteroid use",
    "other_immunotherapy": "other immunotherapy",
    "alternative_therapy": "concurrent alternative therapy",
    "other_clinical_study": "participation in another clinical study",
    "current_prednisone": "current prednisone",
    "concurrent_surgery": "concurrent surgery",
    "concurrent_local_radiation": "concurrent local radiation",
    "pathologic_fracture": "pathologic fracture",
    "bone_metastasis": "bone metastasis",
    "prior_radiation": "prior radiation",
    "high_urethral_obstruction_risk": "urethral-obstruction risk",
    "pulmonary_metastasis": "pulmonary metastasis",
    "regional_lymph_node_metastasis": "regional lymph-node metastasis",
    "prior_cancer_treatment": "prior cancer treatment",
    "current_immunosuppressive_medications": "current immunosuppressive medication",
}


@dataclass(frozen=True)
class SearchAnswers:
    species: str
    cancer: str
    diagnosis_status: str = UNKNOWN
    age: float | None = None
    weight_lb: float | None = None
    sex: str = UNKNOWN
    tumor_status: str = UNKNOWN
    metastasis: str = UNKNOWN
    localized: str = UNKNOWN
    lymphoma_response: str = UNKNOWN
    surgery: str = UNKNOWN
    prior_procedure: str = UNKNOWN
    chemo: str = UNKNOWN
    immunotherapy_history: str = UNKNOWN
    radiation: str = UNKNOWN
    steroids: str = UNKNOWN
    immunosuppressive: str = UNKNOWN
    preferences: frozenset[str] = field(default_factory=frozenset)
    radiation_affordability: str = UNKNOWN
    standard_therapy_unavailable: str = UNKNOWN
    large_inoperable_or_rt_preferred: str = UNKNOWN
    surgery_or_rt_not_possible: str = UNKNOWN
    ct_and_current_biopsy: str = UNKNOWN
    tumor_size_cm: float | None = None
    osa_location: str = UNKNOWN
    tumor_location: str = UNKNOWN
    surface_or_oral_accessible: str = UNKNOWN
    unlisted_diagnosis: str = ""


@dataclass(frozen=True)
class Match:
    label: str
    trial: dict[str, Any]
    reasons: tuple[str, ...]
    needs_confirmation: tuple[str, ...]

def _status_is_open(trial: dict[str, Any]) -> bool:
    if trial.get("status_confidence") not in CURRENT_STATUS_CONFIDENCE:
        return False
    status = str(trial.get("status", "")).lower()
    return not any(phrase in status for phrase in BLOCKED_STATUS_PHRASES)


def _species_matches(trial_species: Any, species: str) -> bool:
    if isinstance(trial_species, (list, tuple, set)):
        values = {str(value).strip() for value in trial_species}
    else:
        values = {value.strip() for value in str(trial_species or "").split("/") if value.strip()}
    return species in values


def _weight_limits(req: dict[str, Any]) -> tuple[float | None, float | None]:
    min_lb = req.get("min_weight_lb")
    max_lb = req.get("max_weight_lb")
    if min_lb is None and req.get("min_weight_kg") is not None:
        min_lb = req["min_weight_kg"] * 2.2046226218
    if max_lb is None and req.get("max_weight_kg") is not None:
        max_lb = req["max_weight_kg"] * 2.2046226218
    return min_lb, max_lb


def _append_once(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def match_trials(
    trials: Iterable[dict[str, Any]],
    answers: SearchAnswers,
    *,
    accepts_diagnosis: Callable[[dict[str, Any], str], tuple[bool, bool]],
    trial_modalities: Callable[[dict[str, Any]], set[str]],
    country_matches: Callable[[str], bool] = lambda _country: True,
) -> list[Match]:
    """Return plausible treatment opportunities without rendering UI."""
    results: list[Match] = []
    unlisted = answers.cancer == "My cancer type isn't listed"
    browse = answers.cancer == "Cancer — any type"

    for trial in trials:
        if not trial.get("available_for_matching", True) or not _status_is_open(trial):
            continue
        if not _species_matches(trial.get("species", ""), answers.species):
            continue
        if not country_matches(str(trial.get("country", "USA"))):
            continue
        if trial.get("study_type", "treatment") not in {"treatment", "other_treatment_access"}:
            continue

        broad_match = False
        if unlisted:
            if "all_tumors" not in trial.get("broad_disease_families", []) and "Cancer — any type" not in trial.get("cancers", []):
                continue
            broad_match = True
        elif not browse:
            accepted, broad_match = accepts_diagnosis(trial, answers.cancer)
            if not accepted:
                continue

        modalities = trial_modalities(trial)
        if answers.preferences and modalities and not modalities.intersection(answers.preferences):
            continue

        req = trial.get("requires", {})
        min_age, max_age = req.get("min_age_years"), req.get("max_age_years")
        min_lb, max_lb = _weight_limits(req)
        if min_age is not None and answers.age is not None and answers.age < min_age:
            continue
        if max_age is not None and answers.age is not None and answers.age > max_age:
            continue
        if min_lb is not None and answers.weight_lb is not None and answers.weight_lb < min_lb:
            continue
        if max_lb is not None and answers.weight_lb is not None and answers.weight_lb > max_lb:
            continue

        if unlisted:
            shown = answers.unlisted_diagnosis.strip() or "unlisted diagnosis"
            results.append(Match(
                "Trial to review — diagnosis requires prescreening", trial,
                (f"{shown} has not been mapped to a trial disease category",),
                ("investigator must confirm diagnosis-specific eligibility",),
            ))
            continue
        if browse:
            reasons = ["cancer type not specified — study shown for diagnosis review"]
            if answers.age is not None:
                reasons.append("age is within any published study limit")
            if answers.weight_lb is not None:
                reasons.append("weight is within any published study limit")
            results.append(Match(
                "Trial to review — cancer type not specified", trial, tuple(reasons),
                ("disease-specific and protocol-specific eligibility requires prescreening",),
            ))
            continue

        trial_text = f"{trial.get('title', '')} {trial.get('notes', '')}".lower()
        if ("epitheliotropic" in trial_text or "cutaneous lymphoma" in trial_text) and answers.cancer != "Cutaneous epitheliotropic lymphoma":
            continue

        exc = trial.get("excludes", {})
        reasons: list[str] = []
        unknown: list[str] = []
        excluded = False

        if req.get("confirmed"):
            if answers.diagnosis_status == "Suspected / not confirmed":
                excluded = True
            elif answers.diagnosis_status == UNKNOWN:
                _append_once(unknown, "pathology/cytology confirmation of the diagnosis")

        if req.get("active_treatment_target"):
            if answers.tumor_status in {"Completely removed — clean margins", "No evidence of disease (NED)"}:
                excluded = True
            elif answers.tumor_status in {UNKNOWN, "Removed — margins unknown", "Removed — incomplete/dirty margins"}:
                _append_once(unknown, "whether an active treatment target is present")
        if req.get("measurable_or_lung_metastasis"):
            if answers.tumor_status not in {"Tumor still present / measurable", "Local recurrence"} and answers.metastasis == "No known metastases":
                excluded = True
            elif answers.tumor_status == UNKNOWN or answers.metastasis in {UNKNOWN, "Suspected / staging incomplete"}:
                _append_once(unknown, "whether measurable disease or lung metastasis is present")

        for key, answer, wording in (
            ("standard_therapy_unavailable", answers.standard_therapy_unavailable, "whether standard anticancer treatment is no longer appropriate or feasible"),
            ("large_inoperable_or_rt_preferred", answers.large_inoperable_or_rt_preferred, "whether the tumor is large/inoperable or radiotherapy is preferred to surgery"),
            ("surgery_or_rt_not_possible", answers.surgery_or_rt_not_possible, "whether curative surgery/radiotherapy is no longer possible"),
            ("ct_and_current_biopsy", answers.ct_and_current_biopsy, "whether current CT and biopsy requirements can be met"),
        ):
            if req.get(key):
                if answer == "No":
                    excluded = True
                elif answer == UNKNOWN:
                    _append_once(unknown, wording)

        for key, answer, positive, wording in (
            ("prior_local_radiation", answers.radiation, {"Previously received", "Currently receiving"}, "whether prior local radiation is excluded"),
            ("prior_surgery", answers.surgery, {"Yes"}, "whether prior surgery is excluded"),
            ("prior_chemo", answers.chemo, {"Previously received", "Currently receiving"}, "whether prior chemotherapy is excluded"),
            ("prior_immunotherapy", answers.immunotherapy_history, {"Previously received", "Currently receiving"}, "whether prior immunotherapy is excluded"),
        ):
            if exc.get(key):
                if answer in positive:
                    excluded = True
                elif answer == UNKNOWN:
                    _append_once(unknown, wording)

        if exc.get("immunosuppressive"):
            if answers.immunosuppressive == "Yes":
                excluded = True
            elif answers.immunosuppressive == UNKNOWN:
                _append_once(unknown, "whether immunosuppressive medication is excluded")

        for key, answer, current_value, washout_key, wording in (
            ("current_chemo", answers.chemo, "Currently receiving", "chemo_washout_days", "chemotherapy"),
            ("current_steroids", answers.steroids, "Currently taking", "steroid_washout_days", "steroid"),
            ("current_radiation", answers.radiation, "Currently receiving", "radiation_washout_days", "radiation"),
        ):
            if exc.get(key):
                if answer == current_value:
                    if req.get(washout_key):
                        _append_once(unknown, f"{wording} washout of {req[washout_key]} days")
                    else:
                        excluded = True
                elif answer == UNKNOWN:
                    _append_once(unknown, f"whether current {wording} is excluded")

        if req.get("prior_radiation") is False and answers.radiation in {"Previously received", "Currently receiving"}:
            excluded = True
        elif req.get("prior_radiation") is False and answers.radiation == UNKNOWN:
            _append_once(unknown, "whether prior radiation is excluded")
        if req.get("prior_radiation") is True and answers.radiation == "Never":
            excluded = True
        elif req.get("prior_radiation") is True and answers.radiation == UNKNOWN:
            _append_once(unknown, "whether prior radiation is required")

        if req.get("planned_surgery") or req.get("planned_amputation") or req.get("planned_amputation_and_chemo"):
            if "Surgery" not in answers.preferences:
                excluded = True
            else:
                _append_once(unknown, "required study surgery/amputation has not yet been confirmed")
        if req.get("planned_radiation"):
            if "Radiation" not in answers.preferences or answers.radiation_affordability == "Would not consider radiation":
                excluded = True
            else:
                _append_once(unknown, "required study radiation has not yet been confirmed")
        if req.get("planned_doxorubicin") or req.get("planned_amputation_and_chemo"):
            if "Chemotherapy" not in answers.preferences:
                excluded = True
            else:
                _append_once(unknown, "required study chemotherapy/doxorubicin has not yet been confirmed")

        sex_req = req.get("sex")
        if sex_req:
            allowed = {sex_req} if isinstance(sex_req, str) else set(sex_req)
            if answers.sex == UNKNOWN:
                _append_once(unknown, "sex requirement")
            elif not any(answers.sex.startswith(value) for value in allowed):
                excluded = True

        if req.get("localized"):
            if answers.localized == "No":
                excluded = True
            elif answers.localized == UNKNOWN:
                _append_once(unknown, "whether the disease is localized")
            else:
                reasons.append("localized disease reported")
        if req.get("measurable"):
            if answers.tumor_status not in {"Tumor still present / measurable", "Local recurrence"}:
                if answers.tumor_status == UNKNOWN:
                    _append_once(unknown, "whether measurable disease is present")
                else:
                    excluded = True
        if req.get("metastatic"):
            if answers.metastasis == "No known metastases":
                excluded = True
            elif answers.metastasis in {UNKNOWN, "Suspected / staging incomplete"}:
                _append_once(unknown, "whether metastasis is confirmed")
        if req.get("no_metastasis"):
            if answers.metastasis == "Confirmed metastases":
                excluded = True
            elif answers.metastasis in {UNKNOWN, "Suspected / staging incomplete"}:
                _append_once(unknown, "whether staging confirms no metastasis")

        min_tumor_cm = req.get("min_tumor_cm")
        max_tumor_cm = req.get("max_tumor_cm")
        if min_tumor_cm is not None:
            if answers.tumor_size_cm is not None and answers.tumor_size_cm < min_tumor_cm:
                excluded = True
            elif answers.tumor_size_cm is None:
                _append_once(unknown, f"minimum tumor size of {min_tumor_cm:g} cm")
        if max_tumor_cm is not None:
            if answers.tumor_size_cm is not None and answers.tumor_size_cm > max_tumor_cm:
                excluded = True
            elif answers.tumor_size_cm is None:
                _append_once(unknown, f"maximum tumor size of {max_tumor_cm:g} cm")

        if req.get("appendicular_location"):
            if answers.osa_location in {"Axial — skull, spine, rib, or pelvis", "Other"}:
                excluded = True
            elif answers.osa_location == UNKNOWN:
                _append_once(unknown, "appendicular limb-bone location requirement")

        skin_locations = {
            "Skin / subcutaneous tissue — limb",
            "Skin / subcutaneous tissue — other area",
        }
        limb_locations = {
            "Skin / subcutaneous tissue — limb",
            "Deeper soft tissue — limb",
        }
        superficial_or_oral_locations = skin_locations | {"Mouth / oral cavity"}
        location_unknown = answers.tumor_location in {UNKNOWN, "Other / not sure"}

        if req.get("cutaneous_sts"):
            if not location_unknown and answers.tumor_location not in skin_locations:
                excluded = True
            elif location_unknown:
                _append_once(unknown, "cutaneous/subcutaneous tumor-location requirement")
        if req.get("extremity_sts"):
            if not location_unknown and answers.tumor_location not in limb_locations:
                excluded = True
            elif location_unknown:
                _append_once(unknown, "extremity tumor-location requirement")

        if req.get("superficial_accessible_tumor") or req.get("superficial_or_oral_tumor"):
            if not location_unknown and answers.tumor_location not in superficial_or_oral_locations:
                excluded = True
            elif location_unknown and answers.surface_or_oral_accessible == "No":
                excluded = True
            elif location_unknown and answers.surface_or_oral_accessible == UNKNOWN:
                _append_once(unknown, "whether the tumor is accessible from the body surface or mouth")

        if min_age is not None and answers.age is None:
            _append_once(unknown, f"minimum age of {min_age:g} years")
        if max_age is not None and answers.age is None:
            _append_once(unknown, f"maximum age of {max_age:g} years")
        if min_lb is not None and answers.weight_lb is None:
            _append_once(unknown, f"minimum weight of {min_lb:.1f} lb")
        if max_lb is not None and answers.weight_lb is None:
            _append_once(unknown, f"maximum weight of {max_lb:.1f} lb")

        if req.get("prior_chemo") is False and answers.chemo in {"Previously received", "Currently receiving"}:
            excluded = True
        elif req.get("prior_chemo") is False and answers.chemo == UNKNOWN:
            _append_once(unknown, "whether prior chemotherapy is excluded")
        if req.get("prior_chemo") is True and answers.chemo == "Never":
            excluded = True
        elif req.get("prior_chemo") is True and answers.chemo == UNKNOWN:
            _append_once(unknown, "whether prior chemotherapy is required")
        if req.get("prior_surgery") is True and answers.surgery == "No":
            excluded = True
        elif req.get("prior_surgery") is True and answers.surgery == UNKNOWN:
            _append_once(unknown, "whether prior surgery is required")
        if req.get("prior_surgery") is False and answers.surgery == "Yes":
            excluded = True
        elif req.get("prior_surgery") is False and answers.surgery == UNKNOWN:
            _append_once(unknown, "whether prior surgery is excluded")

        if req.get("post_splenectomy"):
            if answers.surgery == "No" or answers.prior_procedure == "Other":
                excluded = True
            elif answers.surgery == UNKNOWN or answers.prior_procedure != "Splenectomy":
                _append_once(unknown, "whether splenectomy has been performed")
        if req.get("post_amputation"):
            if answers.surgery == "No" or answers.prior_procedure in {"Limb-sparing surgery", "Other"}:
                excluded = True
            elif answers.surgery == UNKNOWN or answers.prior_procedure != "Amputation":
                _append_once(unknown, "whether amputation has been performed")
        if req.get("pretreatment_biopsy"):
            _append_once(unknown, "pretreatment biopsy requirement")
        if req.get("resectable_or_minimal"):
            _append_once(unknown, "whether disease is resectable/minimal as required")
        if req.get("progressive"):
            if answers.cancer in {"B-cell lymphoma", "T-cell lymphoma", "Lymphoma — other"}:
                if answers.lymphoma_response != "Progression during treatment":
                    if answers.lymphoma_response == UNKNOWN:
                        _append_once(unknown, "whether disease is progressive")
                    else:
                        excluded = True
            else:
                _append_once(unknown, "whether disease is progressive")
        if req.get("relapsed_or_refractory"):
            allowed = {"Progression during treatment", "First relapse after remission", "More than one relapse"}
            if answers.cancer in {"B-cell lymphoma", "T-cell lymphoma", "Lymphoma — other"}:
                if answers.lymphoma_response not in allowed:
                    if answers.lymphoma_response == UNKNOWN:
                        _append_once(unknown, "whether lymphoma is relapsed/refractory")
                    else:
                        excluded = True
            else:
                _append_once(unknown, "whether disease is relapsed/refractory")

        # Preserve the short questionnaire: unanswered protocol-specific fields
        # are disclosed as study-team prescreening items, never treated as passed.
        for key, wording in PRESCREEN_REQUIREMENTS.items():
            if key in {"cutaneous_sts", "extremity_sts"}:
                continue
            if req.get(key):
                _append_once(unknown, wording)
        for key, wording in PRESCREEN_EXCLUSIONS.items():
            if exc.get(key):
                _append_once(unknown, f"whether {wording} is excluded")
        if trial.get("special_requirement"):
            _append_once(unknown, str(trial["special_requirement"]))

        if excluded:
            continue

        reasons.append(
            "broad disease-family eligibility supports investigator review"
            if broad_match else f"{answers.cancer} matches the study disease category"
        )
        if answers.diagnosis_status == "Confirmed by pathology/cytology":
            reasons.append("diagnosis reported as confirmed")
        if answers.tumor_status == "Tumor still present / measurable":
            reasons.append("gross/measurable tumor reported")

        label = "May qualify — study team must confirm"
        if broad_match:
            label = "Broad trial — diagnosis review required"
        if trial.get("study_type") == "other_treatment_access":
            label = "Other treatment-access opportunity"
            reasons = [reason for reason in reasons if reason != "diagnosis reported as confirmed"]
            reasons.insert(0, "funded/assisted standard anticancer treatment is available through this study pathway")

        results.append(Match(label, trial, tuple(reasons), tuple(unknown)))

    priority = {
        "May qualify — study team must confirm": 0,
        "Broad trial — diagnosis review required": 1,
        "Other treatment-access opportunity": 2,
    }
    results.sort(key=lambda match: (priority.get(match.label, 3), bool(match.trial.get("early_phase"))))
    return results
