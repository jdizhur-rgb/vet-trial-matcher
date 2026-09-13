"""Optional, local-only ZIP distance estimates for US trial sorting."""

from __future__ import annotations

import math
from typing import Any

import zipcodes


def _miles(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    radius = 3958.8
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dp = math.radians(b_lat - a_lat)
    dl = math.radians(b_lon - a_lon)
    value = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(value))


def lookup_us_zip(zip_code: str) -> tuple[float, float, str, str] | None:
    cleaned = "".join(character for character in zip_code if character.isdigit())[:5]
    if len(cleaned) != 5:
        return None
    rows = zipcodes.matching(cleaned)
    if not rows:
        return None
    row = rows[0]
    return float(row["lat"]), float(row["long"]), row["city"], row["state"]


def _site_coordinates(city: str, state: str) -> tuple[float, float] | None:
    rows = zipcodes.filter_by(city=city, state=state)
    if not rows:
        return None
    row = rows[0]
    return float(row["lat"]), float(row["long"])


def trial_distance_miles(trial: dict[str, Any], origin: tuple[float, float]) -> float | None:
    candidates: list[tuple[str, str]] = []
    for site in trial.get("sites", []):
        if site.get("city") and site.get("state"):
            candidates.append((str(site["city"]), str(site["state"])))
    if trial.get("city") and trial.get("state"):
        candidates.append((str(trial["city"]), str(trial["state"])))
    distances = []
    for city, state in candidates:
        coordinates = _site_coordinates(city, state)
        if coordinates:
            distances.append(_miles(*origin, *coordinates))
    return min(distances) if distances else None


def sort_matches_by_distance(matches, zip_code: str):
    location = lookup_us_zip(zip_code)
    if not location:
        return list(matches), None
    lat, lon, city, state = location
    decorated = []
    for index, match in enumerate(matches):
        distance = trial_distance_miles(match.trial, (lat, lon))
        decorated.append((distance is None, distance or float("inf"), index, match))
    decorated.sort(key=lambda item: item[:3])
    return [item[3] for item in decorated], {"city": city, "state": state, "distances": {item[3].trial["id"]: item[1] for item in decorated if not item[0]}}

