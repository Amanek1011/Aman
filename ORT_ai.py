import asyncio
import os
from aiogram import types, Router, F
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime, timedelta
import logging

import keyboards

load_dotenv()
# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ort_router = Router()
OPENROUTER_API_KEY = os.getenv('OPEN_AI_CHAT_KEY')
YOUR_SITE_URL = "https://web.telegram.org/k/#@PT_Aman_BOT"
YOUR_SITE_NAME = "PT_Aman"

ort_sessions = {}
SESSION_TIMEOUT = timedelta(minutes=30)


def get_ort_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Сменить предмет")],
            [types.KeyboardButton(text="Пример вопроса")],
            [types.KeyboardButton(text="Выход")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Задайте ваш вопрос..."
    )


async def cleanup_sessions():
    """Функция для очистки неактивных сессий"""
    while True:
        try:
            now = datetime.now()
            expired_users = [
                user_id for user_id, session in ort_sessions.items()
                if now - session['last_activity'] > SESSION_TIMEOUT
            ]
            for user_id in expired_users:
                del ort_sessions[user_id]
                logger.info(f"Сессия пользователя {user_id} очищена по таймауту")
            await asyncio.sleep(300)
        except Exception as e:
            logger.error(f"Ошибка в cleanup_sessions: {e}")
            await asyncio.sleep(60)


@ort_router.callback_query(F.data.in_(['geography', 'informatics', 'russian', 'english']))
async def ort_callback_handler(call: types.CallbackQuery):
    try:
        user_id = call.from_user.id
        logger.info(f"User {user_id} selected {call.data}")

        subjects = {
            'geography': 'географии',
            'informatics': 'информатике',
            'russian': 'русскому языку',
            'english': 'английскому языку'
        }

        ort_sessions[user_id] = {
            'subject': subjects[call.data],
            'last_activity': datetime.now()
        }

        await call.message.answer(
            f"🔍 <b>Режим подготовки к ОРТ по {subjects[call.data]}</b>\n\n"
            "Теперь я могу помочь вам с подготовкой к экзамену. Задавайте вопросы, "
            "и я постараюсь дать развернутые ответы.\n\n"
            "Используйте кнопки ниже для управления сессией.",
            reply_markup=get_ort_keyboard(),
            parse_mode="HTML"
        )
        await call.answer()
    except Exception as e:
        logger.error(f"Error in ort_callback_handler: {e}")
        await call.message.answer("⚠️ Произошла ошибка. Попробуйте выбрать предмет снова.")


async def example_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if user_id not in ort_sessions:
            await message.answer("Сначала выберите предмет для подготовки")
            return

        examples = {
            'географии': "• Какие факторы влияют на климат Южной Америки?\n"
                         "• Объясните круговорот воды в природе\n"
                         "• Какие есть типы почв и их особенности?",
            'информатике': "• Объясни разницу между TCP и UDP\n"
                           "• Что такое бинарный поиск?\n"
                           "• Как работает рекурсия?",
            'русскому языку': "• Как правильно: 'одеть' или 'надеть'?\n"
                              "• Объясните правило 'жи-ши'\n"
                              "• Что такое причастный оборот?",
            'английскому языку': "• Когда используется Present Perfect?\n"
                                 "• В чем разница между Past Simple и Past Continuous?\n"
                                 "• Как правильно использовать артикли?"
        }

        subject = ort_sessions[user_id]['subject']
        ort_sessions[user_id]['last_activity'] = datetime.now()

        await message.answer(
            f"<b>Примеры вопросов по {subject}:</b>\n\n{examples[subject]}\n\n"
            "Можете задать любой из этих вопросов или свой собственный.",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка в example_handler: {e}")



async def change_subject(message: types.Message):
    try:
        from keyboards import inline_ort_subjects
        ort_sessions[message.from_user.id]['last_activity'] = datetime.now()
        await message.answer(
            "Выберите новый предмет для подготовки:",
            reply_markup=inline_ort_subjects
        )
    except Exception as e:
        logger.error(f"Ошибка в change_subject: {e}")



async def exit_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        if user_id in ort_sessions:
            subject = ort_sessions[user_id]['subject']
            del ort_sessions[user_id]
            await message.answer(
                f"Режим подготовки по {subject} завершен.\n"
                "Вы всегда можете вернуться, выбрав предмет снова.",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            await message.answer("Вы не в режиме подготовки",keyboards.reply_menu)
    except Exception as e:
        logger.error(f"Ошибка в exit_handler: {e}")


@ort_router.message(
    F.text &
    F.from_user.id.in_(ort_sessions) &
    ~F.text.in_(["Сменить предмет", "Пример вопроса", "Выход"])
)
async def chat_with_deepseek(message: types.Message):
    try:
        user_id = message.from_user.id
        user_session = ort_sessions[user_id]
        user_session['last_activity'] = datetime.now()

        logger.info(f"Processing question from {user_id}: {message.text}")

        if not OPENROUTER_API_KEY:
            raise ValueError("API key not configured")

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY
        )

        await message.bot.send_chat_action(message.chat.id, "typing")

        # Добавляем контекст предмета в запрос
        prompt = (
            f"Ты эксперт по подготовке к ОРТ по {user_session['subject']}. "
            f"Ответь на вопрос студента подробно, но понятно:\n\n"
            f"Вопрос: {message.text}"
        )

        response = client.chat.completions.create(

            model="google/gemma-2-9b-it:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        answer_ = response.choices[0].message.content
        logger.info(f"DeepSeek response length: {len(answer_)} chars")

        # Разбиваем длинные ответы на части
        if len(answer_) > 4000:
            parts = [answer_[i:i + 4000] for i in range(0, len(answer_), 4000)]
            for part in parts:
                await message.answer(part)
                await asyncio.sleep(0.5)
        else:
            await message.answer(answer_)

    except Exception as e:
        logger.error(f"DeepSeek error: {str(e)}")
        await message.answer(
            "⚠️ Произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте:\n"
            "1. Переформулировать вопрос\n"
            "2. Попробовать позже\n"
            "3. Обратиться к преподавателю"
        )


async def on_startup():
    """Запуск при старте бота"""
    try:
        logger.info("Запуск очистки сессий")
        asyncio.create_task(cleanup_sessions())
    except Exception as e:
        logger.error(f"Ошибка в on_startup: {e}")