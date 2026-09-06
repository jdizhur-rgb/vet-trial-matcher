import streamlit as st
from visit_counter import read_stats

st.title("📊 Visit stats")
stats = read_stats()
cols = st.columns(4)
cols[0].metric("All visits", stats["total"])
cols[1].metric("Today", stats["today"])
cols[2].metric("This week", stats["week"])
cols[3].metric("This month", stats["month"])
st.caption("Counts Streamlit sessions, not unique people. Refreshes inside the same live session are not counted again. No pet, search, IP, email, or browser data is sent to the counter service. Periods use Eastern Time.")
