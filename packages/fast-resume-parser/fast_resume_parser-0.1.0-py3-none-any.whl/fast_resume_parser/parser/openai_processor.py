import openai
import os

# Set OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_API_KEY

async def get_json_openai(extracted_text):
    input_text = f"{extracted_text} ... write your OpenAI prompt here."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        max_tokens=500
    )
    return response.choices[0].text.strip()
