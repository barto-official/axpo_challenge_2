import json
import datetime
import random
import asyncio
import logging
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData


class Sensor:
    def __init__(self, id: str, range: tuple, interval_ms: int):
        self.id = id
        self.range = range
        self.interval_ms = interval_ms

    async def generate(self, client: EventHubProducerClient, topic: str):
        while True:
            data = {
                "sensor_id": int(self.id),
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "value": random.randint(*self.range),
                "metadata": {
                    "location": {"lat": 10, "lng": 10},
                    "unit": "C",
                    "type": "temperature",
                    "description": "sensor description"
                }
            }

            payload = json.dumps(data, default=str)
            logging.info(f"{topic}: {payload}")

            event_data = EventData(payload)
            async with client:
                await client.send_batch([event_data])

            await asyncio.sleep(self.interval_ms / 1000)
