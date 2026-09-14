"""Safe owner-facing contact actions and verification labels."""
from __future__ import annotations

import re
from datetime import datetime

EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+\d{1,3}[ .-]?)?(?:\(\d{2,4}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\d)"
)

FUNDING_BADGES_RE = re.compile(r"^[\s\ufe0f]*(?:🟢|🟡|🟠|🔴)[\s\ufe0f]*")

CONFIRMATION_PRIORITY = (
    "pathology/cytology",
    "active treatment target",
    "measurable disease",
    "minimum weight",
    "maximum weight",
    "visible tumor",
    "tumor location",
    "current chemotherapy",
    "current radiation",
    "current steroid",
)


def contact_actions(contact: str) -> tuple[str | None, str | None]:
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


def clean_funding_text(value: object) -> str:
    """Remove traffic-light badges while preserving the verified funding text."""
    return FUNDING_BADGES_RE.sub("", str(value)).strip()


def compact_confirmations(items: list[str], limit: int = 3) -> tuple[list[str], list[str]]:
    """Keep the most decision-relevant unknowns visible and fold the rest away."""
    unique = list(dict.fromkeys(item.strip() for item in items if item.strip()))

    def rank(item: str) -> tuple[int, int]:
        lowered = item.casefold()
        for index, phrase in enumerate(CONFIRMATION_PRIORITY):
            if phrase in lowered:
                return index, unique.index(item)
        return len(CONFIRMATION_PRIORITY), unique.index(item)

    visible = sorted(unique, key=rank)[:limit]
    visible_set = set(visible)
    hidden = [item for item in unique if item not in visible_set]
    return visible, hidden
