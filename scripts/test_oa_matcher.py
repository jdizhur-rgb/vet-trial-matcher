import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from oa_matcher import UNKNOWN, PatientProfile, evaluate_trial, find_matches

TRIALS = json.loads((ROOT / "data" / "oa_trials.json").read_text(encoding="utf-8"))
BY_ID = {trial["id"]: trial for trial in TRIALS}


def dog(**changes):
    base = PatientProfile(
        species="Dog", age_years=4, weight_kg=25, diagnosis="Yes", xray="Yes",
        joints=("Hip",), lameness="Yes", mobility="Yes", symptom_months=6,
        hip_dysplasia="Yes", librela="No", current_meds=("None",),
        prior_joint_surgery="No", prior_joint_injection="No", prior_prp_or_stem_cells="No",
        other_ortho="No", neurologic="No", immune="No", pregnant="No", oral_medication="Yes",
    )
    return replace(base, **changes)


def cat(**changes):
    base = PatientProfile(
        species="Cat", age_years=10, weight_kg=5, diagnosis="Yes", xray="Yes",
        joints=("Hip",), lameness="Yes", mobility="Yes", symptom_months=12,
        solensia="Not receiving", current_meds=("None",), other_ortho="No",
        neurologic="No", immune="No", indoor_only="Yes", pregnant="No", oral_medication="Yes",
    )
    return replace(base, **changes)


class OAMatcherTests(unittest.TestCase):
    def result(self, trial_id, profile):
        return evaluate_trial(BY_ID[trial_id], profile)

    def test_species_is_hard_filter(self):
        self.assertIsNone(self.result("umn-fehi-feline-oa-2026", dog()))
        self.assertIsNone(self.result("wvrc-oa-vaccine-2026", cat()))

    def test_age_boundaries_are_inclusive(self):
        trial = "utk-oa-collar-2026"
        self.assertIsNotNone(self.result(trial, dog(age_years=1, joints=("Elbow",))))
        self.assertIsNotNone(self.result(trial, dog(age_years=8, joints=("Elbow",))))
        self.assertIsNone(self.result(trial, dog(age_years=0.99, joints=("Elbow",))))
        self.assertIsNone(self.result(trial, dog(age_years=8.01, joints=("Elbow",))))
        self.assertIn("needs confirmation", self.result(trial, dog(age_years=None, joints=("Elbow",))).confidence.lower())

    def test_weight_boundaries_are_inclusive(self):
        trial = "utk-oa-collar-2026"
        self.assertIsNotNone(self.result(trial, dog(weight_kg=15, joints=("Shoulder",))))
        self.assertIsNotNone(self.result(trial, dog(weight_kg=40, joints=("Shoulder",))))
        self.assertIsNone(self.result(trial, dog(weight_kg=14.99, joints=("Shoulder",))))
        self.assertIsNone(self.result(trial, dog(weight_kg=40.01, joints=("Shoulder",))))
        self.assertIsNotNone(self.result(trial, dog(weight_kg=None, joints=("Shoulder",))))

    def test_xray_screening_does_not_reject_no_or_unknown(self):
        for value in ("No", UNKNOWN):
            result = self.result("wvrc-oa-vaccine-2026", dog(xray=value))
            self.assertIsNotNone(result)
            self.assertEqual(result.confidence, "Possible match — needs confirmation")

    def test_wrong_joint_and_multiple_joint_rules(self):
        self.assertIsNone(self.result("utk-polymer-beads-hip-oa-2026", dog(joints=("Elbow",))))
        self.assertIsNotNone(self.result("utk-polymer-beads-hip-oa-2026", dog(joints=("Hip", "Elbow"))))
        self.assertIsNone(self.result("cornell-prp-stifle-oa-2026", dog(joints=("Stifle / knee", "Hip"))))
        self.assertIsNotNone(self.result("cornell-prp-stifle-oa-2026", dog(joints=(), hip_dysplasia=UNKNOWN)))

    def test_required_lameness_and_mobility(self):
        self.assertIsNone(self.result("utk-oa-collar-2026", dog(joints=("Elbow",), lameness="No")))
        self.assertIsNone(self.result("utk-oa-collar-2026", dog(joints=("Elbow",), mobility="No")))
        self.assertIsNotNone(self.result("utk-oa-collar-2026", dog(joints=("Elbow",), lameness=UNKNOWN, mobility=UNKNOWN)))

    def test_symptom_duration_boundary(self):
        trial = "wvrc-oa-vaccine-2026"
        self.assertIsNone(self.result(trial, dog(symptom_months=2)))
        self.assertIsNotNone(self.result(trial, dog(symptom_months=3)))
        self.assertIsNotNone(self.result(trial, dog(symptom_months=4)))
        self.assertEqual(self.result(trial, dog(symptom_months=None)).confidence, "Possible match — needs confirmation")

    def test_librela_known_exclusion_and_unknown(self):
        trial = "wvrc-oa-vaccine-2026"
        self.assertIsNone(self.result(trial, dog(librela="Yes")))
        self.assertIsNotNone(self.result(trial, dog(librela="No")))
        self.assertEqual(self.result(trial, dog(librela=UNKNOWN)).confidence, "Possible match — needs confirmation")

    def test_medications_and_washout(self):
        trial = "utk-oa-collar-2026"
        self.assertIsNotNone(self.result(trial, dog(joints=("Elbow",), current_meds=("NSAID", "Gabapentin"))))
        self.assertIsNone(self.result(trial, dog(joints=("Elbow",), current_meds=("Other pain medication",))))
        result = self.result(trial, dog(joints=("Elbow",), current_meds=("Joint supplement",)))
        self.assertIn("washout", " ".join(result.confirmations))
        result = self.result("umn-fehi-feline-oa-2026", cat(current_meds=("NSAID",)))
        self.assertIn("washout", " ".join(result.confirmations))

    def test_solensia_stability(self):
        self.assertIsNotNone(self.result("umn-fehi-feline-oa-2026", cat(solensia="Yes")))
        result = self.result("umn-fehi-feline-oa-2026", cat(solensia="No"))
        self.assertIn("Solensia", " ".join(result.confirmations))

    def test_previous_procedure_rules_are_enforced_when_present(self):
        synthetic = dict(BY_ID["wvrc-oa-vaccine-2026"])
        synthetic["excludes"] = {**synthetic["excludes"], "prior_joint_surgery": True, "prior_joint_injection": True, "prior_prp_or_stem_cells": True}
        for field in ("prior_joint_surgery", "prior_joint_injection", "prior_prp_or_stem_cells"):
            self.assertIsNone(evaluate_trial(synthetic, dog(**{field: "Yes"})))
            self.assertIsNotNone(evaluate_trial(synthetic, dog(**{field: UNKNOWN})))

    def test_orthopedic_neurologic_and_immune_exclusions(self):
        trial = "utk-polymer-beads-hip-oa-2026"
        self.assertIsNone(self.result(trial, dog(other_ortho="Yes")))
        self.assertIsNone(self.result(trial, dog(neurologic="Yes")))
        self.assertIsNone(self.result(trial, dog(immune="Yes")))
        self.assertIsNotNone(self.result(trial, dog(other_ortho=UNKNOWN, neurologic=UNKNOWN, immune=UNKNOWN)))

    def test_indoor_outdoor_and_unknown_cat(self):
        trial = "umn-fehi-feline-oa-2026"
        self.assertIsNotNone(self.result(trial, cat(indoor_only="Yes")))
        self.assertIsNone(self.result(trial, cat(indoor_only="No")))
        self.assertEqual(self.result(trial, cat(indoor_only=UNKNOWN)).confidence, "Possible match — needs confirmation")

    def test_unknown_never_becomes_hard_exclusion(self):
        unknown_profile = PatientProfile(species="Dog")
        self.assertTrue(find_matches(TRIALS, unknown_profile))

    def test_potential_possible_and_zero_match_states(self):
        potential = self.result("wvrc-oa-vaccine-2026", dog())
        self.assertEqual(potential.confidence, "Potential match")
        possible = self.result("clinaxel-cx25-011-feline-oa", cat())
        self.assertEqual(possible.confidence, "Possible match — needs confirmation")
        zero = find_matches(TRIALS, dog(age_years=0.1, diagnosis="No", xray="No", joints=("Carpus / wrist",), lameness="No", mobility="No", librela="Yes"))
        self.assertEqual(zero, [])

    def test_new_unknown_rule_fails_closed_in_validation(self):
        broken = dict(BY_ID["wvrc-oa-vaccine-2026"])
        broken["requires"] = {**broken["requires"], "future_unhandled_rule": True}
        with self.assertRaises(ValueError):
            evaluate_trial(broken, dog())


if __name__ == "__main__":
    unittest.main(verbosity=2)
