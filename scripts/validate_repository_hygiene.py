#!/usr/bin/env python3
"""Reject stale architecture, generated snapshots, caches and self-mutating automation."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
RETIRED_PATHS = (
    ROOT / "data" / "trial_updates.json",
    ROOT / "rollback",
    ROOT / "rollback_snapshots",
    ROOT / "seo" / "static" / "matcher-preview",
)
RETIRED_SOURCE_FILES = (
    ROOT / "seo" / "center_image_fallbacks.py",
    ROOT / "seo" / "center_image_localizer.py",
)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.splitlines()


def main() -> None:
    problems: list[str] = []

    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        if "contents: write" in text:
            problems.append(f"{workflow.relative_to(ROOT)} grants contents: write")
        if "git push" in text:
            problems.append(f"{workflow.relative_to(ROOT)} runs git push")

    for path in RETIRED_PATHS + RETIRED_SOURCE_FILES:
        if path.exists():
            problems.append(f"retired path exists: {path.relative_to(ROOT)}")
    problems.extend(
        f"retired catalog overlay exists: {path.relative_to(ROOT)}"
        for path in sorted((ROOT / "data").glob("catalog_patch_*.json"))
    )

    for name in tracked_files():
        parts = Path(name).parts
        if name.startswith("seo/site/"):
            problems.append(f"generated production artifact is tracked: {name}")
        if "__pycache__" in parts or name.endswith((".pyc", ".pyo")):
            problems.append(f"runtime cache is tracked: {name}")
        if name.endswith(("~", ".swp", ".tmp")):
            problems.append(f"temporary file is tracked: {name}")

    if problems:
        raise SystemExit("Repository hygiene check failed:\n- " + "\n- ".join(problems))

    print("REPOSITORY_HYGIENE_OK")


if __name__ == "__main__":
    main()
