import streamlit as st
from pages import (
    home,
    what_is_causality,
    selection_bias,
    confounders,
    randomized_experiments,
    difference_in_differences,
)

# Configure page
st.set_page_config(
    page_title="Casual Causality",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


# Navigation
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()


# Render current page
if st.session_state.current_page == "home":
    home.render(navigate_to)
elif st.session_state.current_page == "what_is_causality":
    what_is_causality.render(navigate_to)
elif st.session_state.current_page == "selection_bias":
    selection_bias.render(navigate_to)
elif st.session_state.current_page == "confounders":
    confounders.render(navigate_to)
elif st.session_state.current_page == "randomized_experiments":
    randomized_experiments.render(navigate_to)
elif st.session_state.current_page == "difference_in_differences":
    difference_in_differences.render(navigate_to)
