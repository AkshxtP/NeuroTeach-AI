import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource
def load_teacher():
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    return tokenizer, model

tokenizer, model = load_teacher()


def teach_para(text, lang="English"):

    if lang == "Hinglish":
        prompt = f"""
        Explain the following concept in very simple Hinglish like a real teacher teaching in class.
        Also give one real life example.

        Concept:
        {text}

        Format:
        Explanation:
        Example:
        """
    else:
        prompt = f"""
        Explain the following concept in very simple English like a real teacher teaching in class.
        Also give one real life example.

        Concept:
        {text}

        Format:
        Explanation:
        Example:
        """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=300)

    output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "Example:" in output:
        parts = output.split("Example:")
        explanation = parts[0].replace("Explanation:", "").strip()
        example = parts[1].strip()
    else:
        explanation = output
        example = "Real life example not generated."

    return explanation, example
