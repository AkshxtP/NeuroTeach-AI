import streamlit as st

def settings_page():

    st.header("Learning Settings")

    st.session_state.lang=st.selectbox(
    "Teaching Language",
    ["English","Hinglish"]
    )

    st.session_state.theme=st.radio(
    "Theme",
    ["Dark","Light"]
    )
