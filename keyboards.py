from aiogram.types import InlineKeyboardButton
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

reply_menu = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text='📰 Сервисы'),
                types.KeyboardButton(text='🌎 Благотворительные фонды'),
            ],
            [
                types.KeyboardButton(text='💼 Юридический помощник'),
                types.KeyboardButton(text='🦮 Питомник'),
            ],
        ],
        resize_keyboard=True,
)


inline_news = types.InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='За сегодня ', callback_data='today')],[InlineKeyboardButton(text='За вчера', callback_data='yesterday')],
    ]
)



def get_ort_subjects_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="География", callback_data="geography")
    builder.button(text="Информатика", callback_data="informatics")
    builder.button(text="Русский язык", callback_data="russian")
    builder.button(text="Английский язык", callback_data="english")
    builder.adjust(2)
    return builder.as_markup()

inline_ort_subjects = get_ort_subjects_keyboard()

reply_service = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🌤 Погода"), types.KeyboardButton(text="💱 Курс валют")],
        [types.KeyboardButton(text="📰 Новости"), types.KeyboardButton(text="↩️ Назад")]
    ],
    resize_keyboard=True,
)