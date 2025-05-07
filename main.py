import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, Defaults
from telegram.constants import ParseMode
from handlers import handlers

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    bot_token = os.getenv("TG_TOKEN")
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN)
    application = ApplicationBuilder().token(bot_token).defaults(defaults).build()
    application.add_handlers(handlers)

    application.run_polling()