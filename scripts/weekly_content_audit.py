#!/usr/bin/env python3
"""Build a non-mutating weekly queue for manual recruitment review."""
from __future__ import annotations

import argparse
import json
import re
import socket
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "trials_base.json"
CURRENT = {"current", "confirmed_current"}
USER_AGENT = "Mozilla/5.0 (compatible; VetTrialFinderWeeklyAudit/1.0)"
TIMEOUT = 15

CLOSED_PATTERNS = (
    r"\bnot recruiting\b", r"\benrollment (?:is )?closed\b",
    r"\brecruitment (?:is )?(?:complete|completed|closed)\b", r"\bstudy closed\b",
)
OPEN_PATTERNS = (
    r"\bactively recruiting\b", r"\bnow enrolling\b",
    r"\benrollment (?:is )?open\b", r"\bcurrently enrolling\b",
)


def status_signals(text: str) -> tuple[bool, bool]:
    compact = re.sub(r"\s+", " ", text.lower())
    closed = any(re.search(pattern, compact) for pattern in CLOSED_PATTERNS)
    open_ = any(re.search(pattern, compact) for pattern in OPEN_PATTERNS)
    return open_, closed


def age_days(value: str) -> int | None:
    try:
        return (date.today() - datetime.strptime(value, "%Y-%m-%d").date()).days
    except (TypeError, ValueError):
        return None


def fetch_text(url: str) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read(1_000_000).decode("utf-8", errors="ignore")
            return "ok", re.sub(r"<[^>]+>", " ", body)
    except urllib.error.HTTPError as exc:
        return "uncertain" if exc.code in {401, 403, 405, 429} else "error", f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        return "uncertain", str(exc)


def active_rows() -> list[dict]:
    rows = json.loads(DATA.read_text(encoding="utf-8"))
    return [
        row for row in rows
        if row.get("available_for_matching", True)
        and row.get("status_confidence") in CURRENT
        and row.get("study_type", "treatment") in {"treatment", "other_treatment_access"}
    ]


def build_report(rows: list[dict]) -> str:
    by_url: dict[str, list[dict]] = {}
    stale = []
    incomplete = []
    for row in rows:
        url = str(row.get("url") or row.get("registry_url") or "").strip()
        if url:
            by_url.setdefault(url, []).append(row)
        age = age_days(row.get("verified", ""))
        if age is None or age > 30:
            stale.append((row, age))
        missing = []
        if not row.get("contacts") and not row.get("contact"):
            missing.append("contacts")
        if not row.get("funding"):
            missing.append("funding")
        if missing:
            incomplete.append((row, missing))

    signals = []
    fetch_problems = []
    for url, linked_rows in by_url.items():
        state, content = fetch_text(url)
        ids = ", ".join(f"`{row.get('id', '?')}`" for row in linked_rows)
        if state != "ok":
            fetch_problems.append((ids, state, content, url))
            continue
        open_, closed = status_signals(content)
        if closed:
            signals.append((ids, "ambiguous open + closed language" if open_ else "closure language found", url))

    lines = [
        "# Weekly recruitment review queue", "",
        "This report is a screening aid. It never changes catalog status or verification dates.", "",
        f"Active records: **{len(rows)}** · Official pages checked: **{len(by_url)}**", "",
        f"Closure-language signals: **{len(signals)}** · Fetch problems: **{len(fetch_problems)}** · "
        f"Verified over 30 days ago: **{len(stale)}** · Missing contact/funding fields: **{len(incomplete)}**", "",
        "## Review first: closure language", "",
    ]
    lines += [f"- {ids} · {label} · {url}" for ids, label, url in signals] or ["None."]
    lines += ["", "## Pages requiring manual access", ""]
    lines += [f"- {ids} · {state}: {detail} · {url}" for ids, state, detail, url in fetch_problems] or ["None."]
    lines += ["", "## Stale verification dates", ""]
    lines += [
        f"- `{row.get('id', '?')}` · {row.get('verified') or 'missing'}" +
        (f" · {age} days" if age is not None else "")
        for row, age in stale
    ] or ["None."]
    lines += ["", "## Missing structured details", ""]
    lines += [f"- `{row.get('id', '?')}` · {', '.join(missing)}" for row, missing in incomplete] or ["None."]
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-report", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(active_rows())
    args.markdown_report.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_report.write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
