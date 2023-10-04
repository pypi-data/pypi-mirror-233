import os

import streamlit as st  
import pandas as pd

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True
if not _RELEASE:
    _save_scenario_modal = components.declare_component(
        "save_scenario_modal",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _table_update_create_scenario = components.declare_component("save_scenario_modal", path=build_dir)


def save_scenario_modal(key=None,shape=None,is_open=None):
    return _save_scenario_modal(key=key,shape=shape,is_open=is_open)

def are_dicts_equal(dict1, dict2):
    # Check if both dictionaries have the same keys
    if type(dict2) != dict:
        return False
    if set(dict1.keys()) != set(dict2.keys()):
        return False
    
    # Check if the values for each key are equal
    for key in dict1:
        if dict1[key] != dict2[key]:
            return False
    return True

# Test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run custom_dataframe/__init__.py`
if not _RELEASE:
    shape = {
        "width": "100%",
        "height": "300px"
    }
    is_open="true"
    df = save_scenario_modal(shape= shape,is_open=is_open)