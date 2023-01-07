import logging
import telebot
from os import getenv
from time import sleep
from telebot import types
from sqlalchemy import create_engine
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

bot = telebot.TeleBot(getenv('TOKEN'))
engine = create_engine(getenv('DATABASE'), echo=True)
scheduler = BackgroundScheduler()

@bot.message_handler(commands=['start',])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    cont = types.InlineKeyboardButton(
        text='Продолжить', callback_data='yes')
    keyboard.add(cont)
    bot.send_message(message.chat.id, 'Добро пожаловать в адвент календарь по русскому языку! Меня зовут Катерина Филатова и я помогу тебе восполнить пробелы в теории, которая необходима для сдачи ЕГЭ по русскому языку на высокие баллы.')
    bot.send_message(message.chat.id, 'Уже 5-й год я помогаю старшеклассникам готовиться к экзаменам. Средний результат сдачи ЕГЭ по русскому языку у моих учеников 87+, в чём ты можешь убедиться, посмотрев мои соц.сети. А ещё ты сможешь поближе со мной познакомиться и получить много полезного контента:)')
    bot.send_message(
        message.chat.id, 'Inst: @ katty.phil\nVK: https: // vk.com/egeruslitus\nYoutube: https: // www.youtube.com/@egeruslitus', reply_markup=keyboard)

@bot.message_handler(content_types=['text', ])
def start2_message(message):
    keyboard = types.InlineKeyboardMarkup()
    cont = types.InlineKeyboardButton(
        text='Все понятно!', callback_data='yes2')
    keyboard.add(cont)
    bot.send_message(message.chat.id, 'ПРАВИЛА АДВЕНТ КАЛЕНДАРЯ')
    bot.send_message(message.chat.id, '1. Каждый день тебе будет приходить ссылка на небольшое видео с теорией + конспект. За просмотр видео ты получаешь автоматически 5 баллов.\n\n2. После видео тебе необходимо прорешать 3 задания с выбором ответа, за каждое из которых ты можешь заработать 2 балла.\n\n3.Если ты хочешь больше практики, а также получить ещё дополнительные баллы, то тебе будет доступна ссылка на гугл-форму. Там будут дополнительные задания, некоторые с ручной проверкой (например, cочинения). За решение гугл-форм тебе начислятся баллы 30 декбря.\n\n4. Если ты хочешь получить подробный разбор сочинения с рекомендациями, как исправить ошибки и улучшить результат, то внимательно смотри задания в гугл-формах)', reply_markup=keyboard)

@bot.message_handler(content_types=['text', ])
def register_message(message):
    msg = bot.reply_to(message, 'Отлично, теперь ты знаешь, что тебя ждёт!\n\nСкажи, пожалуйста, как тебя зовут. Напиши свои имя и фамилю одним сообщением.\n\nНапример:\nИван Иванов')
    bot.register_next_step_handler(msg, get_name)

@bot.message_handler(content_types=['text', ])
def get_name(message):
    keyboard = types.InlineKeyboardMarkup()
    cont = types.InlineKeyboardButton(
        text='Жду задания!', callback_data='yes3')
    keyboard.add(cont)
    current_user = message.chat.username
    res = engine.execute(f"SELECT COUNT(*) FROM members WHERE username = '{current_user}'").fetchall()[0][0]
    if res == 0:
        engine.execute(
            f'''INSERT INTO members (username, user_id, name, score) VALUES ('{current_user}', '{message.chat.id}', '{message.text}', '{0}');''')
    bot.reply_to(
        message, 'Приятно познакомиться!\nЖалаю удачи!\n\nИ помни, если у тебя возникнут какие-либо воросы, ты всегда можешь обратиться ко мне в личные сообщения.\n\nМой тг: @wirsme')

@bot.message_handler(content_types=['text', ])
def prompt(message):
    bot.send_message(message.chat.id, 'gyuk')
    scheduler.add_job(prompt(message), 'date', run_date='2023-1-07 19:23:00')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        start2_message(call.message)
    if call.data == "yes2":
        register_message(call.message)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
        scheduler.start()
        print(scheduler.get_jobs())
        while True:
            sleep(1)
    except:
        pass