from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..settings import settings

if settings.PRODUCTION:
    if settings.TESTING:
        SQLALCHEMY_DATABASE_URL = settings.production_test_db_connect
    else:
        SQLALCHEMY_DATABASE_URL = settings.production_db_connect

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    if settings.TESTING:
        SQLALCHEMY_DATABASE_URL = settings.test_db_connect
    else:
        SQLALCHEMY_DATABASE_URL = settings.db_connect

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # only for sqlite
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    Base.metadata.create_all()

