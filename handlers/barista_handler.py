from aiogram import Router, types, F

from database import req

from settings import lexicon


router = Router()



@router.callback_query(F.data.startswith('addAcup_'))
async def handle_confirm_a_cup(cb: types.CallbackQuery):
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