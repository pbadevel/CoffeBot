from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, 
    ReplyKeyboardBuilder
)
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton
)

from settings import config





def reply_back_main():
    return ReplyKeyboardBuilder().row(
        KeyboardButton(text='Главное Меню'),
        width=1
    ).as_markup(resize_keyboard=True)


def main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Мой QR', callback_data='user_qr'),
        InlineKeyboardButton(text='Профиль', callback_data='user_profile'),
        InlineKeyboardButton(text='Система лояльности', callback_data='user_rules'),
        InlineKeyboardButton(text='Реферальная система', callback_data='user_ref'),
        InlineKeyboardButton(text='Поддержка', url=f'{config.SUPPORT_USERNAME}.t.me'),
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