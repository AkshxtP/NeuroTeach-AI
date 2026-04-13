import streamlit as st


# =========================
# 🔐 INIT DEFAULT SETTINGS
# =========================
def init_settings():

    if "lang" not in st.session_state:
        st.session_state.lang = "English"

    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"


# =========================
# ⚙️ SETTINGS UI
# =========================
def settings_page():

    init_settings()

    st.header("⚙️ Learning Settings")

    # =========================
    # 🌐 LANGUAGE
    # =========================
    lang = st.selectbox(
        "Teaching Language",
        ["English", "Hinglish"],
        index=0 if st.session_state.lang == "English" else 1
    )

    # =========================
    # 🎨 THEME
    # =========================
    theme = st.radio(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    # =========================
    # 💾 SAVE BACK TO STATE
    # =========================
    st.session_state.lang = lang
    st.session_state.theme = theme

    # =========================
    # 🔔 UX FEEDBACK
    # =========================
    st.success(f"Language: {lang} | Theme: {theme}")