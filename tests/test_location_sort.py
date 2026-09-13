import unittest

from location_sort import lookup_us_zip, sort_matches_by_distance
from matcher_engine import Match


class LocationSortTests(unittest.TestCase):
    def test_known_zip_is_resolved_locally(self):
        location = lookup_us_zip("01095")
        self.assertIsNotNone(location)
        self.assertEqual("MA", location[3])

    def test_nearest_trial_is_sorted_first(self):
        florida = Match("May qualify — study team must confirm", {
            "id": "fl", "sites": [{"city": "Gainesville", "state": "FL"}],
        }, (), ())
        massachusetts = Match("May qualify — study team must confirm", {
            "id": "ma", "sites": [{"city": "Boston", "state": "MA"}],
        }, (), ())
        ranked, context = sort_matches_by_distance([florida, massachusetts], "01095")
        self.assertEqual("ma", ranked[0].trial["id"])
        self.assertEqual("MA", context["state"])

    def test_invalid_zip_preserves_original_order(self):
        one = Match("x", {"id": "one"}, (), ())
        two = Match("x", {"id": "two"}, (), ())
        ranked, context = sort_matches_by_distance([one, two], "nope")
        self.assertEqual([one, two], ranked)
        self.assertIsNone(context)


if __name__ == "__main__":
    unittest.main()

