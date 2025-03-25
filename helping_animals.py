import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

# Библиотеки, которые мы используем:
# 1. aiogram - для создания бота на платформе Telegram.
# 2. dotenv - для загрузки конфиденциальных данных, таких как токен, из файла .env.

# Загружаем токен для бота из файла .env
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Читаем токен из файла .env
bot = Bot(token=TOKEN)  # Создаем объект бота
dp = Dispatcher()  # Создаем диспетчера для работы с ботом

# Вопросы анкеты
questions = [
    {"text": "Вы готовы заботиться о питомце всю его жизнь?", "buttons": ["Да", "Нет"]},  # Простой вопрос с двумя вариантами ответа
]

# Словари для хранения данных
user_answers = {}  # Здесь будут храниться ответы пользователей на вопросы анкеты
donations = {}  # Здесь будут храниться данные о пожертвованиях

# Список питомцев с их данными (имя, описание, возраст, фото)
pets = [
    {"id": 1, "name": "Барсик", "photo": "https://avatars.mds.yandex.net/get-yapic/63032/9dCFO5ep64bkpVqUwPDt5BtylO4-1/orig", "desc": "Сосал?", "age": 2},
    {"id": 2, "name": "Принцесса", "photo": "https://steamuserimages-a.akamaihd.net/ugc/1843657553609784928/3DD91D4D5FE2131A9CD758CC208CA62DE2BA09F3/?imw=512&imh=384&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true", "desc": "Фея Винкс", "age": 3},
    {"id": 3, "name": "Саша", "photo": "https://i.pinimg.com/originals/8d/f2/b8/8df2b823d002938b08974a8297469316.jpg", "desc": "Саша свин, верни деньги", "age": 1}
]

logging.basicConfig(level=logging.INFO)  # Настроим логирование для отладки

# Когда пользователь пишет команду /start, бот выводит кнопки для выбора
@dp.message(Command("start"))
async def start(message: types.Message):
    # Создаем клавиатуру с двумя кнопками: "Забрать питомца" и "Пожертвовать"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Забрать питомца")],  # Кнопка для начала анкеты
            [KeyboardButton(text="Пожертвовать")],  # Кнопка для пожертвования
        ],
        resize_keyboard=True  # Уменьшаем размер кнопок, чтобы они хорошо вмещались на экране
    )
    await message.answer("Привет! Я бот помощи животным. Ты хочешь забрать питомца или сделать пожертвование?",
                         reply_markup=keyboard)  # Отправляем сообщение с клавиатурой

# Когда пользователь нажимает кнопку "Забрать питомца", начинается анкета
@dp.message(lambda msg: msg.text == "Забрать питомца")
async def start_survey(message: types.Message):
    user_answers[message.from_user.id] = []  # Создаем список для хранения ответов пользователя
    await ask_question(message.from_user.id, message)  # Задаем первый вопрос анкеты

# Функция для вывода вопросов анкеты
async def ask_question(user_id, message):
    q_index = len(user_answers[user_id])  # Получаем индекс текущего вопроса

    # Если есть еще вопросы, задаем их
    if q_index < len(questions):
        question = questions[q_index]  # Берем текущий вопрос
        keyboard = InlineKeyboardBuilder()  # Создаем клавиатуру с кнопками для выбора ответа
        for option in question["buttons"]:  # Для каждого варианта ответа создаем кнопку
            keyboard.button(text=option, callback_data=f"answer_{q_index}_{option}")  # Кнопки с ответами

        await message.answer(question["text"], reply_markup=keyboard.as_markup())  # Отправляем вопрос с кнопками
    else:
        await analyze_answers(user_id, message)  # Если вопросы закончились, анализируем ответы

# Когда пользователь нажимает на кнопку с ответом
@dp.callback_query(lambda c: c.data.startswith("answer_"))
async def handle_answer(callback: types.CallbackQuery):
    # Извлекаем индекс вопроса и ответ из данных нажатой кнопки
    _, q_index, answer = callback.data.split("_", 2)
    user_id = callback.from_user.id
    user_answers[user_id].append(answer)  # Сохраняем ответ пользователя

    await callback.answer()  # Подтверждаем ответ
    await ask_question(user_id, callback.message)  # Переходим к следующему вопросу

# Функция для анализа ответов пользователя
async def analyze_answers(user_id, message):
    answers = user_answers[user_id]  # Получаем все ответы пользователя

    # Если в ответах есть "Нет", значит пользователь не готов заботиться о питомце
    if "Нет" in answers[:3]:  # Мы проверяем первые три вопроса
        await message.answer("К сожалению, вы не прошли проверку. Попробуйте позже.")
        del user_answers[user_id]  # Удаляем ответы, чтобы пользователь мог начать заново
    else:
        await message.answer("Вы прошли проверку! Вот доступные питомцы:")
        await show_pet(user_id, message)  # Показываем доступных питомцев

# Словарь для хранения текущего питомца для каждого пользователя
user_pets_index = {}

# Функция для показа питомца
async def show_pet(user_id, message, pet_index=0):
    if user_id not in user_pets_index:
        user_pets_index[user_id] = pet_index  # Изначально показываем первого питомца

    pet_index = user_pets_index[user_id]  # Получаем текущий питомец
    pet = pets[pet_index]  # Получаем данные питомца
    media = InputMediaPhoto(media=pet["photo"],
                            caption=f"Имя: {pet['name']}\nОписание: {pet['desc']}\nВозраст: {pet['age']} лет")

    # Отправляем фото питомца и его описание
    await message.answer_media_group([media])

    # Клавиатура для навигации по питомцам
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"back_{pet_index}")],  # Кнопка для перехода назад
        [InlineKeyboardButton(text="Следующий", callback_data=f"skip_{pet_index}")],  # Кнопка для перехода к следующему питомцу
        [InlineKeyboardButton(text="Выбрать", callback_data=f"adopt_{pet['id']}")]  # Кнопка для выбора питомца
    ])

    # Если это первый питомец, убираем кнопку "Назад"
    if pet_index == 0:
        keyboard.inline_keyboard[0] = [InlineKeyboardButton(text="Назад", callback_data="no_back")]

    await message.answer(f"Вы смотрите на питомца {pet['name']}. Что вы хотите сделать?", reply_markup=keyboard)

# Когда пользователь нажимает на кнопку "Следующий", показываем следующего питомца
@dp.callback_query(lambda c: c.data.startswith("skip_"))
async def skip_pet(callback: types.CallbackQuery):
    pet_index = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    # Переходим к следующему питомцу
    if pet_index + 1 < len(pets):
        user_pets_index[user_id] = pet_index + 1
        await show_pet(user_id, callback.message, pet_index + 1)
    else:
        await callback.message.answer("Все питомцы просмотрены. Вы можете выбрать одного из них.")
    await callback.answer()

# Когда пользователь нажимает на кнопку "Назад", показываем предыдущего питомца
@dp.callback_query(lambda c: c.data.startswith("back_"))
async def back_pet(callback: types.CallbackQuery):
    pet_index = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    # Переходим к предыдущему питомцу
    if pet_index > 0:
        user_pets_index[user_id] = pet_index - 1
        await show_pet(user_id, callback.message, pet_index - 1)
    else:
        await callback.message.answer("Вы уже на первом питомце.")
    await callback.answer()

# Когда пользователь нажимает на кнопку "Выбрать", питомец выбирается
@dp.callback_query(lambda c: c.data.startswith("adopt_"))
async def adopt_pet(callback: types.CallbackQuery):
    pet_id = int(callback.data.split("_")[1])
    pet = next((p for p in pets if p["id"] == pet_id), None)

    if pet:
        await callback.message.answer(f"Поздравляем! Вы выбрали {pet['name']}. Приют скоро с вами свяжется!")
    else:
        await callback.message.answer("Ошибка! Питомец не найден.")
    await callback.answer()

# Функции для пожертвования
@dp.message(lambda msg: msg.text == "Пожертвовать")
async def donate_start(message: types.Message):
    await message.answer("Введите сумму, которую хотите пожертвовать (в сомах):")

@dp.message(lambda msg: msg.text.isdigit())
async def donate_process(message: types.Message):
    amount = int(message.text)

    if amount < 10:
        await message.answer("Минимальная сумма пожертвования — 10 сом. Попробуйте снова.")
        return

    donations[message.from_user.id] = amount
    await message.answer(f"Спасибо за ваше пожертвование в размере {amount} сом! ❤️")

