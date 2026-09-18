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

from site_shell import apply_navigation  # noqa: E402


def run(*args: str, pythonpath: str | None = None) -> None:
    env = os.environ.copy()
    if pythonpath:
        env["PYTHONPATH"] = str(ROOT / pythonpath)
    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)


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
    run("scripts/build_matcher_preview_data.py")

    static = ROOT / "seo" / "static"
    if static.exists():
        shutil.copytree(static, SITE, dirs_exist_ok=True)

    # Promote the fully tested hidden matcher portal to its permanent URL.
    # Keep the preview copy available as a rollback until the live deployment
    # has been checked, but publish an indexable /matcher/ copy.
    preview = static / "matcher-preview"
    matcher = SITE / "matcher"
    if preview.exists():
        shutil.copytree(preview, matcher, dirs_exist_ok=True)
        for page in matcher.rglob("*.html"):
            text = page.read_text(encoding="utf-8")
            text = text.replace("matcher-preview", "matcher")
            text = apply_navigation(text)
            text = re.sub(
                r'<meta name="robots" content="noindex[^"]*">',
                "",
                text,
                flags=re.IGNORECASE,
            )
            page.write_text(text, encoding="utf-8")

    # Owner-facing articles generated here enter the same final indexing pass
    # as the rest of the production site.
    run("seo/clinical_trials_for_pets_article.py", pythonpath="seo")
    run("seo/lump_before_surgery_article.py", pythonpath="seo")

    # These deterministic finishing stages operate on the generated HTML.
    run("seo_index_cleanup.py")
    run("help_content_update.py")
    run("center_zip_search.py")
    run("seo/ensure_center_images.py")
    run("seo/enforce_sentence_case.py", pythonpath="seo")
    run("scripts/validate_production_sync.py")
    subprocess.run(
        ["node", "scripts/test_matcher_logic.js"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
