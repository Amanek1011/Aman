 import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv


# Загружаем токен для бота из файла .env
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Читаем токен из файла .env
bot = Bot(token=TOKEN)  # Создаем объект бота
dp = Dispatcher()  # Создаем диспетчера для работы с ботом

# Вопросы анкеты
questions = [
    {"text": "Вы готовы заботиться о питомце всю его жизнь?", "buttons": ["Да", "Нет"]},
    {"text": "Готовы ли вы посещать ветеринара в случае необходимости?", "buttons": ["Да", "Нет"]},
    {"text": "Вы можете обеспечить питомцу комфортные условия жизни?", "buttons": ["Да", "Нет"]},
]

# Словари для хранения данных
user_answers = {}  # Здесь будут храниться ответы пользователей на вопросы анкеты
donations = {}  # Здесь будут храниться данные о пожертвованиях

# Список питомцев с их данными (имя, описание, возраст, фото)
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

# Фиксированный номер телефона питомника
shelter_phone = "+88005553535"

logging.basicConfig(level=logging.INFO)  # Настроим логирование для отладки

# Когда пользователь пишет команду /start, бот выводит кнопки для выбора
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Забрать питомца")],
            [KeyboardButton(text="Пожертвовать")],
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Я бот помощи животным. Ты хочешь забрать питомца или сделать пожертвование?", reply_markup=keyboard)

# Когда пользователь нажимает кнопку "Забрать питомца", начинается анкета
@dp.message(lambda msg: msg.text == "Забрать питомца")
async def start_survey(message: types.Message):
    user_answers[message.from_user.id] = []
    await ask_question(message.from_user.id, message)

# Функция для вывода вопросов анкеты
async def ask_question(user_id, message):
    q_index = len(user_answers[user_id])

    if q_index < len(questions):
        question = questions[q_index]
        keyboard = InlineKeyboardBuilder()
        for option in question["buttons"]:
            keyboard.button(text=option, callback_data=f"answer_{q_index}_{option}")

        await message.answer(question["text"], reply_markup=keyboard.as_markup())
    else:
        await analyze_answers(user_id, message)

# Когда пользователь нажимает на кнопку с ответом
@dp.callback_query(lambda c: c.data.startswith("answer_"))
async def handle_answer(callback: types.CallbackQuery):
    _, q_index, answer = callback.data.split("_", 2)
    user_id = callback.from_user.id
    user_answers[user_id].append(answer)

    await callback.answer()
    await ask_question(user_id, callback.message)

# Функция для анализа ответов пользователя
async def analyze_answers(user_id, message):
    answers = user_answers[user_id]

    # Если в ответах есть "Нет", значит пользователь не готов заботиться о питомце
    if "Нет" in answers[:3]:
        await message.answer("К сожалению, вы не прошли проверку. Попробуйте позже.")
        del user_answers[user_id]  # Удаляем ответы, чтобы пользователь мог начать заново
    else:
        await message.answer("Вы прошли проверку! Вот доступные питомцы:")
        await show_pet(user_id, message)

# Словарь для хранения текущего питомца для каждого пользователя
user_pets_index = {}

# Функция для показа питомца
# Функция для показа питомца
async def show_pet(user_id, message, pet_index=0):
    # Если пользователь еще не просматривал питомцев, устанавливаем индекс в 0
    if user_id not in user_pets_index or pet_index == 0:
        user_pets_index[user_id] = 0

    pet_index = user_pets_index[user_id]
    pet = pets[pet_index]
    media = InputMediaPhoto(media=pet["photo"],
                            caption=f"Имя: {pet['name']}\nОписание: {pet['desc']}\nВозраст: {pet['age']} лет")

    await message.answer_media_group([media])

    # Клавиатура для навигации по питомцам
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"back_{pet_index}")] if pet_index > 0 else [],
        [InlineKeyboardButton(text="Следующий", callback_data=f"skip_{pet_index}")] if pet_index < len(pets) - 1 else [],
        [InlineKeyboardButton(text="Выбрать", callback_data=f"adopt_{pet['id']}")]
    ])

    await message.answer(f"Вы смотрите на питомца {pet['name']}. Что вы хотите сделать?", reply_markup=keyboard)


# Когда пользователь нажимает на кнопку "Выбрать", питомец выбирается
@dp.callback_query(lambda c: c.data.startswith("adopt_"))
async def adopt_pet(callback: types.CallbackQuery):
    pet_id = int(callback.data.split("_")[1])
    pet = next((p for p in pets if p["id"] == pet_id), None)

    if pet:
        await callback.message.answer(f"Поздравляем! Вы выбрали {pet['name']}. Приют скоро с вами свяжется!")
        await callback.message.answer(f"Для связи с приютом звоните по номеру: {shelter_phone}")
    else:
        await callback.message.answer("Ошибка! Питомец не найден.")
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("skip_"))
async def next_pet(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_index = int(callback.data.split("_")[1])

    if current_index + 1 < len(pets):  # Проверяем, что есть следующий питомец
        user_pets_index[user_id] = current_index + 1
        await show_pet(user_id, callback.message, pet_index=current_index + 1)
    else:
        await callback.message.answer("Это последний питомец в списке.")

    await callback.answer()


# Когда пользователь нажимает кнопку "Назад", бот показывает предыдущего питомца
@dp.callback_query(lambda c: c.data.startswith("back_"))
async def previous_pet(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_index = int(callback.data.split("_")[1])

    if current_index > 0:  # Проверяем, что есть предыдущий питомец
        user_pets_index[user_id] = current_index - 1
        await show_pet(user_id, callback.message, pet_index=current_index - 1)
    else:
        await callback.message.answer("Это первый питомец в списке.")

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
    await message.answer(f"Для связи с приютом звоните по номеру: {shelter_phone}")

# Запуск бота
if __name__ == "__main__":
    print("Starting")
    import asyncio

    async def main():
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)

    asyncio.run(main())

