import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from handlers import handlers

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    bot_token = os.getenv("TG_TOKEN")
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handlers(handlers)

    application.run_polling()