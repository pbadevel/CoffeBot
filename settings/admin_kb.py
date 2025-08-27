from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, 
    InlineKeyboardMarkup
)
from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton
)

from utils.ProjectEnums import UserRole




def main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Персонал', callback_data='adminMain_staff'),
        InlineKeyboardButton(text='Рассылка', callback_data='adminMain_send'),
        width=1
    ).as_markup()


def back_to_main():
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(text='Назад', callback_data='adminMain_mainback'),
        width=1
    ).as_markup()


def confirm_send_post():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить",callback_data=f"post_confirm")],
        [InlineKeyboardButton(text="Отменить", callback_data=f"post_cncl")]
    ])

    










# Personal



def keyboard_select_role() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора роли для редактирования
    :return:
    """
    button_1 = InlineKeyboardButton(text='Бариста',
                                    callback_data=f'edit_list_{UserRole.barista}')
    button_2 = InlineKeyboardButton(text="Назад", callback_data="admin_mainback")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    
    return keyboard


def keyboard_select_action() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора действия которое нужно совершить с ролью
    :return:
    """
    button_1 = InlineKeyboardButton(text='Назначить',
                                    callback_data='personal_add')
    button_2 = InlineKeyboardButton(text='Разжаловать',
                                    callback_data='personal_delete')
    button_3 = InlineKeyboardButton(text="Назад", callback_data="adminMain_mainback")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2], [button_3]])
    return keyboard


def keyboards_add_admin(list_admin, back, forward, count) -> InlineKeyboardMarkup:
    """
    Клавиатура с пагинацией для добавления персонала
    :param list_admin:
    :param back:
    :param forward:
    :param count:
    :return:
    """

    # проверка чтобы не ушли в минус
    if back < 0:
        back = 0
        forward = 2
    # считаем сколько всего блоков по заданному количество элементов в блоке
    count_users = len(list_admin)
    whole = count_users // count
    remains = count_users % count
    max_forward = whole + 1
    # если есть остаток то, увеличиваем количество блоков на один, чтобы показать остаток
    if remains:
        max_forward = whole + 2
    if forward > max_forward:
        forward = max_forward
        back = forward - 2
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for row in list_admin[back*count:(forward-1)*count]:
        text = row[1]
        button = f'admin_add_{row[0]}'
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    button_back = InlineKeyboardButton(text='<<<<',
                                       callback_data=f'admin_back_{str(back)}')
    button_count = InlineKeyboardButton(text=f'{back+1}',
                                        callback_data='none')
    button_next = InlineKeyboardButton(text='>>>>',
                                       callback_data=f'admin_forward_{str(forward)}')

    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_count, button_next)
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data="adminMain_mainback"), width=1)

    return kb_builder.as_markup()


def keyboard_add_list_personal() -> InlineKeyboardMarkup:
    """
    Клавиатура для подтверждения добавления пользователя в список персонала
    :return:
    """
    button_1 = InlineKeyboardButton(text='Назначить',
                                    callback_data='add_personal_list')
    button_2 = InlineKeyboardButton(text='Отменить',
                                    callback_data='not_add_personal_list')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])
    return keyboard


# АДМИНИСТРАТОРЫ -> Разжаловать
def keyboards_del_admin(list_admin, back, forward, count):
    
    # проверка чтобы не ушли в минус
    if back < 0:
        back = 0
        forward = 2
    # считаем сколько всего блоков по заданному количество элементов в блоке
    count_users = len(list_admin)
    whole = count_users // count
    remains = count_users % count
    max_forward = whole + 1
    # если есть остаток, то увеличиваем количество блоков на один, чтобы показать остаток
    if remains:
        max_forward = whole + 2
    if forward > max_forward:
        forward = max_forward
        back = forward - 2
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for row in list_admin[back*count:(forward-1)*count]:

        buttons.append(InlineKeyboardButton(
            text=str(row[1]),
            callback_data=f'controller_del_{row[0]}'
            )
        )
        

    button_back = InlineKeyboardButton(text='<<<<',
                                       callback_data=f'admin_del_back_{str(back)}')
    button_count = InlineKeyboardButton(text=f'{back+1}',
                                        callback_data='none')
    button_next = InlineKeyboardButton(text='>>>>',
                                       callback_data=f'admin_del_forward_{str(forward)}')

    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_count, button_next)
    kb_builder.row(InlineKeyboardButton(text="Назад", callback_data="adminMain_mainback"), width=1)

    return kb_builder.as_markup()


# АДМИНИСТРАТОРЫ -> Разжаловать -> подтверждение добавления админа в список админов
def keyboard_del_list_admins() -> InlineKeyboardMarkup:
    """
    Клавиатура для разжалования пользователя в список администраторов
    :return:
    """
    button_1 = InlineKeyboardButton(text='Разжаловать',
                                    callback_data='del_personal_list')
    button_2 = InlineKeyboardButton(text='Отменить',
                                    callback_data='not_del_personal_list')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])
    return keyboard
