from sqlalchemy import Column, UUID, ForeignKey, String
from sqlalchemy.orm import relationship

from src.models import BaseModel
from src.utils import generate_uuid


class Submenu(BaseModel):
    __tablename__ = 'submenu'

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    menu_id = Column(String, ForeignKey('menu.id'))
    menu = relationship('Menu', back_populates='submenus', uselist=False)
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')

