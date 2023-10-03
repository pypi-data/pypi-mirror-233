import json
import aio_pika
import pika
from aio_pika.abc import DeliveryMode, ExchangeType
from pika.exchange_type import ExchangeType as PikaExchangeType


class AsyncPublisher:
    rabbitmq_url: str

    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url

    async def publish(self, queue: str, exchange: str, payload: dict) -> None:
        connection = await aio_pika.connect(self.rabbitmq_url)

        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(queue)

            exchange = await channel.declare_exchange(exchange, PikaExchangeType.fanout)
            body = json.dumps(payload, default=str)
            await exchange.publish(
                aio_pika.Message(
                    body=str.encode(body), delivery_mode=DeliveryMode.PERSISTENT
                ),
                routing_key=queue,
            )


class SyncPublisher:
    connection_params: pika.URLParameters

    def __init__(self, rabbitmq_url: str):
        self.connection_params = pika.URLParameters(url=rabbitmq_url)

    def publish(self, queue: str, exchange: str, payload: dict):
        connection = pika.BlockingConnection(self.connection_params)

        with connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue)

            exchange = channel.exchange_declare(exchange, ExchangeType.FANOUT)
            body = json.dumps(payload, default=str)
            exchange.basic_publish(
                body=str.encode(body),
                routing_key=queue,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
