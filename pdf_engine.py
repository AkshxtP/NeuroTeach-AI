import fitz

def extract_pages(uploaded_file):

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    paras = []

    for page in doc:

        blocks = page.get_text("blocks")

        for b in blocks:
            text = b[4].strip()

            # ❌ skip headings / small lines
            if len(text.split()) < 25:
                continue

            # ✅ split big para into smaller chunks (2–3 lines)
            sentences = text.split(". ")

            temp = []
            for s in sentences:
                temp.append(s)

                if len(temp) == 2:
                    paras.append(". ".join(temp))
                    temp = []

            if temp:
                paras.append(". ".join(temp))

    return paras