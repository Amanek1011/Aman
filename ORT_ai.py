
import os

from aiogram import types
from aiogram.types import Message

from openai import OpenAI

from main import dp
from keyboards import inline_news
OPEN_AI_CHAT_KEY = os.getenv('OPEN_AI_CHAT_KEY')


# Глобальная переменная для хранения текущего промпта
current_prompt = ""

async def start_ort_ai(message: Message):
    await message.answer('Здраствуйте, я помощник по ОРТ, по какому предмету вас подготовить?', reply_markup=inline_news)

@dp.callback_query()
async def callback_query_handler(call: types.CallbackQuery):
    global current_prompt  # Делаем переменную глобальной

    if call.data == 'geography':
        current_prompt = ('Ты помощник по подготовке к ОРТ по географии. '
                          'Задавай вопросы пользователю. Если ответ правильный — переходи к следующему вопросу. '
                          'Если неправильный — объясни ошибку и снова задай вопрос.')

    elif call.data == 'informatics':
        current_prompt = ('Ты помощник по подготовке к ОРТ по информатике. '
                          'Задавай вопросы пользователю. Если ответ правильный — переходи к следующему вопросу. '
                          'Если неправильный — объясни ошибку и снова задай вопрос.')

    elif call.data == 'russian':
        current_prompt = ('Ты помощник по подготовке к ОРТ по русскому языку. '
                          'Задавай вопросы пользователю. Если ответ правильный — переходи к следующему вопросу. '
                          'Если неправильный — объясни ошибку и снова задай вопрос.')

    elif call.data == 'english':
        current_prompt = ('Ты помощник по подготовке к ОРТ по английскому языку. '
                          'Задавай вопросы пользователю. Если ответ правильный — переходи к следующему вопросу. '
                          'Если неправильный — объясни ошибку и снова задай вопрос.')

    await call.message.answer(f"Теперь я буду помогать вам с ОРТ по {call.data}. Напишите свой первый вопрос!")

async def chat_with_ai(message: Message):
    global current_prompt

    if not current_prompt:
        await message.answer("Сначала выберите предмет для подготовки!")
        return

    try:
        print("Старт общения с ИИ")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPEN_AI_CHAT_KEY
        )

        completion = client.chat.completions.create(
            model="open-r1/olympiccoder-32b:free",
            messages=[
                {"role": "system", "content": current_prompt},
                {"role": "user", "content": message.text}
            ]
        )

        response_text = completion.choices[0].message.content
        await message.answer(response_text)

    except Exception as e:
        print(e)
        await message.answer("Ошибка при обработке запроса. Попробуйте позже.")


