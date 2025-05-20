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
        try:
            action, data = decode_payload(command.args).split('_')
            user_id = int(data)
        except:
            await message.answer(lexicon.WRONG_QR_TEXT)
            return
        
        if action == 'role': 
            role = ProjectUtils.decode_phrase(user_id)
            new_barista = None

            if message.from_user.id in config.ADMIN_IDS:
                await message.answer('Вы являетесь админом, но вы можете считывать qr так же как и <b>БАРИСТА</b>')
                return

            if role == UserRole.barista:
                new_barista = await req.update_user(
                    user_id=message.from_user.id,
                    role=UserRole.barista
                )
            
            if new_barista:
                for admin_id in config.ADMIN_IDS:
                    try:
                        await message.bot.send_message(
                            chat_id=admin_id,
                            text=f'Новый <b>БАРИСТА</b> - {"@"+new_barista.username if new_barista.username else new_barista.fullname}!'
                        )
                    except:
                        pass
            
            await message.answer('Поздравляем! Вам выдали роль БАРИСТА!\n\nЗапустите бота с новыми функциями!', 
                                 reply_markup=barista_kb.main())
            return
        


        if action == 'ref':
            referrer = await req.get_user_by_id(user_id)
            all_referrals_ids = []
            [[all_referrals_ids.append(int(j)) for j in i.referral_ids.split(',') if j!=''] for i in await req.get_users() if i.referral_ids]
            
            if referrer.user_id == message.from_user.id:
                await message.answer(lexicon.CANT_INVITE_YOURSELF_TEXT)
                return
            elif referrer.referral_ids and (message.from_user.id in all_referrals_ids):
                await message.answer(
                    text=lexicon.ALREADY_REF_TEXT.format(
                        name = "@"+message.from_user.username or message.from_user.full_name
                    )
                )
                return
            
            if not referrer.referral_ids:
                referrer.referral_ids = ''

            # Update referrer
            await req.update_user(
                user_id = referrer.user_id,
                # cups = referrer.cups + 1,
                referral_ids = referrer.referral_ids + str(message.from_user.id) + ','
            )

            await message.bot.send_message(
                chat_id = referrer.user_id,
                text = lexicon.REFERRER_TEXT.format(
                    name="@"+message.from_user.username if message.from_user.username else message.from_user.full_name
                )
            )

            # Update new user
            await req.update_user(
                user_id = message.from_user.id,
                referrer_id=referrer.user_id
            )
            
            await message.answer(
                text = lexicon.REFERRAL_TEXT.format(
                    name = "@"+message.from_user.username if message.from_user.username else message.from_user.full_name
                ),
                reply_markup = user_kb.main()
            )

            return



        if user.role == UserRole.user:
 
            await message.answer(
                text = lexicon.NOT_BARISTA_TEXT.format(
                    support = config.SUPPORT_USERNAME
                ),
                reply_markup=user_kb.back_to_main() 
            )

            return



        try:
            current_user = await req.get_user_by_id(user_id)
        except:
            await message.answer(lexicon.NO_SUCH_USER_TEXT)
            return
        

        if current_user.cups >= 9:
            await message.answer(
                text = lexicon.MANY_CUPS_TEXT.format(
                    name = "@"+current_user.username if current_user.username else current_user.fullname,
                    cups = current_user.cups
                ),
                reply_markup = barista_kb.choose_cup_action(user_id = user_id)
            )
            return
        

        await message.answer(
            text = lexicon.ADD_A_CUP_TEXT.format(
                name = "@"+current_user.username if current_user.username else current_user.fullname,
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
    await cb.answer()

    action = cb.data.split('_')[-1]

    # Send Qr
    if action == 'qr':
        qr = await ProjectUtils.generate_qrcode(
            payload = await create_start_link(
                bot = cb.bot,
                payload='qr_'+str(cb.from_user.id),
                encode=True
                )
        )

        await cb.message.answer_photo(photo=qr, reply_markup=user_kb.back_to_main_from_qr())

    # Rules
    elif action == 'rules':
        try:
            await cb.message.edit_text(lexicon.RULES_TEXT, reply_markup=user_kb.back_to_main())
        except:
            await cb.message.answer(lexicon.RULES_TEXT, reply_markup=user_kb.back_to_main())

    # Referral system
    elif action == 'ref':
        try:
            await cb.message.edit_text(
                text=lexicon.REFERRAL_SYSTEM_TEXT.format(
                    referral_link = await create_start_link(
                        bot=cb.bot,
                        payload="ref_"+str(cb.from_user.id),
                        encode=True
                    )
                ), reply_markup=user_kb.back_to_main())
        except:
            await cb.message.answer(lexicon.REFERRAL_SYSTEM_TEXT, reply_markup=user_kb.back_to_main())
        
    # Show User Profile
    elif action == 'profile':
        user = await req.get_user_by_id(cb.from_user.id)
        try:
            await cb.message.edit_text(
                text=lexicon.USER_PROFILE_TEXT.format(
                    name = user.fullname,
                    username = f"[@{user.username}]" if user.username else '',
                    cups = user.cups,
                    cups_remain = 9 - user.cups if user.cups < 10 else 0,
                    referrals = len([i for i in user.referral_ids.split(',') if i!='']) if user.referral_ids else 0
                ),
                reply_markup=user_kb.back_to_main()
            )
        except:
            await cb.message.answer(
                text=lexicon.USER_PROFILE_TEXT.format(
                    name = user.fullname,
                    username = f"[@{user.username}]" if user.username else '',
                    cups = user.cups,
                    referrals = len([i for i in user.referral_ids.split(',') if i!='']) if user.referral_ids else 0
                ),
                reply_markup=user_kb.back_to_main()
            )
    # To Delete QR
    elif action == 'backqr':
        await cb.message.delete()

    # Back Button
    else:
        try:
            await cb.message.edit_text(lexicon.START_USER_TEXT, reply_markup=user_kb.main())
        except:
            await cb.message.answer(lexicon.START_USER_TEXT, reply_markup=user_kb.main())

