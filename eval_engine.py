from sentence_transformers import SentenceTransformer, util
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

def evaluate(student, correct):

    emb1 = model.encode(student, convert_to_tensor=True)
    emb2 = model.encode(correct, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item()
    percentage = (score + 1) / 2 * 100

    return round(percentage,2)
