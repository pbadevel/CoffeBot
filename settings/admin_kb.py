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
        InlineKeyboardButton(text='Персонал', callback_data='admin_staff'),
        InlineKeyboardButton(text='Рассылка', callback_data='admin_send'),
        width=1
    ).as_markup()


def back_to_main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Назад', callback_data='admin_back'),
        width=1
    ).as_markup()