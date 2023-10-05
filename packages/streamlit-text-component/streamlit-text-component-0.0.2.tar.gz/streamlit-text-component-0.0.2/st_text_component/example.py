import streamlit as st
from __init__ import text_component



with st.sidebar:
    data = [
        {"index":0, "label":"My Subscriptions"},
        {"index":1, "label":"Logout", "icon":"ri-logout-box-r-line"}
    ]

    num_clicks = text_component(data=data, styles=None, key="foo")
    st.write(num_clicks)
