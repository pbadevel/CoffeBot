from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import ForeignKey, String, BigInteger, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column


import asyncio
from datetime import datetime
from utils import ProjectEnums
from typing import List, Optional

engine = create_async_engine(
    url="sqlite+aiosqlite:///database/db.sqlite3",
    pool_size=20,
    max_overflow=0,
    pool_recycle=500,
    connect_args={"check_same_thread": False}
)


async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass




class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fullname: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    cups: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    referrer_id: Mapped[int] = mapped_column(Integer, nullable=True)
    referral_ids: Mapped[str] = mapped_column(String, nullable=True)

    role: Mapped[ProjectEnums.UserRole] = mapped_column(String(50), nullable=False, default=ProjectEnums.UserRole.user)




async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())