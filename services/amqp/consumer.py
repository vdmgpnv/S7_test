import json

import pika
from pika.adapters.blocking_connection import BlockingChannel

from config import rabbit_host, rabbit_password, rabbit_user


class RabbitConsumer:
    def __init__(self, queue: str):
        self.url = f"amqp://{rabbit_user}:" f"{rabbit_password}@{rabbit_host}/"
        self.queue = queue
        self.channel = self.create_channel()

    def create_channel(self) -> BlockingChannel:
        """Создаем конекшн к кролику"""
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        return connection.channel()

    def consume(self, callback_func) -> None:
        """Функция начала прослушки кролика"""
        self.channel.queue_declare(self.queue, durable=True)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback_func, auto_ack=True
        )
        self.channel.start_consuming()
