#!/usr/bin/env python3
"""Regression gates for blanket external-blocker claims and missing diagnoses."""
import copy
import unittest
from validate_audit_gap_review import validate


class GapReviewTests(unittest.TestCase):
    def setUp(self):
        self.receipt = {"run_id": "run", "sources": [{"source_id": "s", "content_sufficient": False,
            "attempted_urls": [{"url": "https://example.org/trials"}]}]}
        self.review = {"original_run_id": "run", "rows": [{"source_id": "s", "category": "protocol_uncertainty",
            "processing_assessment": "not_established", "question": "Recruitment conflict", "reason": "Missing completion proof",
            "next_action": "Review controlling primary", "evidence": {"source_id": "s", "attempted_urls": ["https://example.org/trials"]}}]}

    def test_uncertain_processing_keeps_coverage_incomplete(self):
        errors, summary = validate(self.review, self.receipt)
        self.assertEqual(errors, [])
        self.assertEqual(summary["processing_completion"], "NOT_VERIFIED")
        self.assertEqual(summary["strict_coverage_status"], "INCOMPLETE")

    def test_blanket_external_label_is_rejected(self):
        review = copy.deepcopy(self.review)
        review["rows"][0]["processing_assessment"] = "external_blocker"
        self.assertTrue(validate(review, self.receipt)[0])

    def test_omitted_gap_and_invented_attempt_are_rejected(self):
        review = copy.deepcopy(self.review)
        review["rows"] = []
        self.assertTrue(validate(review, self.receipt)[0])
        review = copy.deepcopy(self.review)
        review["rows"][0]["evidence"]["attempted_urls"] = ["https://example.org/not-visited"]
        self.assertTrue(validate(review, self.receipt)[0])


if __name__ == "__main__":
    unittest.main()
