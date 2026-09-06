import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import streamlit as st

_SUPABASE_URL = "https://bvghrabcfrexvynlyhqb.supabase.co"
_VISIT_MARKER = "__app_visit__"


def _key():
    return str(st.secrets.get("SUPABASE_KEY", "")).strip()


def _headers(extra=None):
    key = _key()
    h = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if extra:
        h.update(extra)
    return h


def _count_since(since=None):
    if not _key():
        return None
    params = {
        "select": "trial_center",
        "trial_center": f"eq.{_VISIT_MARKER}",
    }
    if since is not None:
        params["created_at"] = "gte." + since.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    url = f"{_SUPABASE_URL}/rest/v1/eligibility_feedback?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        method="GET",
        headers=_headers({"Prefer": "count=exact", "Range": "0-0"}),
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            content_range = r.headers.get("Content-Range", "")
            total = content_range.rsplit("/", 1)[-1]
            return int(total) if total.isdigit() else 0
    except Exception:
        return None


now = datetime.now(timezone.utc)
total = _count_since()
day = _count_since(now - timedelta(days=1))
week = _count_since(now - timedelta(days=7))
month = _count_since(now - timedelta(days=30))

st.title("📊 Private visit stats")
if total is None:
    st.error("Visit counter is not available yet.")
else:
    cols = st.columns(4)
    cols[0].metric("All visits", total)
    cols[1].metric("Last 24h", day)
    cols[2].metric("Last 7 days", week)
    cols[3].metric("Last 30 days", month)
    st.caption("Counts Streamlit sessions, not people. Form answers and pet data are not stored. This stats page is not counted.")
