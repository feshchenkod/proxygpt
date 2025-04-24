import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong")

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

if __name__ == '__main__':
    bot_token = os.getenv("TG_TOKEN")
    application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    ping_handler = CommandHandler('ping', ping)
    random_handler = CommandHandler('random', random)
    gpt_handler = CommandHandler('gpt', gpt)
    talk_handler = CommandHandler('talk', talk)
    quiz_handler = CommandHandler('quiz', quiz)
    application.add_handler(start_handler)
    application.add_handler(ping_handler)
    application.add_handler(random_handler)
    application.add_handler(gpt_handler)
    application.add_handler(talk_handler)
    application.add_handler(quiz_handler)

    application.run_polling()