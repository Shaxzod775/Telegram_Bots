from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from keyboard import btn_markup, btn_markup1, btn_markup2
from configs import get_key, save_text_to_db, insert_trans_from_db, LANGUAGES
from googletrans import Translator

TOKEN = '6528255699:AAGSiOAyzz_jBXr82aP95DH1aJPa0XOLsBE'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'history', 'about', 'help'])
def command_start(message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.full_name
    if message.text == '/start':
        bot.send_message(chat_id, f'Здравствуйте {user_name} Вас приветствует бот переводчик')
        confirm_src(message)
    elif message.text == '/history':
        send_translation_history(chat_id)
    elif message.text == '/about':
        bot.send_message(chat_id, 'Этот бот создан чтобы переводить введёный текст с Русского на любой язык')
    elif message.text == '/help':
        bot.send_message(chat_id, 'За технической помощью обращайтесь к @chris_collins_UTC')


def send_translation_history(chat_id):
    translations = insert_trans_from_db(chat_id)
    if translations:
        bot.send_message(chat_id, "Ваша история переводов:")
        for src_text, dest_text in translations:
            bot.send_message(chat_id, f"Введёный текст: {src_text}\nПеревод: {dest_text}")
    else:
        bot.send_message(chat_id, "Ваша история переводов пуста.")


def confirm_src(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'С какого языка вы бы хотели перевести?', reply_markup=btn_markup())
    bot.register_next_step_handler(msg, confirm_dest)


def confirm_dest(message: Message):
    chat_id = message.chat.id
    text_src = message.text
    try:
        if text_src in LANGUAGES.values():
            msg = bot.send_message(chat_id, 'На какой язык вы бы хотели перевести?', reply_markup=btn_markup())
            bot.register_next_step_handler(msg, confirm_dest_and_src, text_src)
    except:
        pass

def confirm_dest_and_src(message, text_src):
    chat_id = message.chat.id
    text_dest = message.text

    if text_dest == '/start' or text_dest == '/history' or text_dest == '/about' or text_dest == '/help':
        command_start(message)
    else:
        msg = bot.send_message(chat_id, 'Введите текст для перевода', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, text_translation, text_src, text_dest)


def text_translation(message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text

    if text == '/start' or text_dest == '/history' or text_dest == '/about' or text_dest == 'help':
        command_start(message)
    else:
        teacher = Translator()
        msg = teacher.translate(text=text, src=get_key(text_src), dest=get_key(text_dest)).text
        bot.send_message(chat_id, msg)

        save_text_to_db(str(chat_id), text, msg)

        new_msg = bot.send_message(chat_id, 'Хотите перевести что-нибудь ещё?', reply_markup=btn_markup1())

        bot.register_next_step_handler(new_msg, continue_translation, text_src, text_dest)


def continue_translation(message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text

    if text == 'Да':
        msg = bot.send_message(chat_id, 'Введите текст для перевода')
        bot.register_next_step_handler(msg, text_translation, text_src, text_dest)
    elif text == 'Нет':
        command_start(message)



bot.infinity_polling()

