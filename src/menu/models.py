from sqlalchemy import Column, String, and_, func, select
from sqlalchemy.orm import column_property, relationship

from src.dish.models import Dish
from src.models import BaseModel
from src.submenu.models import Submenu
from src.utils import generate_uuid


class Menu(BaseModel):
    __tablename__ = 'menu'

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    submenus = relationship('Submenu', backref='menu', cascade='delete', lazy='selectin')

    submenus_count = column_property(
        select(func.count(Submenu.id)).where(Submenu.menu_id == id).scalar_subquery(),
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .join(Submenu)
        .where(and_(Submenu.menu_id == id, Submenu.id == Dish.submenu_id))
        .correlate_except(Dish)
        .scalar_subquery()
    )
