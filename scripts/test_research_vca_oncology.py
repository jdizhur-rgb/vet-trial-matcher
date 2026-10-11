"""Regression checks for actual VCA suite-address layouts."""
import unittest
from scripts.research_vca_oncology import address_parts


class VcaAddressTests(unittest.TestCase):
    def test_current_single_space_suite_addresses(self):
        self.assertEqual(address_parts('6650 Hawaii Kai Drive Suite 105 Honolulu HI 96825'),
                         ('6650 Hawaii Kai Drive Suite 105', 'Honolulu', 'HI', '96825'))
        self.assertEqual(address_parts('1612 N. High Point Road Suite 100 Middleton WI 53562'),
                         ('1612 N. High Point Road Suite 100', 'Middleton', 'WI', '53562'))

    def test_separated_locality_with_trailing_suite(self):
        self.assertEqual(address_parts('1612 N. High Point Road  Middleton WI 53562  Suite 100'),
                         ('1612 N. High Point Road Suite 100', 'Middleton', 'WI', '53562'))

    def test_existing_layout_and_unknown_input(self):
        self.assertEqual(address_parts('12531 Old Seward Highway  Anchorage AK 99515'),
                         ('12531 Old Seward Highway', 'Anchorage', 'AK', '99515'))
        self.assertEqual(address_parts('unresolved address'), ('', '', '', ''))


if __name__ == '__main__':
    unittest.main()
