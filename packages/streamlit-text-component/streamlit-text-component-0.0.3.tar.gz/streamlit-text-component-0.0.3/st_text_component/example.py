import streamlit as st
import streamlit_float
from __init__ import text_component

st.set_page_config(layout="wide")

if "test" not in st.session_state:
    st.session_state["test"] = None

if "st_float_" not in st.session_state:
    st.session_state["st_float_"] = None

st.session_state["st_float_"] = streamlit_float.float_init()

st.session_state["st_float_"] 


with st.sidebar:
    st.markdown(
        """
            <style>
                section[data-testid="stSidebar"]{
                    background-color:#111;
                }
            </style>
        """, unsafe_allow_html=True
    )
data = [
    {"index":0, "label":"My Subscriptions"},
    {"index":1, "label":"Logout", "icon":"ri-logout-box-r-line"}
]

def on_change(key):
    selection = st.session_state[key]
    st.session_state["test"][0].write(f"Selection changed to {selection}")

with st.container():
    num_clicks = text_component(data=data, styles=None, on_change=on_change, key="foo")
    # streamlit_float.float_parent(css="top:1%; position:fixed; left:72%;")
    streamlit_float.float_parent(css="top:1%; position:absolute; right:0;")
    # st.write(num_clicks)
    st.session_state["test"] = st.columns(1)
