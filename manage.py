import os
import parsers
import db_psql
import logging

from dotenv import find_dotenv, load_dotenv
from config import cookies, headers, params, url

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink

logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv())

bot = Bot(token=str(os.getenv("TOKEN")), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

by = parsers.Parser(url=url, cookies=cookies, headers=headers, params=params)
db = db_psql.PostgresDataVacancy()

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["start"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Записать ключевое слово", reply_markup=keyboard)
    
@dp.message_handler()
async def get_vacancies(message: types.Message):
    get_text = await message.reply(message.text)
    
    for vacan in db.select_data_from_db(str(get_text['text'])):
        card = f"{hlink(vacan[2], vacan[2])}\n"   
        await message.answer(card)

def main():
    by.find_total_sum_vacancies()
    by.find_all_pages_urls()
    try:    
        db.delete_tables_if_exist()
        db.create_tables_if_not_exist()
    
        for data in by.find_data_vacancy():
            try:
                db.insert_data_into_db(data)
            except Exception as ex:
                print(ex)
                continue

        executor.start_polling(dp)
 
    except Exception as ex:
        print(ex)
    finally:
        db.close_connection() 
        

if __name__ == '__main__':
    main()
 
