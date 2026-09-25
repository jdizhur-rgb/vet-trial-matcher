#!/usr/bin/env python3
"""Build the complete production website from the files committed to main."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "seo" / "site"
sys.path.insert(0, str(ROOT / "seo"))

from site_shell import apply_page_title_component, wrap_html  # noqa: E402


FORBIDDEN_TRACKING_MARKERS = (
    "cloud.umami.is",
    "window.umami",
    "matcher-search",
)


def run(*args: str, pythonpath: str | None = None) -> None:
    env = os.environ.copy()
    if pythonpath:
        env["PYTHONPATH"] = str(ROOT / pythonpath)
    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)


def validate_no_tracking() -> None:
    findings: list[str] = []
    for path in SITE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".js"}:
            continue
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_TRACKING_MARKERS:
            if marker in text:
                findings.append(f"{path.relative_to(ROOT)}: {marker}")
    if findings:
        raise RuntimeError("Tracking code found in production output:\n" + "\n".join(findings))
    print("NO_TRACKING_OK")


def validate_public_page_shell() -> None:
    pages = list(SITE.rglob("*.html"))
    missing_title_component: list[str] = []
    missing_care_links: list[str] = []
    expected_links = (
        '<a href="https://vettrialfinder.com/matcher/centers/">Find oncology care near you</a>',
        '<a href="https://vettrialfinder.com/centers/">Browse all oncology centers</a>',
    )
    for path in pages:
        text = path.read_text(encoding="utf-8")
        h1_tags = re.findall(r"<h1\b[^>]*>", text, flags=re.IGNORECASE)
        if h1_tags and any(
            not re.search(r'class=["\'][^"\']*\bpage-title\b', tag) for tag in h1_tags
        ):
            missing_title_component.append(str(path.relative_to(ROOT)))
        if '<header class="site-header">' in text and any(link not in text for link in expected_links):
            missing_care_links.append(str(path.relative_to(ROOT)))
    if missing_title_component:
        raise RuntimeError(
            "Public H1 missing shared page-title component:\n"
            + "\n".join(missing_title_component)
        )
    if missing_care_links:
        raise RuntimeError(
            "Shared header missing oncology-care directory links:\n"
            + "\n".join(missing_care_links)
        )
    print("PUBLIC_PAGE_SHELL_OK", len(pages))


def main() -> None:
    # Production builds must remain reproducible from committed source. This
    # rejects workflows that rewrite the repository after a push.
    run("scripts/validate_repository_hygiene.py")

    # The deployment artifact is generated, not an incremental cache. Starting
    # clean prevents retired pages committed by an older generator from being
    # carried into the next build with stale canonicals or metadata.
    shutil.rmtree(SITE, ignore_errors=True)
    run("seo/build_production_site.py")
    run("seo/validate_cancer_depth.py", "--site", "seo/site", pythonpath="seo")
    run("scripts/build_matcher_data.py")
    run("scripts/build_oncology_center_catalog.py")
    run("seo/generate_oncology_center_finder.py")
    run("seo/validate_oncology_centers.py")

    # The committed matcher templates are the single source for /matcher/.
    # Copy only that tree; preview and rollback routes are intentionally absent.
    static = ROOT / "seo" / "static"
    matcher_source = static / "matcher"
    matcher = SITE / "matcher"
    if not matcher_source.exists():
        raise RuntimeError("Missing canonical matcher templates")
    shutil.copytree(matcher_source, matcher)
    for page in matcher.rglob("*.html"):
        text = wrap_html(page.read_text(encoding="utf-8"))
        if page.relative_to(matcher) != Path("ect/index.html"):
            text = re.sub(
                r'<meta name="robots" content="noindex[^"]*">',
                "",
                text,
                flags=re.IGNORECASE,
            )
        page.write_text(text, encoding="utf-8")

    # Copy immutable shared assets and verification files explicitly. This
    # avoids treating seo/static as a second, implicit website generator.
    for source in static.iterdir():
        if source.name == "matcher":
            continue
        destination = SITE / source.name
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    # Owner-facing articles generated here enter the same final indexing pass
    # as the rest of the production site.
    run("seo/clinical_trials_for_pets_article.py", pythonpath="seo")
    run("seo/lump_before_surgery_article.py", pythonpath="seo")

    # These deterministic finishing stages operate on the generated HTML.
    run("seo_index_cleanup.py")
    run("help_content_update.py")
    run("center_zip_search.py")
    run("seo/validate_center_profiles.py")
    run("seo/enforce_sentence_case.py", pythonpath="seo")
    run("scripts/validate_production_sync.py")
    for page in SITE.rglob("*.html"):
        page.write_text(
            apply_page_title_component(page.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
    validate_no_tracking()
    validate_public_page_shell()
    subprocess.run(
        ["node", "scripts/test_matcher_logic.js"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
