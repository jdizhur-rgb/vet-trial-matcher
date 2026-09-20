import streamlit as st
import streamlit.components.v1 as components


DESTINATION = "https://vettrialfinder.com/matcher/"

st.set_page_config(
    page_title="Vet Trial Finder has moved",
    page_icon="🐾",
    layout="centered",
)

# Use both a document-level refresh and a top-window redirect. Browser security
# settings vary for embedded components, so the visible link remains as a
# reliable fallback.
st.markdown(
    f'<meta http-equiv="refresh" content="0; url={DESTINATION}">',
    unsafe_allow_html=True,
)
components.html(
    f"""
    <script>
      try {{
        window.top.location.replace({DESTINATION!r});
      }} catch (error) {{
        window.open({DESTINATION!r}, "_top");
      }}
    </script>
    """,
    height=0,
)

st.title("Vet Trial Finder has moved")
st.write("The current trial finder is now available on VetTrialFinder.com.")
st.link_button("Open the current trial finder", DESTINATION, type="primary")
