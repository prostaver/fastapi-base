import pytest

from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from main import app
from db.base_class import Base

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    # Create db tables.
    Base.metadata.create_all(bind=engine)

    db_session = TestSessionLocal()

    yield db_session

    # Close database connection and drop the tables.
    db_session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db() -> Generator:
    yield TestSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
