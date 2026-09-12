import unittest

from matcher_engine import BLOCKED_STATUS_PHRASES, SearchAnswers, match_trials
from trial_catalog import load_trials, trial_accepts_diagnosis, trial_modalities


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
    "Ocular melanoma / iris melanocytic tumor", "Oral melanoma",
    "Oral squamous cell carcinoma", "Oral tumor — other", "Osteosarcoma",
    "Other bone tumor", "Other liver tumor", "Other sarcoma", "Other solid tumor",
    "Pancreatic carcinoma", "Peripheral nerve sheath tumor", "Primary lung tumor",
    "Prostate cancer", "Renal tumor", "Rhabdomyosarcoma", "Salivary gland cancer",
    "Sinonasal carcinoma", "Soft tissue sarcoma", "Spindle cell sarcoma",
    "Squamous cell carcinoma", "Squamous cell carcinoma — other", "T-cell lymphoma",
    "Thymoma / thymic tumor", "Thyroid carcinoma", "Thyroid tumor / carcinoma",
    "Urothelial / transitional cell carcinoma", "Urothelial carcinoma",
]


class CatalogMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trials = load_trials()

    def test_every_species_and_cancer_combination_is_safe(self):
        for species in ("Dog", "Cat"):
            for cancer in CANCERS:
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
                        self.assertEqual("USA", match.trial.get("country", "USA"))
                        status = str(match.trial.get("status", "")).lower()
                        self.assertFalse(any(value in status for value in BLOCKED_STATUS_PHRASES))

    def test_suspected_diagnosis_never_passes_confirmed_requirement(self):
        for species in ("Dog", "Cat"):
            for cancer in CANCERS:
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


if __name__ == "__main__":
    unittest.main()
