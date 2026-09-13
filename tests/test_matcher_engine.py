import unittest

from matcher_engine import SearchAnswers, match_trials
from trial_catalog import load_trials, trial_accepts_diagnosis, trial_modalities


ALL_TREATMENTS = frozenset({
    "Chemotherapy", "Radiation", "Surgery", "Immunotherapy",
    "Targeted therapy", "Experimental drug",
})


def run_real(answers):
    return match_trials(
        load_trials(), answers,
        accepts_diagnosis=trial_accepts_diagnosis,
        trial_modalities=trial_modalities,
        country_matches=lambda country: country == "USA",
    )


class MatcherEngineTests(unittest.TestCase):
    def test_engine_has_no_implicit_country_preference(self):
        trials = [
            {
                "id": country, "species": "Dog", "country": country,
                "cancers": ["Test cancer"], "status": "Recruiting",
                "status_confidence": "confirmed_current", "study_type": "treatment",
            }
            for country in ("USA", "France")
        ]
        matches = match_trials(
            trials, SearchAnswers(species="Dog", cancer="Test cancer"),
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual({"USA", "France"}, {match.trial["country"] for match in matches})

    def test_yasha_does_not_match_any_us_hs_trial(self):
        answers = SearchAnswers(
            species="Dog",
            cancer="Histiocytic sarcoma",
            diagnosis_status="Confirmed by pathology/cytology",
            age=13,
            weight_lb=24.25,
            tumor_status="Removed — incomplete/dirty margins",
            metastasis="No known metastases",
            localized="Yes",
            surgery="Yes",
            chemo="Currently receiving",
            immunotherapy_history="Never",
            radiation="Never",
            preferences=ALL_TREATMENTS,
        )
        ids = {match.trial["id"] for match in run_real(answers)}
        hs_ids = {
            "uf-hs-trametinib", "auburn-palbociclib-solid-cancers",
            "msu-hs-quasiorganelle", "msu-hs-sting-cmp002",
        }
        self.assertFalse(ids.intersection(hs_ids), ids.intersection(hs_ids))

    def test_unknown_age_does_not_exclude_trial(self):
        trial = {
            "id": "age-test", "species": "Dog", "country": "USA",
            "cancers": ["Test cancer"], "status": "Recruiting",
            "status_confidence": "confirmed_current", "study_type": "treatment",
            "requires": {"min_age_years": 2},
        }
        matches = match_trials(
            [trial], SearchAnswers(species="Dog", cancer="Test cancer"),
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual(1, len(matches))
        self.assertIn("minimum age", " ".join(matches[0].needs_confirmation))

    def test_unasked_protocol_detail_is_disclosed_for_prescreening(self):
        trial = {
            "id": "size-test", "species": "Dog", "country": "USA",
            "cancers": ["Test cancer"], "status": "Recruiting",
            "status_confidence": "confirmed_current", "study_type": "treatment",
            "requires": {"min_tumor_cm": 2},
        }
        matches = match_trials(
            [trial], SearchAnswers(species="Dog", cancer="Test cancer"),
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual(1, len(matches))
        self.assertIn("minimum tumor size", " ".join(matches[0].needs_confirmation))

    def test_known_tumor_size_can_exclude_a_trial(self):
        trial = {
            "id": "size-test", "species": "Dog", "country": "USA",
            "cancers": ["Test cancer"], "status": "Recruiting",
            "status_confidence": "confirmed_current", "study_type": "treatment",
            "requires": {"min_tumor_cm": 2},
        }
        answers = SearchAnswers(species="Dog", cancer="Test cancer", tumor_size_cm=1.5)
        matches = match_trials(
            [trial], answers,
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual([], matches)

    def test_inaccessible_surface_tumor_can_exclude_a_trial(self):
        trial = {
            "id": "access-test", "species": "Dog", "country": "USA",
            "cancers": ["Test cancer"], "status": "Recruiting",
            "status_confidence": "confirmed_current", "study_type": "treatment",
            "requires": {"superficial_accessible_tumor": True},
        }
        answers = SearchAnswers(
            species="Dog", cancer="Test cancer", surface_or_oral_accessible="No",
        )
        matches = match_trials(
            [trial], answers,
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual([], matches)

    def test_known_non_extremity_location_excludes_extremity_trial(self):
        trial = {
            "id": "location-test", "species": "Dog", "country": "USA",
            "cancers": ["Test cancer"], "status": "Recruiting",
            "status_confidence": "confirmed_current", "study_type": "treatment",
            "requires": {"extremity_sts": True},
        }
        answers = SearchAnswers(
            species="Dog", cancer="Test cancer",
            tumor_location="Deeper soft tissue — other area",
        )
        matches = match_trials(
            [trial], answers,
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual([], matches)

    def test_current_chemo_with_published_washout_remains_possible(self):
        trial = {
            "id": "washout-test", "species": "Dog", "country": "USA",
            "cancers": ["Test cancer"], "status": "Recruiting",
            "status_confidence": "confirmed_current", "study_type": "treatment",
            "requires": {"chemo_washout_days": 14},
            "excludes": {"current_chemo": True},
        }
        answers = SearchAnswers(species="Dog", cancer="Test cancer", chemo="Currently receiving")
        matches = match_trials(
            [trial], answers,
            accepts_diagnosis=lambda trial, cancer: (cancer in trial["cancers"], False),
            trial_modalities=lambda trial: set(),
        )
        self.assertEqual(1, len(matches))
        self.assertIn("washout of 14 days", " ".join(matches[0].needs_confirmation))


if __name__ == "__main__":
    unittest.main()
