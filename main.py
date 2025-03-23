import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

import keyboards as kb
from news import get_news_today, get_data_today, get_news_yesterday, get_data_yesterday, send_long_message

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name or message.from_user.username}, выберите из меню",
                         reply_markup=kb.reply_menu)

@dp.message()
async def text_handler(message: types.Message):
    if message.text == "📰 Новости":
        await message.answer('За какое время вам показывать новости?',reply_markup=kb.inline_news)
    elif message.text == '🌎 Благотворительные фонды':
        pass

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
