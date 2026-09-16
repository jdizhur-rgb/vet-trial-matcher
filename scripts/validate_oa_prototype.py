import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "oa_trials.json"
PAGE = ROOT / "pages" / "4_Osteoarthritis_Trial_Finder.py"

trials = json.loads(DATA.read_text(encoding="utf-8"))
assert trials, "OA catalog is empty"
assert len(trials) >= 9, f"Expected at least 9 vetted OA protocols, got {len(trials)}"

required = {"id", "title", "center", "country", "species", "status", "status_confidence", "study_type", "url", "verified", "requires", "excludes"}
ids = set()
for t in trials:
    missing = required - set(t)
    assert not missing, f"{t.get('id', '<no id>')} missing {sorted(missing)}"
    assert t["id"] not in ids, f"duplicate id: {t['id']}"
    ids.add(t["id"])
    assert t["species"] in {"Dog", "Cat"}, (t["id"], t["species"])
    assert t["status_confidence"] == "current", f"non-current record in patient-facing OA data: {t['id']}"
    assert t["study_type"] == "treatment", f"non-treatment record in patient-facing OA data: {t['id']}"
    assert t["url"].startswith("https://"), f"non-https source: {t['id']}"
    assert isinstance(t["requires"], dict) and isinstance(t["excludes"], dict)

# Known protocol facts that must not regress during later edits.
by_id = {t["id"]: t for t in trials}
assert by_id["wvrc-oa-vaccine-2026"]["excludes"].get("prior_librela") is True
assert by_id["wvrc-oa-vaccine-2026"]["requires"].get("min_symptom_months") == 3
assert by_id["utk-polymer-beads-hip-oa-2026"]["requires"].get("affected_joint") == ["Hip"]
assert by_id["utk-polymer-beads-hip-oa-2026"]["requires"].get("hip_dysplasia_related") is True
assert by_id["umn-fehi-feline-oa-2026"]["requires"].get("indoor_only") is True
assert by_id["cornell-prp-stifle-oa-2026"]["requires"].get("affected_joint") == ["Stifle / knee"]

# Basic duplicate guard: same normalized title + species should never appear twice.
def norm(s):
    return " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in s).split())
seen = set()
for t in trials:
    key = (t["species"], norm(t["title"]))
    assert key not in seen, f"probable exact-title duplicate: {t['title']}"
    seen.add(key)

# Compile the actual Streamlit page so syntax/import-time parse errors fail CI.
py_compile.compile(str(PAGE), doraise=True)

# Ensure every matching rule used by the data is implemented by the page.
page = PAGE.read_text(encoding="utf-8")
rule_tokens = {
    "min_age_years", "max_age_years", "min_weight_kg", "max_weight_kg",
    "radiographic_oa", "oa_or_mobility_problem", "lameness", "mobility_problem",
    "affected_joint", "hip_dysplasia_related", "min_symptom_months", "indoor_only",
    "decreased_muscle_mass", "supplement_washout_days", "prior_librela",
    "joint_instability", "other_orthopedic_disease", "non_oa_gait_problem",
    "neurologic_gait_disease", "immune_mediated_disease"
}
used = {k for t in trials for side in ("requires", "excludes") for k in t[side]}
unimplemented = sorted(k for k in used if k not in page)
assert not unimplemented, f"catalog rules not implemented by matcher: {unimplemented}"

print(f"OA prototype validation passed: {len(trials)} current treatment protocols; {len(used)} rule types checked.")
