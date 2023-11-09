from sqlalchemy.orm import Session

from core.security import verify_password
import crud
import schemas
import models


def test_create(session: Session):
    full_name: str = "Test Name"
    email: str = "email@email.com"
    password: str = "password"
    is_active: bool = True

    user_in: schemas.UserCreate = schemas.UserCreate(
        full_name=full_name,
        email=email,
        password=password,
        is_active=is_active,
    )
    user: models.User = crud.user.create(session, obj_in=user_in)

    assert user.full_name == full_name
    assert user.email == email
    assert verify_password(password, user.hashed_password)
    assert user.is_active == is_active


def test_get(session: Session):
    user: models.User = crud.user.get(session, 100)

    assert user.full_name == "John Doe"
    assert user.email == "johndoe@email.com"
    assert verify_password("testpassword", user.hashed_password)
    assert user.is_active is False


def test_get_many(session: Session):
    users: list[models.User] = crud.user.get_multi(session)

    assert type(users) is list
    assert users


def test_get_by_email(session: Session):
    user: models.User = crud.user.get_by_email(
        session, email="johndoe@email.com"
    )

    assert user.full_name == "John Doe"
    assert user.email == "johndoe@email.com"
    assert verify_password("testpassword", user.hashed_password)
    assert user.is_active is False


def test_update(session: Session):
    db_user = crud.user.get(session, 100)

    user: models.User = crud.user.update(
        session,
        db_obj=db_user,
        obj_in=schemas.UserUpdate(full_name="Jane Doe"),
    )

    assert user.full_name == "Jane Doe"


def test_delete(session: Session):
    crud.user.remove(session, id=100)

    assert crud.user.get(session, 100) is None
