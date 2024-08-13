from app.models import AppBase
from app.models import Pagination
from app.models import PrimaryKey
from typing import Optional


class ApiKeyBase(AppBase):
    api_key: str
    offical_key: str = None
    endpoint: str = None
    active: bool
    model_name: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKeyUpdate(ApiKeyBase):
    pass


class ApiKeyRead(ApiKeyBase):
    id: Optional[PrimaryKey]


class ApiKeyPagination(Pagination):
    items: list[ApiKeyRead] = []
