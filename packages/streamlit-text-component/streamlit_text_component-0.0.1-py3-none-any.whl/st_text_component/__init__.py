import os
import streamlit.components.v1 as components

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

def text_component(data=None, key=None, default=None):
    
    component_value = _text_component(data=data, key=key, default=default)

    return component_value 
