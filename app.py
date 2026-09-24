import streamlit as st
import streamlit.components.v1 as components


MATCHER_URL = "https://vettrialfinder.com/matcher/"

st.set_page_config(
    page_title="Vet Trial Finder",
    page_icon="🎯",
    layout="centered",
)

st.markdown(
    f'<meta http-equiv="refresh" content="0; url={MATCHER_URL}">',
    unsafe_allow_html=True,
)

components.html(
    f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="0; url={MATCHER_URL}">
        <script>
          window.parent.location.replace({MATCHER_URL!r});
        </script>
      </head>
      <body></body>
    </html>
    """,
    height=0,
)

st.title("Vet Trial Finder has moved")
st.write("The cancer treatment trial matcher now lives on our main website.")
st.link_button("Open the trial matcher", MATCHER_URL, type="primary")
