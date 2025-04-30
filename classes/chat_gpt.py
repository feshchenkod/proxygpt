import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance= super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._client = AsyncOpenAI(
            api_key= os.getenv("AI_TOKEN"),
        )

    @staticmethod
    def _load_prompt(prompt_name: str) -> str:
        prompt_path = os.path.join('resources', 'prompts', f'{prompt_name}.txt')
        with open(prompt_path) as file:
            prompt = file.read()
        return prompt

    async def text_request(self, prompt_name: str) -> str:
        response = await self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    'role': 'system',
                    'content': self._load_prompt(prompt_name),
                }
            ]
        )
        return response.choices[0].message.content