import asyncio
import pika
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


# async def make_relations():
#     async with db_helper.session_factory() as session:
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
# await get_accounts_with_user_with_reviews(session=session)


# class RabbitMQManager:
#     def __init__(self, host, queue_names):
#         self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
#         self.channel = self.connection.channel()
#         self.queue_names = queue_names
#
#         for queue_name in queue_names:
#             self.channel.queue_declare(queue=queue_name)
#
#     def send_message(self, queue_name, message):
#         self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)
#         print(message)
#
#     def receive_message(self, queue_name, callback):
#         self.channel.basic_consume(
#             queue=queue_name, on_message_callback=callback, auto_ack=True
#         )
#         self.channel.start_consuming()
#
#
# class Order:
#     def __init__(self, order_id, customer_name, items):
#         self.order_id = order_id
#         self.customer_name = customer_name
#         self.items = items
#
#
# def create_order(order_id, customer_name, items):
#     order = Order(order_id, customer_name, items)
#     return order
#
#
# def process_order_callback(ch, method, properties, body):
#     # Получаем информацию о заказе
#     order_info = body.decode("utf-8")
#
#     # Добавьте здесь логику обработки заказа
#     # Например, подтверждение заказа, обновление статуса, подготовка к доставке
#
#     print(f"Заказ обработан: {order_info}")
async def main():
    async with db_helper.session_factory() as session:


if __name__ == "__main__":
    asyncio.run(main())
    # rabbitmq_manager = RabbitMQManager(
    #     "localhost",
    #     ["new_orders_queue", "process_orders_queue", "notify_clients_queue"],
    # )
    # order = create_order("#54321", "Макар Ельцин", ["Мешок", "Шило"])
    # rabbitmq_manager.send_message(
    #     "new_orders_queue",
    #     f"Новый заказ: {order.order_id} от {order.customer_name} содержит {order.items}",
    # )
    # rabbitmq_manager.receive_message("new_orders_queue", process_order_callback)
    # rabbitmq_manager.connection.close()
