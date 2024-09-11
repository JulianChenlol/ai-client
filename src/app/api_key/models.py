from typing import Optional

from app.models import AppBase
from app.models import Pagination
from app.models import PrimaryKey


class ApiKeyBase(AppBase):
    active: bool


class ApiKeyCreate(ApiKeyBase):
    active: bool = True


class ApiKeyUpdate(ApiKeyBase):
    pass


class ApiKeyRead(ApiKeyBase):
    id: Optional[PrimaryKey]
    key: Optional[str]


class ApiKeyPagination(Pagination):
    items: list[ApiKeyRead] = []
