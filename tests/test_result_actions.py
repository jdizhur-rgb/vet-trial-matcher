import unittest

from result_actions import contact_actions, verification_label


class ResultActionTests(unittest.TestCase):
    def test_extracts_email_and_us_phone(self):
        email, phone = contact_actions("Team — trials@example.edu · (509) 592-3668")
        self.assertEqual(email, "trials@example.edu")
        self.assertEqual(phone, "5095923668")

    def test_does_not_treat_date_as_phone(self):
        self.assertEqual(contact_actions("Verified 2026-09-10"), (None, None))

    def test_formats_verification_date(self):
        self.assertEqual(verification_label("2026-09-10"), "Last checked: Sep 10, 2026")


if __name__ == "__main__":
    unittest.main()
