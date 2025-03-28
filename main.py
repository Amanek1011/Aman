import asyncio
import os


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from dotenv import load_dotenv

import keyboards as kb
from database import db
from charity import get_charity
from helping_animals import *
from news import get_news_today, get_data_today, get_news_yesterday, get_data_yesterday, send_long_message, \
    news_handler, weather_handler, back_to_main, currency_handler
from ORT_ai import ort_router, on_startup, example_handler, change_subject, exit_handler
from bot_jurist import jurist_router, start_jurist, show_lawyers, how_to_apply, basic_rights, \
    exit_jurist  # Импортируем новый роутер

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Подключаем все роутеры
dp.include_router(ort_router)
dp.include_router(jurist_router)

# Инициализация переменных
user_states = {}
donations = {}
shelter_phone = "+996 555 123456"


@dp.message(CommandStart())
async def start(message: types.Message):
    # Добавляем пользователя в базу данных
    await db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        f"Привет {message.from_user.first_name or message.from_user.username}, выберите из меню",
        reply_markup=kb.reply_menu
    )

@dp.message()
async def text_handler(message: types.Message):
    user_id = message.from_user.id

    # Обработка пожертвований
    if user_id in user_states and user_states[user_id] == 'waiting_for_donation':
        try:
            amount = int(message.text)
            if amount < 10:
                await message.answer("Минимальная сумма пожертвования — 10 сом. Попробуйте снова.")
                return

            donations[user_id] = amount
            await message.answer(f"Спасибо за ваше пожертвование в размере {amount} сом! ❤️")
            await message.answer(f"Для связи с приютом звоните по номеру: {shelter_phone}")
            del user_states[user_id]
        except ValueError:
            await message.answer("Пожалуйста, введите корректную сумму (только цифры).")
        return

    # Основное меню
    if message.text == "📰 Сервисы":
        await message.answer('Выберите сервис', reply_markup=kb.reply_service)
    elif message.text == '📰 Новости':
        await news_handler(message)
    elif message.text == '🌤 Погода':
        await weather_handler(message)
    elif message.text == '💱 Курс валют':
        await currency_handler(message)
    elif message.text == '↩️ Назад':
        await back_to_main(message)
    elif message.text == '🌎 Благотворительные фонды':
        charity_info, markup = await get_charity(0)
        if charity_info is None:
            await message.answer("Ошибка: Не удалось загрузить данные фонда. Попробуйте позже.")
            return
        await message.answer(charity_info, reply_markup=markup)
    elif message.text == "🦮 Питомник":
        await start_animals(message)
    elif message.text == 'Забрать питомца':
        await start_survey(message)
    elif message.text == 'Пожертвовать':
        await donate_start(message)
    elif message.text == "Пример вопроса":
        await example_handler(message)
    elif message.text == 'Сменить предмет':
        await change_subject(message)
    elif message.text == 'Выход':
        await exit_handler(message)
    elif message.text == '💼 Юридический помощник':
        await start_jurist(message)
    elif message.text == 'Бесплатные юристы':
        await show_lawyers(message)
    elif message.text == 'Как подать заявление?':
        await how_to_apply(message)
    elif message.text == 'Мои права':
        await basic_rights(message)
    elif message.text == '↩️ Выйти в меню':
        await exit_jurist(message)
    # Юридический помощник теперь обрабатывается через jurist_router

@dp.callback_query(lambda c: c.data.startswith("next:"))
async def process_next_fund(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split(":")[1])
    charity_info, markup = await get_charity(index)

    if charity_info is None:
        await callback_query.answer("Больше фондов нет.")
        return

    await callback_query.message.answer(charity_info, reply_markup=markup)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data in ["today", "yesterday"])
async def news_callback_handler(call: types.CallbackQuery):
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
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith(('answer_', 'adopt_', 'skip_', 'back_')))
async def animals_callback_handler(call: types.CallbackQuery):
    if call.data.startswith('answer_'):
        await handle_answer(call)
    elif call.data.startswith('adopt_'):
        await adopt_pet(call)
    elif call.data.startswith('skip_'):
        await next_pet(call)
    elif call.data.startswith('back_'):
        await previous_pet(call)



async def donate_start(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = 'waiting_for_donation'
    await message.answer("Введите сумму, которую хотите пожертвовать (в сомах):")


async def main():
    # Инициализация базы данных
    await db.connect()
    await db.create_tables()

    await on_startup()
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
