import streamlit as st
from pdf_engine import extract_pages
from teach_engine import teach_para
from ui_engine import typing_effect
from session_engine import init_session,next_para,save_session,load_sessions
from settings_engine import settings_page
from streamlit_pdf_viewer import pdf_viewer
from ui_theme import apply_theme

st.set_page_config(layout="wide")

apply_theme()
init_session()

mode=st.sidebar.selectbox("",["Learning","Settings"])

load_sessions()

st.sidebar.markdown("## NeuroTeach")

if mode=="Settings":
    settings_page()
    st.stop()

pdf=st.file_uploader("Upload PDF",type=["pdf"])

if pdf:

    if "paras" not in st.session_state:
        st.session_state.paras=extract_pages(pdf)
        st.session_state.progress=0
        st.session_state.started=False

    col1,col2=st.columns([2,1])

    with col1:
        pdf_viewer(pdf.getvalue(),width=650,height=750)

    with col2:

        st.markdown("### Teaching Panel")

        if not st.session_state.started:
            btn=st.button("Begin Teaching")
            if btn:
                st.session_state.started=True
        else:
            btn=st.button("Teach Next")

        if btn:

            if st.session_state.progress < len(st.session_state.paras):

                para=st.session_state.paras[
                st.session_state.progress
                ]

                explanation=teach_para(
                para,
                st.session_state.get("lang","English")
                )

                st.markdown("#### Explanation")
                typing_effect(explanation)

                next_para()

save_session()
