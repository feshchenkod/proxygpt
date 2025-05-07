import asyncio
import os
import aiofiles
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from telegram.constants import ChatAction
from classes import gpt_client
from misc import read_text, read_image

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
    message = await read_text('messages', 'main.txt')
    photo = await read_image('main.jpg')
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=message, photo=photo)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await read_text('messages', 'random.txt')
    photo = await read_image('random.jpg')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    response = await gpt_client.text_request('random')
    keyboard = [
        [
            InlineKeyboardButton('Хочу еще факт', callback_data='/random'),
            InlineKeyboardButton('Закончить', callback_data='/start'),
        ]
    ]
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=response, photo=photo, reply_markup=InlineKeyboardMarkup(keyboard))

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await read_text('messages', 'gpt.txt')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ASK_GPT

async def gpt_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await read_image('gpt.jpg')
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
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
            ASK_GPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_input)],
        },
        fallbacks=[CommandHandler('start', start)],
    ),
    CommandHandler('talk', talk),
    CommandHandler('quiz', quiz),
]