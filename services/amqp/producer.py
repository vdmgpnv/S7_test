import json
from typing import Any

import pika
from pika.adapters.blocking_connection import BlockingChannel
from loguru import logger

from config import rabbit_host, rabbit_password, rabbit_user


class RabbitProducer:
    def __init__(self, queue: str):
        self.url = f"amqp://{rabbit_user}:" f"{rabbit_password}@{rabbit_host}/"
        self.queue = queue

    def __enter__(self):
        try:
            self.channel = self.create_channel()
        except Exception as e:
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()

    def create_channel(self) -> BlockingChannel:
        """Создаем подключение к кролику"""
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        return connection.channel()

    def send_message(self, body: dict[str, Any]):
        """Объявляем очередь, если она не объявлена и отправляем туда переданное сообщение"""
        message = json.dumps(body)
        self.channel.queue_declare(queue=self.queue, durable=True)
        logger.info(f"Sending the message {body}")
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
