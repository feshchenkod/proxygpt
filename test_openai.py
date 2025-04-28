from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("AI_TOKEN")

if __name__ == '__main__':
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions="You are a coding assistant that talks like a pirate.",
        input="How do I check if a Python object is an instance of a class?",
    )

    print(response.output_text)