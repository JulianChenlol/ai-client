from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Annotated, List

from .models.chat import ChatRequest, ChatResponse
from .factory import FactoryProducer
from .constants import LLM
from app.api_key.service import check_api_key
from app.api_key.schemas import ApiKey

router = APIRouter()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)):
    return check_api_key(api_key)


@router.post("/completion", response_model=ChatResponse)
def complete(
    chat_request: ChatRequest, api_key_list: Annotated[List[ApiKey], Depends(get_api_key)]
):
    models = [api_key.model for api_key in api_key_list]
    if chat_request.model not in models:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": f"{chat_request.model} is not allowed for this api key."}],
        )
    model_instance = FactoryProducer.get_factory(LLM).get_model(chat_request.model)
    if not model_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "This model does not exist."}],
        )
    else:
        return model_instance.complete(chat_request.messages, chat_request.stream)
