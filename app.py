import streamlit as st

st.set_page_config(page_title="Widget test", page_icon="🐾")
st.title("Widget test")
st.write("Text renders.")
st.selectbox("Species", ["Dog", "Cat"])
st.write("Selectbox rendered.")
