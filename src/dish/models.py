from sqlalchemy import Column, ForeignKey, Numeric, String

from src.models import BaseModel
from src.utils import generate_uuid


class Dish(BaseModel):
    __tablename__ = 'dish'

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    price = Column(Numeric(10, 2))
    submenu_id = Column(String, ForeignKey('submenu.id'))
