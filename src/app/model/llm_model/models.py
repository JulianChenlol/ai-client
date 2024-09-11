from typing import Optional, Literal

from app.models import AppBase, Pagination, PrimaryKey, NameStr


class LlmModelBase(AppBase):
    name: NameStr
    display_name: NameStr
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
    id: Optional[PrimaryKey]


class LlmModelPagination(Pagination):
    items: list[LlmModelRead] = []
