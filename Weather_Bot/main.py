from telebot import TeleBot
from telebot.types import Message
from keyboard import weather_btn
from datetime import datetime
import requests


telegram_TOKEN = '6658578278:AAEEaKWCYa6TYldyibVLlwmWbKjXzu51rQ0'

bot = TeleBot(telegram_TOKEN)

user_states = {}


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    msg = f'Привет, {message.from_user.full_name}!'
    bot.send_message(chat_id, msg, reply_markup=weather_btn())
    user_states[chat_id] = 'waiting_for_language'


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_language')
def get_language(message: Message):
    chat_id = message.chat.id
    user_states[chat_id] = 'waiting_for_city'
    bot.send_message(chat_id, 'Enter language')


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_city')
def get_city(message: Message):
    chat_id = message.chat.id
    language = message.text
    user_states[chat_id] = 'waiting_for_weather'
    msg = bot.send_message(chat_id, 'Enter city: ')
    user_states[chat_id] = {'language': language}
    bot.register_next_step_handler(msg, get_weather)

def get_weather(message: Message):
    chat_id = message.chat.id
    city = message.text
    language = user_states[chat_id]['language']

    parameters = {
            'appid': 'eb8269f63e5bee7531ddcc348bac701f',
            'units': 'metric',
            'lang': f'{language}'
        }

    parameters['q'] = city
    try:
        data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters).json()

        city_name = data['name']
        temp = data['main']['temp']
        wind = data['wind']['speed']
        timezone = data['timezone']

        sunrise = datetime.utcfromtimestamp(int(data['sys']['sunrise']) + int(timezone))
        sunset = datetime.utcfromtimestamp(int(data['sys']['sunset']) + int(timezone))

        description = data['weather'][0]['description']

        if language == 'ru':
            bot.send_message(chat_id, f'''В {city_name} сейчас {description}  
Температура 🌡: {temp} °C
Скорость ветра 💨: {wind} м/с
Рассвет 🌅: {sunrise}
Закат 🌅: {sunset}''')
        elif language == 'en':
            bot.send_message(chat_id, f'''The weather in {city_name} now is {description.capitalize()}  
Temperature 🌡: {temp} °C
Wind speed 💨: {wind} m/s
Sunrise 🌅: {sunrise}
Sunset 🌅: {sunset}''')


    except:
        bot.send_message(chat_id, f'Invalid city: {city}. Please try again.')


bot.infinity_polling()

