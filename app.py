import streamlit as st
from pages import home, what_is_causality

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
