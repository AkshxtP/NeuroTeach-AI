import streamlit as st


def apply_theme():

    theme = st.session_state.get("theme", "Dark")

    if theme == "Light":

        st.markdown("""
        <style>

        /* MAIN BACKGROUND */
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #f1f5f9;
        }

        /* TEXT */
        h1, h2, h3, h4, h5, h6, p, span {
            color: #000000 !important;
        }

        /* BUTTONS */
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
        }

        /* RADIO + SELECT */
        .stSelectbox, .stRadio {
            color: black;
        }

        </style>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <style>

        /* MAIN BACKGROUND */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #020617;
        }

        /* TEXT */
        h1, h2, h3, h4, h5, h6, p, span {
            color: #ffffff !important;
        }

        /* BUTTONS */
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
        }

        </style>
        """, unsafe_allow_html=True)