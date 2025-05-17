from aiogram.filters import Filter
from aiogram.types import Message

from settings import config
from utils.ProjectEnums import UserRoleEnum

from database import req



class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in config.ADMIN_IDS


class BaristaProtect(Filter):
    async def __call__(self, message: Message):
        user = await req.get_user_by_id(message.from_user.id)
        
        if user:
            return user.role == UserRoleEnum.barista.value
        
        return False



