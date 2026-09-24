import streamlit as st
import streamlit.components.v1 as components


MATCHER_URL = "https://vettrialfinder.com/matcher/"

st.set_page_config(
    page_title="Vet Trial Finder has moved",
    page_icon="🎯",
    layout="centered",
)

components.html(
    f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <script>
          window.top.location.replace({MATCHER_URL!r});
        </script>
      </head>
      <body></body>
    </html>
    """,
    height=0,
)

st.title("Vet Trial Finder has moved")
st.write("The cancer treatment trial matcher now lives on our main website.")
st.markdown(
    f'<a href="{MATCHER_URL}" target="_top" '
    'style="display:inline-block;padding:.75rem 1rem;border-radius:.5rem;'
    'background:#175b8c;color:white;text-decoration:none;font-weight:700">'
    'Open the trial matcher</a>',
    unsafe_allow_html=True,
)
