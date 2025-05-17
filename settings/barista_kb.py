from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, 
    ReplyKeyboardBuilder
)
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton
)





def main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Мой Профиль', callback_data='barista_profile'),
        width=1
    ).as_markup()