import openai
import os


def get_response(prompt, model="gpt-3.5-turbo-16k"):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    return openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
