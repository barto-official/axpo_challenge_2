import json
import asyncio
import logging
from azure.eventhub.aio import EventHubProducerClient
from sensor import Sensor
from settings import get_settings

class Generator:
    """
    A class to generate sensor data and send it to Azure Event Hub.
    """

    def __init__(self):
        """
        Initializes the Generator with settings and sensors.
        """
        self.settings = get_settings()

        self.client = EventHubProducerClient.from_connection_string(
            conn_str=self.settings.event_hub.connection_str,
            eventhub_name=self.settings.event_hub.event_hub_name
        )

        with open("sensors.json") as sensors_json:
            _sensors = json.load(sensors_json)
            self.sensors = [
                Sensor(k, v.get("range", [0, 100]), self.settings.general.interval_ms)
                for k, v in _sensors.items()
            ]

    async def generate(self):
        """
        Generates data from sensors and sends it to Azure Event Hub.
        """
        logging.basicConfig(level=self.settings.general.logging_level)
        try:
            tasks = [s.generate(self.client, "sensors") for s in self.sensors]
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            await self.client.close()
            logging.info("Generator stopped.")

if __name__ == "__main__":
    generator = Generator()
    asyncio.run(generator.generate())
