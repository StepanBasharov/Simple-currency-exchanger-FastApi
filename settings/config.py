import os

from dotenv import load_dotenv

load_dotenv()


class ConfigService:
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))


class ConfigDB:
    DB_URL = os.getenv("DB_URL")


class ConfigCelery:
    BROKER = os.getenv("BROKER_URL")
    BACKEND = os.getenv("RESULT_BACKEND")

class ConfigExchangeApi:
    API_KEY = os.getenv("API_KEY")
    PRICES_URL = os.getenv("PRICES_URL")
    NAMES_URL = os.getenv("NAMES_URL")
    DB_URL = os.getenv("DB_SYNC_URL")
