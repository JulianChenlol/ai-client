from app.database.core import Base

from slugify import slugify
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property


class LlmModel(Base):
    __table_args__ = {"schema": "app_core", "extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    instance = Column(String)
    type = Column(String, default="LLM")
    properties = Column(String)
    server_ip = Column(String)
    tpm = Column(Integer)
    rpm = Column(Integer)
    online = Column(Boolean)
    max_request_num = Column(Integer)
    gpu = Column(String)

    @hybrid_property
    def slug(self):
        return slugify(self.name)
