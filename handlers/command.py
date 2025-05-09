from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from telegram.constants import ChatAction
from classes import gpt_client
from misc import read_text, read_image, random_keyboard, gpt_keyboard, talk_keyboard, talk_choose_keyboard

ASK_GPT, TALK_CHOOSE, TALK_ASK, QUIZ = range(4)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == '/start':
        await start(update, context)
    elif query.data == '/random':
        await random(update, context)
    elif query.data == '/gpt':
        await gpt(update, context)
    elif query.data == '/talk':
        await talk(update, context)
    else:
        await query.edit_message_caption(caption="Неизвестная команда.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)
    return ConversationHandler.END

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
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=response, photo=photo, reply_markup=random_keyboard())

async def random_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await random(update, context)
    return ConversationHandler.END

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await read_text('messages', 'gpt.txt')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ASK_GPT

async def gpt_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await read_image('gpt.jpg')
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    response = await gpt_client.text_request('gpt', user_text)
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=response, photo=photo, reply_markup=gpt_keyboard())

async def gpt_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await gpt(update, context)
    return ConversationHandler.END

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["messages"] = []
    message = await read_text('messages', 'talk.txt')
    photo = await read_image('talk.jpg')
    keyboard = await talk_keyboard()
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=message, photo=photo, reply_markup=keyboard)
    return TALK_CHOOSE

async def talk_choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    personality = query.data
    context.user_data["personality"] = personality
    prompt = await read_text('prompts', f'{personality}.txt')
    context.user_data["messages"] = [{"role": "system", "content": prompt}]
    name = prompt.split(', ')[0][5:]
    photo = await read_image(f'{personality}.jpg')
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=f"Вы выбрали: {name}. Напишите ваш вопрос:", photo=photo, reply_markup=talk_choose_keyboard())
    return TALK_ASK

async def talk_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    personality = context.user_data.get("personality")
    photo = await read_image(f'{personality}.jpg')
    user_text = update.message.text
    context.user_data["messages"].append({"role": "user", "content": user_text})
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    response = await gpt_client.dialog(context.user_data["messages"])
    context.user_data["messages"].append({"role": "assistant", "content": response})
    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=response, photo=photo, reply_markup=talk_choose_keyboard())
    return TALK_ASK

async def talk_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await talk(update, context)
    return ConversationHandler.END

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing here, try later...")

fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('start', cancel),
            CommandHandler('random', random_restart),
            CommandHandler('gpt', gpt_restart),
            CommandHandler('talk', talk_restart),
            CommandHandler('quiz', quiz),
        ]

handlers = [
    CommandHandler('start', start),
    CommandHandler('random', random),
    ConversationHandler(
        entry_points=[CommandHandler('gpt', gpt), CommandHandler('gpt', gpt_restart)],
        states={
            ASK_GPT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_ask),
                CallbackQueryHandler(gpt, pattern="^gpt_restart$"),
                CallbackQueryHandler(cancel, pattern="^cancel"),
            ],
        },
        fallbacks=fallbacks,
        allow_reentry=True,
    ),
    ConversationHandler(
        entry_points=[CommandHandler("talk", talk), CommandHandler("talk", talk_restart)],
        states={
            TALK_CHOOSE: [CallbackQueryHandler(talk_choose)],
            TALK_ASK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, talk_ask),
                CallbackQueryHandler(talk, pattern="^talk_restart$"),
                CallbackQueryHandler(cancel, pattern="^cancel"),
            ],
        },
        fallbacks=fallbacks,
        allow_reentry=True,
    ),
    CommandHandler('quiz', quiz),
    CallbackQueryHandler(button_handler),
]