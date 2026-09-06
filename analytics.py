import hashlib
import time
import urllib.parse
import urllib.request
import streamlit as st

_DEFAULT_MEASUREMENT_ID = "G-TQOYHMOOM5"


def _client_id():
    """Stable anonymous ID for this Streamlit session; no pet/form data is included."""
    if "_ga_client_id" not in st.session_state:
        raw = f"{time.time_ns()}-{id(st.session_state)}"
        digest = hashlib.sha256(raw.encode()).hexdigest()
        st.session_state["_ga_client_id"] = f"{int(time.time())}.{int(digest[:12], 16)}"
    return st.session_state["_ga_client_id"]


@st.cache_data(ttl=1800, show_spinner=False)
def _send_page_view(measurement_id, api_secret, client_id):
    endpoint = "https://www.google-analytics.com/mp/collect?" + urllib.parse.urlencode(
        {"measurement_id": measurement_id, "api_secret": api_secret}
    )
    payload = (
        '{"client_id":"%s","events":[{"name":"page_view","params":'
        '{"page_location":"https://vet-cancer-trial-finder.streamlit.app/",'
        '"page_title":"Vet Cancer Treatment Finder","engagement_time_msec":100,'
        '"session_id":"%s"}}]}' % (client_id, client_id.split(".", 1)[0])
    ).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "VetCancerTrialFinder/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status in (200, 204)
    except Exception:
        return False


def install_analytics():
    """Send a privacy-minimized GA4 page_view from the Streamlit server.

    Requires GA_API_SECRET in Streamlit secrets. No diagnosis, age, weight,
    search terms, names, email addresses, or other form values are transmitted.
    The cache prevents Streamlit reruns from inflating page-view counts.
    """
    measurement_id = str(st.secrets.get("GA_MEASUREMENT_ID", _DEFAULT_MEASUREMENT_ID)).strip()
    api_secret = str(st.secrets.get("GA_API_SECRET", "")).strip()
    if not measurement_id or not api_secret:
        return
    _send_page_view(measurement_id, api_secret, _client_id())
