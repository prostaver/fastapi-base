# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa F401
from models.item import Item  # noqa: F401
from models.user import User  # noqa: F401
