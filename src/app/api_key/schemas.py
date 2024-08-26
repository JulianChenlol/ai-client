from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from app.database.core import Base
from app.models import TimeStampMixin
from app.auth.schemas import AppUser
from app.model_instance.schemas import ModelInstance


class ApiKey(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    official_key = Column(String)
    endpoint = Column(String)
    model = Column(String)
    active = Column(Boolean)


class UserApiKey(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(AppUser.id))
    user = relationship(AppUser, backref="api_keys")

    api_key_id = Column(Integer, ForeignKey(ApiKey.id))
    api_key = relationship(ApiKey, backref="users")


class ModelInstanceApiKey(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    model_instance_id = Column(Integer, ForeignKey(ModelInstance.id))
    model_instance = relationship(ModelInstance, backref="api_keys")

    api_key_id = Column(Integer, ForeignKey(ApiKey.id))
    api_key = relationship(ApiKey, backref="model_instances")
