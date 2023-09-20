from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def weather_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='⛅️Get Weather')
    markup.add(btn)
    return markup



