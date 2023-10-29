import smtplib

import pika


class RabbitMQManager:
    def __init__(self, host, queue_names):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queue_names = queue_names

        for queue_name in queue_names:
            self.channel.queue_declare(queue=queue_name)

    def send_message(self, queue_name, message):
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(message)

    def receive_message(self, queue_name, callback):
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()


class Order:
    def __init__(self, order_id, customer_name, status, items):
        self.order_id = order_id
        self.customer_name = customer_name
        self.status = status
        self.items = items


fake_new_orders = []
fake_accepted_orders = []


def create_and_send_order(order_id, customer_name, status, items):
    order = Order(order_id, customer_name, status, items)
    rabbitmq_manager.send_message(
        "new_orders_queue",
        f"Новый заказ: {order.order_id} от {order.customer_name} содержит {order.items}",
    )
    fake_new_orders.append(order)


def confirm_order(order_id):
    # Получите доступ к данным по заказу. Например, у нас есть функция get_order_data,
    # которая возвращает информацию о заказе по его ID.

    global fake_new_orders  # Добавляем глобальную переменную

    for order in fake_new_orders:
        if order.order_id == order_id:
            # Смените статус заказа на 'Подтвержден'
            order.status = "Подтвержден"

            print(f"Заказ {order_id} подтвержден.")
            return True

    print(f"Заказ {order_id} не найден.")
    return None


def process_order_callback(ch, method, properties, body):
    global fake_new_orders

    order_info = body.decode("utf-8")

    # Парсим информацию о заказе
    order_id = order_info.split(":")[1].split(" от")[0].strip()

    # Находим соответствующий заказ
    order_to_process = None
    for order in fake_new_orders:
        if order.order_id == order_id:
            order_to_process = order
            break

    if order_to_process is not None:
        # Меняем статус
        order_to_process.status = "Обработан"
        print(f"Заказ {order_id} обработан.")

        # Ваши остальные действия...

    # В случае если заказ не найден
    else:
        print(f"Заказ {order_id} не найден.")


def send_email_notification(customer_email, order_status):
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    subject = "Уведомление о заказе"
    body = f"Статус вашего заказа: {order_status}"

    message = f"Subject: {subject}\n\n{body}"
    print(f"Ваш заказ ...")
    # with smtplib.SMTP("smtp.gmail.com", 587) as server:
    #     server.starttls()
    #     server.login(sender_email, sender_password)
    #     server.sendmail(sender_email, customer_email, message)


def send_email_notification_callback(ch, method, properties, body):
    email_info = body.decode("utf-8")
    customer_email = "User.email"
    order_status = "Confirmed"
    # Разберите email_info на более мелкие компоненты
    send_email_notification(customer_email=customer_email, order_status=order_status)
    print(f"Уведомление отправлено: {email_info}")


if __name__ == "__main__":
    rabbitmq_manager = RabbitMQManager(
        "localhost",
        ["new_orders_queue", "process_orders_queue", "notify_clients_queue"],
    )
    create_and_send_order("#54321", "Владимир Путин", "Accepted", ["Мешок", "Шило"])
    for order in fake_new_orders:
        print(f"Order ID: {order.order_id}")
        print(f"Customer Name: {order.customer_name}")
        print(f"Status: {order.status}")
        print(f"Items: {order.items}")
        print("=" * 30)
    rabbitmq_manager.receive_message(
        "process_orders_queue",
        process_order_callback,
    )
    rabbitmq_manager.receive_message(
        "notify_clients_queue", send_email_notification_callback
    )
    rabbitmq_manager.connection.close()
