#!/usr/bin/env python3
"""Validate owner-facing study links in the effective active catalog.

Checks both the direct study URL (`url`) and the optional Veterinary Clinical
Trials Registry URL (`registry_url`). Hard-dead links (malformed, 404, 410)
fail the check. Bot-blocked/rate-limited/transient responses are reported as
uncertain so they can be reviewed without creating false dead-link failures.
This validator intentionally uses the same active-treatment semantics as the Finder.
"""
from __future__ import annotations

import json
import argparse
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import date, datetime

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CURRENT = {"current", "confirmed_current"}
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
TIMEOUT = 20


def verification_age_days(value: str) -> int | None:
    try:
        return (date.today() - datetime.strptime(value, "%Y-%m-%d").date()).days
    except (TypeError, ValueError):
        return None


def markdown_report(rows, checks, missing_direct) -> str:
    dead = [x for x in checks if x[0] == "dead"]
    uncertain = [x for x in checks if x[0] == "uncertain"]
    stale = []
    for row in rows:
        age = verification_age_days(row.get("verified", ""))
        if age is None or age > 30:
            stale.append((str(row.get("id") or "?"), row.get("verified") or "missing", age))

    lines = [
        "# Trial link review",
        "",
        f"Active records: **{len(rows)}**  ",
        f"Dead links: **{len(dead)}** · Uncertain checks: **{len(uncertain)}** · "
        f"Missing links: **{len(missing_direct)}** · Verification older than 30 days: **{len(stale)}**",
        "",
    ]

    def section(title, items):
        lines.extend([f"## {title}", ""])
        if not items:
            lines.extend(["None.", ""])
            return
        for item in items:
            lines.append(f"- `{item[1]}` · {item[2]} · {item[4]} · {item[3]}")
        lines.append("")

    section("Dead links", dead)
    section("Uncertain — manual review", uncertain)
    lines.extend(["## Records without a link", ""])
    lines.extend([f"- `{rid}` · {title}" for rid, title in missing_direct] or ["None."])
    lines.extend(["", "## Stale verification dates", ""])
    lines.extend([
        f"- `{rid}` · verified: {verified}" + (f" · {age} days ago" if age is not None else "")
        for rid, verified, age in stale
    ] or ["None."])
    lines.append("")
    return "\n".join(lines)


def load_effective() -> list[dict]:
    rows = json.loads((DATA / "trials_base.json").read_text())
    return [
        r for r in rows
        # Match the patient-facing finder exactly: legacy records without an
        # explicit availability flag are considered available unless disabled.
        if r.get("available_for_matching", True)
        and r.get("status_confidence") in CURRENT
        and r.get("study_type", "treatment") in {"treatment", "other_treatment_access"}
    ]


def check_url(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "dead", "malformed URL"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = getattr(resp, "status", 200) or 200
            final_url = resp.geturl()
            if 200 <= status < 400:
                return "ok", f"HTTP {status} -> {final_url}"
            return "uncertain", f"HTTP {status}"
    except urllib.error.HTTPError as exc:
        if exc.code in {404, 410}:
            return "dead", f"HTTP {exc.code}"
        if exc.code in {401, 403, 405, 429}:
            return "uncertain", f"HTTP {exc.code} (site may block automated checks)"
        if 400 <= exc.code < 500:
            return "dead", f"HTTP {exc.code}"
        return "uncertain", f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        return "uncertain", f"network error: {exc}"
    except Exception as exc:
        return "uncertain", f"unexpected error: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-report", type=Path)
    args = parser.parse_args()
    rows = load_effective()
    checks: list[tuple[str, str, str, str, str]] = []
    missing_direct = []

    for row in rows:
        rid = str(row.get("id") or "?")
        title = str(row.get("title") or "")
        direct = str(row.get("url") or "").strip()
        registry = str(row.get("registry_url") or "").strip()

        if not direct and not registry:
            missing_direct.append((rid, title))
            continue

        for field, url in (("registry_url", registry), ("url", direct)):
            if not url:
                continue
            state, detail = check_url(url)
            checks.append((state, rid, field, url, detail))

    dead = [x for x in checks if x[0] == "dead"]
    uncertain = [x for x in checks if x[0] == "uncertain"]
    ok = [x for x in checks if x[0] == "ok"]

    print(f"ACTIVE_RECORDS {len(rows)}")
    print(f"LINKS_OK {len(ok)}")
    print(f"LINKS_UNCERTAIN {len(uncertain)}")
    print(f"LINKS_DEAD {len(dead)}")
    print(f"ACTIVE_RECORDS_WITHOUT_ANY_LINK {len(missing_direct)}")

    for state, rid, field, url, detail in checks:
        print(f"{state.upper()}\t{rid}\t{field}\t{detail}\t{url}")
    for rid, title in missing_direct:
        print(f"MISSING\t{rid}\tno owner-facing study link\t{title}")

    if args.markdown_report:
        args.markdown_report.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_report.write_text(
            markdown_report(rows, checks, missing_direct), encoding="utf-8"
        )

    if dead or missing_direct:
        print("TRIAL_LINK_VALIDATION_FAILED", file=sys.stderr)
        return 1
    print("TRIAL_LINK_VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
