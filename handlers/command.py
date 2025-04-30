import os
import aiofiles
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from classes import gpt_client

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == '/start':
        await start(update, context)
    elif query.data == '/random':
        await random(update, context)
    else:
        await query.edit_message_caption(caption="Неизвестная команда.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_path = os.path.join('resources', 'messages', 'main.txt')
    photo_path = os.path.join('resources', 'images', 'main.jpg')
    async with aiofiles.open(text_path, 'r') as file:
        text = await file.read()
    async with aiofiles.open(photo_path, 'rb') as file:
        photo = await file.read()
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=text, photo=photo)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = os.path.join('resources', 'images', 'random.jpg')
    async with aiofiles.open(photo_path, 'rb') as file:
        photo = await file.read()
    keyboard = [
        [
            InlineKeyboardButton('Хочу еще факт', callback_data='/random'),
            InlineKeyboardButton('Закончить', callback_data='/start'),
        ]
    ]
    text = await gpt_client.text_request('random')
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=text, photo=photo, reply_markup=InlineKeyboardMarkup(keyboard))

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

handlers = [
    CallbackQueryHandler(button_handler),
    CommandHandler('start', start),
    CommandHandler('random', random),
    CommandHandler('gpt', gpt),
    CommandHandler('talk', talk),
    CommandHandler('quiz', quiz),
]