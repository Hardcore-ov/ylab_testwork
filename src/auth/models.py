import uuid
from datetime import datetime

from sqlalchemy import JSON, TIMESTAMP, UUID, Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Base):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    permissions = Column(JSON)
    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(UUID, ForeignKey('role.id'))
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    role = relationship('Role', back_populates='users')
