import streamlit as st


MATCHER_URL = "https://vettrialfinder.com/matcher/"

st.set_page_config(
    page_title="Vet Trial Finder has moved",
    page_icon="🎯",
    layout="centered",
)

st.title("Vet Trial Finder has moved")
st.write("The cancer treatment trial matcher now lives on our main website.")
st.link_button(
    "Open the trial matcher",
    MATCHER_URL,
    type="primary",
    use_container_width=True,
)
