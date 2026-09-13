import json
import unittest
from unittest.mock import patch

from search_telemetry import record_search_outcome, tumor_size_bucket


class SearchTelemetryTests(unittest.TestCase):
    def test_size_is_bucketed(self):
        self.assertEqual(tumor_size_bucket(None), "unknown")
        self.assertEqual(tumor_size_bucket(1.7), "1_to_under_2_cm")
        self.assertEqual(tumor_size_bucket(5), "5_cm_or_more")

    def test_private_and_location_fields_are_not_logged(self):
        with patch("search_telemetry.LOGGER.info") as log:
            record_search_outcome(
                result_count=0,
                fields={"cancer": "Soft tissue sarcoma", "zip_code": "01095", "ip": "1.2.3.4"},
            )
        payload = json.loads(log.call_args.args[1])
        self.assertTrue(payload["zero_results"])
        self.assertEqual(payload["cancer"], "Soft tissue sarcoma")
        self.assertNotIn("zip_code", payload)
        self.assertNotIn("ip", payload)


if __name__ == "__main__":
    unittest.main()
