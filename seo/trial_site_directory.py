from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from seo.center_directory import addresses_for


def _clean(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _site_name(site: Dict[str, Any]) -> str:
    return _clean(site.get("name") or site.get("hospital") or site.get("label"))


def _structured_address(site: Dict[str, Any]) -> str:
    street = _clean(site.get("street"))
    city = _clean(site.get("city"))
    state = _clean(site.get("state"))
    postal = _clean(site.get("postal_code") or site.get("zip"))
    country = _clean(site.get("country"))
    if not street:
        return ""
    locality = ", ".join(x for x in [city, state] if x)
    if postal:
        locality = (locality + " " + postal).strip()
    parts = [street]
    if locality:
        parts.append(locality)
    if country and country.upper() not in {"US", "USA", "UNITED STATES"}:
        parts.append(country)
    return ", ".join(parts)


def _embedded_full_address(site: Dict[str, Any]) -> str:
    """Use a stored full address when an older patch embedded it in label/hospital."""
    for value in (site.get("label"), site.get("hospital")):
        text = _clean(value)
        if not text or not re.search(r"\d", text):
            continue
        # Require more than a bare street fragment: US ZIP, international postcode,
        # or at least a comma-separated locality after a numbered street.
        if re.search(r"\b\d{5}(?:-\d{4})?\b", text):
            return text
        if len(text.split(",")) >= 3:
            return text
    return ""


def site_addresses(site: Dict[str, Any], *, trial_center: str = "") -> List[str]:
    """Resolve physical addresses for one stored participating-site record.

    Priority is trial-specific structured street data, then a full address already
    embedded by older catalog patches, then the central center directory.
    City/state-only labels are never promoted to street addresses.
    """
    direct = _structured_address(site)
    if direct:
        return [direct]

    embedded = _embedded_full_address(site)
    if embedded:
        return [embedded]

    candidates = []
    for key in (site.get("name"), site.get("hospital"), trial_center):
        key = _clean(key)
        if key and key not in candidates:
            candidates.append(key)
    for key in candidates:
        vals = [_clean(x) for x in addresses_for(key) if _clean(x)]
        if vals:
            return vals
    return []


def trial_site_records(trial: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return every physical site stored for a trial with per-trial status."""
    out: List[Dict[str, Any]] = []
    center = _clean(trial.get("center"))
    trial_id = _clean(trial.get("id"))

    def add_many(items: Iterable[Dict[str, Any]], default_status: str) -> None:
        for raw in items or []:
            site = dict(raw or {})
            status = _clean(site.get("status") or default_status).lower()
            if status not in {"active", "inactive"}:
                status = default_status
            name = _site_name(site)
            addresses = site_addresses(site, trial_center=center)
            out.append({
                "trial_id": trial_id,
                "organization": center,
                "site_name": name,
                "status": status,
                "addresses": addresses,
                "source_site": site,
            })

    add_many(trial.get("sites") or [], "active")
    add_many(trial.get("inactive_sites") or [], "inactive")

    # Single-site trials sometimes store only a center name and no sites array.
    if not out and center:
        addresses = [_clean(x) for x in addresses_for(center) if _clean(x)]
        if addresses:
            out.append({
                "trial_id": trial_id,
                "organization": center,
                "site_name": center,
                "status": "active",
                "addresses": addresses,
                "source_site": {},
            })
    return out


def active_trial_addresses(trial: Dict[str, Any]) -> List[str]:
    seen = set()
    result: List[str] = []
    for rec in trial_site_records(trial):
        if rec["status"] != "active":
            continue
        for address in rec["addresses"]:
            if address and address not in seen:
                seen.add(address)
                result.append(address)
    return result


def build_directory(trials: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Build organization -> sites -> trial-status directory from merged catalog."""
    organizations: Dict[str, Dict[str, Any]] = {}
    trial_index: Dict[str, Any] = {}

    for trial in trials:
        trial_id = _clean(trial.get("id"))
        center = _clean(trial.get("center")) or "Unspecified organization"
        records = trial_site_records(trial)
        trial_index[trial_id] = {
            "organization": center,
            "active_sites": [],
            "inactive_sites": [],
        }
        org = organizations.setdefault(center, {"sites": {}})

        for rec in records:
            site_key = rec["site_name"] or (rec["addresses"][0] if rec["addresses"] else "Unresolved site")
            site_entry = org["sites"].setdefault(site_key, {
                "name": rec["site_name"] or site_key,
                "addresses": [],
                "trials": {},
            })
            for address in rec["addresses"]:
                if address not in site_entry["addresses"]:
                    site_entry["addresses"].append(address)
            site_entry["trials"][trial_id] = rec["status"]
            bucket = "active_sites" if rec["status"] == "active" else "inactive_sites"
            if site_key not in trial_index[trial_id][bucket]:
                trial_index[trial_id][bucket].append(site_key)

    return {"organizations": organizations, "trials": trial_index}
