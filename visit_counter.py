import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

BASE = "https://countapi.mileshilliard.com/api/v1"
PREFIX = "vctf_6f9e4d2b7a31c85e"
ET = ZoneInfo("America/New_York")

def _hit(key):
    try:
        with urllib.request.urlopen(f"{BASE}/hit/{key}", timeout=4) as r:
            data = json.loads(r.read().decode("utf-8"))
            return int(data.get("value", 0))
    except Exception:
        return None

def _get(key):
    try:
        with urllib.request.urlopen(f"{BASE}/get/{key}", timeout=4) as r:
            data = json.loads(r.read().decode("utf-8"))
            return int(data.get("value", 0))
    except Exception:
        return 0

def _keys(now=None):
    now = now or datetime.now(ET)
    iso_year, iso_week, _ = now.isocalendar()
    return {
        "total": f"{PREFIX}_total",
        "today": f"{PREFIX}_day_{now:%Y%m%d}",
        "week": f"{PREFIX}_week_{iso_year}{iso_week:02d}",
        "month": f"{PREFIX}_month_{now:%Y%m}",
    }

def record_visit():
    """Count one visit per live Streamlit session. Never blocks the app."""
    if st.session_state.get("_visit_counter_done"):
        return
    keys = _keys()
    ok = False
    for key in keys.values():
        if _hit(key) is not None:
            ok = True
    if ok:
        st.session_state["_visit_counter_done"] = True

def read_stats():
    keys = _keys()
    return {name: _get(key) for name, key in keys.items()}
