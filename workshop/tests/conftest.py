from sqlalchemy_utils import create_database, drop_database
from workshop.settings import settings
import pytest


@pytest.fixture(scope='session')
def temp_db():
    create_database(settings.test_db_connect)

    try:
        yield
    finally:
        drop_database(settings.test_db_connect)
