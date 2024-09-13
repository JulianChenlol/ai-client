from app.database.core import Base

from sqlalchemy import Column, Integer, String
from app.models import TimeStampMixin
from app.post.schemas import Post
from sqlalchemy.sql.schema import ForeignKey


class Poll(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id))
    option = Column(String)
    order = Column(Integer, default=0)
    amount = Column(Integer, default=0)
