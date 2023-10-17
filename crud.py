import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Account, Review


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # user: User = result.scalar_one_or_none()
    # user: User = result.scalar_one()
    user: User = await session.scalar(stmt)
    print(f"Found user: '{username}' with info: {user}")
    return user


async def create_reviews(
    session: AsyncSession,
    user_id: int,
    rating: int,
    *reviews_titles: str,
) -> list[Review]:
    reviews = [
        Review(title=title, user_id=user_id, rating=rating) for title in reviews_titles
    ]
    session.add_all(reviews)
    await session.commit()
    print(reviews)
    return reviews


async def create_user_account(
    session: AsyncSession,
    user_id: int,
    last_name: str | None = None,
    balance: int = None,
    bio: str | None = None,
) -> Account:
    account = Account(user_id=user_id, last_name=last_name, balance=balance, bio=bio)
    session.add(account)
    await session.commit()
    return account


async def get_users_with_accounts(session: AsyncSession):
    stmt = select(User).options(joinedload(User.account)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # user = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.account.balance)


async def get_reviews_with_users(session: AsyncSession):  # запрос один к одному
    stmt = select(Review).options(joinedload(Review.user)).order_by(Review.id)
    reviews = await session.scalars(stmt)
    for rev in reviews:  # type: Review
        print("review:", rev.title)
        print("author:", rev.user)


async def get_users_with_reviews(session: AsyncSession):  # один ко многим
    stmt = select(User).options(selectinload(User.reviews)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for review in user.reviews:
            print("-", review)


async def get_users_with_reviews_and_accounts(
    session: AsyncSession,
):  # запрос один ко многим
    stmt = (
        select(User)
        .options(joinedload(User.account), selectinload(User.reviews))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:  # type: User
        print("**" * 10)
        print(user, user.account and user.account.last_name)
        for review in user.reviews:
            print("-", review)


async def get_accounts_with_user_with_reviews(
    session: AsyncSession,
):  # подгружаем несколько связей насквозь
    stmt = (
        select(Account)
        .options(joinedload(Account.user).selectinload(User.reviews))
        .where(Account.last_name == "Trapicin")
        .order_by(Account.id)
    )
    accounts = await session.scalars(stmt)
    for acc in accounts:
        print("***" * 10)
        print(acc.last_name, acc.user)
        print(acc.user.reviews)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="gilyaz")
        # await create_user(session=session, username="trapa")
        # await create_user(session=session, username="Maria")
        #
        # user1 = await get_user_by_username(session=session, username="gilyaz")
        # user2 = await get_user_by_username(session=session, username="trapa")
        # # await create_user_account(
        # #     session=session,
        # #     user_id=user1.id,
        #     balance=1280,
        #     bio="koresh",
        # )
        # await create_user_account(
        #     session=session,
        #     user_id=user2.id,
        #     last_name="Trapicin",
        #     balance=12,
        #     bio="priyatel",
        # )
        # await get_users_with_accounts(session=session)
        # await create_reviews(session, user1.id, 3, "SQLA 2.0", "HOW DEAP IS YOUR LOVE")
        # await create_reviews(session, user2.id, 4, "MY THROAT", "yet another")
        # await get_users_with_reviews(session=session)
        # await get_reviews_with_users(session=session)
        # await get_users_with_reviews_and_accounts(session=session)
        await get_accounts_with_user_with_reviews(session=session)


if __name__ == "__main__":
    asyncio.run(main())
