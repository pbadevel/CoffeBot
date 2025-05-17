from aiogram import Router, types, F
from aiogram.filters import CommandStart, CommandObject

from database import req
from settings import config, lexicon, user_kb, admin_kb, barista_kb
from utils.ProjectEnums import UserRoleEnum


router = Router()



@router.message(CommandStart())
async def start(message: types.Message, command: CommandObject):
    
    role = UserRoleEnum.user.value
    user = await req.get_user_by_id(message.from_user.id)
    
    if message.from_user.id in config.ADMIN_IDS:
        role = UserRoleEnum.admin.value
    
    if user:
        if user.role == UserRoleEnum.barista.value:
            role = UserRoleEnum.barista.value

    await req.add_user(
        user_id = message.from_user.id,
        username = message.from_user.username,
        fullname = message.from_user.full_name,
        role = role
    )
    

    if command.args:
        # QR CODE HERE
        return
    

    if role == UserRoleEnum.barista.value:
        await message.answer(lexicon.START_BARISTA_TEXT, reply_markup=barista_kb.main())
    elif role == UserRoleEnum.admin.value:
        await message.answer(lexicon.START_ADMIN_TEXT, reply_markup=admin_kb.main())
    else:
        await message.answer(lexicon.START_USER_TEXT, reply_markup=user_kb.main())
