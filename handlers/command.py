from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

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

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

handlers = [
    CommandHandler('start', start),
    CommandHandler('ping', ping),
    CommandHandler('random', random),
    CommandHandler('gpt', gpt),
    CommandHandler('talk', talk),
    CommandHandler('quiz', quiz),
    MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
    CommandHandler('caps', caps),
    MessageHandler(filters.COMMAND, unknown),
]