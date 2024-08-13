from app.database.core import Base
from app.models import TimeStampMixin
from sqlalchemy import Column, String, Boolean, Integer


class ApiKey(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    official_key = Column(String)
    endpoint = Column(String)
    model_name = Column(String)
    active = Column(Boolean)
