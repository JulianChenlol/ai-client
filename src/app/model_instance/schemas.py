from app.database.core import Base
from sqlalchemy import Column, Integer, String, Boolean


class ModelInstance(Base):
    id = Column(Integer, primary_key=True)
    official_key = Column(String)
    endpoint = Column(String)
    instance = Column(String)
    model = Column(String)
    active = Column(Boolean)
