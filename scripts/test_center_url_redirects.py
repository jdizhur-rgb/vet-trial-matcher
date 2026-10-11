#!/usr/bin/env python3
"""Check published historical center routes in the final deployment artifact."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "seo" / "site"
DOMAIN = "https://vettrialfinder.com"

# Former indexed routes from the October 11 Search Console export, matched to
# current same-institution pages. Retired/unresolved centers are not substitutes.
EXPECTED = {
    "tufts-university-cummings-school-of-veterinary-medicine": "tufts-university-cummings",
    "michigan-state-university-college-of-veterinary-medicine": "michigan-state-university",
    "nc-state-college-of-veterinary-medicine": "nc-state",
    "bridge-animal-referral-center-barc": "bridge-animal-referral-center",
    "auburn-university-college-of-veterinary-medicine": "auburn-university",
    "university-of-florida-college-of-veterinary-medicine": "university-of-florida",
    "university-of-georgia-college-of-veterinary-medicine": "university-of-georgia",
    "university-of-illinois-college-of-veterinary-medicine": "university-of-illinois",
    "ohio-state-university-college-of-veterinary-medicine": "ohio-state-university",
    "purdue-university-college-of-veterinary-medicine": "purdue-university",
    "cornell-university-college-of-veterinary-medicine": "cornell-university",
    "university-of-minnesota-college-of-veterinary-medicine": "university-of-minnesota",
    "university-of-missouri-college-of-veterinary-medicine": "university-of-missouri",
    "virginia-maryland-college-of-veterinary-medicine-virginia-tech": "virginia-maryland-virginia-tech",
}

RESTORED = {
    "schwarzman-animal-medical-center": 0,
    "louisiana-state-university-school-of-veterinary-medicine": 0,
    "medvet-clinical-studies-center": 1,
    "anivive-lifesciences-multicenter": 1,
    "european-multicenter-study-floryne-buishand": 1,
}


def main():
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    search = (SITE / "search" / "index.html").read_text(encoding="utf-8")
    index = json.loads(re.search(r'<script type="application/json" id="site-search-index">(.*?)</script>', search, re.S)[1])
    indexed = {row["url"] for row in index}
    redirects = 0
    for page in (SITE / "centers").glob("*/index.html"):
        text = page.read_text(encoding="utf-8")
        refresh = re.search(r'<meta http-equiv="refresh" content="0; url=([^"]+)">', text)
        if not refresh:
            continue
        redirects += 1
        target = refresh[1]
        assert target.startswith(DOMAIN + "/centers/"), (page, target)
        destination = SITE / target.removeprefix(DOMAIN).strip("/") / "index.html"
        assert destination.is_file(), (page, destination)
        final = destination.read_text(encoding="utf-8")
        assert 'http-equiv="refresh"' not in final, (page, "redirect chain")
        assert f'<link rel="canonical" href="{target}">' in text, page
        assert f'<link rel="canonical" href="{target}">' in final, destination
        assert 'noindex' in text, page
        old = f"{DOMAIN}/centers/{page.parent.name}/"
        assert f"<loc>{old}</loc>" not in sitemap, page
        assert old not in indexed, page
    for former, current in EXPECTED.items():
        text = (SITE / "centers" / former / "index.html").read_text(encoding="utf-8")
        assert f'content="0; url={DOMAIN}/centers/{current}/"' in text, former
    for slug, count in RESTORED.items():
        text = (SITE / "centers" / slug / "index.html").read_text(encoding="utf-8")
        url = f"{DOMAIN}/centers/{slug}/"
        assert f'<link rel="canonical" href="{url}">' in text, slug
        assert 'http-equiv="refresh"' not in text, slug
        assert text.count('<article class="card">') == count, slug
        assert url in indexed, slug
        if count:
            assert 'name="robots" content="noindex' not in text, slug
            assert f'<loc>{url}</loc>' in sitemap, slug
        else:
            assert 'No currently verified treatment opportunity is listed here.' in text, slug
            assert 'name="robots" content="noindex' in text, slug
            assert f'<loc>{url}</loc>' not in sitemap, slug
    medvet = (SITE / "centers/medvet-clinical-studies-center/index.html").read_text(encoding="utf-8")
    card = re.search(r'<article class="card">(.*?)</article>', medvet, re.S)[1]
    for hospital in ('Salt Lake City', 'Cincinnati', 'Cleveland', 'Pittsburgh'):
        assert f'MedVet {hospital}' in card, hospital
    for other_site in ('Chicago', 'Bridge Animal Referral Center', 'Hope Veterinary Oncology', 'VCCS', '$695'):
        assert other_site not in card, other_site
    anivive = (SITE / "centers/anivive-lifesciences-multicenter/index.html").read_text(encoding="utf-8")
    assert 'Cornell University Hospital for Animals' in anivive
    assert 'current patient admission remains subject to Cornell prescreen' in anivive
    print(f"CENTER_URL_REGRESSION_OK historical_routes={len(EXPECTED)} redirects={redirects}")
    print(f"RESTORED_CENTER_PROFILES_REGRESSION_OK profiles={len(RESTORED)}")


if __name__ == "__main__":
    main()
