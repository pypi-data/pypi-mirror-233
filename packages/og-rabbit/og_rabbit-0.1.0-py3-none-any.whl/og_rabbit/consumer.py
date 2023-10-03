import asyncio
import json

import aio_pika
from aio_pika import ExchangeType


class Consumer:
    def __init__(self, url, pool_size=10):
        self.rabbitmq_url = url
        self.pool_size = pool_size
        self._connections = asyncio.Queue()

    async def initialize(self):
        for _ in range(self.pool_size):
            connection = await aio_pika.connect_robust(self.rabbitmq_url)
            await self._connections.put(connection)

    async def listen(self, event_name, fn):
        connection = await self._connections.get()

        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(event_name)
            exchange = await channel.declare_exchange(event_name, ExchangeType.FANOUT)

            await queue.bind(exchange)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        data = json.loads(message.body.decode())
                        await fn(data)
