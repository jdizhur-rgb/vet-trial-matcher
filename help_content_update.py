#!/usr/bin/env python3
"""Keep live Help content aligned with current region and center-search behavior."""
from pathlib import Path


PAGE = Path(__file__).resolve().parent / "seo" / "site" / "help" / "index.html"


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    marker = '<details><summary>Still not sure what to do?</summary>'
    if marker not in text:
        raise AssertionError("Help FAQ insertion point changed")
    additions = (
        '<details><summary>Which countries are included?</summary><div class="help-answer">'
        '<p>The finder includes current opportunities in the United States and other countries that we can verify from official sources. The United States is selected by default, but you can choose another available country or region in the location section. A study in another country may require travel, and the study team must confirm whether it can accept an animal coming from abroad.</p>'
        '</div></details>\n'
        '<details><summary>How do I find the nearest clinical trial centers?</summary><div class="help-answer">'
        '<p>Open Trial Centers and enter a five-digit US ZIP code. The directory sorts listed US centers by approximate straight-line distance and shows the mileage. It is not a driving-distance estimate. You can also search the directory by hospital, city, state or country; international centers are available through text search and browsing.</p>'
        '<p><a href="https://vettrialfinder.com/centers/">Search clinical trial centers</a></p>'
        '</div></details>\n'
    )
    if 'Which countries are included?' not in text:
        text = text.replace(marker, additions + marker, 1)
    PAGE.write_text(text, encoding="utf-8")
    print("HELP_CONTENT_OK details=", text.count("<details>"))


if __name__ == "__main__":
    main()
