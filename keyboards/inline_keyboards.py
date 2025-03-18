from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data='button1')],
        [InlineKeyboardButton("Кнопка 2", callback_data='button2')]
    ]
    return InlineKeyboardMarkup(keyboard)