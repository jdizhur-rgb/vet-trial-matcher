"""Regression coverage for credential-bearing map embeds and script payloads."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from check_evidence_keys import check_files, redact_text


class EvidenceKeyTests(unittest.TestCase):
    def test_nested_payload_preserves_clinic_facts_and_json(self):
        key = "AIza" + "x" * 35
        payload = {
            "url": "https://clinic.example/oncology/",
            "text": "Oncology, 2089 SW 16th Avenue, Gainesville",
            "map_embeds": ["https://maps.example/place?key=" + key + "&q=Gainesville"],
            "scripts": ["var apiKey = '" + key + "';"],
            "attempted_at": "2026-10-11T07:14:56-04:00",
        }
        cleaned = redact_text(json.dumps(payload))
        result = json.loads(cleaned)
        self.assertNotIn(key, cleaned)
        for name in ("url", "text", "attempted_at"):
            self.assertEqual(result[name], payload[name])
        self.assertIn("&q=Gainesville", result["map_embeds"][0])
        self.assertEqual(redact_text(cleaned), cleaned)

    def test_scanner_detects_without_printing_and_redacts(self):
        key = "AIza" + "a_-" * 11 + "ab"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text(json.dumps({"script": key, "name": "Clinic"}))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(check_files([path]), 1)
                self.assertEqual(check_files([path], redact=True), 1)
                self.assertEqual(check_files([path]), 0)
            self.assertNotIn(key, output.getvalue())
            self.assertEqual(json.loads(path.read_text())["name"], "Clinic")


if __name__ == "__main__":
    unittest.main()
