import streamlit as st
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM

@st.cache_resource
def load_model():
    tokenizer=AutoTokenizer.from_pretrained("google/flan-t5-small")
    model=AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    return tokenizer,model

tokenizer,model=load_model()

def teach_para(para,lang):

    if lang=="Hinglish":
        prompt=f"""
Explain this academic concept in Hinglish using Hindi words written in English like a teacher in class.
Explain properly in detail not line by line.

Concept:
{para}
"""
    else:
        prompt=f"""
Explain this academic concept in simple English like a teacher teaching in class.
Explain properly in detail not line by line.

Concept:
{para}
"""

    inputs=tokenizer(prompt,return_tensors="pt",truncation=True)
    output=model.generate(**inputs,max_length=250)

    return tokenizer.decode(output[0],skip_special_tokens=True)
