from app.database.core import Base

from slugify import slugify
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from app.models import ModelMixin, TimeStampMixin


class LlmModel(Base, ModelMixin, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    type = Column(String, default="LLM")
    tpm = Column(Integer)
    rpm = Column(Integer)
    max_request_num = Column(Integer)

    @hybrid_property
    def slug(self):
        return slugify(self.name)
