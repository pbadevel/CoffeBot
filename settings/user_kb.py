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
        InlineKeyboardButton(text='Мой QR', callback_data='user_qr'),
        InlineKeyboardButton(text='Система лояльности', callback_data='user_rules'),
        InlineKeyboardButton(text='Реферальная система', callback_data='user_qr'),
        width=1
    ).as_markup()