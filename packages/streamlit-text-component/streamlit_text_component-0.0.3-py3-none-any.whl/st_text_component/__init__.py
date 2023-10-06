import os
import streamlit as st
import streamlit.components.v1 as components
from streamlit_callback import register_callback

_RELEASE = True 

if not _RELEASE:
    _text_component = components.declare_component(
        "text_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _text_component = components.declare_component("text_component", path=build_dir)

def text_component(data=None, key=None, styles=None, on_change=None, default=None):

    if on_change is not None:
        if key is None:
            st.error("You must pass a key if you want to use the on_change callback for the option menu")
        else:    
            register_callback(key, on_change, key)
    
    component_value = _text_component(data=data, styles=styles, key=key, default=default)

    return component_value 
