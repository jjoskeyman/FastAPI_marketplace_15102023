import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import db_helper, User, Account, Review, Order, Product
from core.models.order_product_association import OrderProductAssociation


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


async def make_relations():
    async with db_helper.session_factory() as session:
        await create_user(session=session, username="gilyaz")
        await create_user(session=session, username="trapa")
        await create_user(session=session, username="Maria")

    user1 = await get_user_by_username(session=session, username="gilyaz")
    user2 = await get_user_by_username(session=session, username="trapa")
    await create_user_account(
        session=session,
        user_id=user1.id,
        balance=1280,
        bio="koresh",
    )
    await create_user_account(
        session=session,
        user_id=user2.id,
        last_name="Trapicin",
        balance=12,
        bio="priyatel",
    )
    # await get_users_with_accounts(session=session)
    # await create_reviews(session, user1.id, 3, "SQLA 2.0", "HOW DEAP IS YOUR LOVE")
    # await create_reviews(session, user2.id, 4, "MY THROAT", "yet another")
    # await get_users_with_reviews(session=session)
    # await get_reviews_with_users(session=session)
    # await get_users_with_reviews_and_accounts(session=session)
    # await get_accounts_with_user_with_reviews(session=session)


async def create_order(
    session: AsyncSession,
    status: str,
    comment: str | None = None,
) -> Order:
    order = Order(status=status, comment=comment)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    product_name: str,
    description: str | None = None,
    price: int | None = 100,
    product_category: str | None = None,
) -> Product:
    product = Product(
        product_name=product_name,
        description=description,
        price=price,
        product_category=product_category,
    )
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products():
    async with db_helper.session_factory() as session:
        order1 = await create_order(session, "Accepted", "")
        order2 = await create_order(session, "Accepted", "bla-bla-bla")
        order3 = await create_order(session, "Accepted", "Hello")

        display = await create_product(
            session, "LG", "good gaming monitor", 1021, "electronics"
        )
        mouse = await create_product(
            session, "chinamouse", "office mouse", 17, "electronics"
        )
        chair = await create_product(
            session, "office chair", "best office chair", 1215, "furniture"
        )
        order1 = await session.scalar(
            select(Order)
            .where(Order.id == order1.id)
            .options(selectinload(Order.products)),
        )
        order2 = await session.scalar(
            select(Order)
            .where(Order.id == order2.id)
            .options(selectinload(Order.products)),
        )
        order3 = await session.scalar(
            select(Order)
            .where(Order.id == order3.id)
            .options(selectinload(Order.products)),
        )
        order1.products.append(mouse)
        order1.products.append(display)
        order2.products = [mouse, display, chair]
        order3.products = [chair]
        await session.commit()


async def get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products_association(session)
    for order in orders:
        print("id:", order.id, "status:", order.status, order.created_at, "products: ")
        for product in order.products:  # type: Product
            print(
                "--",
                product.id,
                product.product_name,
                product.product_category,
                product.price,
            )


async def get_orders_with_products_association(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def demo_get_orders_with_products_with_association(session: AsyncSession):
    orders = await get_orders_with_products_association(session)
    for order in orders:
        print("id:", order.id, "status:", order.status, order.created_at, "products: ")
        for (
            order_product_details
        ) in order.products_details:  # type: OrderProductAssociation
            print(
                "--",
                order_product_details.product.id,
                order_product_details.product.product_name,
                order_product_details.product.description,
                order_product_details.product.price,
                "qty:",
                order_product_details.count,
            )


async def create_gifts_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_association(session)
    gift = await create_product(
        session,
        "sticker",
        "gift item",
        0,
        "gifts",
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=2,
                unit_price=0,
                product=gift,
            ),
        )

    await session.commit()


async def demo_m2m(session: AsyncSession):
    # await get_orders_with_products_through_secondary(session)
    # await create_gifts_for_existing_orders(session)
    await demo_get_orders_with_products_with_association(session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


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
