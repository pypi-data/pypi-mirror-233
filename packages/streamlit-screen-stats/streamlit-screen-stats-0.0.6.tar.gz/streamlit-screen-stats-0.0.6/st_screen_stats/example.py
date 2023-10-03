import streamlit as st
from __init__ import st_screen_data
# from st_screen_stats import st_screen_data


st.subheader("Component with constant args")

num_clicks = st_screen_data()
st.write(num_clicks)


if "count_" not in st.session_state:
    st.session_state["count_"] = 0

st.session_state["count_"] += 1
st.write(st.session_state["count_"])


