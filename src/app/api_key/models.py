from typing import Optional

from app.models import AppBase
from app.models import Pagination
from app.models import PrimaryKey


class ApiKeyBase(AppBase):
    key: Optional[str]
    active: bool


class ApiKeyCreate(ApiKeyBase):
    active: bool = True


class ApiKeyUpdate(ApiKeyBase):
    pass


class ApiKeyRead(ApiKeyBase):
    id: Optional[PrimaryKey]


class ApiKeyPagination(Pagination):
    items: list[ApiKeyRead] = []
