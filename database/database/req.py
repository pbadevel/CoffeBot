from database.models import User,Token, async_session

from sqlalchemy import select, update
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, NoResultFound

from typing import Optional, List

import logging as lg


"""-----  ADD METHODS  -----"""

async def add_user(user_id: int, **kw) -> Optional[User]:
    '''
    Add new user in database

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
        existing_user = await session.get(User, kw['user_id'])
        return existing_user
        
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None



async def add_token(tg_creator_id: int, **kw) -> Token:
    '''
    kw:
    '''
    
    try:
        async with async_session() as session:
            new_token = Token(
                creator_tg_id=tg_creator_id,
                **kw
            )
            
            session.add(new_token)
            await session.commit()
            await session.refresh(new_token)
            return new_token
            
    except IntegrityError as e:
        existing_token = await session.get(Token, kw['token_id'])
        return existing_token
        
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None





"""-----  GET METHODS  -----"""

async def get_token_by_id(token_id: int):
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Token)
                .where(Token.token_id == token_id) 
            )
            return result.scalars().one()
    except NoResultFound:
        return None


async def get_user_by_id(user_id: int) -> Optional[User]:
    '''
    Get user by user_id from database

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


async def get_users() -> Optional[List[User]]:
    '''
    Get all users
    '''
    try:
        async with async_session() as session:
            result = await session.execute(
                select(User)
            )
            return result.scalars().all()
        
    except NoResultFound:
        return None



async def user_exists(user_id: int) -> Optional[User]:
    '''
    Checks if user exists
    
    Args:
        user_id: required (int)
    Return:
        database.models.User object
    
    '''
    async with async_session() as session:
        return await session.get(User, user_id)
    

    

"""-----  UPDATE METHODS  -----"""


async def update_user(user_id: int, **data) -> Optional[User]:
    '''
    Update user in database by user_id
    
    Args:
        user_id: required (int)
    Return:
        database.models.User object
    '''
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
    

async def update_token(token_id: int, is_active: bool = False):
    try:
        async with async_session() as session:
            token = await session.get(Token, token_id)
            
            if not token:
                return None
                
            setattr(token, "is_active", is_active)
            
            await session.commit()
            await session.refresh(token)
            return token
        
    except SQLAlchemyError as e:
        print(f"Error updating token: {e}")
        # await session.rollback()
        return None    




import asyncio

# async def test():
#     print('database test')
#     # await add_user(user_id=123)
#     print(await user_exists(1223))
#     print('database test ok')


# asyncio.get_event_loop().run_until_complete(test())
