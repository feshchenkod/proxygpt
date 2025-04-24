import asyncio
import telegram
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    bot_token = os.getenv("TG_TOKEN")
    bot = telegram.Bot(bot_token)
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())