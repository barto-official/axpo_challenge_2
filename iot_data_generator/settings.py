from dotenv import load_dotenv
import os
from functools import lru_cache

load_dotenv()

class EventHubSettings:
    def __init__(self):
        self.connection_str = os.getenv("EVENT_HUB_CONNECTION_STR")
        self.event_hub_name = os.getenv("EVENT_HUB_NAME")

class GeneralSettings:
    def __init__(self):
        self.interval_ms = int(os.getenv("INTERVAL_MS", 1000))
        self.logging_level = int(os.getenv("LOGGING_LEVEL", 30))

class Settings:
    def __init__(self):
        self.event_hub = EventHubSettings()
        self.general = GeneralSettings()

@lru_cache()
def get_settings() -> Settings:
    return Settings()
