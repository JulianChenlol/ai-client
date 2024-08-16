from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.models import TimeStampMixin
from app.auth.schemas import AppUser


class ApiKey(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    official_key = Column(String)
    endpoint = Column(String)
    model = Column(String)
    active = Column(Boolean)


class UserApiKey(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(AppUser.id), primary_key=True)
    user = relationship(AppUser, backref="api_keys")

    api_key_id = Column(Integer, ForeignKey(ApiKey.id), primary_key=True)
    api_key = relationship(ApiKey, backref="users")
