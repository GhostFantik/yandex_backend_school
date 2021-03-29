from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    db_connect = os.getenv('db_connect')
    test_db_connect = os.getenv('test_db_connect')
    TESTING = os.getenv('TESTING')


settings = Settings()
