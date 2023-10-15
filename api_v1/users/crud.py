"""
CREATE
READ
UPDATE
DELETE
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from .schemas import UserCreate, UserUpdate, UserUpdatePartial


async def get_users(session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def update_user(
        session: AsyncSession,
        user: User, user_update: UserUpdate | UserUpdatePartial,
        partial: bool = False,
) -> User:
    for key, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, key, value)
    await session.commit()
    return user


async def delete_user(
        session: AsyncSession,
        user: User,
) -> None:
    await session.delete(user)
    await session.commit()

# async def update_user_partial(session: AsyncSession, user: User, user_update: UserUpdatePartial) -> User:
#     for key, value in user_update.model_dump(exclude_unset=True).items():
#         setattr(user, key, value)
#     await session.commit()
#     return user
