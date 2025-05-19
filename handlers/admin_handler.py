from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

from settings.AdminStates import Personal, Mailing
from settings import admin_kb, lexicon

from utils.ProjectEnums import UserRole
from utils import ProjectUtils

from security import filter

from database import req







router = Router()
router.message.middleware(filter.AlbumMiddleware())




@router.callback_query(F.data.startswith('admin_'))
async def handle_admin(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    action = callback.data.split('_')[-1]
    
    # Change Staff
    if action == 'staff':
        try:
            await callback.message.edit_text(text="Выберите роль которую вы хотите изменить.",
                                            reply_markup=admin_kb.keyboard_select_role())
        except:
            await callback.message.answer(text="Выберите роль которую вы хотите изменить.",
                                        reply_markup=admin_kb.keyboard_select_role())
    
    # Send any to Users
    elif action == 'send':
            await callback.message.edit_text("Пришлите сообщение для рассылки\n\n<b>Поддерживается:</b>\nФото, видео, текст - в разных вариациях.\n<b>Макс кол-во медиа - 10шт.</b>", reply_markup=admin_kb.back_to_main())
            await state.set_state(Mailing.waiting_for_post)

    
    # Back
    else:
        try:await state.clear()
        except:pass
             
        try:
            await callback.message.edit_text(text=lexicon.START_ADMIN_TEXT,
                                            reply_markup=admin_kb.main())
        except:
            await callback.message.answer(text=lexicon.START_ADMIN_TEXT,
                                        reply_markup=admin_kb.main())
    

    


@router.message(Mailing.waiting_for_post, F.photo)
@router.message(Mailing.waiting_for_post, F.video)
@router.message(Mailing.waiting_for_post, F.text)
async def mailing_2(message: types.Message, state: FSMContext, album: list=None):
    media_group = []
    media_for_preview_list = []
    if album:
        count_photos = len(album)
        await message.reply(f"всего {count_photos} медиа файлов")
        
        for idx, msg in enumerate(album):
            
            if msg.photo:
                media_for_preview = types.InputMediaPhoto(media=msg.photo[-1].file_id)
                media = "p!"+msg.photo[-1].file_id
            elif msg.video:
                media_for_preview =types.InputMediaVideo(media=msg.video.file_id)
                media = "v!"+msg.video.file_id
            else:
                continue
            
            if idx == 0:
                caption = msg.caption or None
                media_for_preview.caption = msg.caption
            
            media_group.append(media)
            media_for_preview_list.append(media_for_preview)
        
        await message.bot.send_media_group(chat_id=message.from_user.id, media=media_for_preview_list)
        await state.update_data(
                media_ids=media_group,
                text=caption,
                isOnlyText=0
            )

    else:
        isOnlyText = 1
        if message.photo:
            await state.update_data(media_ids="p!"+message.photo[-1].file_id, text=None)
            if message.caption:
                await state.update_data(text=message.caption)
                await message.answer_photo(photo=message.photo[-1].file_id, caption=message.caption)
                isOnlyText = 0
            else:
                await message.answer_photo(photo=message.photo[-1].file_id)

        if message.video:
            await state.update_data(media_ids="v!"+message.video.file_id, text=None)
            if message.caption:
                await state.update_data(text=message.caption)
                isOnlyText = 0
                await message.answer_video(video=message.video.file_id, caption=message.caption)
            else:
                await message.answer_video(video=message.video.file_id)
    
        if message.text:
            await state.update_data(text=message.text)
            await state.update_data(media_ids="")
            isOnlyText = 1
            await message.answer(message.text)

        await state.update_data(isOnlyText=isOnlyText)


    await message.answer('Подтвердите отправку поста ВСЕМ пользователям', reply_markup=admin_kb.confirm_send_post())
    



@router.callback_query(F.data.startswith('post_'))
async def handle_post(cb: types.CallbackQuery, state: FSMContext):
    confirm = cb.data.split('_')[-1]
    await cb.answer()

    try:
        data = await state.get_data()
        media_ids = data['media_ids']
        text = data['text']
        try:
            isOnlyText = data['isOnlyText']
        except:
            isOnlyText = 0
    except:
        await cb.message.edit_text('Запрос устарел!', reply_markup=admin_kb.back_to_main())
        return
    
    await state.clear()
    
    if confirm == 'confirm':
        users = [i for i in await req.get_users() if i.role == UserRole.user]

        if media_ids == '' and isOnlyText:
            for user in users:
                try:
                    await cb.bot.send_message(
                        chat_id=user.user_id,
                        text=text
                    )
                except:
                    continue

                
        elif len(media_ids)>0:
            if type(media_ids) == list:
                media_group = ProjectUtils.create_media_group(
                    list_media_id=media_ids,
                    caption=text
                    )
            else:
                media_group = ProjectUtils.create_media_group(
                    list_media_id=[media_ids],
                    caption=text
                    )

            for user in users:
                await cb.bot.send_media_group(
                    chat_id=user.user_id, 
                    media=media_group
                )
                
        await cb.message.edit_text("Рассылка завершена успешно!", reply_markup=admin_kb.back_to_main())
    else:
        await cb.message.edit_text("Отмена рассылки!", reply_markup=admin_kb.back_to_main())








# PERSONAL
@router.callback_query(F.data.startswith('edit_list_'))
async def process_select_action(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Выбор действия которое нужно совершить с ролью при редактировании
    :param callback:
    :param state:
    :return:
    """
    edit_role = callback.data.split('_')[2]

    role = "<b>БАРИСТА</b>"
   
    await state.update_data(edit_role=edit_role)
    await callback.message.edit_text(text=f"Добавить или удалить {role}?",
                                     reply_markup=admin_kb.keyboard_select_action())
    await callback.answer('')


@router.callback_query(F.data == 'personal_add')
async def process_personal_add(callback: types.CallbackQuery, state: FSMContext) -> None:

    data = await state.get_data()
    edit_role = data['edit_role']
    role = "<b>БАРИСТА</b>"

    await callback.message.edit_text(text=f'Пришлите Telegram ID пользователя для назначения его {role}.\n\n'
                                          f'❗️<b>Пользователь должен запустить бота</b>❗️\n\n'
                                          f'Получить Telegram ID пользователя можно при помощи бота: '
                                          f'@getmyid_bot или @username_to_id_bot', reply_markup=admin_kb.back_to_main())
    await state.set_state(Personal.id_tg_personal)


@router.message(Personal.id_tg_personal, F.text)
async def get_id_tg_personal(message: types.Message, state: FSMContext):
    """
    Получаем id телеграм для добавления в список персонала
    :param message:
    :param state:
    :return:
    """
    if not message.text.isdigit():
        await message.answer('ID пользователя - это число!\nВведите еще раз:')
        return
    
    tg_id_personal = int(message.text)
    data = await state.get_data()
    edit_role = data['edit_role']
    role = "<b>БАРИСТА</b>"
    await state.clear()
    # await req.update_user(
    #     user_id=tg_id_personal,
    #     role=edit_role
    # )
    user = await req.get_user_by_id(user_id=tg_id_personal)
    if user:
        try:
            await message.edit_text(
                text=f'Для добавления пользователя в список {role},'\
                    'отправьте ему пригласительную ссылку:\n'\
                    f'<code>{await create_start_link(bot=message.bot, payload=edit_role+"_"+str(user.user_id), encode=True)}</code>',
                reply_markup=admin_kb.back_to_main())
        except:
            await message.answer(
                text=f'Для добавления пользователя в список {role},'\
                    'отправьте ему пригласительную ссылку:\n'\
                    f'<code>{await create_start_link(bot=message.bot, payload=edit_role+"_"+str(user.user_id), encode=True)}</code>',
                reply_markup=admin_kb.back_to_main())
    else:
        await message.answer(text=f'Пользователь c id={tg_id_personal} в базе данных не найден, попробуйте еще раз:', reply_markup=admin_kb.back_to_main())
        



# отмена добавления пользователя в список администраторов
@router.callback_query(F.data == 'not_add_personal_list')
async def process_not_add_admin_list(callback: types.CallbackQuery) -> None:
    """
    Отмена назначение персонала
    :param callback:
    :param bot:
    :return:
    """

    await callback.message.delete()
    await handle_admin(callback.message)


# удаление после подтверждения
@router.callback_query(F.data == 'add_personal_list')
async def process_add_admin_list(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Подтверждение назначение персонала
    :param callback:
    :param state:
    :param bot:
    :return:
    """

    await callback.message.delete()
    data = await state.get_data()
    edit_role = data['edit_role']
    tg_id = data['add_personal']

    role = "БАРИСТА"

    await req.update_user(user_id=tg_id, role=edit_role)
    
    


# разжалование администратора
@router.callback_query(F.data == 'personal_delete')
async def process_del_admin(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Выбор пользователя для разжалования его из персонала
    :param callback:
    :param state:
    :return:
    """

    data = await state.get_data()
    edit_role = data['edit_role']
    role = "БАРИСТА"
    
    
    list_users = [i for i in await req.get_users() if i.role == edit_role]
    
    list_personal = [[user.user_id, user.username or user.fullname] for user in list_users]
    
    
    if list_personal == []:
        await callback.answer(text=f'Нет пользователей для удаления из списка {role}', show_alert=True)
        return
    
    role = '<b>'+ role +'</b>'
    keyboard = admin_kb.keyboards_del_admin(list_personal, 0, 2, 6)

    await callback.message.edit_text(text=f'Выберите пользователя, которого нужно удалить из {role}',
                                     reply_markup=keyboard)
    await callback.answer()


# >>>>
@router.callback_query(F.data.startswith('admin_del_forward_'))
async def process_forward_del_admin(callback: types.CallbackQuery, state: FSMContext) -> None:

    await callback.answer('')
    data = await state.get_data()
    edit_role = data['edit_role']
    role = "<b>БАРИСТА</b>"
    
    list_users = [i for i in await req.get_users() if i.role == edit_role]
    list_personal = [[user.user_id, user.username or user.fullname] for user in list_users]
    # :
    #     list_personal.append()
    forward = int(callback.data.split('_')[3]) + 1
    back = forward - 2
    keyboard = admin_kb.keyboards_del_admin(list_personal, back, forward, 2)
    try:
        await callback.message.edit_text(text=f'Выберите пользователя, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)
    except :
        await callback.message.answer(text=f'Выберитe пользоватeля, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)



# <<<<
@router.callback_query(F.data.startswith('admin_del_back'))
async def process_back_del_admin(callback: types.CallbackQuery, state: FSMContext) -> None:

    await callback.answer('')
    data = await state.get_data()
    edit_role = data['edit_role']
    role = "<b>БАРИСТА</b>"
    
    list_users = [i for i in await req.get_users() if i.role == edit_role]
    list_personal = []
    for user in list_users:
        list_personal.append([user.user_id, user.username or user.fullname])
    back = int(callback.data.split('_')[3]) - 1
    forward = back + 2
    keyboard = admin_kb.keyboards_del_admin(list_personal, back, forward, 2)
    try:
        await callback.message.edit_text(text=f'Выберите пользователя, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)
    except :
        await callback.message.answer(text=f'Выберитe пользоватeля, которого вы хотите удалить из {role}',
                                         reply_markup=keyboard)



# подтверждение добавления админа в список
@router.callback_query(F.data.startswith('controller_del_'))
async def process_delete_user(callback: types.CallbackQuery, state: FSMContext) -> None:

    role = "<b>БАРИСТА</b>"
    
    
    telegram_id = int(callback.data.split('_')[-1])

    user = await req.get_user_by_id(user_id=telegram_id)
    await state.update_data(del_personal=telegram_id)

    try:
        await callback.message.edit_text(text=f'Удалить пользователя {"@"+user.username if user.username else user.fullname} из {role}',
                                        reply_markup=admin_kb.keyboard_del_list_admins())
    except:
        await callback.message.answer(text=f'Удалить пользователя {"@"+user.username if user.username else user.fullname} из {role}',
                                        reply_markup=admin_kb.keyboard_del_list_admins())

# отмена удаления пользователя в список администраторов
@router.callback_query(F.data == 'not_del_personal_list')
async def process_not_del_personal_list(callback: types.CallbackQuery) -> None:
    """
    Отмена изменения роли пользователя
    :param callback:
    :param bot:
    :return:
    """

    try:
        await callback.message.delete()
    except :
        pass

    await callback.message.answer('Отменено', reply_markup=admin_kb.back_to_main())


# удаление после подтверждения
@router.callback_query(F.data == 'del_personal_list')
async def process_del_personal_list(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    
    data = await state.get_data()
    tg_id = data['del_personal']
    
    role = "<b>БАРИСТА</b>"

    await req.update_user(
        user_id=tg_id,
        role=UserRole.user
    )
    
    await callback.message.answer(text=f'Пользователь успешно удален из {role}', reply_markup=admin_kb.back_to_main())
