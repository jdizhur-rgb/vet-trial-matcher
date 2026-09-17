import unittest
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class StreamlitPageSmokeTests(unittest.TestCase):
    def load_oa(self):
        return AppTest.from_file(ROOT / "pages" / "4_Osteoarthritis_Trial_Finder.py", default_timeout=30).run()

    def test_shared_navigation_loads(self):
        at = AppTest.from_file(ROOT / "app.py", default_timeout=30).run()
        self.assertFalse(at.exception)

    def test_cancer_search_still_runs(self):
        at = AppTest.from_file(ROOT / "pages" / "1_Clinical_Trial_Finder.py", default_timeout=30).run()
        self.assertFalse(at.exception)
        at.selectbox[2].set_value("Mast cell tumor").run()
        next(button for button in at.button if button.label == "Find potential trials").click().run()
        self.assertFalse(at.exception)
        text = " ".join(x.value for x in [*at.success, *at.warning, *at.info])
        self.assertTrue(any(word in text.lower() for word in ("match", "trial", "opportunit")))

    def test_oa_unknown_answers_produce_possible_matches_and_links(self):
        at = self.load_oa()
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertTrue(any("Possible match" in item.value for item in at.markdown))
        self.assertGreater(len(at.get("link_button")), 0)

    def test_oa_potential_match_state(self):
        at = self.load_oa()
        # Core positive WVRC profile.
        for i in (1, 2, 3, 4):
            at.selectbox[i].set_value("Yes")
        at.multiselect[0].set_value(["Hip"])
        at.number_input[0].set_value(8)
        at.number_input[1].set_value(40)
        at.number_input[2].set_value(3)
        at.selectbox[5].set_value("No")
        for i in (6, 7, 8, 9, 10, 11, 12):
            at.selectbox[i].set_value("No")
        at.selectbox[13].set_value("Yes")
        at.multiselect[1].set_value(["None"])
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertTrue(any(item.value == "**Potential match**" for item in at.markdown))

    def test_oa_zero_match_state(self):
        at = self.load_oa()
        at.number_input[0].set_value(0.1)
        at.selectbox[1].set_value("No")
        at.selectbox[2].set_value("No")
        at.multiselect[0].set_value(["Carpus / wrist"])
        at.selectbox[3].set_value("No")
        at.selectbox[4].set_value("No")
        at.selectbox[5].set_value("Yes")
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertTrue(any("No current study" in item.value for item in at.warning))


if __name__ == "__main__":
    unittest.main(verbosity=2)
