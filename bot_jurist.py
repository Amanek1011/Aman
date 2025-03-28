from aiogram import Router, types

from dotenv import load_dotenv
import keyboards as kb
load_dotenv()

jurist_router = Router(name="jurist_router")  # Добавляем имя для отладки


# Список бесплатных юридических организаций
free_legal_services = """
📚 <b>Бесплатная юридическая помощь в Кыргызстане:</b>

1. <b>Юридическая клиника "Адилет"</b>
   - Телефон: +996 312 66 06 66
   - Адрес: г. Бишкек, ул. Тыныстанова, 78

2. <b>ОФ "Центр помощи женщинам"</b>
   - Телефон: +996 312 88 03 88

3. <b>ОФ "Правовая помощь"</b>
   - Горячая линия: 0 800 00 00

4. <b>Юридическая клиника КГЮА</b>
   - Телефон: +996 312 54 32 10
"""


def get_jurist_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Бесплатные юристы")],
            [types.KeyboardButton(text="Как подать заявление?")],
            [types.KeyboardButton(text="Мои права")],
            [types.KeyboardButton(text="↩️ Выйти в меню")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Задайте юридический вопрос..."
    )



async def start_jurist(message: types.Message):
    await message.answer(
        "👨⚖️ <b>Юридический помощник</b>\n\n"
        "Выберите опцию :",
        reply_markup=get_jurist_keyboard(),
        parse_mode='HTML'
    )



async def show_lawyers(message: types.Message):
    await message.answer(free_legal_services, parse_mode='HTML')



async def how_to_apply(message: types.Message):
    await message.answer(
        "📝 <b>Как подать заявление:</b>\n\n"
        "1. Подготовьте документы\n2. Составьте заявление\n"
        "3. Подайте в инстанцию\n4. Получите отметку",
        parse_mode='HTML'
    )



async def basic_rights(message: types.Message):
    await message.answer(
        "🔹 <b>Основные права:</b>\n\n"
        "- Право на жизнь\n- Право на труд\n- Право на жилище\n"
        "- Право на медицинскую помощь",
        parse_mode='HTML'
    )



async def exit_jurist(message: types.Message):
    await message.answer(
        "Возвращаемся в главное меню",
        reply_markup=kb.reply_menu)



# @jurist_router.message(F.text)
# async def handle_question(message: types.Message):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Ты юрист КР. Отвечай кратко по законодательству."},
#                 {"role": "user", "content": message.text}
#             ],
#             temperature=0.3,
#             max_tokens=500
#         )
#
#         answer = response.choices[0].message.content
#         await message.answer(
#             f"⚖️ <b>Ответ:</b>\n\n{answer}",
#             parse_mode='HTML',
#             reply_markup=get_jurist_keyboard()
#         )
#     except Exception as e:
#         await message.answer("⚠️ Ошибка. Попробуйте позже.")