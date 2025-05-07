from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
            InlineKeyboardButton('Есть еще вопрос', callback_data='/gpt'),
            InlineKeyboardButton('Закончить', callback_data='/start'),
        ]
    ])