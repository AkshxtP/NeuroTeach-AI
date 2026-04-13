import time
import streamlit as st


# =========================
# 🎯 SMART TYPING EFFECT
# =========================
def typing_effect(text, speed=0.015):

    placeholder = st.empty()

    # 🛡️ Safety check
    if not text:
        placeholder.markdown("⚠️ No content to display")
        return

    words = text.split()

    # 🚀 For long text → skip animation (performance boost)
    if len(words) > 120:
        placeholder.markdown(text)
        return

    full_text = ""

    for i, word in enumerate(words):

        full_text += word + " "

        # 🔥 Update every 2 words (reduces lag)
        if i % 2 == 0:
            placeholder.markdown(full_text)
            time.sleep(speed)

    # ✅ Final full render (ensures complete text)
    placeholder.markdown(full_text)