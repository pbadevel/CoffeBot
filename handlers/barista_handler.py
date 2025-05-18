from aiogram import Router, types, F

from database import req

from settings import lexicon, barista_kb

from security import filter


router = Router()



@router.callback_query(F.data.startswith('barista_'), filter.BaristaProtect())
async def handle_barista(cb: types.CallbackQuery):
    await cb.answer()

    action = cb.data.split('_')[-1]
    

    if action == 'profile':
        user = await req.get_user_by_id(cb.from_user.id)
        try:
            await cb.message.edit_text(
                text=lexicon.BARISTA_PROFILE_TEXT.format(
                    name = user.fullname,
                    username = f"[@{user.username}]" if user.username else '',
                ),
                reply_markup=barista_kb.back_to_main()
            )
        except:
            await cb.message.answer(
                text=lexicon.BARISTA_PROFILE_TEXT.format(
                    name = user.fullname,
                    username = f"[@{user.username}]" if user.username else '',
                ),
                reply_markup=barista_kb.back_to_main()
            )
    else:
        try:
            await cb.message.edit_text(lexicon.START_BARISTA_TEXT, reply_markup=barista_kb.main())
        except:
            await cb.message.answer(lexicon.START_BARISTA_TEXT, reply_markup=barista_kb.main())



@router.callback_query(F.data.startswith('addAcup_'), filter.BaristaProtect())
async def handle_confirm_a_cup(cb: types.CallbackQuery):
    await cb.answer()

    action = cb.data.split('_')[-2]
    

    # Add Points
    if action == 'confirm':
        user_id = int(cb.data.split('_')[-1])
        user = await req.get_user_by_id(user_id)
        
        user = await req.update_user(
            user_id=user_id,
            cups=user.cups + 1
        )
        if user:
            await cb.message.edit_text(
                text=lexicon.SUCCESS_ADD_A_CUP_TEXT.format(
                    cups = user.cups
                ))
    
    # Deduct Points
    elif action == 'deduct':
        user_id = int(cb.data.split('_')[-1])
        user = await req.get_user_by_id(user_id)
        
        user = await req.update_user(
            user_id=user_id,
            cups=user.cups - 10
        )
        if user:
            await cb.message.edit_text(
                text=lexicon.SUCCESS_DEDUCT_A_CUP_TEXT.format(
                    cups = user.cups
                )
            )

    # Cancel
    else:
        await cb.message.edit_text(lexicon.CANCEL_TEXT)