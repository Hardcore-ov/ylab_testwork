from sqlalchemy import Column, UUID, ForeignKey, String, func, select
from sqlalchemy.orm import relationship, column_property

from src.dish.models import Dish
from src.models import BaseModel
from src.utils import generate_uuid


class Submenu(BaseModel):
    __tablename__ = 'submenu'

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    menu_id = Column(String, ForeignKey('menu.id'))
    dishes = relationship('Dish', backref='submenu', cascade='delete', lazy="selectin")

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id == id).scalar_subquery(),
    )
