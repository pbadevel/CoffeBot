from aiogram import Router, types, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload

from database import req
from settings import config, lexicon, user_kb, admin_kb, barista_kb

from utils.ProjectEnums import UserRole
from utils import ProjectUtils




router = Router()



@router.message(CommandStart())
async def start(message: types.Message, command: CommandObject):
    
    role = UserRole.user
    user = await req.get_user_by_id(message.from_user.id)
    
    if message.from_user.id in config.ADMIN_IDS:
        role = UserRole.admin
    
    if user:
        if user.role == UserRole.barista:
            role = user.role

    await req.add_user(
        user_id = message.from_user.id,
        username = message.from_user.username,
        fullname = message.from_user.full_name,
        role = role
    )
    

    if command.args:
        # QR CODE HERE
        
        if user.role != UserRole.barista:
            await message.answer(
                text = 'Вы не являетесь'\
                       'баристой кофейни'\
                       'если это не так -'\
                       ' свяжитесь с поддержкой ',
                reply_markup=user_kb.back_to_main()
            )\
            \
             if user.role == UserRole.user else \
            \
            await message.answer(
                text = 'Вы не являетесь'\
                       'баристой кофейни'\
                       'если это не так -'\
                       ' свяжитесь с поддержкой ',
                reply_markup=admin_kb.back_to_main()
            )
            return
        
        try:
            user_id = int(decode_payload(command.args))
        except:
            await message.answer('Не правильный QR-код!')
            return
        
        try:
            current_user = await req.get_user_by_id(user_id)
        except:
            await message.answer('Данного пользователя нет в боте!\nПользователь должен <b>обязательно</b> нажать на кнопку "START"')
            return
        

        if current_user.cups >= 10:
            await message.answer(
                text = lexicon.MANY_CUPS_TEXT.format(
                    name = current_user.username or current_user.fullname,
                    cups = current_user.cups
                ),
                reply_markup = barista_kb.choose_cup_action(user_id = user_id)
            )
            return
        

        await message.answer(
            text = lexicon.ADD_A_CUP_TEXT.format(
                name = current_user.username or current_user.fullname,
                cups = current_user.cups
            ),
            reply_markup = barista_kb.confirm_a_cup(user_id = user_id)
        )

        return
    

    if role == UserRole.barista:
        await message.answer(lexicon.START_BARISTA_TEXT, reply_markup=barista_kb.main())
    elif role == UserRole.admin:
        await message.answer(lexicon.START_ADMIN_TEXT, reply_markup=admin_kb.main())
    else:
        await message.answer(lexicon.START_USER_TEXT, reply_markup=user_kb.main())











@router.callback_query(F.data.startswith('user_'))
async def user_handler(cb: types.CallbackQuery):
    
    action = cb.data.split('_')[-1]

    # Send Qr
    if action == 'qr':
        qr = await ProjectUtils.generate_qrcode(
            payload = await create_start_link(
                bot = cb.bot,
                payload=str(cb.from_user.id),
                encode=True
                )
        )

        await cb.message.answer_photo(photo=qr, reply_markup=user_kb.back_to_main())

    # Rules
    elif action == 'rules':
        try:
            await cb.message.edit_text(lexicon.RULES_TEXT, reply_markup=user_kb.back_to_main())
        except:
            await cb.message.answer(lexicon.RULES_TEXT, reply_markup=user_kb.back_to_main())

    # Referral system
    elif action == 'ref':
        try:
            await cb.message.edit_text(lexicon.REFERRAL_SYSTEM_TEXT, reply_markup=user_kb.back_to_main())
        except:
            await cb.message.answer(lexicon.REFERRAL_SYSTEM_TEXT, reply_markup=user_kb.back_to_main())
        
    # Back Button
    else:
        try:
            await cb.message.edit_text(lexicon.START_USER_TEXT, reply_markup=user_kb.main())
        except:
            await cb.message.answer(lexicon.START_USER_TEXT, reply_markup=user_kb.main())

