import fitz

def highlight_text_in_pdf(pdf_path, text_to_highlight):
    doc = fitz.open(pdf_path)

    search_text = " ".join(text_to_highlight.split())[:50]
    found = False

    for page in doc:
        text_instances = page.search_for(search_text)

        if text_instances:
            found = True
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=(0, 1, 0))
                highlight.set_opacity(0.4)
                highlight.update()

    if not found:
        for page in doc:
            blocks = page.get_text("blocks")
            if blocks:
                rect = fitz.Rect(blocks[0][:4])
                highlight = page.add_highlight_annot(rect)
                highlight.set_colors(stroke=(1, 1, 0))
                highlight.update()
                break

    output_path = f"highlighted_{abs(hash(search_text))}.pdf"
    doc.save(output_path)
    doc.close()

    return output_path