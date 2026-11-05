#!/usr/bin/env python3
"""Regressions for the November 1 status/queue/discovery completion failure."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from audit_execution_gate import current_source_sufficient, validate, REGIONS, PASSES, seed_queue


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "evidence.json").write_text('{"text":"Actual saved primary protocol"}')
        (self.root / "deadline.json").write_text(json.dumps({"rows": [{"record_id": "trial"}]}))
        self.start = datetime(2026, 11, 2, 3, tzinfo=timezone.utc)
        self.end = datetime(2026, 11, 2, 4, tzinfo=timezone.utc)
        self.source = {"source_id": "s", "content_sufficient": True, "processing_complete": True,
                       "attempted_urls": [{"method": "shell_curl", "completed_at": self.end.isoformat(),
                                           "evidence_file": "evidence.json"}]}
        self.decision = {"source_id": "s", "reviewed_at": self.end.isoformat(),
                         "current_official_content": True, "roster_complete": True,
                         "protocols": ["trial"], "finding": "Named protocol is open",
                         "catalog_comparison": [{"canonical_id": "trial", "decision": "unchanged"}],
                         "roster_evidence_refs": ["evidence.json"], "evidence_refs": ["evidence.json"],
                         "remaining_available_steps": [], "completion_basis": "Current named roster reconciled"}
        self.baseline = {"run_id": "run", "started_at": self.start.isoformat(),
                         "execution_deadline": "2026-11-02T06:00:00+00:00",
                         "source_ids": ["s"], "catalog_ids": ["trial"], "issues": []}
        self.review = {"run_id": "run", "ended_at": self.end.isoformat(),
                       "source_reviews": [self.decision], "issue_updates": [], "leads": [],
                       "discovered_urls": [], "deadline_review_ref": "deadline.json",
                       "discovery_queries": [{"region": r, "pass": p, "country": "named country",
                           "language": "en", "query": "specific recruitment query", "evidence_refs": ["evidence.json"]}
                           for r in REGIONS for p in PASSES],
                       "stop": {"reason": "completed_available_work", "detail": "No permitted tasks remain"}}
        self.receipt = {"run_id": "run", "sources": [self.source], "content_sufficient_total": 1}

    def check(self):
        return validate(self.baseline, self.review, self.receipt, self.root)

    def test_complete_current_accounting_passes(self):
        self.assertEqual(self.check()[0], [])

    def add_current_source(self):
        data = self.root / "data"
        data.mkdir(exist_ok=True)
        (data / "source_inventory.json").write_text(json.dumps({"sources": [{"id": "s"}, {"id": "new"}]}))
        self.review["added_source_ids"] = ["new"]
        self.receipt["sources"].append({**copy.deepcopy(self.source), "source_id": "new"})
        self.review["source_reviews"].append({**copy.deepcopy(self.decision), "source_id": "new"})
        self.receipt["content_sufficient_total"] = 2

    def test_declared_current_source_addition_preserves_frozen_sources(self):
        self.add_current_source()
        errors, summary, _ = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["source_total"], 2)
        self.assertEqual(summary["baseline_source_total"], 1)
        self.assertEqual(summary["sources_added"], 1)
        self.receipt["sources"] = self.receipt["sources"][1:]
        self.assertTrue(any("every frozen source" in e for e in self.check()[0]))

    def test_undeclared_or_nonexistent_source_addition_is_rejected(self):
        self.add_current_source()
        self.review["added_source_ids"] = []
        self.assertTrue(any("every frozen source" in e for e in self.check()[0]))
        self.review["added_source_ids"] = ["new"]
        (self.root / "data/source_inventory.json").write_text(json.dumps({"sources": [{"id": "s"}]}))
        self.assertTrue(any("actual current inventory" in e for e in self.check()[0]))

    def test_previous_partial_does_not_prevent_promotion(self):
        self.source.update(previous_content_sufficient=False, previous_result="partial")
        self.assertTrue(current_source_sufficient(self.source, self.decision, self.root, self.start, self.end))

    def test_previous_complete_does_not_establish_current_roster(self):
        self.source.update(previous_content_sufficient=True, current_content_comparison=[{"whole_text_equal": True}])
        del self.decision["roster_evidence_refs"]
        self.assertTrue(any("content_sufficient differs" in e for e in self.check()[0]))

    def test_unchanged_page_cannot_mask_unreviewed_changed_page(self):
        self.source["current_content_comparison"] = [
            {"whole_text_equal": True, "current_evidence": "unchanged.json"},
            {"whole_text_equal": False, "current_evidence": "evidence.json"}]
        self.assertTrue(self.check()[0])
        self.decision["change_reviews"] = [{"current_evidence": "evidence.json",
            "finding": "Only page navigation changed", "catalog_impact": "No protocol facts changed"}]
        self.assertEqual(self.check()[0], [])

    def test_old_evidence_timestamp_and_restriction_review_are_not_current_visit(self):
        for change in [{"completed_at": "2026-11-01T03:00:00+00:00"},
                       {"method": "restriction_review_no_request"}]:
            with self.subTest(change=change):
                source = copy.deepcopy(self.source)
                source["attempted_urls"][0].update(change)
                self.assertFalse(current_source_sufficient(source, self.decision, self.root, self.start, self.end))

    def test_copying_queue_without_current_decision_is_rejected(self):
        self.baseline["issues"] = [{"issue_id": "full_protocol:trial", "trial_id": "trial", "kind": "full_protocol"}]
        self.assertTrue(any("inherited issues omitted" in e for e in self.check()[0]))

    def issue(self, state):
        issue = {"issue_id": "full_protocol:trial", "trial_id": "trial", "kind": "full_protocol",
                 "state": state, "reviewed_at": self.end.isoformat(), "finding": "Exact current question retained",
                 "question": "Current intake not stated", "next_action": "Read newly published primary if present",
                 "evidence_refs": ["evidence.json"]}
        self.baseline["issues"] = [{"issue_id": issue["issue_id"], "trial_id": "trial", "kind": "full_protocol"}]
        self.review["issue_updates"] = [issue]
        return issue

    def test_real_blocker_can_finish_available_work_without_clinical_complete(self):
        self.issue("BLOCKED")["restriction_or_unpublished_evidence_refs"] = ["evidence.json"]
        errors, summary, _ = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["clinical_reconciliation"], "INCOMPLETE")

    def test_permitted_work_cannot_be_reported_finished(self):
        self.issue("OPEN_AVAILABLE")
        self.assertTrue(any("permitted tasks remain" in e for e in self.check()[0]))

    def test_fake_early_timeout_rejected_real_deadline_retains_work(self):
        self.issue("OPEN_AVAILABLE")
        self.review["stop"] = {"reason": "time_limit", "detail": "Run boundary reached",
                               "deadline": "2026-11-02T06:00:00+00:00"}
        self.assertTrue(any("time limit not reached" in e for e in self.check()[0]))
        self.review["stop"]["deadline"] = self.end.isoformat()
        self.assertTrue(any("time limit not reached" in e for e in self.check()[0]))
        self.review["stop"]["deadline"] = self.baseline["execution_deadline"]
        self.review["ended_at"] = self.baseline["execution_deadline"]
        errors, summary, _ = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["clinical_reconciliation"], "INCOMPLETE")

    def test_expired_deferral_and_new_signal_cannot_hide_due_work(self):
        item = self.issue("DEFERRED")
        item.update(recheck_after="2026-11-03T06:00:00+00:00", deferral_basis="Individual published gap")
        self.assertEqual(self.check()[0], [])
        item["deadline_crossed"] = True
        self.assertTrue(any("due signal" in e for e in self.check()[0]))

    def test_known_source_is_not_canonical_protocol_identity(self):
        self.review["discovered_urls"] = ["https://example.org/new-protocol"]
        lead = {"url": self.review["discovered_urls"][0], "disposition": "VERIFIED_EXISTING",
                "primary_url": "https://example.org/new-protocol", "reason": "Known institution",
                "related_source_id": "s", "evidence_refs": ["evidence.json"]}
        self.review["leads"] = [lead]
        self.assertTrue(any("exact canonical identity" in e for e in self.check()[0]))
        lead.update(canonical_ids=["trial"], identity_comparison="Same protocol number and cohort")
        self.assertEqual(self.check()[0], [])

    def test_full_protocol_resolution_needs_all_facts(self):
        item = self.issue("RESOLVED")
        self.assertTrue(any("incomplete full protocol" in e for e in self.check()[0]))
        item["facts_checked"] = ["identity", "recruitment_sites", "eligibility", "funding", "contacts"]
        errors, summary, handoff = self.check()
        self.assertEqual(errors, [])
        self.assertEqual(summary["issues_resolved"], 1)
        self.assertEqual(handoff[0]["state"], "RESOLVED")

    def seed_files(self, prior):
        data = self.root / "data"
        data.mkdir()
        (data / "audit_state.json").write_text(json.dumps({"protocol_selection_review": {"progress_receipt": "progress.json"}}))
        (data / "protocol_selection_cases.json").write_text(json.dumps({"reviews": [{"trial_id": "trial"}]}))
        (data / "audit_execution_queue.json").write_text(json.dumps({"issues": prior}))
        (self.root / "progress.json").write_text(json.dumps([{"trial_id": "trial", "status": "current_full_protocol_not_verified"}]))

    def test_resolved_work_is_not_reopened_by_obsolete_pending_list(self):
        self.seed_files([{"issue_id": "full_protocol:trial", "trial_id": "trial", "kind": "full_protocol", "state": "RESOLVED"}])
        trial = {"id": "trial", "url": "https://example.org/trial", "verified": "2026-11-01"}
        queue = seed_queue(self.root, [trial], [trial], self.end)
        self.assertEqual(queue["issues"], [])
        self.assertEqual(len(queue["resolved_history"]), 1)
        trial["verified"] = "2026-09-01"
        self.assertEqual(len(seed_queue(self.root, [trial], [trial], self.end)["issues"]), 1)

    def test_seed_queue_accepts_wrapped_progress_receipt(self):
        self.seed_files([])
        (self.root / "progress.json").write_text(json.dumps({"rows": [
            {"trial_id": "trial", "status": "current_full_protocol_not_verified",
             "remaining_fact": "Current contact is not published"}
        ]}))
        trial = {"id": "trial", "url": "https://example.org/trial", "verified": "2026-11-01"}
        issue = seed_queue(self.root, [trial], [trial], self.end)["issues"][0]
        self.assertEqual(issue["question"], "Current contact is not published")

    def test_unknown_date_and_missing_cases_seed_real_work(self):
        self.seed_files([])
        (self.root / "data/protocol_selection_cases.json").write_text('{"reviews":[]}')
        trial = {"id": "other", "url": "https://example.org/other"}
        kinds = {x["kind"] for x in seed_queue(self.root, [trial], [trial], self.end)["issues"]}
        self.assertEqual(kinds, {"full_protocol", "independent_selection"})

    def policy_fixture(self, rule):
        item = self.issue("POLICY_RESOLVED")
        self.baseline["issues"][0]["state"] = "OWNER_DECISION"
        item.update(previous_verified="2026-10-20", full_protocol_review_complete=False,
                    resolved_scope="current_access" if rule == "avma_closed" else "deadline_interpretation",
                    policy_resolution={"rule": rule, "evidence_refs": ["evidence.json"],
                                       "identity_comparison": "Exact protocol/cohort identifier compared"})
        data = self.root / "data"
        data.mkdir(exist_ok=True)
        (data / "audit_owner_policy.json").write_text(json.dumps({"rules": {rule: {"enabled": True}}}))
        trial = {"id": "trial", "verified": "2026-10-20"}
        return item, trial

    def test_owner_closed_policy_requires_exact_inactive_registry_record(self):
        item, trial = self.policy_fixture("avma_closed")
        item["policy_resolution"].update(registry_status="Completed", avma_vct_code="VCT123")
        trial.update(available_for_matching=False, registry_status="Completed", avma_vct_code="VCT123")
        path = self.root / "data/trials_base.json"
        path.write_text(json.dumps([trial]))
        self.assertEqual(self.check()[0], [])
        self.assertEqual(self.check()[1]["policy_questions_resolved"], 1)
        trial["available_for_matching"] = True
        path.write_text(json.dumps([trial]))
        self.assertTrue(any("unsupported owner-policy" in e for e in self.check()[0]))

    def test_owner_date_policy_needs_persisted_date_and_cannot_refresh_clinical_date(self):
        item, trial = self.policy_fixture("study_end_as_recruitment_end")
        item["policy_resolution"]["published_study_end"] = "2027-03-31"
        trial.update(recruitment_end="2027-03-31", recruitment_end_basis={
            "rule": "study_end_as_recruitment_end", "primary_url": "https://example.org/protocol",
            "published_study_end": "2027-03-31", "evidence_refs": ["evidence.json"]})
        path = self.root / "data/trials_base.json"
        path.write_text(json.dumps([trial]))
        self.assertEqual(self.check()[0], [])
        trial["verified"] = "2026-11-02"
        path.write_text(json.dumps([trial]))
        self.assertTrue(any("unsupported owner-policy" in e for e in self.check()[0]))

    def test_owner_date_policy_cannot_close_a_different_clinical_scope(self):
        item, trial = self.policy_fixture("study_end_as_recruitment_end")
        item["policy_resolution"]["published_study_end"] = "2027-03-31"
        item["resolved_scope"] = "funding"
        trial.update(recruitment_end="2027-03-31", recruitment_end_basis={
            "rule": "study_end_as_recruitment_end", "primary_url": "https://example.org/protocol",
            "published_study_end": "2027-03-31", "evidence_refs": ["evidence.json"]})
        (self.root / "data/trials_base.json").write_text(json.dumps([trial]))
        self.assertTrue(any("unsupported owner-policy" in e for e in self.check()[0]))

    def test_policy_resolution_history_does_not_reopen_until_full_review_is_due(self):
        self.seed_files([{"issue_id": "full_protocol:trial", "trial_id": "trial", "kind": "full_protocol",
                          "state": "POLICY_RESOLVED"}])
        trial = {"id": "trial", "url": "https://example.org/trial", "verified": "2026-11-01"}
        self.assertEqual(seed_queue(self.root, [trial], [trial], self.end)["issues"], [])
        (self.root / "progress.json").write_text(json.dumps([{"trial_id": "trial",
            "status": "current_full_protocol_not_verified", "remaining_fact": "Old owner date question"}]))
        trial["verified"] = "2026-09-01"
        due = seed_queue(self.root, [trial], [trial], self.end)["issues"]
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["due_reason"], "28_day_review")
        self.assertNotEqual(due[0]["question"], "Old owner date question")

    def test_unprocessed_discovery_url_cannot_disappear(self):
        self.review["discovered_urls"] = ["https://example.org/not-reviewed"]
        self.assertTrue(any("all discovered URLs" in e for e in self.check()[0]))


if __name__ == "__main__":
    unittest.main()
