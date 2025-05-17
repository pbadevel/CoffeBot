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
        InlineKeyboardButton(text='Профиль', callback_data='user_profile'),
        InlineKeyboardButton(text='Система лояльности', callback_data='user_rules'),
        InlineKeyboardButton(text='Реферальная система', callback_data='user_ref'),
        width=1
    ).as_markup()



def back_to_main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Назад', callback_data='user_back'),
        width=1
    ).as_markup()

def back_to_main_from_qr():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Назад', callback_data='user_backqr'),
        width=1
    ).as_markup()