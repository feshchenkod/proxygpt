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

def quiz_init_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Программирование', callback_data='quiz_prog'),
            InlineKeyboardButton('Математика', callback_data='quiz_math'),
        ],
        [
            InlineKeyboardButton('Биология', callback_data='quiz_biology'),
            InlineKeyboardButton('Закончить', callback_data='cancel'),
        ]
    ])

def quiz_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Программирование', callback_data='quiz_prog'),
            InlineKeyboardButton('Математика', callback_data='quiz_math'),
        ],
        [
            InlineKeyboardButton('Биология', callback_data='quiz_biology'),
            InlineKeyboardButton('Повторить тему', callback_data='quiz_more'),
        ],
        [
            InlineKeyboardButton('Перезапуск', callback_data='quiz_restart'),
            InlineKeyboardButton('Закончить', callback_data='cancel'),
        ]
    ])

def quiz_answer_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Перезапуск', callback_data='quiz_restart'),
            InlineKeyboardButton('Закончить', callback_data='cancel'),
        ]
    ])