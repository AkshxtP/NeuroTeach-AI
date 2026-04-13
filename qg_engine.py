import random

def generate_mcq(text):

    main = text.split(".")[0]

    question = f"What does this explain: '{main[:50]}...' ?"

    correct = main

    wrong = [
        "A completely different topic",
        "Something unrelated",
        "Not discussed here"
    ]

    options = wrong + [correct]
    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "answer": correct
    }