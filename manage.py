import os
import parsers
import databases
import logging
from datetime import date, datetime
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
db = databases.PostgresDataVacancy()

keyboard = types.InlineKeyboardMarkup() 
button = types.InlineKeyboardButton(text="Show more", callback_data="Show more")
keyboard.add(button)

@dp.message_handler(commands="start")
async def start(message: types.Message): 
    await message.answer("Записать ключевые слова через пробел\nНапример: python django docker\nРезультат выдачи зависит от порядка слов")

 
@dp.callback_query_handler(Text(equals="Show more"))
async def next_vecancies(callback: types.CallbackQuery): 
    offset = 3
    for vacan in list_urls[:offset]:
        card = f"{hlink(vacan[2], vacan[2])}\n"                            
        await callback.message.answer(card, reply_markup=keyboard)
        list_urls.remove(vacan)
        if not list_urls:
            await callback.message.answer("По вашему запросу больше вакансий нет.") 

@dp.message_handler()
async def get_vacancies(message: types.Message): 
    global get_text, list_urls
    get_text = await message.reply(message.text)
    get_text = f"%{'%'.join(str(get_text['text']).split())}%"
    print(get_text)
    list_urls = db.select_data_from_db(get_text)
    await message.answer(f"По вашему запросу: {len(list_urls)} вакансий")
    if len(list_urls) > 0:
        await message.answer("Для просмотра вакансий нажмите: Show more", reply_markup=keyboard)
    


def main():

    try:       
        if db.get_today_date()[0] != date.today():
            db.delete_tables_if_exist()
            db.create_tables_if_not_exist()
            by.find_total_sum_vacancies()
            by.find_all_pages_urls()
            for data in by.find_data_vacancy():
                try:
                    db.insert_data_into_db(data)
                except Exception as ex:
                    print(ex)
                    continue

        print(db.select_count_vacancies()[0])

        executor.start_polling(dp)
 
    except Exception as ex:
        print(ex)
    finally:
        db.close_connection() 
        

if __name__ == '__main__':
    main()
 
