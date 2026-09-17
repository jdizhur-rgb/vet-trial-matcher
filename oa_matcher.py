"""Pure, testable eligibility logic for the OA research matcher."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

UNKNOWN = "I don't know"

SUPPORTED_REQUIRES = {
    "min_age_years", "max_age_years", "min_weight_kg", "max_weight_kg",
    "radiographic_oa", "oa_or_mobility_problem", "diagnosed_oa", "lameness",
    "mobility_problem", "affected_joint", "single_affected_joint",
    "hip_dysplasia_related", "min_symptom_months", "indoor_only",
    "decreased_muscle_mass", "supplement_washout_days",
    "medication_washout_days", "stable_solensia_months", "oral_medication",
}
SUPPORTED_EXCLUDES = {
    "prior_librela", "joint_instability", "other_orthopedic_disease",
    "non_oa_gait_problem", "neurologic_gait_disease", "immune_mediated_disease",
    "pregnant", "current_medications", "prior_joint_surgery",
    "prior_joint_injection", "prior_prp_or_stem_cells",
}


@dataclass(frozen=True)
class PatientProfile:
    species: str
    age_years: float | None = None
    weight_kg: float | None = None
    diagnosis: str = UNKNOWN
    xray: str = UNKNOWN
    joints: tuple[str, ...] = ()
    lameness: str = UNKNOWN
    mobility: str = UNKNOWN
    symptom_months: int | None = None
    hip_dysplasia: str = UNKNOWN
    librela: str = UNKNOWN
    solensia: str = UNKNOWN
    current_meds: tuple[str, ...] = ()
    prior_joint_surgery: str = UNKNOWN
    prior_joint_injection: str = UNKNOWN
    prior_prp_or_stem_cells: str = UNKNOWN
    other_ortho: str = UNKNOWN
    neurologic: str = UNKNOWN
    immune: str = UNKNOWN
    indoor_only: str = UNKNOWN
    pregnant: str = UNKNOWN
    oral_medication: str = UNKNOWN


@dataclass(frozen=True)
class MatchResult:
    confidence: str
    trial: dict[str, Any]
    reasons: tuple[str, ...] = field(default_factory=tuple)
    confirmations: tuple[str, ...] = field(default_factory=tuple)


def _unique(items: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


def validate_rule_schema(trial: dict[str, Any]) -> None:
    unknown_requires = set(trial.get("requires", {})) - SUPPORTED_REQUIRES
    unknown_excludes = set(trial.get("excludes", {})) - SUPPORTED_EXCLUDES
    if unknown_requires or unknown_excludes:
        raise ValueError(
            f"{trial.get('id', '<unknown>')} has unsupported rules: "
            f"requires={sorted(unknown_requires)}, excludes={sorted(unknown_excludes)}"
        )


def evaluate_trial(trial: dict[str, Any], patient: PatientProfile) -> MatchResult | None:
    """Return a conservative match result, or None for a known hard mismatch."""
    validate_rule_schema(trial)
    if trial.get("species") != patient.species or trial.get("status_confidence") != "current":
        return None

    req, exc = trial.get("requires", {}), trial.get("excludes", {})
    reasons: list[str] = []
    confirm: list[str] = []

    for key, label, value in (
        ("min_age_years", "minimum age", patient.age_years),
        ("min_weight_kg", "minimum weight", patient.weight_kg),
    ):
        limit = req.get(key)
        if limit is not None:
            if value is None:
                confirm.append(f"{label} {limit:g}{' years' if 'age' in key else ' kg'}")
            elif value < limit:
                return None
    for key, label, value in (
        ("max_age_years", "maximum age", patient.age_years),
        ("max_weight_kg", "maximum weight", patient.weight_kg),
    ):
        limit = req.get(key)
        if limit is not None:
            if value is None:
                confirm.append(f"{label} {limit:g}{' years' if 'age' in key else ' kg'}")
            elif value > limit:
                return None

    if req.get("diagnosed_oa"):
        if patient.diagnosis == "No":
            return None
        if patient.diagnosis != "Yes":
            confirm.append("a veterinary diagnosis of osteoarthritis")
        else:
            reasons.append("osteoarthritis diagnosis reported")
    if req.get("oa_or_mobility_problem"):
        if patient.diagnosis == "Yes" or patient.mobility == "Yes":
            reasons.append("OA or a mobility problem reported")
        elif patient.diagnosis == "No" and patient.mobility == "No":
            return None
        else:
            confirm.append("OA or a qualifying mobility problem")
    if req.get("radiographic_oa"):
        if patient.xray == "Yes":
            reasons.append("OA reported as confirmed on X-rays")
        elif patient.xray == "No" and trial.get("xray_at_screening"):
            confirm.append("radiographic OA confirmation at study screening")
        elif patient.xray == "No":
            return None
        else:
            confirm.append("radiographic OA confirmation")
    for key, value, label in (
        ("lameness", patient.lameness, "required lameness"),
        ("mobility_problem", patient.mobility, "required mobility impairment"),
    ):
        if req.get(key):
            if value == "No":
                return None
            if value == UNKNOWN:
                confirm.append(label)
            else:
                reasons.append(label.replace("required ", "") + " reported")

    allowed_joints = req.get("affected_joint")
    known_joints = {j for j in patient.joints if j != UNKNOWN}
    if allowed_joints:
        if known_joints and not known_joints.intersection(allowed_joints):
            return None
        if not known_joints:
            confirm.append("affected joint: " + ", ".join(allowed_joints))
        else:
            reasons.append("affected joint matches the public criteria")
    if req.get("single_affected_joint"):
        if len(known_joints) > 1 or "Multiple / other" in known_joints:
            return None
        if not known_joints:
            confirm.append("only one qualifying joint is affected")
    if req.get("hip_dysplasia_related"):
        if patient.hip_dysplasia == "No":
            return None
        if patient.hip_dysplasia == UNKNOWN:
            confirm.append("hip dysplasia as the cause of hip OA")
        else:
            reasons.append("hip dysplasia reported")
    minimum_months = req.get("min_symptom_months")
    if minimum_months is not None:
        if patient.symptom_months is None:
            confirm.append(f"symptoms present for at least {minimum_months} months")
        elif patient.symptom_months < minimum_months:
            return None
        else:
            reasons.append(f"symptom duration meets the {minimum_months}-month minimum")
    if req.get("indoor_only"):
        if patient.indoor_only == "No":
            return None
        if patient.indoor_only == UNKNOWN:
            confirm.append("indoor-only requirement")
        else:
            reasons.append("indoor-only requirement reported as met")
    if req.get("decreased_muscle_mass"):
        confirm.append("decreased muscle mass on study-team assessment")
    if req.get("oral_medication"):
        if patient.oral_medication == "No":
            return None
        if patient.oral_medication == UNKNOWN:
            confirm.append("ability to receive oral medication without undue stress")

    if req.get("supplement_washout_days") and "Joint supplement" in patient.current_meds:
        confirm.append(f"joint-supplement washout of {req['supplement_washout_days']} days")
    if req.get("medication_washout_days") and any(m not in {"None", UNKNOWN} for m in patient.current_meds):
        confirm.append(f"medication washout of at least {req['medication_washout_days']} days")
    if req.get("stable_solensia_months") and patient.solensia != "Not receiving":
        if patient.solensia != "Yes":
            confirm.append(f"Solensia stable for at least {req['stable_solensia_months']} months or protocol washout")

    if exc.get("prior_librela"):
        if patient.librela == "Yes":
            return None
        if patient.librela == UNKNOWN:
            confirm.append("no previous Librela exposure")
    gait_exclusion = any(exc.get(k) for k in ("joint_instability", "other_orthopedic_disease", "non_oa_gait_problem"))
    if gait_exclusion:
        if patient.other_ortho == "Yes":
            return None
        if patient.other_ortho == UNKNOWN:
            confirm.append("no other orthopedic cause of gait problems")
    for key, value, label in (
        ("neurologic_gait_disease", patient.neurologic, "no neurologic disease affecting gait"),
        ("immune_mediated_disease", patient.immune, "no immune-mediated disease"),
        ("pregnant", patient.pregnant, "not pregnant"),
        ("prior_joint_surgery", patient.prior_joint_surgery, "no disqualifying prior joint surgery"),
        ("prior_joint_injection", patient.prior_joint_injection, "no disqualifying prior joint injection"),
        ("prior_prp_or_stem_cells", patient.prior_prp_or_stem_cells, "no disqualifying prior PRP or stem-cell treatment"),
    ):
        if exc.get(key):
            if value == "Yes":
                return None
            if value == UNKNOWN:
                confirm.append(label)
    disallowed_meds = set(exc.get("current_medications", []))
    if disallowed_meds.intersection(patient.current_meds):
        return None

    # Sparse public criteria must never produce an overconfident result.
    if trial.get("criteria_completeness") != "detailed":
        confirm.append("additional eligibility criteria are not publicly available")
    confirm.extend(trial.get("study_team_confirmation", []))

    if not reasons:
        reasons.append("no known public criterion rules this study out")
    confidence = "Potential match" if not confirm else "Possible match — needs confirmation"
    return MatchResult(confidence, trial, _unique(reasons), _unique(confirm))


def find_matches(trials: list[dict[str, Any]], patient: PatientProfile) -> list[MatchResult]:
    matches = [result for trial in trials if (result := evaluate_trial(trial, patient)) is not None]
    return sorted(matches, key=lambda x: (x.confidence != "Potential match", x.trial["center"]))
