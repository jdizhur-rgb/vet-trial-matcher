"""Privacy-minimal structured events for understanding Finder search gaps."""
from __future__ import annotations

import json
import logging
from typing import Any

LOGGER = logging.getLogger("vet_trial_finder.search")
LOGGER.setLevel(logging.INFO)


def tumor_size_bucket(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value < 1:
        return "under_1_cm"
    if value < 2:
        return "1_to_under_2_cm"
    if value < 5:
        return "2_to_under_5_cm"
    return "5_cm_or_more"


def record_search_outcome(*, result_count: int, fields: dict[str, Any]) -> None:
    """Log one anonymous search event; callers must not pass ZIP or identifiers."""
    forbidden = {"zip", "zip_code", "email", "phone", "name", "session_id", "ip"}
    safe_fields = {
        key: value
        for key, value in fields.items()
        if key not in forbidden and value not in (None, "")
    }
    event = {
        "event": "vet_trial_search",
        "result_count": int(result_count),
        "zero_results": result_count == 0,
        **safe_fields,
    }
    LOGGER.info("SEARCH_TELEMETRY %s", json.dumps(event, ensure_ascii=True, sort_keys=True))
