#!/usr/bin/env python3
"""Apply the production indexing policy after the static site is generated.

The public pages remain available to owners.  This pass only controls which
pages we ask search engines to index and keeps all SEO signals on the custom
domain.
"""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse


SITE = "https://vettrialfinder.com"
CONTACT_EMAIL = "info@vettrialfinder.com"
LANGUAGE_PREFIXES = {"de", "fr", "es", "it", "nl"}
HOME_TITLE = "Vet Cancer Care Finder | Veterinary Cancer Trials and Oncology Centers"
HOME_DESCRIPTION = (
    "Find veterinary cancer clinical trials and oncology centers for dogs and cats. "
    "Free search with no registration, email or paywall."
)


def add_robots_noindex(text: str) -> str:
    if re.search(r'<meta\s+name=["\']robots["\']', text, re.I):
        return re.sub(
            r'<meta\s+name=["\']robots["\'][^>]*>',
            '<meta name="robots" content="noindex, follow">',
            text,
            count=1,
            flags=re.I,
        )
    return text.replace("</head>", '<meta name="robots" content="noindex, follow"></head>', 1)


def remove_unready_hreflang(text: str) -> str:
    return re.sub(
        r'<link\s+rel="alternate"\s+hreflang="(?:de|fr|es|it|nl)"[^>]*>',
        "",
        text,
        flags=re.I,
    )


def reinforce_homepage_metadata(text: str) -> str:
    """Keep every homepage title signal explicit and mutually consistent."""
    text = re.sub(
        r'<title>.*?</title>',
        f'<title>{HOME_TITLE}</title>',
        text,
        count=1,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{HOME_DESCRIPTION}">',
        text,
        count=1,
        flags=re.I,
    )
    social = (
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="Vet Cancer Care Finder">'
        f'<meta property="og:title" content="{HOME_TITLE}">'
        f'<meta property="og:description" content="{HOME_DESCRIPTION}">'
        f'<meta property="og:url" content="{SITE}/">'
        f'<meta property="og:image" content="{SITE}/assets/vet-trial-finder-logo.png">'
        f'<meta property="og:image:secure_url" content="{SITE}/assets/vet-trial-finder-logo.png">'
        '<meta property="og:image:type" content="image/png">'
        '<meta property="og:image:width" content="1208">'
        '<meta property="og:image:height" content="920">'
        '<meta property="og:image:alt" content="Vet Cancer Care Finder dog logo">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="twitter:title" content="{HOME_TITLE}">'
        f'<meta name="twitter:description" content="{HOME_DESCRIPTION}">'
        f'<meta name="twitter:image" content="{SITE}/assets/vet-trial-finder-logo.png">'
    )
    # Rebuilding must be idempotent even if generated input later gains social tags.
    text = re.sub(r'<meta property="og:(?:type|site_name|title|description|url|image(?::(?:secure_url|type|width|height|alt))?)"[^>]*>', '', text, flags=re.I)
    text = re.sub(r'<meta name="twitter:(?:card|title|description|image)"[^>]*>', '', text, flags=re.I)
    return text.replace('</head>', social + '</head>', 1)


def open_matcher_links_in_new_tab(text: str) -> str:
    """Keep the static site open when a visitor launches the matcher app."""
    pattern = r'<a(?![^>]*\btarget=)([^>]*\bhref="https://(?:c-trials|vet-cancer-trial-finder)\.streamlit\.app/[^"]*"[^>]*)>'
    return re.sub(pattern, r'<a\1 target="_blank" rel="noopener">', text, flags=re.I)


def opportunity_count(text: str) -> int | None:
    match = re.search(r'class="opportunity-count"[^>]*>\s*(\d+)\s+current', text, re.I)
    if not match:
        match = re.search(r'>\s*(\d+)\s+current treatment opportunities', text, re.I)
    return int(match.group(1)) if match else None


def canonical_url(text: str) -> str | None:
    match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', text, re.I)
    return html.unescape(match.group(1)) if match else None


def page_title(text: str) -> str:
    match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    if not match:
        match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    value = re.sub(r'<[^>]+>', '', match.group(1) if match else "Vet Cancer Care Finder")
    return html.unescape(value).strip()


def polish_metadata(text: str) -> str:
    """Apply final metadata after the visual/structured-page enhancement pass."""
    text = re.sub(
        r'Find ([2-9]\d*|1\d+) current ([^"<>]+?) clinical trial and treatment options',
        r'Find \1 current \2 clinical trials and treatment options',
        text,
    )
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    kind = re.search(r'<p class="center-type">(.*?)</p>', text, re.I | re.S)
    if not h1 or not kind:
        return text
    center = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip()
    entity_type = html.unescape(re.sub(r'<[^>]+>', '', kind.group(1))).strip()
    if entity_type == "Multicenter Study":
        title = f"{center} | Veterinary Cancer Study | Vet Cancer Care Finder"
        description = f"Current veterinary cancer treatment study information, participating locations, eligibility details and official links for {center}."
    elif entity_type == "Research Organization":
        title = f"{center} | Veterinary Cancer Research | Vet Cancer Care Finder"
        description = f"Current veterinary cancer research and treatment opportunities from {center}, with eligibility details, contacts and official links."
    else:
        title = f"{center} | Veterinary Oncology & Clinical Trials | Vet Cancer Care Finder"
        description = f"Veterinary oncology services, cancer clinical trials and current treatment opportunities at {center}."
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.I | re.S)
    text = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{html.escape(description, quote=True)}">',
        text,
        count=1,
        flags=re.I,
    )
    return text


def breadcrumbs(path: str, title: str) -> list[dict[str, str]]:
    parts = [part for part in path.strip('/').split('/') if part]
    crumbs = [{"name": "Vet Cancer Care Finder", "item": f"{SITE}/"}]
    if not parts:
        return crumbs
    if len(parts) >= 3 and parts[0] in {"north-america", "uk-europe"} and parts[1] in {"dogs", "cats"}:
        crumbs.append({"name": "Cancer Types", "item": f"{SITE}/cancer-types/"})
    elif parts[0] == "centers" and len(parts) > 1:
        crumbs.append({"name": "Trial Centers", "item": f"{SITE}/centers/"})
    crumbs.append({"name": title, "item": f"{SITE}/{path.strip('/')}/"})
    return crumbs


def add_structured_data(text: str, path: str) -> str:
    # Keep richer page-owned breadcrumb graphs, but do not let an existing
    # WebSite/Organization graph prevent other pages from receiving breadcrumbs.
    if '"BreadcrumbList"' in text:
        return text
    if not path:
        if f'{SITE}/#website' in text:
            return text
        if 'property="og:site_name"' not in text:
            text = text.replace(
                "</head>",
                '<meta property="og:site_name" content="Vet Cancer Care Finder"></head>',
                1,
            )
        data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": f"{SITE}/#website",
                    "url": f"{SITE}/",
                    "name": "Vet Cancer Care Finder",
                    "alternateName": ["VetCancerCareFinder", "vettrialfinder.com"],
                    "description": "Free search for veterinary cancer clinical trials, oncology centers and other treatment options for dogs and cats.",
                },
                {
                    "@type": "Organization",
                    "@id": f"{SITE}/#organization",
                    "name": "Vet Cancer Care Finder",
                    "url": f"{SITE}/",
                    "founder": {"@type": "Person", "name": "Yuliia Dizhur"},
                },
            ],
        }
    else:
        items = [
            {"@type": "ListItem", "position": i, "name": crumb["name"], "item": crumb["item"]}
            for i, crumb in enumerate(breadcrumbs(path, page_title(text)), 1)
        ]
        breadcrumb = {"@type": "BreadcrumbList", "itemListElement": items}
        if f'{SITE}/#website' in text:
            data = {"@context": "https://schema.org", **breadcrumb}
        else:
            data = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "WebSite",
                        "@id": f"{SITE}/#website",
                        "url": f"{SITE}/",
                        "name": "Vet Cancer Care Finder",
                        "alternateName": ["VetCancerCareFinder", "vettrialfinder.com"],
                        "publisher": {"@id": f"{SITE}/#organization"},
                    },
                    {
                        "@type": "Organization",
                        "@id": f"{SITE}/#organization",
                        "name": "Vet Cancer Care Finder",
                        "url": f"{SITE}/",
                    },
                    breadcrumb,
                ],
            }
    script = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    return text.replace("</head>", script + "</head>", 1)


def should_noindex(relative: Path, text: str) -> bool:
    if re.search(r'<meta\s+name=["\']robots["\'][^>]*noindex', text, re.I):
        return True
    parts = relative.parts
    if parts and parts[0] == "uk-europe":
        return True
    if parts and parts[0] in LANGUAGE_PREFIXES:
        return True
    if len(parts) >= 4 and parts[0] in {"north-america", "uk-europe"} and parts[1] in {"dogs", "cats"}:
        count = opportunity_count(text)
        # The owner-guide renderer intentionally removes the old numeric summary,
        # so the absence of study cards is the durable zero-opportunity signal.
        return count == 0 or '<article class="card">' not in text
    if len(parts) >= 3 and parts[0] == "centers":
        count = opportunity_count(text)
        return count == 0
    return False


def write_sitemap(root: Path, indexable: list[str]) -> None:
    # lastmod is optional. The disposable build has no per-page change history;
    # neither a fixed date nor the build time represents a content update.
    entries = "".join(
        f"  <url><loc>{html.escape(url)}</loc></url>\n"
        for url in sorted(indexable, key=lambda value: (value != f"{SITE}/", value))
    )
    (root / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + entries
        + '</urlset>\n',
        encoding="utf-8",
    )


def write_404(root: Path) -> None:
    (root / "404.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex, follow"><title>Page Not Found | Vet Cancer Care Finder</title>'
        '<style>body{margin:0;background:#f6f8fb;color:#17324d;font:16px/1.55 system-ui,sans-serif}'
        'main{max-width:680px;margin:12vh auto;padding:24px}a{color:#175b8c}</style></head><body><main>'
        '<h1>We could not find that page</h1><p>The page may have moved or the listing may have changed.</p>'
        f'<p><a href="{SITE}/">Go to Vet Cancer Care Finder</a> · '
        f'<a href="{SITE}/cancer-types/">Browse cancer types</a></p></main></body></html>',
        encoding="utf-8",
    )


def write_verification_page(root: Path) -> None:
    """Build the editorial-policy page from the current site shell."""
    source = root / "help" / "index.html"
    if not source.exists():
        raise AssertionError("Help page is required as the production shell source")
    text = source.read_text(encoding="utf-8")
    title = "How we verify listings and sources | Vet Cancer Care Finder"
    description = (
        "How Vet Cancer Care Finder checks sources for cancer trials, veterinary oncology care, "
        "other treatments and tests, and what those checks can and cannot establish."
    )
    text = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', text, count=1, flags=re.S)
    text = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">',
        text,
        count=1,
    )
    text = re.sub(
        r'<link rel="canonical" href="[^"]+">',
        f'<link rel="canonical" href="{SITE}/how-we-verify/">',
        text,
        count=1,
    )
    # The page receives its own breadcrumb graph during the normal page pass.
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', '', text, flags=re.S)
    body = f'''<main><style>
.verification-page{{max-width:820px}}.verification-page .lead{{max-width:760px}}
.verification-page section{{background:#fff;border:1px solid #d9e2ea;border-radius:13px;padding:17px 19px;margin:14px 0}}
.verification-page section h2{{font-size:1.16rem;margin:0 0 7px}}.verification-page section p{{margin:.45rem 0}}
.verification-page ul{{margin:.55rem 0;padding-left:21px}}.verification-page li{{margin:.35rem 0}}
@media(max-width:600px){{.verification-page section{{padding:15px 16px}}}}
</style><div class="verification-page">
<h1>How We Verify Listings</h1>
<p class="lead">Vet Cancer Care Finder is an independent, free resource for owners of dogs and cats with cancer. We bring together treatment studies, veterinary oncology care, other treatment options and selected tests. These are different kinds of information, so we do not treat a recruiting study, a clinic service and a laboratory test as interchangeable options.</p>
<section><h2>Where the information comes from</h2><p>We use official university and hospital pages, research teams, study registries, treatment providers, manufacturers and published research. Professional directories help us find practices and clinicians. Listings link to their sources so owners can read the information and contact the relevant team directly.</p><p>A news story, conference presentation or social post can lead us to something worth investigating. It does not by itself establish that a study is recruiting, a treatment is available or a clinic provides a particular service.</p></section>
<section><h2>Clinical trials and treatment access</h2><p>For treatment studies, we check the published recruitment information, species and cancer types, eligibility requirements, participating locations, contacts and stated financial support. We compare records across sources to avoid counting the same multicenter study several times. Separate study cohorts and locations can have different requirements or enrollment status.</p><p>The trial finder focuses on opportunities that may provide an actual anticancer treatment. Observational studies, surveys, sample collection, biobanks and diagnostic-only research are not presented as treatment matches. An expanded-access program or another treatment-access route is identified separately from a conventional clinical trial.</p><p>Matching uses the information an owner enters and the publicly available eligibility rules. Explicit exclusions take priority, and missing information remains a question for the study team. A result is a reason to inquire, not confirmation that the animal is eligible or that the treatment is appropriate.</p></section>
<section><h2>Clinics, local services and online consultations</h2><p>For care listings, we check published practice locations, contact details, cancer services and clinician information. A service described by a hospital network is not automatically available at every branch. Where the treating location or clinician is unclear, we keep that limitation visible rather than assign the service to an unconfirmed hospital.</p><p>Local cancer care can include chemotherapy or tumor surgery provided by a general veterinarian. A service listing does not by itself mean that a board-certified oncologist works there. For remote consultations, we distinguish owner appointments from veterinarian-to-veterinarian advice and describe the published format and geographic limits when available.</p><p>Service and clinician information is compiled from practice websites and professional public directories. Vet Cancer Care Finder does not independently verify clinicians, licenses, credentials or quality of care. Inclusion is not a recommendation. Confirm the clinician, service, current intake and appointment arrangements directly with the practice.</p></section>
<section><h2>Other treatments and tests</h2><p>A treatment can be commercially available, used through a special-access route or offered only within a study. We describe the available route and the evidence behind it separately. Availability does not establish effectiveness, and a published result does not necessarily mean that owners can obtain the treatment now.</p><p>When discussing research, we distinguish laboratory findings from studies in dogs or cats and explain the relevant limits, such as small numbers or the absence of a comparison group. A result for one cancer or species cannot simply be applied to another.</p><p>Tests are listed separately from administered treatments. We describe what a test is intended to measure, the animals or cancers it is offered for, its sample requirements and published limitations. Finding a possible drug target does not prove that the suggested drug will help that animal. A manufacturer's claim is identified as such; access to a test is not proof that using it improves treatment outcomes.</p></section>
<section><h2>Dates, availability and costs</h2><p>A verification or review date records a check of the information described in that listing. It is not a guarantee that every detail is still unchanged, that a study has space today or that a clinic is accepting new patients. Some details may remain unpublished or require direct confirmation. We retain those uncertainties rather than fill them with assumptions.</p><p>We describe funding and prices only to the extent supported by the source. Free study medication, covered study visits, reimbursement and fully funded treatment are different arrangements. Travel, an initial examination, standard care, complications or care after leaving a study may still be owner-paid. Confirm the full costs with the provider before enrolling or booking.</p><p>Studies can pause, fill or close, and practices can change staff, services or locations. When sources conflict, we look for current information from the team responsible and keep unresolved questions explicit. A missing listing does not establish that no treatment or local care is available.</p></section>
<section><h2>What this site does not do</h2><p>Vet Cancer Care Finder does not diagnose cancer, prescribe treatment, decide final study eligibility or replace a veterinary oncologist. We do not rank experimental treatment as better than standard care or promise a cure. A listing is information to discuss with the professionals treating the animal.</p><p>Owners can use the site without paying for a search or report. Research teams and veterinary hospitals do not pay to be listed.</p></section>
<section><h2>Corrections and missing information</h2><p>If a listing has an outdated contact, changed service, closed study or another error, email <a href="mailto:info@vettrialfinder.com">info@vettrialfinder.com</a> with the page link and the source of the correction, if available. You can also suggest a study, practice or other resource we may have missed. Please do not send medical records or urgent requests. Questions about an animal's eligibility or care belong with the study team or treating veterinarian.</p></section>
<p><a class="cta" href="{SITE}/help/">Help using the site</a></p>
</div></main>'''
    text = re.sub(r'<main>.*?</main>', body, text, count=1, flags=re.S)
    directory = root / "how-we-verify"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.html").write_text(text, encoding="utf-8")


def add_verification_footer_link(text: str) -> str:
    footer_match = re.search(r'<footer\b[^>]*>.*?</footer>', text, re.S)
    if not footer_match:
        return text
    footer = footer_match.group(0)
    if re.search(r'href="[^"]*/how-we-verify/">How we verify</a>', footer, re.I):
        return text
    marker = f'<a href="{SITE}/help/">Help</a>'
    footer = footer.replace(
        marker,
        marker + f'<a href="{SITE}/how-we-verify/">How We Verify</a>',
        1,
    )
    return text[:footer_match.start()] + footer + text[footer_match.end():]


def add_contact_footer_link(text: str) -> str:
    """Expose the project email in the shared footer without duplicating it."""
    link = f'<a href="mailto:{CONTACT_EMAIL}">Contact</a>'
    footer_match = re.search(r'<footer\b[^>]*>.*?</footer>', text, re.S)
    if not footer_match:
        return text
    footer_html = footer_match.group(0)
    if link in footer_html or f'href="{SITE}/contact/"' in footer_html:
        return text
    footer = footer_html.replace('</footer>', f'<p>{link}</p></footer>', 1)
    return text[:footer_match.start()] + footer + text[footer_match.end():]


def add_contact_section(text: str) -> str:
    """Add a small, useful contact block to About and Help."""
    if 'class="site-contact"' in text:
        return text
    css = (
        '.site-contact{margin-top:26px;padding:15px 17px;background:#fff;'
        'border:1px solid #d9e2ea;border-radius:12px}'
        '.site-contact h2{font-size:1.08rem;margin:0 0 5px}'
        '.site-contact p{margin:0}'
    )
    text = text.replace('</style>', css + '</style>', 1)
    section = (
        '<section class="site-contact"><h2>Contact</h2>'
        f'<p>Questions, corrections or a study we should add? '
        f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p></section>'
    )
    return text.replace('</main>', section + '</main>', 1)


def main() -> None:
    root = Path(__file__).resolve().parent / "seo" / "site"
    if not root.exists():
        raise SystemExit(f"generated site not found: {root}")

    # These retired cancer-page families must not reach the deployment artifact.
    # International center and research-program pages remain intentionally intact.
    shutil.rmtree(root / "uk-europe", ignore_errors=True)
    for language in LANGUAGE_PREFIXES:
        shutil.rmtree(root / language, ignore_errors=True)

    write_verification_page(root)

    indexable: list[str] = []
    noindexed = 0
    for page in sorted(root.rglob("index.html")):
        relative = page.relative_to(root)
        path = "" if relative == Path("index.html") else relative.parent.as_posix()
        text = page.read_text(encoding="utf-8")
        if not path:
            text = reinforce_homepage_metadata(text)
        text = polish_metadata(text)
        text = remove_unready_hreflang(text)
        text = open_matcher_links_in_new_tab(text)
        text = text.replace('>Oncology Centers</a>', '>Trial Centers</a>')
        canonical = canonical_url(text)
        if not canonical or urlparse(canonical).netloc != "vettrialfinder.com":
            raise AssertionError(f"invalid production canonical in {relative}: {canonical}")
        if should_noindex(relative, text):
            text = add_robots_noindex(text)
            noindexed += 1
        else:
            indexable.append(canonical)
        text = add_structured_data(text, path)
        text = add_verification_footer_link(text)
        text = add_contact_footer_link(text)
        if path in {"about", "help"}:
            text = add_contact_section(text)
        page.write_text(text, encoding="utf-8")

    write_sitemap(root, indexable)
    (root / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    write_404(root)

    sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
    assert "jdizhur-rgb.github.io" not in sitemap
    assert f"{SITE}/uk-europe/" not in sitemap
    assert not any(f"{SITE}/{lang}/" in sitemap for lang in LANGUAGE_PREFIXES)
    assert not (root / "uk-europe").exists()
    assert not any((root / lang).exists() for lang in LANGUAGE_PREFIXES)
    assert len(indexable) == len(set(indexable))
    home = (root / "index.html").read_text(encoding="utf-8")
    assert f'<title>{HOME_TITLE}</title>' in home
    assert f'<link rel="canonical" href="{SITE}/">' in home
    assert f'<meta property="og:title" content="{HOME_TITLE}">' in home
    assert f'<meta property="og:url" content="{SITE}/">' in home
    assert 'Lymphoma Clinical Trials for Cats' not in home
    print(f"SEO_INDEX_POLICY_OK indexable={len(indexable)} noindex={noindexed}")


if __name__ == "__main__":
    main()
