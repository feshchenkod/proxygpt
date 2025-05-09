import os
import aiofiles

async def read_text(resource_type: str, resource_name: str):
    path = os.path.join('resources', resource_type, resource_name)
    async with aiofiles.open(path, 'r') as file:
        message = await file.read()
    return message

async def read_image(resource_name: str):
    path = os.path.join('resources', 'images', resource_name)
    async with aiofiles.open(path, 'rb') as file:
        image = await file.read()
    return image

def load_prompts_list(prompt_starts):
    prompts_path = os.path.join('resources', 'prompts')
    prompts_list = [file for file in os.listdir(prompts_path) if file.startswith(prompt_starts)]
    return prompts_list