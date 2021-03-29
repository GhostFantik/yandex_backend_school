from sqlalchemy_utils import create_database, drop_database
import pytest

from workshop.settings import settings


@pytest.fixture(scope='session')
def temp_db():
    if settings.PRODUCTION:
        db_url = settings.production_test_db_connect
    else:
        db_url = settings.test_db_connect

    create_database(db_url)

    try:
        yield
    finally:
        drop_database(db_url)
