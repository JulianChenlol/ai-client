from slugify import slugify
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import ForeignKey


from app.database.core import Base
from app.models import TimeStampMixin
from app.auth.schemas import AppUser


class Post(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(AppUser.id))
    title = Column(String)
    content = Column(String)
    question = Column(String)
    status = Column(String, default="draft")

    @hybrid_property
    def slug(self):
        return slugify(self.title)
