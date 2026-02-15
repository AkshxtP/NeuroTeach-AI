import streamlit as st
import json
import os

def init_session():
    if "progress" not in st.session_state:
        st.session_state.progress=0

def next_para():
    st.session_state.progress+=1

def save_session():
    data={"progress":st.session_state.progress}
    with open("session.json","w") as f:
        json.dump(data,f)

def load_sessions():
    if os.path.exists("session.json"):
        with open("session.json","r") as f:
            data=json.load(f)
            st.session_state.progress=data["progress"]
