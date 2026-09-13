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
from pathlib import Path
from urllib.parse import urlparse


SITE = "https://vettrialfinder.com"
CONTACT_EMAIL = "info@vettrialfinder.com"
LANGUAGE_PREFIXES = {"de", "fr", "es", "it", "nl"}
LASTMOD = "2026-09-12"


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
    value = re.sub(r'<[^>]+>', '', match.group(1) if match else "Vet Trial Finder")
    return html.unescape(value).strip()


def breadcrumbs(path: str, title: str) -> list[dict[str, str]]:
    parts = [part for part in path.strip('/').split('/') if part]
    crumbs = [{"name": "Vet Trial Finder", "item": f"{SITE}/"}]
    if not parts:
        return crumbs
    if len(parts) >= 3 and parts[0] in {"north-america", "uk-europe"} and parts[1] in {"dogs", "cats"}:
        crumbs.append({"name": "Cancer Types", "item": f"{SITE}/cancer-types/"})
    elif parts[0] == "centers" and len(parts) > 1:
        crumbs.append({"name": "Trial Centers", "item": f"{SITE}/centers/"})
    crumbs.append({"name": title, "item": f"{SITE}/{path.strip('/')}/"})
    return crumbs


def add_structured_data(text: str, path: str) -> str:
    # The cancer-page renderer already emits a richer WebPage/Breadcrumb graph.
    # Never stack a second graph on pages which own their structured data.
    if 'type="application/ld+json"' in text:
        return text
    if not path:
        data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": f"{SITE}/#website",
                    "url": f"{SITE}/",
                    "name": "Vet Trial Finder",
                    "description": "Free finder for cancer clinical trials and treatment options for dogs and cats.",
                },
                {
                    "@type": "Organization",
                    "@id": f"{SITE}/#organization",
                    "name": "Vet Trial Finder",
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
        data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
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
    entries = "".join(
        f"  <url><loc>{html.escape(url)}</loc><lastmod>{LASTMOD}</lastmod></url>\n"
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
        '<meta name="robots" content="noindex, follow"><title>Page Not Found | Vet Trial Finder</title>'
        '<style>body{margin:0;background:#f6f8fb;color:#17324d;font:16px/1.55 system-ui,sans-serif}'
        'main{max-width:680px;margin:12vh auto;padding:24px}a{color:#175b8c}</style></head><body><main>'
        '<h1>We could not find that page</h1><p>The page may have moved or the listing may have changed.</p>'
        f'<p><a href="{SITE}/">Go to Vet Trial Finder</a> · '
        f'<a href="{SITE}/cancer-types/">Browse cancer types</a></p></main></body></html>',
        encoding="utf-8",
    )


def write_verification_page(root: Path) -> None:
    """Build the editorial-policy page from the current site shell."""
    source = root / "help" / "index.html"
    if not source.exists():
        raise AssertionError("Help page is required as the production shell source")
    text = source.read_text(encoding="utf-8")
    title = "How We Verify Clinical Trial Listings | Vet Trial Finder"
    description = (
        "How Vet Trial Finder finds, verifies and updates veterinary cancer clinical trials, "
        "eligibility details, funding information and treatment listings."
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
<p class="lead">Vet Trial Finder is an independent, free resource for owners of dogs and cats with cancer. We collect information that is scattered across university, hospital, registry and study websites and organize it so owners can find options worth asking about.</p>
<section><h2>What we include</h2><p>The searchable catalog focuses on opportunities that may provide an actual anticancer treatment to a client-owned dog or cat. These may include clinical trials, expanded-access programs and selected treatments available through veterinary oncology centers.</p><p>Observational studies, surveys, sample collection, biobanks and diagnostic-only research are not presented as treatment matches.</p></section>
<section><h2>Where the information comes from</h2><p>We use primary sources whenever possible: official university and veterinary hospital pages, study registries, research teams and sponsors. Each listing links to its official source so owners can read the original information and contact the study team directly.</p></section>
<section><h2>How we check whether an option is current</h2><p>A listing must have a current, usable route to treatment or enrollment. We check published recruitment status, participating locations, contacts and recent institutional updates. “Last verified” is the most recent date we checked the information; it does not guarantee that a place is still available today.</p></section>
<section><h2>How matching works</h2><p>The finder compares the information an owner enters with the eligibility rules that are publicly available. We apply explicit exclusions conservatively and do not turn missing information into a promise of eligibility. A result means “worth checking,” not “accepted.” The research team always makes the final decision after reviewing the medical record.</p></section>
<section><h2>Costs and funding</h2><p>We describe funding only when it is stated by an official source. “Fully funded” may still exclude travel, an initial examination, care unrelated to the study or treatment of unrelated medical problems. If the source does not clearly state what is covered, the listing tells owners to confirm costs with the study team.</p></section>
<section><h2>Duplicates, locations and changes</h2><p>The same study may appear on a registry, a university page and several hospital websites. We combine those records into one listing and show verified participating locations. Studies can close, pause or change eligibility without notice. When an official source conflicts with our listing, the official study team’s information takes priority.</p></section>
<section><h2>What this site does not do</h2><p>Vet Trial Finder does not diagnose cancer, recommend a particular treatment or replace a veterinary oncologist. We do not promise a cure and we do not rank experimental treatment as better than standard care. Our job is to make current options easier to find and easier to discuss with the professionals treating the animal.</p></section>
<p><a class="cta" href="{SITE}/cancer-types/">Browse cancer types</a></p>
</div></main>'''
    text = re.sub(r'<main>.*?</main>', body, text, count=1, flags=re.S)
    directory = root / "how-we-verify"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "index.html").write_text(text, encoding="utf-8")


def add_verification_footer_link(text: str) -> str:
    if f'href="{SITE}/how-we-verify/">How We Verify' in text:
        return text
    marker = f'<a href="{SITE}/help/">Help</a>'
    return text.replace(marker, marker + f'<a href="{SITE}/how-we-verify/">How We Verify</a>', 1)


def add_contact_footer_link(text: str) -> str:
    """Expose the project email in the shared footer without duplicating it."""
    link = f'<a href="mailto:{CONTACT_EMAIL}">Contact</a>'
    if link in text:
        return text
    marker = f'<a href="{SITE}/how-we-verify/">How We Verify</a>'
    if marker not in text:
        raise AssertionError("shared footer navigation marker not found")
    return text.replace(marker, marker + link, 1)


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

    write_verification_page(root)

    indexable: list[str] = []
    noindexed = 0
    for page in sorted(root.rglob("index.html")):
        relative = page.relative_to(root)
        path = "" if relative == Path("index.html") else relative.parent.as_posix()
        text = page.read_text(encoding="utf-8")
        text = remove_unready_hreflang(text)
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
    assert len(indexable) == len(set(indexable))
    print(f"SEO_INDEX_POLICY_OK indexable={len(indexable)} noindex={noindexed}")


if __name__ == "__main__":
    main()
