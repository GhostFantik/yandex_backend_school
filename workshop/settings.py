from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    db_connect = os.getenv('db_connect')
    tz = os.getenv('TZ')


settings = Settings()
