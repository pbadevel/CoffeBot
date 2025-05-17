from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, 
    ReplyKeyboardBuilder
)
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton
)



def _():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='', callback_data=''),
        width=1
    ).as_markup()



def main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Мой Профиль', callback_data='barista_profile'),
        width=1
    ).as_markup()

def back_to_main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Назад', callback_data='barista_back'),
        width=1
    ).as_markup()


def confirm_a_cup(user_id):
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='✅', callback_data=f'addAcup_confirm_{user_id}'),
        InlineKeyboardButton(text='❌', callback_data=f'addAcup_decline_{user_id}'),
        width=2
    ).as_markup()

def choose_cup_action(user_id):
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='✅ Начислить ✅', callback_data=f'addAcup_confirm_{user_id}'),
        InlineKeyboardButton(text='❌ Списать баллы ❌', callback_data=f'addAcup_deduct_{user_id}'),
        InlineKeyboardButton(text='❌ Отмена ❌', callback_data=f'addAcup_decline_{user_id}'),
        width=1
    ).as_markup()
