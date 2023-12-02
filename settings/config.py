import os

from dotenv import load_dotenv

load_dotenv()


class ConfigService:
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))


class ConfigDB:
    DB_URL = os.getenv("DB_URL")
