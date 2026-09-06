import hashlib
import json
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


def _payload(client_id):
    session_id = int(time.time())
    return {
        "client_id": client_id,
        "events": [
            {
                "name": "page_view",
                "params": {
                    "page_location": "https://vet-cancer-trial-finder.streamlit.app/",
                    "page_title": "Vet Cancer Treatment Finder",
                    "engagement_time_msec": 100,
                    "session_id": session_id,
                },
            }
        ],
    }


def _post(endpoint, payload):
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "VetCancerTrialFinder/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=8) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


@st.cache_data(ttl=1800, show_spinner=False)
def _send_page_view(measurement_id, api_secret, client_id):
    endpoint = "https://www.google-analytics.com/mp/collect?" + urllib.parse.urlencode(
        {"measurement_id": measurement_id, "api_secret": api_secret}
    )
    try:
        status, _ = _post(endpoint, _payload(client_id))
        return status in (200, 204)
    except Exception:
        return False


def _debug_result(measurement_id, api_secret, client_id):
    endpoint = "https://www.google-analytics.com/debug/mp/collect?" + urllib.parse.urlencode(
        {"measurement_id": measurement_id, "api_secret": api_secret}
    )
    try:
        status, body = _post(endpoint, _payload(client_id))
        parsed = json.loads(body or "{}")
        return {"http_status": status, "validationMessages": parsed.get("validationMessages", [])}
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def install_analytics():
    """Send a privacy-minimized GA4 page_view from the Streamlit server.

    Requires GA_API_SECRET in Streamlit secrets. No diagnosis, age, weight,
    search terms, names, email addresses, or other form values are transmitted.
    The cache prevents Streamlit reruns from inflating page-view counts.

    Temporary diagnostic mode: add ?ga_debug=1 to the app URL. It shows only
    whether the required secrets are present and Google's validation messages;
    it never displays the secret itself.
    """
    measurement_id = str(st.secrets.get("GA_MEASUREMENT_ID", _DEFAULT_MEASUREMENT_ID)).strip()
    api_secret = str(st.secrets.get("GA_API_SECRET", "")).strip()
    client_id = _client_id()

    if st.query_params.get("ga_debug") == "1":
        if not api_secret:
            st.error("GA debug: GA_API_SECRET is missing in Streamlit Secrets.")
            return
        result = _debug_result(measurement_id, api_secret, client_id)
        if result.get("validationMessages") == [] and result.get("http_status") in (200, 204):
            st.success("GA debug: Google accepted the Measurement Protocol payload with no validation errors.")
        else:
            st.warning("GA debug result")
            st.json(result)
        return

    if not measurement_id or not api_secret:
        return
    _send_page_view(measurement_id, api_secret, client_id)
