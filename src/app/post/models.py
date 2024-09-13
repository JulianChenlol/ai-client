from typing import Optional, Literal, List

from app.models import AppBase, Pagination, PrimaryKey
from app.poll.models import PollRead


class PostPoll(AppBase):
    poll: PollRead
    analysis: str = ""


class PostBase(AppBase):
    user_id: PrimaryKey
    title: str
    content: str
    question: str
    status: Literal["draft", "published"] = "draft"


class PostCreate(PostBase):
    polls: Optional[List[PostPoll]]


class PostUpdate(PostBase):
    polls: Optional[List[PostPoll]]


class PostRead(PostBase):
    id: Optional[PrimaryKey]


class PostPagination(Pagination):
    items: list[PostRead] = []
