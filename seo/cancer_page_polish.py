"""Shared owner-guide polish installed before the production build runs."""
from cancer_branch_depth import DOG_BASELINE_BRANCHES, CAT_BASELINE_BRANCHES

POLISH_CSS = r'''
.guide-accordions summary{position:relative;list-style:none;padding-right:42px}
.guide-accordions summary::-webkit-details-marker{display:none}
.guide-accordions summary:after{content:'+';position:absolute;right:15px;top:50%;transform:translateY(-50%);color:#9aabba;font-size:1.25rem;font-weight:400}
.guide-accordions details[open] summary:after{content:'-'}
.guide-accordions details[open] summary{background:#f8fbfd}
.guide-detail p{margin:.45rem 0}
@media(max-width:600px){.guide-accordions summary{padding-right:38px}.guide-accordions summary:after{right:13px}}
'''.strip()


def install():
    import practical_cancer_pages as pages
    import feline_branch_content as feline

    for key, items in DOG_BASELINE_BRANCHES.items():
        current = list(pages.BRANCHES.get(key, []))
        pages.BRANCHES[key] = list(items) + current

    for key, items in CAT_BASELINE_BRANCHES.items():
        current = list(feline.FELINE_BRANCHES.get(key, []))
        feline.FELINE_BRANCHES[key] = list(items) + current

    if POLISH_CSS not in pages.CSS:
        pages.CSS = pages.CSS + POLISH_CSS
