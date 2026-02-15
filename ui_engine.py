import time
import streamlit as st

def typing_effect(text):

    placeholder=st.empty()
    full=""

    for word in text.split():
        full+=word+" "
        placeholder.markdown(full)
        time.sleep(0.02)
