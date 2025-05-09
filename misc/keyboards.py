import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .utils import load_prompts_list, read_text

def random_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Хочу еще факт', callback_data='/random'),
            InlineKeyboardButton('Закончить', callback_data='/start'),
        ]
    ])

def gpt_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Есть еще вопрос', callback_data='gpt_restart'),
            InlineKeyboardButton('Закончить', callback_data='cancel'),
        ]
    ])

async def talk_keyboard():
    files_list = load_prompts_list('talk_')
    buttons = []
    for celebrity in files_list:
        name = await read_text('prompts', celebrity)
        button_name = name.split(', ')[0][5:]
        buttons.append([InlineKeyboardButton(button_name, callback_data=f'{celebrity.split('.')[0]}')])

    return InlineKeyboardMarkup(buttons)

def talk_choose_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Сменить собеседника', callback_data='talk_restart'),
            InlineKeyboardButton('Закончить', callback_data='cancel'),
        ]
    ])