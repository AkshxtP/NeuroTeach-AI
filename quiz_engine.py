import re


# =========================
# 🧠 CLEAN TEXT FUNCTION
# =========================
def normalize(text):
    text = text.lower()
    text = text.strip()
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    return text


# =========================
# 🎯 MAIN EVALUATION
# =========================
def evaluate_answer(selected, correct):

    if not selected or not correct:
        return False

    selected_clean = normalize(selected)
    correct_clean = normalize(correct)

    # ✅ Exact match
    if selected_clean == correct_clean:
        return True

    # ✅ Partial match (important for AI outputs)
    if correct_clean in selected_clean or selected_clean in correct_clean:
        return True

    return False