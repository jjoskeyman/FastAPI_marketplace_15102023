import pika
from pydantic import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RabbitMQ:
    def __init__(self, host, port, queue_name):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port)
        )
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)

    def send_order(self, order):
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=json.dumps(order)
        )

    def receive_order(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()


class Order(BaseModel):
    order_id: str
    customer_name: str
    status: str
    items: list


list_of_orders = {}


def confirm_order(order_id):
    global list_of_orders
    # В этой функции вы будете обновлять статус заказа в вашей системе.
    # Например, если у вас есть список заказов, то найдите заказ с соответствующим order_id
    # и установите его статус в "Подтвержден".
    # Если у вас есть специальная база данных, используйте ее для обновления статуса заказа.

    if order_id in list_of_orders:
        list_of_orders[order_id]["status"] = "Подтвержден"
        print(f"Заказ {order_id} подтвержден.")
    else:
        print(f"Заказ {order_id} не найден.")


def prepare_order_for_delivery(order_id):
    # В этой функции вы готовите заказ к доставке.
    # Например, у вас может быть список заказов и вы помечаете заказ с соответствующим order_id
    # как "Готов к доставке".

    global list_of_orders

    if order_id in list_of_orders:
        list_of_orders[order_id]["status"] = "Готов к доставке"
        print(f"Заказ {order_id} готов к доставке.")
    else:
        print(f"Заказ {order_id} не найден.")


@app.post("/orders/")
async def create_order(order: Order):
    rabbit_mq = RabbitMQ("localhost", 5672, "new_orders_queue")
    rabbit_mq.send_order(order.model_dump())
    rabbit_mq.close_connection()
    return {"Message": "Order created and sent to the queue"}


@app.get("/orders/")
async def process_orders():
    def process_order_method(ch, method, properties, body):
        order = json.loads(body)
        confirm_order(order["order_id"])
        prepare_order_for_delivery(order["order_id"])

    rabbit_mq = RabbitMQ("localhost", 5672, "new_orders_queue")
    rabbit_mq.receive_order(process_order_method)
    rabbit_mq.close_connection()
    return {"Message": "Orders processed"}


if __name__ == "__main__":
    rabbitmq_manager = RabbitMQ(
        "localhost",
        ["new_orders_queue", "process_orders_queue", "notify_clients_queue"],
    )
