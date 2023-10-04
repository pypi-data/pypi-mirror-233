import docx2txt

async def extract_text_from_docx(docx_path):
    text = docx2txt.process(docx_path)
    return text
