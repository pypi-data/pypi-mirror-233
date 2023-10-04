import os
import re
import json
import shutil
from fast_resume_parser.parser.pdf_parser import extract_text_from_pdf
from fast_resume_parser.parser.docx_parser import extract_text_from_docx
from fast_resume_parser.parser.image_parser import extract_text_from_image
from fast_resume_parser.parser.openai_processor import get_json_openai

class ResumeParser:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    async def parse_resume(self, file_path):
        try:
            # Process the uploaded file based on its extension
            if file_path.endswith('.pdf'):
                extracted_text = await extract_text_from_pdf(file_path)
            elif file_path.endswith(('.doc', '.docx')):
                extracted_text = await extract_text_from_docx(file_path)
            elif file_path.endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = await extract_text_from_image(file_path)
            else:
                raise ValueError("Unsupported file type")

            # Process extracted text using OpenAI
            extracted_text = re.sub(r'[^\w\s]', '', extracted_text)
            response = await get_json_openai(extracted_text, self.openai_api_key)
            resume_data = json.loads(response)

            return resume_data
        except Exception as e:
            return {"error": str(e)}
