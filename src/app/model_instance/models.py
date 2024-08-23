from pydantic import BaseModel


class ModelInstanceBase(BaseModel):
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


class ModelInstancePagination(BaseModel):
    items: list[ModelInstanceRead] = []
