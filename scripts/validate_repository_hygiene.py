#!/usr/bin/env python3
"""Reject self-mutating automation and retired layered catalog inputs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
RETIRED_DATA = (ROOT / "data" / "trial_updates.json",)


def main() -> None:
    problems: list[str] = []

    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        if "contents: write" in text:
            problems.append(f"{workflow.relative_to(ROOT)} grants contents: write")
        if "git push" in text:
            problems.append(f"{workflow.relative_to(ROOT)} runs git push")

    problems.extend(
        str(path.relative_to(ROOT))
        for path in RETIRED_DATA
        if path.exists()
    )
    problems.extend(
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "data").glob("catalog_patch_*.json"))
    )

    if problems:
        raise SystemExit(
            "Repository hygiene check failed:\n- " + "\n- ".join(problems)
        )

    print("REPOSITORY_HYGIENE_OK")


if __name__ == "__main__":
    main()
