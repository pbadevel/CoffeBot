from database.models import User, async_session
from utils import ProjectEnums

from sqlalchemy import select, update
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound

from typing import Optional

import logging as lg


"""-----  ADD METHODS  -----"""

async def add_user(user_id: int, **kw) -> Optional[User]:
    '''
    Добавляет нового пользователя в базу данных.

    Args:
        user_id: required (int)
        **kw: fullname, username, etc.
    
    '''

    
    try:
        async with async_session() as session:
            
            if await user_exists(user_id):
                await update_user(user_id=user_id, **kw)
                return
            
            new_user = User(
                user_id=user_id,
                **kw
            )
            
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            return new_user
            
    except IntegrityError as e:
        # await session.rollback()
        # print(f"Ошибка целостности: {e}")
        # Если пользователь уже существует, можно вернуть существующего
        existing_user = await session.get(User, kw['user_id'])
        return existing_user
        
    except SQLAlchemyError as e:
        # await session.rollback()
        print(f"Ошибка базы данных: {e}")
        return None
        
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None







"""-----  GET METHODS  -----"""


async def get_user_by_id(user_id: int) -> Optional[User]:
    '''
    Добавляет нового пользователя в базу данных.

    Args:
        user_id: required (int)
    Return:
        database.models.User object
    
    '''
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User)
                .where(User.user_id == user_id) 
            )
            return result.scalars().one()
    except NoResultFound:
        return None


async def user_exists(user_id: int) -> Optional[User]:
    '''
    Добавляет нового пользователя в базу данных.

    Args:
        user_id: required (int)
    Return:
        database.models.User object
    
    '''
    async with async_session() as session:
        return await session.get(User, user_id)
    

    

"""-----  UPDATE METHODS  -----"""


async def update_user(user_id: int, **data) -> Optional[User]:
    try:
        async with async_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return None
                
            for key, value in data.items():
                setattr(user, key, value)
                
            await session.commit()
            await session.refresh(user)
            return user
    except SQLAlchemyError as e:
        print(f"Error updating user: {e}")
        # await session.rollback()
        return None
    




import asyncio

# async def test():
#     print('database test')
#     # await add_user(user_id=123)
#     print(await user_exists(1223))
#     print('database test ok')


# asyncio.get_event_loop().run_until_complete(test())
