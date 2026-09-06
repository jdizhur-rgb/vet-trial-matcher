import json
import streamlit as st
import streamlit.components.v1 as components


# Public GA4 measurement ID. A Streamlit secret with the same name can override it.
_DEFAULT_MEASUREMENT_ID = "G-TQOYHMOOM5"


def install_analytics():
    """Install GA4 in a hidden Streamlit component.

    The first version tried to inject JavaScript with st.html(), which can be
    sandboxed/ignored for this use. components.html() executes the script in a
    dedicated iframe, which is sufficient to send GA4 page_view events.

    Privacy choices:
    - no names, email, form values, diagnosis text, age, weight, or other pet data are sent;
    - Google Signals/ad personalization are disabled;
    - the owner's browser can opt out persistently with ?analytics_off=1;
    - ?analytics_on=1 reverses the local opt-out.
    """
    measurement_id = str(st.secrets.get("GA_MEASUREMENT_ID", _DEFAULT_MEASUREMENT_ID)).strip()
    if not measurement_id:
        return

    mid = json.dumps(measurement_id)
    components.html(
        f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<script>
(() => {{
  try {{
    const id = {mid};
    const parentUrl = (() => {{
      try {{ return new URL(window.parent.location.href); }}
      catch (_) {{ return new URL(document.referrer || 'https://vet-cancer-trial-finder.streamlit.app/'); }}
    }})();

    let storage;
    try {{ storage = window.parent.localStorage; }}
    catch (_) {{ storage = window.localStorage; }}

    if (parentUrl.searchParams.get('analytics_off') === '1') {{
      try {{ storage.setItem('vet_trial_analytics_off', '1'); }} catch (_) {{}}
    }}
    if (parentUrl.searchParams.get('analytics_on') === '1') {{
      try {{ storage.removeItem('vet_trial_analytics_off'); }} catch (_) {{}}
    }}
    try {{
      if (storage.getItem('vet_trial_analytics_off') === '1') return;
    }} catch (_) {{}}

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){{ window.dataLayer.push(arguments); }};
    window.gtag('js', new Date());
    window.gtag('consent', 'default', {{
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'analytics_storage': 'granted'
    }});
    window.gtag('config', id, {{
      'send_page_view': true,
      'allow_google_signals': false,
      'allow_ad_personalization_signals': false,
      'page_location': parentUrl.origin + parentUrl.pathname,
      'page_title': 'Vet Cancer Treatment Finder'
    }});

    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
  }} catch (_) {{}}
}})();
</script>
</head>
<body></body>
</html>
""",
        height=0,
        width=0,
    )
