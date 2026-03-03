import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in .env")

client = Mistral(api_key=MISTRAL_API_KEY)


def generate_response(prompt: str) -> str:
    """
    Sends prompt to Mistral chat model and returns response text.
    """

    response = client.chat.complete(
        model="mistral-small-latest",  # You can change to mistral-large if needed
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content