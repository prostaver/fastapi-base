from sqlalchemy.orm import Session

import crud
import models
import schemas


def test_create(session: Session):
    item_name: str = "test item"
    item_description: str = "test description"
    user_in: schemas.ItemCreate = schemas.ItemCreate(
        name=item_name,
        description=item_description,
    )
    item: models.Item = crud.item.create(session, obj_in=user_in)

    assert item.name == item_name
    assert item.description == item_description


def test_get(session: Session):
    item: models.Item = crud.item.get(session, 100)

    assert item.name == "existing item"
    assert item.description == "existing item description"


def test_get_many(session: Session):
    print("test get many")
    items: list[models.Item] = crud.item.get_multi(session)

    assert type(items) is list
    assert items


def test_update(session: Session):
    db_item: models.Item = crud.item.get(session, 100)

    updated_description: str = "This is the new description."
    item: models.Item = crud.item.update(
        session,
        db_obj=db_item,
        obj_in=schemas.ItemUpdate(description=updated_description),
    )

    assert item.description == updated_description


def test_delete(session: Session):
    print("test delete")
    crud.item.remove(session, id=100)

    assert crud.item.get(session, 100) is None
