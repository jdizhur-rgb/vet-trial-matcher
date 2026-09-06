import json
import time
import uuid
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import streamlit as st

_SUPABASE_URL = "https://bvghrabcfrexvynlyhqb.supabase.co"
_VISIT_MARKER = "__app_visit__"


def _key():
    return str(st.secrets.get("SUPABASE_KEY", "")).strip()


def _headers(extra=None):
    h = {"apikey": _key(), "Content-Type": "application/json"}
    if extra:
        h.update(extra)
    return h


def _post_visit():
    if not _key():
        return False
    payload = json.dumps(
        {
            "trial_center": _VISIT_MARKER,
            "exclusion_reason": st.session_state.setdefault("_visit_id", uuid.uuid4().hex),
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{_SUPABASE_URL}/rest/v1/eligibility_feedback",
        data=payload,
        method="POST",
        headers=_headers({"Prefer": "return=minimal"}),
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status in (200, 201, 204)
    except Exception:
        return False


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


def _render_stats():
    now = datetime.now(timezone.utc)
    total = _count_since()
    day = _count_since(now - timedelta(days=1))
    week = _count_since(now - timedelta(days=7))
    month = _count_since(now - timedelta(days=30))

    st.title("📊 Private visit stats")
    if total is None:
        st.error("Visit counter is not available yet.")
        return
    cols = st.columns(4)
    cols[0].metric("All visits", total)
    cols[1].metric("Last 24h", day)
    cols[2].metric("Last 7 days", week)
    cols[3].metric("Last 30 days", month)
    st.caption("Counts Streamlit sessions, not people. Form answers and pet data are not stored. Stats mode is never counted.")


def install_analytics(disabled=False):
    """Private, zero-cost session counter using the app's existing Supabase table."""
    # Read query flags first. Keep st.stop() OUTSIDE the broad exception handler:
    # Streamlit implements stop with an internal control exception.
    if disabled:
        return
    try:
        params = st.query_params
        stats_mode = str(params.get("stats", "")) == "1"
        analytics_off = str(params.get("analytics_off", "")) == "1"
        analytics_on = str(params.get("analytics_on", "")) == "1"
    except Exception:
        stats_mode = analytics_off = analytics_on = False

    if stats_mode:
        st.session_state["_analytics_off"] = True
        _render_stats()
        st.stop()

    try:
        if analytics_off:
            st.session_state["_analytics_off"] = True
        if analytics_on:
            st.session_state.pop("_analytics_off", None)

        if st.session_state.get("_analytics_off"):
            return
        if not st.session_state.get("_visit_logged"):
            if _post_visit():
                st.session_state["_visit_logged"] = True
                st.session_state["_visit_logged_at"] = int(time.time())
    except Exception:
        # Analytics must never interfere with the matcher.
        return
