from PyPDF2 import PdfReader

async def extract_text_from_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text
