import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from oa_matcher import SUPPORTED_EXCLUDES, SUPPORTED_REQUIRES, validate_rule_schema

DATA = ROOT / "data" / "oa_trials.json"
PAGE = ROOT / "pages" / "4_Osteoarthritis_Trial_Finder.py"

trials = json.loads(DATA.read_text(encoding="utf-8"))
assert trials, "OA catalog is empty"

required = {
    "id", "title", "center", "country", "species", "status", "status_confidence",
    "study_type", "intervention", "protocol_key", "sites", "url", "verified",
    "requires", "excludes", "criteria_completeness", "notes",
}
ids, protocol_keys = set(), set()
for trial in trials:
    missing = required - set(trial)
    assert not missing, f"{trial.get('id', '<no id>')} missing {sorted(missing)}"
    assert trial["id"] not in ids, f"duplicate id: {trial['id']}"
    assert trial["protocol_key"] not in protocol_keys, f"duplicate protocol: {trial['protocol_key']}"
    ids.add(trial["id"]); protocol_keys.add(trial["protocol_key"])
    assert trial["species"] in {"Dog", "Cat"}
    assert trial["status_confidence"] == "current"
    assert trial["study_type"] == "treatment"
    assert trial["criteria_completeness"] in {"detailed", "limited"}
    assert trial["url"].startswith("https://")
    assert re.fullmatch(r"2026-\d{2}-\d{2}", trial["verified"])
    assert isinstance(trial["sites"], list) and trial["sites"]
    validate_rule_schema(trial)

# Guard against silent schema drift in either direction.
used_requires = {key for t in trials for key in t["requires"]}
used_excludes = {key for t in trials for key in t["excludes"]}
assert used_requires <= SUPPORTED_REQUIRES
assert used_excludes <= SUPPORTED_EXCLUDES

# Semantic duplicate guard: these identity signals together describe one protocol.
def norm(value):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.lower()).split())

seen_identity = set()
for trial in trials:
    identity = (
        trial["species"], norm(trial["intervention"]),
        norm(trial.get("sponsor", trial["center"])),
        tuple(sorted(trial["requires"].get("affected_joint", []))),
    )
    assert identity not in seen_identity, f"probable semantic duplicate: {trial['id']}"
    seen_identity.add(identity)

# Protocol facts whose regression would materially change matching.
by_id = {t["id"]: t for t in trials}
assert by_id["wvrc-oa-vaccine-2026"]["excludes"]["prior_librela"] is True
assert by_id["wvrc-oa-vaccine-2026"]["requires"]["min_symptom_months"] == 3
assert by_id["utk-polymer-beads-hip-oa-2026"]["requires"]["affected_joint"] == ["Hip"]
assert by_id["umn-fehi-feline-oa-2026"]["requires"]["stable_solensia_months"] == 3
assert by_id["cornell-prp-stifle-oa-2026"]["requires"]["single_affected_joint"] is True

py_compile.compile(str(ROOT / "oa_matcher.py"), doraise=True)
py_compile.compile(str(PAGE), doraise=True)

print(f"OA validation passed: {len(trials)} unique current treatment protocols; {len(used_requires) + len(used_excludes)} rule types checked.")
