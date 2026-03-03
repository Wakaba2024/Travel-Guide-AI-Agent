# rag/embeddings.py

import os
import time
from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)


def generate_embedding(text: str, retries: int = 3):
    """
    Generate embedding with retry + rate limit protection
    """

    for attempt in range(retries):
        try:
            response = client.embeddings.create(
                model="mistral-embed",
                inputs=text
            )
            time.sleep(0.5)  # throttle requests (IMPORTANT)
            return response.data[0].embedding

        except SDKError as e:
            if "429" in str(e):
                wait_time = 5
                print(f"Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("Embedding failed after retries.")