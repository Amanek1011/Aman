from aiogram.types import InlineKeyboardButton
from aiogram import types

reply_menu = types.ReplyKeyboardMarkup(
    keyboard=[
            [
                types.KeyboardButton(text='📰 Новости'),
                types.KeyboardButton(text='🌎 Благотворительные фонды'),
            ],
        ],
        resize_keyboard=True,
)


inline_news = types.InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='За сегодня ', callback_data='today')],[InlineKeyboardButton(text='За вчера', callback_data='yesterday')],
    ]
)