#!/usr/bin/env python3
"""Build the complete production website from the files committed to main."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "seo" / "site"


def run(*args: str, pythonpath: str | None = None) -> None:
    env = os.environ.copy()
    if pythonpath:
        env["PYTHONPATH"] = str(ROOT / pythonpath)
    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)


def main() -> None:
    run("seo/build_production_site.py")
    run("seo/validate_cancer_depth.py", "--site", "seo/site", pythonpath="seo")

    static = ROOT / "seo" / "static"
    if static.exists():
        shutil.copytree(static, SITE, dirs_exist_ok=True)

    # Owner-facing article is generated before the indexing pass so it receives
    # the same canonical, structured-data and sitemap validation as the site.
    run("seo/dog_cancer_trials_article.py", pythonpath="seo")

    # These deterministic finishing stages operate on the generated HTML.
    run("seo_index_cleanup.py")
    # TEST BRANCH ONLY. Fold this rule into seo_index_cleanup.py before main.
    run("seo_index_review_preview.py")
    run("help_content_update.py")
    run("center_zip_search.py")
    run("seo/ensure_center_images.py")


if __name__ == "__main__":
    main()
