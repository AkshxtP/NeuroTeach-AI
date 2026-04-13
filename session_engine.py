import streamlit as st
import json
import os

SESSION_FILE = "session.json"


# =========================
# 🔐 INIT SESSION
# =========================
def init_session():
    if "progress" not in st.session_state:
        st.session_state.progress = 0


# =========================
# ➡️ NEXT PARA
# =========================
def next_para():
    if "progress" in st.session_state:
        st.session_state.progress += 1


# =========================
# 💾 SAVE SESSION
# =========================
def save_session():

    try:
        data = {
            "progress": st.session_state.get("progress", 0)
        }

        with open(SESSION_FILE, "w") as f:
            json.dump(data, f)

    except Exception as e:
        pass  # silent fail (important for demo safety)


# =========================
# 📂 LOAD SESSION
# =========================
def load_sessions():

    if not os.path.exists(SESSION_FILE):
        return

    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)

        # 🛡️ Safe assignment
        if "progress" in data:
            st.session_state.progress = data["progress"]

    except Exception as e:
        # corrupted file → reset safely
        st.session_state.progress = 0