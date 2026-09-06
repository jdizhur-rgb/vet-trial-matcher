import json
import streamlit as st


def install_analytics():
    """Install GA4 only when GA_MEASUREMENT_ID is configured in Streamlit secrets.

    Privacy choices:
    - no names, email, form values, diagnosis text, age, weight, or other pet data are sent;
    - Google Signals/ad personalization are disabled;
    - the owner's browser can opt out persistently with ?analytics_off=1;
    - ?analytics_on=1 reverses the local opt-out.
    """
    measurement_id = str(st.secrets.get("GA_MEASUREMENT_ID", "")).strip()
    if not measurement_id:
        return

    mid = json.dumps(measurement_id)
    st.html(
        f"""
<script>
(() => {{
  try {{
    const p = window.parent;
    const u = new URL(p.location.href);
    if (u.searchParams.get('analytics_off') === '1') {{
      p.localStorage.setItem('vet_trial_analytics_off', '1');
      u.searchParams.delete('analytics_off');
      p.history.replaceState({{}}, '', u.toString());
    }}
    if (u.searchParams.get('analytics_on') === '1') {{
      p.localStorage.removeItem('vet_trial_analytics_off');
      u.searchParams.delete('analytics_on');
      p.history.replaceState({{}}, '', u.toString());
    }}
    if (p.localStorage.getItem('vet_trial_analytics_off') === '1') return;

    const id = {mid};
    if (!p.document.getElementById('vet-trial-ga4')) {{
      const s = p.document.createElement('script');
      s.id = 'vet-trial-ga4';
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
      p.document.head.appendChild(s);
    }}
    p.dataLayer = p.dataLayer || [];
    p.gtag = p.gtag || function(){{p.dataLayer.push(arguments);}};
    p.gtag('js', new Date());
    p.gtag('consent', 'default', {{
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'analytics_storage': 'granted'
    }});
    p.gtag('config', id, {{
      'send_page_view': true,
      'allow_google_signals': false,
      'allow_ad_personalization_signals': false,
      'page_location': p.location.origin + p.location.pathname,
      'page_title': p.document.title || 'Vet Cancer Treatment Finder'
    }});
  }} catch (e) {{
    // Analytics must never interfere with the matcher.
  }}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )
