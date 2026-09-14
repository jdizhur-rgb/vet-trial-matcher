"""Safe owner-facing contact actions and verification labels."""
from __future__ import annotations

import re
from datetime import datetime

EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+\d{1,3}[ .-]?)?(?:\(\d{2,4}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\d)"
)\n\nFUNDING_BADGES_RE = re.compile(r"^[\\s\\ufe0f]*(?:🟢|🟡|🟠|🔴)[\\s\\ufe0f]*")\n\nCONFIRMATION_PRIORITY = (\n    "pathology/cytology",\n    "active treatment target",\n    "measurable disease",\n    "minimum weight",\n    "maximum weight",\n    "visible tumor",\n    "tumor location",\n    "current chemotherapy",\n    "current radiation",\n    "current steroid",\n)\n\n\ndef contact_actions(contact: str) -> tuple[str | None, str | None]:
    """Return the first unambiguous email and callable phone number."""
    email_match = EMAIL_RE.search(contact or "")
    phone_match = PHONE_RE.search(contact or "")
    email = email_match.group(0) if email_match else None
    phone = None
    if phone_match:
        raw = phone_match.group(0)
        digits = re.sub(r"\D", "", raw)
        if 10 <= len(digits) <= 15:
            phone = ("+" if raw.lstrip().startswith("+") else "") + digits
    return email, phone


def verification_label(value: str | None) -> str:
    if not value:
        return "Last checked: date not recorded"
    try:
        checked = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return f"Last checked: {value}"
    return f"Last checked: {checked.strftime('%b')} {checked.day}, {checked.year}"
\n\ndef clean_funding_text(value: object) -> str:\n    """Remove traffic-light badges while preserving the verified funding text."""\n    return FUNDING_BADGES_RE.sub("", str(value)).strip()\n\n\ndef compact_confirmations(items: list[str], limit: int = 3) -> tuple[list[str], list[str]]:\n    """Keep the most decision-relevant unknowns visible and fold the rest away."""\n    unique = list(dict.fromkeys(item.strip() for item in items if item.strip()))\n\n    def rank(item: str) -> tuple[int, int]:\n        lowered = item.casefold()\n        for index, phrase in enumerate(CONFIRMATION_PRIORITY):\n            if phrase in lowered:\n                return index, unique.index(item)\n        return len(CONFIRMATION_PRIORITY), unique.index(item)\n\n    visible = sorted(unique, key=rank)[:limit]\n    visible_set = set(visible)\n    hidden = [item for item in unique if item not in visible_set]\n    return visible, hidden\n