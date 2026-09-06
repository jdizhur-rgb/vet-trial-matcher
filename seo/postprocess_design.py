#!/usr/bin/env python3
"""Apply presentation-only polish to generated SEO pages."""
from pathlib import Path

SITE = Path(__file__).resolve().parent / "site"
OLD_HOME = '<a href="https://jdizhur-rgb.github.io/vet-trial-matcher/"><strong>Cancer Trial Finder For Dogs And Cats</strong></a>'
NEW_HOME = '<a class="home-link" href="https://jdizhur-rgb.github.io/vet-trial-matcher/" aria-label="Back to Cancer Trial Finder home">← Cancer Trial Finder home</a>'
OLD_HEADER_FREE = '<p><strong>100% FREE.</strong> No registration, email or paywall.</p>'
OLD_FREE_NOTE = '<p class="free-note"><strong>100% FREE — view all matching trials, details, contacts and official enrollment links.</strong><br>Free means free. No hidden trial results. No paid report.</p>'
NEW_FREE_NOTE = '<p class="free-note"><strong>100% FREE — view all matching trials, details, contacts and official enrollment links.</strong><br>No registration. No hidden results. No paid report.</p>'
EXTRA_CSS = '''
h1{font-size:clamp(2rem,5vw,2.65rem);line-height:1.12;margin:28px 0 18px}
header{margin-bottom:22px}
.home-link{display:inline-block;font-weight:700;text-decoration:none;font-size:1rem}
.home-link:hover{text-decoration:underline}
@media(max-width:600px){
 body{padding:22px 20px;line-height:1.5}
 h1{font-size:2rem;line-height:1.14;margin:22px 0 16px}
 header{margin-bottom:18px}
 .free-note{font-size:1rem}
 .cta{width:auto;max-width:100%;box-sizing:border-box}
}
'''

count = 0
for page in SITE.rglob("index.html"):
    text = page.read_text(encoding="utf-8")
    # Keep the catalog home title as branding; make inner-page navigation explicit.
    if page != SITE / "index.html":
        text = text.replace(OLD_HOME, NEW_HOME)
    text = text.replace(OLD_HEADER_FREE, '')
    text = text.replace(OLD_FREE_NOTE, NEW_FREE_NOTE)
    text = text.replace('</style>', EXTRA_CSS + '</style>', 1)
    page.write_text(text, encoding="utf-8")
    count += 1
print(f'POSTPROCESSED_DESIGN pages={count}')
