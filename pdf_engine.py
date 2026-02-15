import fitz

def extract_pages(uploaded_file):

    doc=fitz.open(stream=uploaded_file.read(),filetype="pdf")
    paras=[]

    for page in doc:

        blocks=page.get_text("blocks")

        for b in blocks:
            text=b[4].strip()

            if len(text.split())<40:
                continue

            paras.append(text)

    return paras
