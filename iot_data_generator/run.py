import os
import asyncio
import logging
from generator import Generator

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the generator...")
    generator = Generator()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(generator.generate())
    except KeyboardInterrupt:
        logging.info("Generator stopped by user.")
    finally:
        loop.close()
        logging.info("Generator stopped.")
