import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# =========================
# 🔄 LOAD MODEL (CACHED)
# =========================
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    return tokenizer, model

tokenizer, model = load_model()


# =========================
# 🧠 CLEAN TEXT (REMOVE REPETITION)
# =========================
def clean_output(text):
    sentences = text.split(". ")
    seen = set()
    filtered = []

    for s in sentences:
        s = s.strip()
        if s and s not in seen:
            filtered.append(s)
            seen.add(s)

    return ". ".join(filtered)


# =========================
# 🧠 MAIN TEACH FUNCTION
# =========================
def teach_para(para, lang):

    # 🔥 LIMIT INPUT SIZE (important for stability)
    para = para[:800]

    # 🎯 ADAPTIVE DIFFICULTY
    difficulty = st.session_state.get("difficulty", "normal")

    if difficulty == "easy":
        style = "Explain VERY simply like teaching a beginner with easy examples."
    else:
        style = "Explain clearly with proper understanding and slight depth."

    # 🌍 LANGUAGE MODE
    if lang == "Hinglish":
        language_instruction = "Use Hinglish (Hindi words written in English script)."
    else:
        language_instruction = "Use simple English."

    # 🧠 STRONG PROMPT
    prompt = f"""
You are a highly skilled teacher.

Your job is to explain the concept in a structured, clean and non-repetitive way.

Instructions:
- {language_instruction}
- {style}
- Do NOT repeat sentences
- Do NOT copy text directly
- First give intuition
- Then explain key idea
- Keep it concise but clear
- Avoid unnecessary length

Concept:
{para}
"""

    try:
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        )

        outputs = model.generate(
            **inputs,
            max_length=220,
            temperature=0.6,   # 🔥 less randomness → less hallucination
            top_p=0.85,
            do_sample=True
        )

        result = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # 🧹 CLEAN REPETITION
        result = clean_output(result)

        # 🛡️ FALLBACK (VERY IMPORTANT FOR DEMO)
        if not result.strip() or len(result.split()) < 10:
            return f"Simple Explanation:\n\n{para[:200]}"

        return result

    except Exception as e:
        return f"Basic Explanation:\n\n{para[:200]}"