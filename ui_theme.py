import streamlit as st

def apply_theme():

    theme=st.session_state.get("theme","Dark")

    if theme=="Light":

        st.markdown("""
        <style>
        body {background:#ffffff;color:#000}
        </style>
        """,unsafe_allow_html=True)

    else:

        st.markdown("""
        <style>
        body {background:#0e1117;color:#fff}
        </style>
        """,unsafe_allow_html=True)
