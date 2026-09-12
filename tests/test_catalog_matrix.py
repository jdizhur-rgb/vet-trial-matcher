import unittest

from matcher_engine import BLOCKED_STATUS_PHRASES, SearchAnswers, match_trials
from trial_catalog import CANCERS, load_trials, trial_accepts_diagnosis, trial_modalities


class CatalogMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trials = load_trials()

    def test_every_species_and_cancer_combination_is_safe(self):
        for species in ("Dog", "Cat"):
            for cancer in CANCERS:
                if cancer in {"Cancer — any type", "Other / not sure", "My cancer type isn't listed"}:
                    continue
                with self.subTest(species=species, cancer=cancer):
                    matches = match_trials(
                        self.trials,
                        SearchAnswers(species=species, cancer=cancer),
                        accepts_diagnosis=trial_accepts_diagnosis,
                        trial_modalities=trial_modalities,
                    )
                    ids = [match.trial["id"] for match in matches]
                    self.assertEqual(len(ids), len(set(ids)))
                    for match in matches:
                        status = str(match.trial.get("status", "")).lower()
                        self.assertFalse(any(value in status for value in BLOCKED_STATUS_PHRASES))

    def test_suspected_diagnosis_never_passes_confirmed_requirement(self):
        for species in ("Dog", "Cat"):
            for cancer in CANCERS:
                if cancer in {"Cancer — any type", "Other / not sure", "My cancer type isn't listed"}:
                    continue
                matches = match_trials(
                    self.trials,
                    SearchAnswers(
                        species=species,
                        cancer=cancer,
                        diagnosis_status="Suspected / not confirmed",
                    ),
                    accepts_diagnosis=trial_accepts_diagnosis,
                    trial_modalities=trial_modalities,
                )
                for match in matches:
                    self.assertFalse(match.trial.get("requires", {}).get("confirmed"))

    def test_each_country_can_be_selected_without_losing_other_countries(self):
        countries = sorted({
            trial.get("country", "USA") for trial in self.trials
            if trial.get("status_confidence") in {"current", "confirmed_current"}
        })
        self.assertGreater(len(countries), 1)
        for country in countries:
            with self.subTest(country=country):
                matches = match_trials(
                    self.trials,
                    SearchAnswers(species="Dog", cancer="Cancer — any type"),
                    accepts_diagnosis=trial_accepts_diagnosis,
                    trial_modalities=trial_modalities,
                    country_matches=lambda trial_country, selected=country: trial_country == selected,
                )
                self.assertTrue(all(match.trial.get("country", "USA") == country for match in matches))


if __name__ == "__main__":
    unittest.main()
