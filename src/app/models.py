from pydantic import BaseModel
from datetime import datetime

from pydantic import Field
from pydantic.types import SecretStr, StringConstraints
from typing import Annotated
from sqlalchemy import Column, DateTime, Boolean, String

# pydantic type that limits the range of primary keys
PrimaryKey = Annotated[int, Field(..., gt=0, lt=2**32, description="Primary key")]
NameStr = Annotated[
    str, StringConstraints(pattern=r"^\S.{2,}", strip_whitespace=True, min_length=3)
]
IpAdderss = Annotated[str, StringConstraints(pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")]


# Pydantic models...
class AppBase(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class Pagination(AppBase):
    itemsPerPage: int
    page: int
    total: int


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()


class ModelMixin(object):
    """Model mixin"""

    name = Column(String)
    display_name = Column(String)
    instance = Column(String)
    type = Column(String)
    properties = Column(String)
    server_ip = Column(String)
    online = Column(Boolean)
    gpu = Column(String)
