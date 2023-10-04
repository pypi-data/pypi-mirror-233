import os
import openai

async def get_json_openai(extracted_text, openai_api_key):

    openai.api_key = openai_api_key

    input_text = f"{extracted_text} ... write your OpenAI prompt here."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_text,
        max_tokens=500
    )
    return response.choices[0].text.strip()
