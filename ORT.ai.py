import os

from aiogram import types
from aiogram.types import Message
from openai import OpenAI

from main import dp

OPEN_AI_CHAT_KEY = os.getenv('OPEN_AI_CHAT_KEY')

@dp.callback_query()
async def callback_query_handler(call: types.CallbackQuery):
    if call.data == 'geography':
        pass
    elif call.data == 'informatics':
        pass
    elif call.data == 'russian':
        pass
    elif call.data == 'english':
        pass






async def chat_with_ai(message: Message):
    try:
        print("Старт")
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=f"{OPEN_AI_CHAT_KEY}",
        )

        completion = client.chat.completions.create(
        model="open-r1/olympiccoder-32b:free",
        messages=[
            {
            "role": "user",
            "content": message.text
            },
            {
                "role":"system",
                "content": ''
            }
        ]
        )
        r = completion.choices[0].message.content
        await message.answer(r)
    except Exception as e:
        print(e)