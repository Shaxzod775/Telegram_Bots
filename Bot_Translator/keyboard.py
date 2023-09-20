from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES


def btn_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []

    for lang in LANGUAGES.values():
        buttons.append(lang)

    markup.add(*buttons)
    return markup

def btn_markup1():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton('Да')
    btn2 = KeyboardButton('Нет')

    markup.add(btn1, btn2)
    return markup


def btn_markup2():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton('Начать перевод')

    markup.add(btn)
    return markup




















