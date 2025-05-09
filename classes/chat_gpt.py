import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from misc import read_text

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
    async def _load_prompt(prompt_name: str) -> str:
        return await read_text('prompts', f'{prompt_name}.txt')

    async def text_request(self, prompt_name: str, user_prompt=None) -> str:
        if user_prompt is None:
            response = await self._client.responses.create(
                model="gpt-3.5-turbo",
                input=await self._load_prompt(prompt_name),
            )
        else:
            response = await self._client.responses.create(
                model="gpt-3.5-turbo",
                instructions=await self._load_prompt(prompt_name),
                input=user_prompt,
            )
        return response.output_text

    async def dialog(self, prompt_name: str, user_prompt=None) -> str:
        if user_prompt is None:
            response = await self._client.responses.create(
                model="gpt-3.5-turbo",
                input=self._load_prompt(prompt_name),
            )
        else:
            response = await self._client.responses.create(
                model="gpt-3.5-turbo",
                instructions=self._load_prompt(prompt_name),
                input=user_prompt,
            )
        return response.output_text