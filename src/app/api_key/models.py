from app.models import AppBase
from app.models import Pagination
from app.models import PrimaryKey
from typing import Optional


class ApiKeyBase(AppBase):
    key: Optional[str]
    official_key: Optional[str]
    endpoint: Optional[str]
    active: bool
    model: str


class ApiKeyCreate(ApiKeyBase):
    active: bool = True


class ApiKeyUpdate(ApiKeyBase):
    pass


class ApiKeyRead(ApiKeyBase):
    id: Optional[PrimaryKey]


class ApiKeyPagination(Pagination):
    items: list[ApiKeyRead] = []
