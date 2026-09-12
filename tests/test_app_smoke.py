import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class AppSmokeTests(unittest.TestCase):
    def open_app(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        return AppTest.from_file(str(app_path), default_timeout=30).run()

    def test_safe_initial_state(self):
        app = self.open_app()
        self.assertFalse(app.exception)
        values = {widget.label: widget.value for widget in app.selectbox}
        self.assertIsNone(values["Cancer type"])
        self.assertEqual("I don't know", values["How certain is the diagnosis?"])
        self.assertEqual("USA", values["Country / region"])
        search = next(button for button in app.button if button.label == "Find potential trials")
        self.assertTrue(search.disabled)

    def test_yasha_case_returns_no_plausible_hs_matches(self):
        app = self.open_app()
        next(widget for widget in app.selectbox if widget.label == "Country / region").select("USA")
        next(widget for widget in app.selectbox if widget.label == "Cancer type").select("Histiocytic sarcoma")
        app.run()
        changes = {
            "How certain is the diagnosis?": "Confirmed by pathology/cytology",
            "Current tumor status": "Removed — incomplete/dirty margins",
            "Metastases": "No known metastases",
            "Has your veterinarian said the disease is localized?": "Yes",
            "Surgery": "Yes",
            "Chemotherapy": "Currently receiving",
        }
        for widget in app.selectbox:
            if widget.label in changes:
                widget.select(changes[widget.label])
        next(field for field in app.text_input if field.label == "ZIP code (optional)").input("01095")
        app.run()
        next(button for button in app.button if button.label == "Find potential trials").click()
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any("No plausible matches" in message.value for message in app.info))

    def test_result_renders_funding_without_opening_details(self):
        app = self.open_app()
        next(widget for widget in app.selectbox if widget.label == "Country / region").select("USA")
        next(widget for widget in app.selectbox if widget.label == "Cancer type").select("Mast cell tumor")
        app.run()
        next(widget for widget in app.selectbox if widget.label == "How certain is the diagnosis?").select("Confirmed by pathology/cytology")
        app.run()
        next(button for button in app.button if button.label == "Find potential trials").click()
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Costs / coverage:" in str(markdown.value) for markdown in app.markdown))
        self.assertTrue(any("Where:" in str(markdown.value) for markdown in app.markdown))

    def test_tumor_size_question_is_adaptive(self):
        app = self.open_app()
        self.assertFalse(any(field.label == "Largest tumor measurement (cm)" for field in app.number_input))
        next(widget for widget in app.selectbox if widget.label == "Cancer type").select("Soft tissue sarcoma")
        app.run()
        self.assertTrue(any(box.label == "I know the tumor size" for box in app.checkbox))

    def test_europe_has_a_country_submenu(self):
        app = self.open_app()
        next(widget for widget in app.selectbox if widget.label == "Country / region").select("Europe")
        app.run()
        submenu = next(widget for widget in app.selectbox if widget.label == "European country")
        self.assertEqual("All Europe", submenu.value)
        self.assertIn("France", submenu.options)
        self.assertFalse(any(field.label == "ZIP code (optional)" for field in app.text_input))

    def test_other_countries_have_a_catalog_driven_submenu(self):
        app = self.open_app()
        next(widget for widget in app.selectbox if widget.label == "Country / region").select("Other countries")
        app.run()
        submenu = next(widget for widget in app.selectbox if widget.label == "Country")
        self.assertTrue(submenu.options)
        self.assertNotIn("USA", submenu.options)
        self.assertNotIn("Canada", submenu.options)


if __name__ == "__main__":
    unittest.main()
