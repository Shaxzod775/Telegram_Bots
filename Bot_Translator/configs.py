import psycopg2
from telebot import TeleBot

TOKEN = '6528255699:AAGSiOAyzz_jBXr82aP95DH1aJPa0XOLsBE'

bot = TeleBot(TOKEN)

LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 Английский',
    'it': '🇮🇹 Итальянский',
    'es': '🇪🇸 Испанский',
    'uz': '🇺🇿 Узбекский',
    'ja': '🇯🇵 Японский'
}


def get_key(language):
    for k, v in LANGUAGES.items():
        if language == v:
            return k

def create_new_table():
    db = psycopg2.connect(
        host='localhost',
        port='5432',
        database='bot_perevod',
        user="postgres",
        password='123456')

    cursor = db.cursor()

    cursor.execute('''
         DROP TABLE IF EXISTS user_trans_history;
    
         CREATE TABLE IF NOT EXISTS user_trans_history(
         telegram_id TEXT,
         src_text TEXT,
         dest_text TEXT
         );
    ''')

    db.commit()


def save_text_to_db(id, src_text, dest_text):
    db = psycopg2.connect(
        host='localhost',
        port='5432',
        database='bot_perevod',
        user="postgres",
        password='123456')

    cursor = db.cursor()

    cursor.execute('''
         INSERT INTO user_trans_history(telegram_id, src_text, dest_text) VALUES (%s, %s, %s); ''',
                   (id, src_text, dest_text))

    db.commit()
    db.close()

def insert_trans_from_db(chat_id):
    db = psycopg2.connect(
        host='localhost',
        port='5432',
        database='bot_perevod',
        user="postgres",
        password='123456')

    cursor = db.cursor()

    cursor.execute(f'''
        SELECT src_text, dest_text FROM user_trans_history
        WHERE telegram_id = CAST({chat_id} AS text);
    ''')

    translations = cursor.fetchall()

    db.close()

    return translations













