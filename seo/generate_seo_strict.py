#!/usr/bin/env python3
"""Systematic SEO generator guard: strict diagnosis mapping for every generated page.

The presentation and effective-catalog logic remain in generate_seo.py. This entrypoint
replaces permissive substring diagnosis matching with token/phrase-boundary matching,
normalizes scalar/list cancer fields, runs the generator, then audits the complete
region/species/cancer matrix. It exists to prevent cross-diagnosis leakage such as
`glioma` matching the `paraganglioma` synonym used for chemodectoma.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import generate_seo as g


def _phrase_present(phrase: str, text: str) -> bool:
    """Match a normalized diagnosis phrase as a complete phrase, never inside a word."""
    phrase = g.norm(phrase)
    text = g.norm(text)
    if not phrase or not text:
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])", text) is not None


def canonical_cancer(value):
    raw = g.norm(value)
    if not raw:
        return None
    if any(_phrase_present(term, raw) for term in g.GENERIC_WORDS):
        return None
    for key, aliases in g.CANONICAL_RULES:
        if any(_phrase_present(alias, raw) for alias in aliases):
            return key
    return None


def cancer_values(row):
    value = row.get("cancers", [])
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return []


def row_cancers(row):
    return {mapped for mapped in (canonical_cancer(v) for v in cancer_values(row)) if mapped}


def audit_matrix():
    """Audit every generated diagnosis assignment, not representative pages."""
    rows = g.load_effective()
    by_id = {r["id"]: r for r in rows}
    matrix = {}
    errors = []

    for region, countries in g.REGIONS.items():
        for species_key, species_name in g.SPECIES.items():
            for row in rows:
                if row.get("country") not in countries or not g.species_ok(row, species_name):
                    continue
                for cancer in row_cancers(row):
                    key = f"{region}/{species_key}/{g.slugify(cancer)}"
                    matrix.setdefault(key, []).append(row["id"])

    # Every English diagnosis page must correspond exactly to one non-empty matrix cell.
    for page in g.OUT.glob("*/*/*/index.html"):
        rel = str(page.parent.relative_to(g.OUT)).replace("\\", "/")
        expected = matrix.get(rel, [])
        if not expected:
            errors.append(f"orphan page: {rel}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        card_count = text.count('class="card"')
        if card_count != len(expected):
            errors.append(f"card-count mismatch {rel}: html={card_count} matrix={len(expected)}")

    # Every expected matrix cell must have a generated English page.
    for rel, ids in matrix.items():
        page = g.OUT / rel / "index.html"
        if not page.exists():
            errors.append(f"missing page: {rel} ({len(ids)} records)")

    # Regression for the real substring bug: paraganglioma must never become glioma.
    for row in rows:
        values = [g.norm(v) for v in cancer_values(row)]
        if any("paraganglioma" in v for v in values) and "glioma" in row_cancers(row):
            errors.append(f"paraganglioma leaked into glioma: {row['id']}")

    if errors:
        raise AssertionError("SEO matrix audit failed:\n" + "\n".join(errors[:50]))

    audit = {
        "effective_treatment_records": len(rows),
        "matrix_cells": len(matrix),
        "assignments": sum(len(v) for v in matrix.values()),
        "cells": {k: sorted(v) for k, v in sorted(matrix.items())},
    }
    (g.OUT / "mapping-audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(
        f"STRICT_MATRIX_OK records={audit['effective_treatment_records']} "
        f"cells={audit['matrix_cells']} assignments={audit['assignments']}"
    )


def main():
    # Patch the single canonical mapping used by page discovery and card selection.
    g.canonical_cancer = canonical_cancer
    g.row_cancers = row_cancers
    g.main()
    audit_matrix()


if __name__ == "__main__":
    main()
