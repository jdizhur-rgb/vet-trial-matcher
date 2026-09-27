#!/usr/bin/env python3
"""Enable category and region pickers in the research-center directory."""
from pathlib import Path
import re

PAGE = Path(__file__).resolve().parent / "seo" / "site" / "centers" / "index.html"


def main() -> None:
    html = PAGE.read_text(encoding="utf-8")
    if not re.search(r'<section class="center-directory-section" id="usa"', html):
        raise AssertionError("Grouped center directory not found")
    script = '''<script>
const directorySections=Array.from(document.querySelectorAll('.center-directory-section'));
const directoryButtons=Array.from(document.querySelectorAll('[data-directory-target]'));
let activeSection='usa';
function applyPicker(section){const picker=section.querySelector('[data-region-picker]');const value=picker?picker.value:'';section.querySelectorAll('.center-region').forEach(region=>{region.hidden=!value||region.dataset.region!==value;});}
function showSection(id){activeSection=id;directoryButtons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.directoryTarget===id)));directorySections.forEach(section=>{section.hidden=section.id!==id;if(!section.hidden)applyPicker(section);});}
directoryButtons.forEach(button=>button.addEventListener('click',()=>showSection(button.dataset.directoryTarget)));
document.querySelectorAll('[data-region-picker]').forEach(picker=>picker.addEventListener('change',()=>applyPicker(picker.closest('.center-directory-section'))));
showSection(activeSection);
</script>'''
    html = html.replace('</main>', script+'</main>', 1)
    html = html.replace('</style>', '.center-region[hidden],.center-directory-section[hidden]{display:none!important}</style>', 1)
    PAGE.write_text(html, encoding="utf-8")
    sections = html.count('<section class="center-directory-section"')
    print(f"CENTER_DIRECTORY_PICKER_OK sections={sections}")


if __name__ == "__main__":
    main()
