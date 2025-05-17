from aiogram.fsm.state import State, StatesGroup, default_state



class Personal(StatesGroup):
    id_tg_personal = State()
    id_tg_ban = State()


class Mailing(StatesGroup):
    waiting_for_post=State()