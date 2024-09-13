from typing import Optional

from app.models import AppBase, Pagination, PrimaryKey


class PollBase(AppBase):
    post_id: Optional[PrimaryKey] = None
    option: str
    order: int
    amount: int


class PollCreate(PollBase):
    pass


class PollUpdate(PollBase):
    pass


class PollRead(PollBase):
    id: Optional[PrimaryKey] = None


class PollPagination(Pagination):
    items: list[PollRead] = []
