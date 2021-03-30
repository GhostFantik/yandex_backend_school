from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    db_connect = os.getenv('db_connect')
    test_db_connect = os.getenv('test_db_connect')
    production_db_connect = os.getenv('production_db_connect')
    production_test_db_connect = os.getenv('production_test_db_connect')
    workers = os.getenv('workers')
    TESTING = os.getenv('TESTING')
    PRODUCTION = os.getenv('PRODUCTION')



settings = Settings()
