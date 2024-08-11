from app.models import AppBase, Pagination, PrimaryKey, NameStr
from typing import Optional, Literal


class LlmModelBase(AppBase):
    id: Optional[PrimaryKey]
    name: NameStr
    instance: NameStr
    type: Literal["LLM"] = "LLM"
    properties: Literal["Public", "Private"]
    server_ip: str
    tpm: int
    rpm: int
    online: bool
    max_request_num: int
    gpu: Optional[str] = None


class LlmModelCreate(LlmModelBase):
    pass


class LlmModelUpdate(LlmModelBase):
    pass


class LlmModelRead(LlmModelBase):
    pass


class LlmModelPagination(Pagination):
    items: list[LlmModelRead] = []
