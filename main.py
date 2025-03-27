import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

import keyboards as kb
from charity import get_charity
from helping_animals import start_shelter
from news import get_news_today, get_data_today, get_news_yesterday, get_data_yesterday, send_long_message

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

questions = [
    {"text": "Вы готовы заботиться о питомце всю его жизнь?", "buttons": ["Да", "Нет"]},
    {"text": "Готовы ли вы посещать ветеринара в случае необходимости?", "buttons": ["Да", "Нет"]},
    {"text": "Вы можете обеспечить питомцу комфортные условия жизни?", "buttons": ["Да", "Нет"]},
]

pets = [
    {"id": 1, "name": "Барсик", "photo": "https://melitopol-news.ru/img/20240305/a9073bcadfb86dc6a12733530c3f2333_o.jpg", "desc": "добрый котик", "age": 2},
    {"id": 2, "name": "Принцесса", "photo": "https://i.pinimg.com/736x/22/c1/79/22c17996e3e7f4479d0b9960b4e0cbd0.jpg", "desc": "Любит гулять", "age": 3},
    {"id": 3, "name": "Саша", "photo": "https://i.pinimg.com/736x/59/7a/cf/597acf74dac3b7258bd8a0209efd925f.jpg", "desc": "Саша свинтус", "age": 1},
    {"id": 4, "name": "Люсинка", "photo": "https://pic.rutubelist.ru/user/55/99/55996e286a9c7916e02caca2b1a93394.jpg", "desc": "Красавица и умница", "age": 4},
    {"id": 5, "name": "Томми", "photo": "https://i.pinimg.com/originals/ea/21/b6/ea21b6d98f790d40beb06350a6f6904d.jpg", "desc": "Верный друг", "age": 5},
    {"id": 6, "name": "Луна", "photo": "https://i.pinimg.com/originals/59/a4/06/59a406200e3a54ed084a2a6268e28e18.jpg", "desc": "Очаровательная кошечка", "age": 3},
    {"id": 7, "name": "Мурка", "photo": "https://habrastorage.org/r/w780/getpro/habr/upload_files/779/147/c1f/779147c1fef39f67a04d66eba21b32ff.jpeg", "desc": "Хитрая кошка", "age": 2},
    {"id": 8, "name": "Джек", "photo": "https://avatars.mds.yandex.net/i?id=0dfdcdcf7c863f9cf16e70bf03bdb1cd_l-5370628-images-thumbs&n=13", "desc": "Активный и умный", "age": 1},
    {"id": 9, "name": "Король", "photo": "https://i.pinimg.com/736x/f4/de/2e/f4de2e6f9f2c167d55eded71594b4157.jpg", "desc": "Он для тебя царь и бог", "age": 4},
    {"id": 10, "name": "Боня", "photo": "https://avatars.mds.yandex.net/i?id=cac63cf1a4422abd38a805d5a24a851c_l-9226797-images-thumbs&n=13", "desc": "Любит поесть", "age": 3},
]
user_answers = {}
donations = {}
user_pets_index = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name or message.from_user.username}, выберите из меню",
                         reply_markup=kb.reply_menu)

@dp.message()
async def text_handler(message: types.Message):
    if message.text == "📰 Новости":
        await message.answer('За какое время вам показывать новости?',reply_markup=kb.inline_news)
    elif message.text == '🌎 Благотворительные фонды':
        charity_info, markup = await get_charity(0)
        if charity_info is None:
            await message.answer("Ошибка: Не удалось загрузить данные фонда. Попробуйте позже.")
            return
        await message.answer(charity_info, reply_markup=markup)
    elif message.text == '📚 Подготовка к ОРТ':
        pass
    elif message.text == "🦮 Питомник":
        pass

# 🌎 Благотворительные фонды
@dp.callback_query(lambda c: c.data.startswith("next:"))
async def process_next_fund(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split(":")[1])  # Получаем индекс следующего фонда

    charity_info, markup = await get_charity(index)  # Получаем данные следующего фонда

    if charity_info is None:
        await callback_query.answer("Больше фондов нет.")
        return

    await callback_query.message.answer(charity_info, reply_markup=markup)
    await callback_query.answer()



# 📰 Новости
@dp.callback_query()
async def callback_query_handler(call: types.CallbackQuery):
    if call.data == "today":
        news = await get_news_today()
        data = await get_data_today()
        await send_long_message(call.message, data)
        if news and news.strip():
            await send_long_message(call.message, news)
        else:
            await send_long_message(call.message, "Не удалось загрузить новости. Попробуйте позже.")
    elif call.data == 'yesterday':
        news = await get_news_yesterday()
        data = await get_data_yesterday()
        await send_long_message(call.message, data)
        if news and news.strip():
            await send_long_message(call.message, news)
        else:
            await send_long_message(call.message, "Не удалось загрузить новости. Попробуйте позже.")



async def main():
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
