import asyncio
import psycopg2
import logging
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from time import sleep
from datetime import datetime
from database import session, Members
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

load_dotenv()
load_dotenv(dotenv_path=Path('.')/'.env')

bot = Bot(getenv('TOKEN'))
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler({"apscheduler.timezone": "Europe/Moscow"})
users_list = session.query(Members.user_id).all()

@dp.message(commands=["start"])
async def start_message(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Продолжить',
        callback_data='continue')
    )
    await message.answer('Добро пожаловать в адвент календарь по русскому языку! Меня зовут Катерина Филатова и я помогу тебе восполнить пробелы в теории, которая необходима для сдачи ЕГЭ по русскому языку на высокие баллы.')
    await message.answer('Уже 5-й год я помогаю старшеклассникам готовиться к экзаменам. Средний результат сдачи ЕГЭ по русскому языку у моих учеников 87+, в чём ты можешь убедиться, посмотрев мои соц.сети. А ещё ты сможешь поближе со мной познакомиться и получить много полезного контента:)')
    await message.answer('Inst: @ katty.phil\nVK: https: // vk.com/egeruslitus\nYoutube: https: // www.youtube.com/@egeruslitus', reply_markup=builder.as_markup())

async def start_message_cont(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Все понятно!',
        callback_data='alright')
    )
    await message.answer('ПРАВИЛА АДВЕНТ КАЛЕНДАРЯ')
    await message.answer('1. Каждый день тебе будет приходить ссылка на небольшое видео с теорией + конспект. За просмотр видео ты получаешь автоматически 5 баллов.\n\n2. После видео тебе необходимо прорешать 3 задания с выбором ответа, за каждое из которых ты можешь заработать 2 балла.\n\n3.Если ты хочешь больше практики, а также получить ещё дополнительные баллы, то тебе будет доступна ссылка на гугл-форму. Там будут дополнительные задания, некоторые с ручной проверкой (например, cочинения). За решение гугл-форм тебе начислятся баллы 30 декбря.\n\n4. Если ты хочешь получить подробный разбор сочинения с рекомендациями, как исправить ошибки и улучшить результат, то внимательно смотри задания в гугл-формах)', reply_markup=builder.as_markup())

async def register_message(message: types.Message):
    await message.answer('Отлично, теперь ты знаешь, что тебя ждёт!\n\nСкажи, пожалуйста, как тебя зовут. Напиши свои имя и фамилю одним сообщением.\n\nНапример:\nИван Иванов')
    dp.message.register(get_name, content_types='text')

async def get_name(message: types.Message):
    user = session.query(Members).where(Members.user_id == message.from_user.id).all()
    if user:
        await message.answer('Вы уже зарегестрированы!')
    else:
        new_user = Members(name=message.text, user_id=message.from_user.id, username=message.from_user.username, score=0)
        session.add(new_user)
        try:
            session.commit()
            print('user in db')
            await message.answer('Приятно познакомиться!\nЖалаю удачи!\n\nИ помни, если у тебя возникнут какие-либо воросы, ты всегда можешь обратиться ко мне в личные сообщения.\n\nМой тг: @wirsme')
        except:
            session.rollback()
            print('error')

async def first_task():
    await bot.send_message(chat_id=370289587, text='gufufi')


@dp.callback_query()
async def callback_query(callback: types.CallbackQuery):
    button = callback.data
    if button == 'continue':
        await start_message_cont(callback.message)
    if button == 'alright':
        await register_message(callback.message)


async def main():
    scheduler.add_job(first_task, 'date', run_date=datetime(2023, 2, 1, 0, 1))
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        scheduler.start()
        asyncio.run(main())
        while True:
            sleep(1)
    except:
        pass