from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    pass


# Properties to receive via API on update
class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
