import streamlit as st
import time

from pdf_highlighter import highlight_text_in_pdf
from pdf_engine import extract_pages
from teach_engine import teach_para
from ui_engine import typing_effect
from session_engine import init_session, next_para, save_session, load_sessions
from settings_engine import settings_page
from streamlit_pdf_viewer import pdf_viewer
from ui_theme import apply_theme
from tts_engine import speak_text
from qg_engine import generate_mcq
from quiz_engine import evaluate_answer

st.set_page_config(layout="wide")

apply_theme()
init_session()
load_sessions()

# =========================
# 🔐 SESSION INIT
# =========================
if "score" not in st.session_state:
    st.session_state.score = 0

if "questions_attempted" not in st.session_state:
    st.session_state.questions_attempted = 0

if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = None

if "last_audio_file" not in st.session_state:
    st.session_state.last_audio_file = None

if "highlighted_pdf" not in st.session_state:
    st.session_state.highlighted_pdf = None

if "last_para" not in st.session_state:
    st.session_state.last_para = None

if "current_mcq" not in st.session_state:
    st.session_state.current_mcq = None

if "last_quiz_para" not in st.session_state:
    st.session_state.last_quiz_para = None

# =========================
# 🎛 SIDEBAR
# =========================
mode = st.sidebar.selectbox("", ["Learning", "Settings"])
st.sidebar.markdown("## NeuroTeach")

if mode == "Settings":
    settings_page()
    st.stop()

# =========================
# 📄 PDF UPLOAD
# =========================
pdf = st.file_uploader("Upload PDF", type=["pdf"])

if pdf:

    with open("temp.pdf", "wb") as f:
        f.write(pdf.getbuffer())

    if "paras" not in st.session_state:
        st.session_state.paras = extract_pages(pdf)
        st.session_state.progress = 0
        st.session_state.started = False

    if st.session_state.progress >= len(st.session_state.paras):
        st.session_state.progress = 0

    col1, col2 = st.columns([2, 1])

    # =========================
    # 📄 PDF VIEW
    # =========================
    with col1:
        if st.session_state.highlighted_pdf:
            try:
                with open(st.session_state.highlighted_pdf.split("?")[0], "rb") as f:
                    pdf_viewer(f.read(), width=650, height=750)
            except:
                pdf_viewer(pdf.getvalue(), width=650, height=750)
        else:
            pdf_viewer(pdf.getvalue(), width=650, height=750)

    # =========================
    # 🧠 TEACH PANEL
    # =========================
    with col2:

        st.markdown("### Teaching Panel")

        # 📊 Progress Bar
        total = len(st.session_state.paras)
        progress_val = st.session_state.progress / total
        st.progress(progress_val)
        st.caption(f"Progress: {st.session_state.progress} / {total}")

        # 🐞 DEBUG (remove later if needed)
        st.write("DEBUG → Current Index:", st.session_state.progress)

        if not st.session_state.started:
            if st.button("Begin Teaching"):
                st.session_state.started = True
        else:
            if st.button("Teach Next"):

                if st.session_state.progress < total:

                    para = st.session_state.paras[st.session_state.progress]

                    # =========================
                    # 🧠 EXPLANATION (NO REPEAT)
                    # =========================
                    if st.session_state.last_para != para:

                        explanation = teach_para(
                            para,
                            st.session_state.get("lang", "English")
                        )

                        st.session_state.current_para = para
                        st.session_state.current_explanation = explanation
                        st.session_state.last_para = para

                        # =========================
                        # 🔥 HIGHLIGHT FIX
                        # =========================
                        try:
                            st.session_state.highlighted_pdf = None
                            highlighted_pdf = highlight_text_in_pdf("temp.pdf", para)
                            st.session_state.highlighted_pdf = highlighted_pdf + f"?v={time.time()}"
                        except:
                            pass

                        # =========================
                        # 🔊 AUDIO
                        # =========================
                        try:
                            lang_code = "en"
                            if st.session_state.get("lang") == "Hinglish":
                                lang_code = "hi"

                            if st.session_state.last_explanation != explanation:
                                audio_file = speak_text(explanation, lang=lang_code)
                                st.session_state.last_explanation = explanation
                                st.session_state.last_audio_file = audio_file
                            else:
                                audio_file = st.session_state.last_audio_file

                            st.session_state.audio = audio_file
                        except:
                            st.session_state.audio = None

                    next_para()
                    st.rerun()

        # =========================
        # 📘 SHOW EXPLANATION
        # =========================
        if "current_explanation" in st.session_state:

            st.markdown("#### Explanation")
            typing_effect(st.session_state.current_explanation)

            if st.session_state.get("audio"):
                st.audio(st.session_state.audio)

        # =========================
        # 🧠 QUIZ SYSTEM (NO REPEAT)
        # =========================
        if "current_para" in st.session_state:

            if st.session_state.progress % 3 == 0:

                st.markdown("## 🧠 Quick Check")

                para = st.session_state.current_para

                if st.session_state.last_quiz_para != para:
                    mcq = generate_mcq(para)
                    st.session_state.current_mcq = mcq
                    st.session_state.last_quiz_para = para
                else:
                    mcq = st.session_state.current_mcq

                selected = st.radio(
                    mcq["question"],
                    mcq["options"],
                    key=f"quiz_{st.session_state.progress}"
                )

                if st.button("Submit Answer"):

                    st.session_state.questions_attempted += 1

                    if evaluate_answer(selected, mcq["answer"]):
                        st.success("✅ Correct!")
                        st.session_state.score += 1
                    else:
                        st.error("❌ Incorrect")
                        st.info(f"Correct Answer: {mcq['answer']}")

                    accuracy = st.session_state.score / max(
                        1, st.session_state.questions_attempted
                    )

                    if accuracy < 0.5:
                        st.session_state["difficulty"] = "easy"
                        st.warning("Switching to simpler explanations")
                    else:
                        st.session_state["difficulty"] = "normal"
                        st.success("Good understanding")

save_session()