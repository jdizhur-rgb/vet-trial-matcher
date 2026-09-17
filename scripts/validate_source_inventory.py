#!/usr/bin/env python3
"""Validate the persistent veterinary trial discovery source inventory."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "source_inventory.json"
REQUIRED = {
    "id",
    "name",
    "country",
    "source_type",
    "master_url",
    "required_cadence",
    "last_checked",
    "last_result",
    "content_fingerprint",
}
SOURCE_TYPES = {
    "registry",
    "directory",
    "university",
    "hospital_program",
    "specialty_network",
    "cro_sponsor",
    "foundation",
    "investigator_lab",
}
RESULTS = {"pending", "reachable", "changed", "unchanged", "unreachable", "partial"}


def canonical_url(raw: str) -> str:
    parts = urlsplit(raw)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/") or "/", "", ""))


def fail(message: str) -> None:
    raise SystemExit(f"SOURCE_INVENTORY_VALIDATION_FAILED: {message}")


def main() -> None:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        fail("schema_version must be 1")
    try:
        date.fromisoformat(payload["updated"])
    except (KeyError, TypeError, ValueError):
        fail("updated must be an ISO date")

    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("sources must be a non-empty list")

    ids: set[str] = set()
    urls: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            fail(f"source #{index + 1} is not an object")
        missing = sorted(REQUIRED - source.keys())
        if missing:
            fail(f"source #{index + 1} missing fields: {', '.join(missing)}")

        source_id = source["id"]
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source_id):
            fail(f"invalid id: {source_id!r}")
        if source_id in ids:
            fail(f"duplicate id: {source_id}")
        ids.add(source_id)

        for field in ("name", "country"):
            if not isinstance(source[field], str) or not source[field].strip():
                fail(f"{source_id}: {field} must be nonblank")
        if source["source_type"] not in SOURCE_TYPES:
            fail(f"{source_id}: invalid source_type {source['source_type']!r}")
        if source["required_cadence"] != "daily":
            fail(f"{source_id}: required_cadence must be daily")
        if source["last_result"] not in RESULTS:
            fail(f"{source_id}: invalid last_result {source['last_result']!r}")

        url = source["master_url"]
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"{source_id}: master_url must be an absolute HTTPS URL")
        normalized_url = canonical_url(url)
        if normalized_url in urls:
            fail(f"duplicate master_url: {url}")
        urls.add(normalized_url)

        checked = source["last_checked"]
        if checked is not None:
            try:
                date.fromisoformat(checked)
            except (TypeError, ValueError):
                fail(f"{source_id}: last_checked must be null or an ISO date")
        if source["last_result"] == "pending" and checked is not None:
            fail(f"{source_id}: pending source must not have last_checked")
        if source["last_result"] != "pending" and checked is None:
            fail(f"{source_id}: checked source must have last_checked")

        fingerprint = source["content_fingerprint"]
        if fingerprint is not None and not re.fullmatch(r"sha256:[0-9a-f]{64}", fingerprint):
            fail(f"{source_id}: invalid content_fingerprint")

    digest = hashlib.sha256(INVENTORY.read_bytes()).hexdigest()[:12]
    print(f"SOURCE_INVENTORY_VALIDATION_OK sources={len(sources)} digest={digest}")


if __name__ == "__main__":
    main()
