"""Canonical selection rules for owner-facing catalog surfaces."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "trials_base.json"
CURRENT_STATUSES = {"current", "confirmed_current"}
PUBLIC_STUDY_TYPES = {"treatment", "other_treatment_access"}


def load_catalog(path: Path = SOURCE) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_current_public(row: dict) -> bool:
    return (
        row.get("available_for_matching", True)
        and row.get("status_confidence") in CURRENT_STATUSES
        and row.get("study_type", "treatment") in PUBLIC_STUDY_TYPES
    )


def current_public(rows: list[dict] | None = None) -> list[dict]:
    return [row for row in (rows if rows is not None else load_catalog()) if is_current_public(row)]


def current_treatments(rows: list[dict] | None = None) -> list[dict]:
    return [row for row in current_public(rows) if row.get("study_type", "treatment") == "treatment"]


def current_access(rows: list[dict] | None = None) -> list[dict]:
    return [row for row in current_public(rows) if row.get("study_type") == "other_treatment_access"]
