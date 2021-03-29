from sqlalchemy_utils import create_database, drop_database
import pytest

from workshop.settings import settings


@pytest.fixture(scope='session')
def temp_db():
    db_url = settings.test_db_connect
    if not settings.PRODUCTION:
        create_database(db_url)

    try:
        yield
    finally:
        if not settings.PRODUCTION:
            drop_database(db_url)
