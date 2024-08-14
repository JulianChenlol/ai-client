from fastapi import APIRouter, HTTPException, status, Depends
from .models.chat import ChatRequest, ChatResponse
from .factory import FactoryProducer
from .constants import LLM
from app.api_key.service import check_api_key

router = APIRouter()


@router.post("/completion", response_model=ChatResponse)
def complete(chat_request: ChatRequest, api_key: Depends(check_api_key)):
    if chat_request.model != api_key.model_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"msg": "This model is not allowed for this api key."}],
        )
    model_instance = FactoryProducer.get_factory(LLM).get_model(chat_request.model)
    if not model_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "This model does not exist."}],
        )
    else:
        return model_instance.complete(chat_request.messages, chat_request.stream)
