from typing import Optional, Literal

from app.models import AppBase, Pagination, PrimaryKey, NameStr


class PostBase(AppBase):
    user_id: PrimaryKey
    title: NameStr
    content: NameStr
    question: NameStr
    status: Literal["draft", "published"] = "draft"


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostRead(PostBase):
    id: Optional[PrimaryKey]


class PostPagination(Pagination):
    items: list[PostRead] = []
