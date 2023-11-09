from typing import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.security import get_password_hash
from main import app
from db.base_class import Base
import models

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

    # Add test data
    add_user_data(db_session)
    add_item_data(db_session)

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


def add_user_data(db_session: Session):
    db_user: models.User = models.User(
        id=100,
        full_name="John Doe",
        email="johndoe@email.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=False,
    )
    db_session.add(db_user)
    db_session.commit()


def add_item_data(db_session: Session):
    db_item: models.Item = models.Item(
        id=100,
        name="existing item",
        description="existing item description",
    )
    db_session.add(db_item)
    db_session.commit()
