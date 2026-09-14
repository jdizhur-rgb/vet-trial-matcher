import unittest

from result_actions import clean_funding_text, compact_confirmations, contact_actions, verification_label


class ResultActionTests(unittest.TestCase):
    def test_extracts_email_and_us_phone(self):
        email, phone = contact_actions("Team — trials@example.edu · (509) 592-3668")
        self.assertEqual(email, "trials@example.edu")
        self.assertEqual(phone, "5095923668")

    def test_does_not_treat_date_as_phone(self):
        self.assertEqual(contact_actions("Verified 2026-09-10"), (None, None))

    def test_formats_verification_date(self):
        self.assertEqual(verification_label("2026-09-10"), "Last checked: Sep 10, 2026")

    def test_removes_funding_badge(self):
        self.assertEqual(clean_funding_text("🟢 Fully funded after enrollment."), "Fully funded after enrollment.")

    def test_limits_visible_confirmation_items(self):
        visible, hidden = compact_confirmations([
            "whether current chemotherapy is excluded",
            "minimum weight of 44.1 lb",
            "whether measurable disease is present",
            "pathology/cytology confirmation of the diagnosis",
            "whether active wounds is excluded",
        ])
        self.assertEqual(len(visible), 3)
        self.assertEqual(visible[0], "pathology/cytology confirmation of the diagnosis")
        self.assertIn("whether active wounds is excluded", hidden)


if __name__ == "__main__":
    unittest.main()
