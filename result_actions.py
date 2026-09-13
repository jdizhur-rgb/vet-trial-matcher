"""Safe owner-facing contact actions and verification labels."""
from __future__ import annotations

import re
from datetime import datetime

EMAIL_RE = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+\d{1,3}[ .-]?)?(?:\(\d{2,4}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\d)"
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
