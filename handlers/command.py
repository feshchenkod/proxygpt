import asyncio
import os
import aiofiles
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from classes import gpt_client

ASK_GPT, TALK, QUIZ = range(3)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == '/start':
        await start(update, context)
    elif query.data == '/random':
        await random(update, context)
    elif query.data == '/gpt':
        await gpt(update, context)
    else:
        await query.edit_message_caption(caption="Неизвестная команда.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_path = os.path.join('resources', 'messages', 'main.txt')
    photo_path = os.path.join('resources', 'images', 'main.jpg')
    async with aiofiles.open(message_path, 'r') as file:
        message = await file.read()
    async with aiofiles.open(photo_path, 'rb') as file:
        photo = await file.read()
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=message, photo=photo)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_path = os.path.join('resources', 'messages', 'random.txt')
    async with aiofiles.open(message_path, 'r') as file:
        message = await file.read()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    photo_path = os.path.join('resources', 'images', 'random.jpg')
    async with aiofiles.open(photo_path, 'rb') as file:
        photo = await file.read()
    keyboard = [
        [
            InlineKeyboardButton('Хочу еще факт', callback_data='/random'),
            InlineKeyboardButton('Закончить', callback_data='/start'),
        ]
    ]
    response = await gpt_client.text_request('random')
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=response, photo=photo, reply_markup=InlineKeyboardMarkup(keyboard))

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_path = os.path.join('resources', 'messages', 'gpt.txt')
    async with aiofiles.open(message_path, 'r') as file:
        message = await file.read()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ASK_GPT

async def gpt_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = os.path.join('resources', 'images', 'gpt.jpg')
    async with aiofiles.open(photo_path, 'rb') as file:
        photo = await file.read()
    user_text = update.message.text
    response = await gpt_client.text_request('gpt', user_text)
    keyboard = [
        [
            InlineKeyboardButton('Есть еще вопрос', callback_data='/gpt'),
            InlineKeyboardButton('Закончить', callback_data='/start'),
        ]
    ]
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=response, photo=photo, reply_markup=InlineKeyboardMarkup(keyboard))

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

handlers = [
    CallbackQueryHandler(button_handler),
    CommandHandler('start', start),
    CommandHandler('random', random),
    ConversationHandler(
        entry_points=[CommandHandler('gpt', gpt)],
        states={
            ASK_GPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_handle)],
        },
        fallbacks=[CommandHandler('start', start)],
    ),
    CommandHandler('talk', talk),
    CommandHandler('quiz', quiz),
]