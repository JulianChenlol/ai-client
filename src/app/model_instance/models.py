from typing import List, Optional

from app.models import AppBase
from app.models import PrimaryKey
from app.api_key.models import ApiKeyRead


class ModelInstanceBase(AppBase):
    official_key: str
    endpoint: str
    instance: str
    model: str
    active: bool


class ModelInstanceCreate(ModelInstanceBase):
    active: bool = True


class ModelInstanceUpdate(ModelInstanceBase):
    pass


class ModelInstanceRead(ModelInstanceBase):
    id: int


class ModelInstancePagination(AppBase):
    items: list[ModelInstanceRead] = []


class ApiKeyModelInstance(AppBase):
    api_key: Optional[ApiKeyRead]
    model_instances: Optional[List[ModelInstanceRead]] = []


class UserApiKeyModelInstance(AppBase):
    user_id: Optional[PrimaryKey]
    api_keys: Optional[List[ApiKeyModelInstance]] = []
