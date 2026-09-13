import unittest

from scripts.weekly_content_audit import status_signals


class WeeklyContentAuditTests(unittest.TestCase):
    def test_finds_clear_closure_language(self):
        self.assertEqual(status_signals("Recruitment is completed."), (False, True))

    def test_finds_open_language(self):
        self.assertEqual(status_signals("This study is actively recruiting dogs."), (True, False))

    def test_reports_ambiguous_page(self):
        self.assertEqual(
            status_signals("Study A is actively recruiting. Study B: enrollment closed."),
            (True, True),
        )


if __name__ == "__main__":
    unittest.main()
