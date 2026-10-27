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

    def test_route_coverage_prose_does_not_prove_reconciliation(self):
        review = copy.deepcopy(self.review)
        row = review["rows"][0]
        row["processing_assessment"] = "external_blocker"
        row["completion_decision"] = {
            "remaining_fact": "Current recruitment at the exact site",
            "routes_exhausted_evidence": "The configured URL was fetched",
            "available_reconciliation_done_evidence": "All configured master/fallback routes were attempted today or withheld only by an exact recorded route restriction.",
        }
        self.assertTrue(any("route-attempt coverage" in e for e in validate(review, self.receipt)[0]))

    def test_unconfirmed_processing_cannot_be_complete(self):
        receipt = copy.deepcopy(self.receipt)
        receipt["sources"][0]["processing_complete"] = True
        self.assertTrue(any("cannot be marked complete" in e for e in validate(self.review, receipt)[0]))

    def test_distinct_source_specific_completion_is_accepted(self):
        review = copy.deepcopy(self.review)
        row = review["rows"][0]
        row["processing_assessment"] = "external_blocker"
        row["completion_decision"] = {
            "remaining_fact": "The extra site is unnamed in the published protocol",
            "routes_exhausted_evidence": "The official protocol and its linked site list were read",
            "available_reconciliation_done_evidence": "The only named clinic matches the catalog; the protocol calls the second site TBD, so its identity remains unpublished.",
        }
        self.assertEqual(validate(review, self.receipt)[0], [])

    def test_same_reconciliation_text_cannot_close_different_sources(self):
        review = copy.deepcopy(self.review)
        receipt = copy.deepcopy(self.receipt)
        row = review["rows"][0]
        row["processing_assessment"] = "external_blocker"
        row["completion_decision"] = {
            "remaining_fact": "Unpublished current roster",
            "routes_exhausted_evidence": "Configured routes attempted",
            "available_reconciliation_done_evidence": "All available work done; no further facts available.",
        }
        other = copy.deepcopy(row)
        other["source_id"] = other["evidence"]["source_id"] = "other"
        review["rows"].append(other)
        receipt["sources"].append({**copy.deepcopy(receipt["sources"][0]), "source_id": "other"})
        self.assertTrue(any("repeated blanket" in e for e in validate(review, receipt)[0]))


if __name__ == "__main__":
    unittest.main()
