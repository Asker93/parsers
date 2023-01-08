import asyncio
import json
import datetime

from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from config import token_tg_bot, id_tg
from parser_securitylab_news import check_news_update


bot = Bot(token_tg_bot, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    start_buttons = ['Все новости', "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Лента новостей', reply_markup=keyboard)


@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(message: types.Message):
    with open('news_dict.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items(), key=lambda x: x[0]):
        # print(k)
        # news = f'<b>{datetime.datetime.fromtimestamp(v["date_timestamp"])}</b>\n' \
        #        f'<u>{v["title"]}</u>\n' \
        #        f'<code>{v["context"]}</code>\n' \
        #        f'{v["link"]}'

        # news = f'{hbold(datetime.datetime.fromtimestamp(v["date_timestamp"]))}\n' \
        #        f'{hunderline(v["title"])}\n' \
        #        f'{hcode(v["context"])}\n' \
        #        f'{hlink(v["title"], v["link"])}'

        news = f'{hbold(datetime.datetime.fromtimestamp(v["date_timestamp"]))}\n' \
               f'{hlink(v["title"], v["link"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='Последние 5 новостей'))
async def get_last_five(message: types.Message):
    with open('news_dict.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items(), key=lambda x: x[0])[-5:]:
        news = f'{hbold(datetime.datetime.fromtimestamp(v["date_timestamp"]))}\n' \
               f'{hlink(v["title"], v["link"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='Свежие новости'))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items(), key=lambda x: x[1]['date_timestamp']):
            news = f'{hbold(datetime.datetime.fromtimestamp(v["date_timestamp"]))}\n' \
                   f'{hlink(v["title"], v["link"])}'

            await message.answer(news)
    else:
        await message.answer('Нет свежих новостей!!!')


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items(), key=lambda x: x[1]['date_timestamp']):
                news = f'{hbold(datetime.datetime.fromtimestamp(v["date_timestamp"]))}\n' \
                       f'{hlink(v["title"], v["link"])}'

                await bot.send_message(id_tg, news)
        else:
            await bot.send_message(id_tg, 'Пока нет свежих новостей', disable_notification=True)

        await asyncio.sleep(20)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
