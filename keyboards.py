from aiogram.types import InlineKeyboardButton
from aiogram import types

reply_menu = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text='📰 Новости'),
                types.KeyboardButton(text='🌎 Благотворительные фонды'),
            ],
            [
                types.KeyboardButton(text='📚 Подготовка к ОРТ')
            ]
        ],
        resize_keyboard=True,
)


inline_news = types.InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='За сегодня ', callback_data='today')],[InlineKeyboardButton(text='За вчера', callback_data='yesterday')],
    ]
)

inline_ai = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🗺 География', callback_data='geography')],[InlineKeyboardButton(text='💻 Информатика', callback_data='informatics')],
        [InlineKeyboardButton(text='🇷🇺 Русский язык',callback_data='russian')],[InlineKeyboardButton(text='🇺🇸 Английский язык', callback_data='english')],
    ],
)