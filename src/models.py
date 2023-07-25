from sqlalchemy import Column, String

from src.database import Base


class BaseModel(Base):
    __abstract__ = True

    title = Column(String, unique=True)
    description = Column(String)

